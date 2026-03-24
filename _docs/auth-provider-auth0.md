# Auth0 Provider

This MCP server supports Auth0 as an OAuth authentication provider via FastMCP's `Auth0Provider`.

## How It Works

1. `mcp_instance.py` checks whether auth is enabled (`AUTH_ENABLED=true|True|1`).
2. If enabled, `AUTH_PROVIDER` selects the provider — set it to `auth0`.
3. `get_auth_provider("auth0")` in `config/auth_provider.py` builds an `Auth0Provider` instance using environment variables.
4. The provider handles the full OAuth 2.0 / OpenID Connect flow using Auth0's well-known configuration endpoint.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `AUTH_ENABLED` | Yes | Set to `true`, `True`, or `1` to enable authentication |
| `AUTH_PROVIDER` | Yes | Set to `auth0` |
| `AUTH0_DOMAIN` | Yes | Your Auth0 tenant domain (e.g. `my-app.us.auth0.com`) |
| `AUTH0_CLIENT_ID` | Yes | Application Client ID from Auth0 dashboard |
| `AUTH0_CLIENT_SECRET` | Yes | Application Client Secret from Auth0 dashboard |
| `AUTH0_AUDIENCE` | Yes | API audience identifier (e.g. `https://api.example.com`) |
| `RESOURCE_BASE_URL` | No | Server base URL (defaults to `http://localhost:8000`) |
| `JWT_SIGNING_KEY` | Yes | Key used to sign JWTs issued by the MCP server |
| `STORAGE_ENCRYPTION_KEY` | Yes | Fernet key for encrypting client storage |
| `REDIS_HOST` | Yes | Redis host for client token storage |
| `REDIS_PORT` | Yes | Redis port |
| `REDIS_PASSWORD` | No | Redis password (if required) |

### Example `.env`

```env
AUTH_ENABLED=true
AUTH_PROVIDER=auth0

AUTH0_DOMAIN=my-app.us.auth0.com
AUTH0_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AUTH0_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AUTH0_AUDIENCE=https://api.example.com

RESOURCE_BASE_URL=http://localhost:8000
JWT_SIGNING_KEY=your-jwt-signing-key
STORAGE_ENCRYPTION_KEY=your-fernet-key

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

## Auth0 Dashboard Setup

1. Create an **Application** (type: Regular Web Application) in the Auth0 dashboard.
2. Copy the **Domain**, **Client ID**, and **Client Secret** into your `.env`.
3. Create an **API** and set its **Identifier** — this becomes your `AUTH0_AUDIENCE`.
4. Under the API's **Permissions** tab, add any scopes your tools require (e.g. `tool:get_user_info`).
5. Under **Machine to Machine Applications**, authorize your application and grant the required scopes.

## Provider Configuration

The Auth0 provider is initialized in `config/auth_provider.py`:

```python
Auth0Provider(
    config_url=f"https://{auth0_domain}/.well-known/openid-configuration",
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    audience=auth0_audience,
    base_url=base_url,
    required_scopes=["openid", "profile", "email"],
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=client_storage
)
```

- `config_url` — Auth0's OpenID Connect discovery endpoint, derived from the domain.
- `required_scopes` — The provider requests `openid`, `profile`, and `email` by default.
- `client_storage` — Uses a Redis-backed, Fernet-encrypted store for persisting client tokens.

## Tool-Level Authorization

### Permission-based auth

Use `require_permissions()` from `utils/helpers.py` to gate a tool behind specific `permissions` claims in the access token. Pass one or more permission strings — the checker verifies that **all** of them exist in the token's `permissions` claim.

```python
from mcp_server.utils.helpers import require_permissions

@mcp.tool(
    name="my_protected_tool",
    description="A tool that requires specific permissions",
    auth=require_permissions("tool:my_protected_tool")
)
async def my_protected_tool() -> dict:
    ...
```

The permissions must be configured in the Auth0 API's **Permissions** tab and assigned to the application.

## Accessing the Token & User Info Inside a Tool

Once a tool is protected with `auth=`, you can retrieve the current access token and fetch the authenticated user's profile inside the tool handler.

### Step 1 — Import `get_access_token`

```python
from fastmcp.server.dependencies import get_access_token
```

`get_access_token()` is a FastMCP dependency that returns the access token for the current request. It gives you a token object with:

- `token.token` — the raw access token string
- `token.claims` — a dict of decoded JWT claims (`iss`, `aud`, `scope`, `permissions`, etc.)

### Step 2 — Import `get_auth0_user_info`

```python
from mcp_server.utils.helpers import get_auth0_user_info
```

`get_auth0_user_info()` calls Auth0's `/userinfo` endpoint with the raw access token and returns the user's profile (name, email, picture, etc.) based on the granted scopes.

### Step 3 — Use them in your tool

```python
from mcp_server.mcp_instance import mcp
from mcp_server.utils.helpers import require_permissions, get_auth0_user_info
from fastmcp.server.dependencies import get_access_token

@mcp.tool(
    name="get_user_info",
    description="Return auth user info",
    auth=require_permissions("tool:get_user_info")
)
async def get_user_info() -> dict:
    token = get_access_token()

    return {
        "issuer": token.claims.get("iss"),
        "audience": token.claims.get("aud"),
        "scope": token.claims.get("scope"),
        "permissions": token.claims.get("permissions"),
        "user_info": get_auth0_user_info(token.token)
    }
```

**What happens here:**

1. `get_access_token()` retrieves the token from the current authenticated request.
2. `token.claims` gives you the decoded JWT claims — useful for reading `iss`, `aud`, `scope`, and `permissions` directly.
3. `get_auth0_user_info(token.token)` takes the raw token string and calls `https://<AUTH0_DOMAIN>/userinfo` to fetch the full user profile from Auth0.

### `get_auth0_user_info` implementation

Located in `utils/helpers.py`:

```python
def get_auth0_user_info(token: str) -> dict:
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    url = f"https://{auth0_domain}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
```

The returned dict typically includes `sub`, `name`, `email`, `picture`, and other fields depending on the scopes granted.

## Token Claims

When using Auth0, the access token typically contains:

| Claim | Description |
|---|---|
| `iss` | Issuer — your Auth0 domain URL |
| `aud` | Audience — the API identifier |
| `scope` | Granted scopes (space-separated string) |
| `permissions` | Array of permissions assigned via Auth0 RBAC |
