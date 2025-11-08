# MCP SDK OAuth vs Custom GitHub OAuth - Design Decision

## Question: Why not use MCP SDK's OAuth features?

**You're right!** MCP SDK DOES have OAuth authentication support. This document explains why a custom GitHub OAuth implementation was chosen instead.

---

## What MCP SDK OAuth Provides

The MCP SDK has OAuth 2.0 support via RFC 9728 (Resource Server Metadata):

```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP

class SimpleTokenVerifier(TokenVerifier):
    """Token verifier for OAuth tokens"""
    async def verify_token(self, token: str) -> AccessToken | None:
        # Verify the OAuth token
        # Return AccessToken or None
        pass

mcp = FastMCP(
    "My Service",
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://auth.example.com"),
        resource_server_url=AnyHttpUrl("http://localhost:3001"),
        required_scopes=["user"],
    ),
)

@mcp.tool()
async def protected_tool() -> dict:
    """This tool is protected by OAuth"""
    return {"status": "authenticated"}
```

### What This Provides:
- ✅ **TokenVerifier interface**: Verify OAuth tokens
- ✅ **AuthSettings**: Configure OAuth metadata
- ✅ **RFC 9728 compliance**: OAuth 2.0 Resource Server Metadata
- ✅ **Scope validation**: Check required scopes
- ✅ **Bearer token support**: Accept tokens in requests

---

## The Key Difference: Resource Server vs Full OAuth

### MCP SDK OAuth = **Resource Server**

```
You are the PROTECTED RESOURCE
Someone else handles authorization

┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│    Client    │────▶│ Authorization   │────▶│ Your Server  │
│              │     │ Server (?)      │     │ (Resource)   │
│              │◀────│ (External)      │◀────│ + TokenVerifier│
└──────────────┘     └─────────────────┘     └──────────────┘
     ↑                                              ↑
     │                                              │
     │ Token                                Token verification
     │                                       You implement verify_token()
```

**You need to provide:**
- ❌ Authorization server (GitHub, Auth0, Keycloak, etc.)
- ❌ OAuth flow implementation (authorize endpoint, callback)
- ❌ Token issuance logic
- ✅ Token verification logic (you implement `verify_token()`)

**What you get:**
- ✅ Token validation framework
- ✅ Scope checking
- ✅ RFC 9728 metadata

### Custom GitHub OAuth = **Full OAuth Flow**

```
You are the OAUTH CLIENT
GitHub is the authorization server

┌──────────┐    ┌──────────┐    ┌────────────┐
│   User   │───▶│  GitHub  │───▶│Your Server │
│          │    │  OAuth   │    │+ Full Flow │
│          │◀───│ Provider │◀───│+ Sessions  │
└──────────┘    └──────────┘    └────────────┘
```

**What's included:**
- ✅ Authorization URL generation
- ✅ OAuth callback handling
- ✅ Code-to-token exchange
- ✅ User profile fetching
- ✅ Session management
- ✅ Web UI for OAuth flow
- ✅ CSRF protection
- ✅ Complete working solution

---

## Why Custom GitHub OAuth Was Chosen

### Reason 1: **No Authorization Server Requirement**

**With MCP SDK OAuth:**
```python
class MyTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # ❓ Where does the token come from?
        # ❓ Who issued it?
        # ❓ How do users get tokens?
        # You need to:
        # 1. Set up an authorization server (Auth0, Keycloak, etc.)
        # 2. Implement OAuth flow separately
        # 3. Issue tokens to users
        # 4. Then verify those tokens here
        pass
```

**With Custom GitHub OAuth:**
```python
# ✅ GitHub IS the authorization server
# ✅ GitHub handles token issuance
# ✅ OAuth flow built-in
# ✅ Just works out of the box

@mcp.custom_route("/auth/login")
async def login():
    # Redirect to GitHub - done!
    return RedirectResponse(auth_url)
```

**Decision point**: Custom OAuth = complete solution, MCP OAuth = framework only

---

### Reason 2: **User Experience - OAuth Flow**

**With MCP SDK OAuth:**
```
User Journey:
1. User needs a token... how?
2. ❓ Where do they go to get a token?
3. ❓ Do we build a separate OAuth flow?
4. ❓ Do we use Auth0 ($$$)?
5. ❓ Build our own authorization server?
6. Once they have token → pass to MCP server
```

**With Custom GitHub OAuth:**
```
User Journey:
1. User calls 'github_login' tool
2. ✅ Click URL → GitHub OAuth page
3. ✅ Click "Authorize" button
4. ✅ Redirected back → authenticated!
5. ✅ Beautiful success page
```

**Decision point**: Custom OAuth = complete UX, MCP OAuth = bring your own

---

### Reason 3: **Token Issuance - Who Issues Tokens?**

**With MCP SDK OAuth:**
```python
auth=AuthSettings(
    issuer_url=AnyHttpUrl("https://auth.example.com"),  # ❓ Who is this?
    # Options:
    # 1. Auth0 ($99/month for production)
    # 2. Keycloak (complex self-hosted)
    # 3. Build your own (weeks of work)
    # 4. Some other OAuth provider
)
```

**With Custom GitHub OAuth:**
```python
# ✅ issuer_url = "https://github.com"
# ✅ Free
# ✅ Already exists
# ✅ Users already have accounts
# ✅ Trusted by developers
```

**Decision point**: Why add another service when GitHub works perfectly?

---

### Reason 4: **Implementation Complexity**

**Using MCP SDK OAuth (minimal example):**

```python
# Step 1: Choose authorization server (Auth0, Keycloak, custom)
# Let's say Auth0...

# Step 2: Set up Auth0 account ($)

# Step 3: Configure Auth0 application

# Step 4: Implement token verification
class Auth0TokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Verify JWT signature
        # Check expiration
        # Validate issuer
        # Check audience
        # Validate claims
        # ... complex logic
        pass

# Step 5: Configure MCP
mcp = FastMCP(
    "My Service",
    token_verifier=Auth0TokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://yourapp.auth0.com",
        resource_server_url="http://localhost:3001",
        required_scopes=["user"],
    ),
)

# Step 6: Build OAuth flow (separate!)
# - Authorization endpoint
# - Callback handling
# - Token exchange
# - Session management
# - Web UI

# Step 7: Handle token passing
# - How do MCP clients get the token?
# - Store it where?
# - Refresh tokens?
```

**Total**: ~500+ lines of code + external service dependency

**Using Custom GitHub OAuth:**

```python
# Step 1: Get GitHub OAuth credentials (free, 5 minutes)

# Step 2: Set environment variables
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=yyy

# Step 3: Done! Everything is implemented
# - OAuth flow ✅
# - Callback handling ✅
# - Token exchange ✅
# - Session management ✅
# - Web UI ✅
# - User profile ✅
```

**Total**: Just configuration, all code already written

**Decision point**: 5 minutes vs several days + ongoing costs

---

### Reason 5: **Access to User Data**

**With MCP SDK OAuth:**
```python
class MyTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # You get back an AccessToken object
        # But what about user profile?
        # - Username?
        # - Email?
        # - Avatar?
        # - GitHub repos?
        # 
        # You'd need to:
        # 1. Call a separate API to get user info
        # 2. Make additional requests
        # 3. Handle those responses
        return AccessToken(...)
```

**With Custom GitHub OAuth:**
```python
@mcp.tool()
@require_auth
async def my_tool(ctx: Context) -> str:
    session = get_current_session()
    # ✅ session.user.login
    # ✅ session.user.email
    # ✅ session.user.avatar_url
    # ✅ session.user.name
    # ✅ session.user.bio
    # ✅ session.user.location
    # ✅ session.user.company
    # ✅ session.access_token (for API calls)
    
    # Can even fetch repos:
    repos = await fetch_user_repos(session.access_token)
```

**Decision point**: Rich user data vs token-only

---

### Reason 6: **Session Management**

**With MCP SDK OAuth:**
```python
# MCP SDK handles token verification per-request
# But session management?
# - Store user sessions where?
# - How long do they last?
# - How to logout?
# - Session state?
# 
# You need to implement all of this yourself
```

**With Custom GitHub OAuth:**
```python
# ✅ Built-in session management
# ✅ Session store (in-memory, easily → Redis)
# ✅ get_current_session()
# ✅ set_current_session()
# ✅ clear_current_session()
# ✅ Session expiration logic
# ✅ Multiple session support

session = get_current_session()  # Just works!
```

**Decision point**: Build session management vs get it included

---

### Reason 7: **MCP Client Integration**

**With MCP SDK OAuth:**
```
Problem: How does the MCP client (Cursor) get the token?

Option A: User manually gets token
- User goes to authorization server
- Gets a token
- Copies it
- Pastes into Cursor config
- 😞 Bad UX

Option B: Cursor implements OAuth
- Cursor needs to handle OAuth
- Each client implements differently
- Fragmented experience
```

**With Custom GitHub OAuth:**
```
Solution: Server handles everything

1. User calls 'github_login' tool
2. Server returns URL
3. User opens URL in browser
4. Authenticates with GitHub
5. Server handles callback
6. Session created automatically
7. ✅ Seamless experience
```

**Decision point**: Server-driven flow vs client-driven

---

## When Would You Use MCP SDK OAuth?

### Good Use Cases:
1. **Enterprise Environment**: You already have Auth0/Okta/Keycloak
2. **Multiple Services**: Centralized auth across many services
3. **Complex Requirements**: Custom token format, special claims
4. **Existing Infrastructure**: OAuth server already running

### Example:
```python
# Your company already has Auth0 for everything
# Just add your MCP server as another resource

class CompanyTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Verify against company's Auth0
        # All employees already have tokens
        return await verify_with_auth0(token)

# Makes sense! Reuse existing infrastructure
```

---

## When Custom OAuth Makes Sense (Our Case)

### Good Use Cases:
1. **Public Application**: Users don't have existing tokens
2. **GitHub Integration**: Want GitHub-specific features
3. **Rapid Development**: Need auth working quickly
4. **No Infrastructure**: Don't have authorization server
5. **Developer Tools**: Users are developers (have GitHub)

### Our Requirements:
- ✅ Public application (anyone can use)
- ✅ No existing auth infrastructure
- ✅ Want GitHub user data (repos, profile)
- ✅ Need it working fast
- ✅ Developer audience (GitHub users)

**Result**: Custom GitHub OAuth is perfect fit

---

## Detailed Comparison Table

| Aspect | MCP SDK OAuth | Custom GitHub OAuth |
|--------|--------------|-------------------|
| **Authorization Server** | Need external (Auth0, etc.) | GitHub (free, built-in) |
| **Cost** | $0-$99+/month | $0 |
| **Setup Time** | Days/weeks | 5 minutes |
| **OAuth Flow** | Build yourself | Included ✅ |
| **Callback Handling** | Build yourself | Included ✅ |
| **Token Exchange** | Build yourself | Included ✅ |
| **User Profile** | Build yourself | Included ✅ |
| **Session Management** | Build yourself | Included ✅ |
| **Web UI** | Build yourself | Included ✅ |
| **CSRF Protection** | Build yourself | Included ✅ |
| **User Tools** | Build yourself | Included ✅ |
| **Documentation** | Minimal | Complete ✅ |
| **Dependencies** | External service | GitHub only |
| **Complexity** | High | Low ✅ |
| **Maintenance** | Ongoing | Minimal ✅ |
| **Best For** | Enterprise, existing auth | Public apps, rapid dev ✅ |

---

## Could We Use Both?

### Hypothetical: MCP SDK OAuth + GitHub

```python
# Use MCP SDK OAuth framework
class GitHubTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Verify it's a GitHub token
        user = await get_github_user(token)
        return AccessToken(
            token=token,
            scopes=["user"],
            # ... but still missing session management
            # ... still missing OAuth flow
            # ... still missing web UI
        )

mcp = FastMCP(
    "Service",
    token_verifier=GitHubTokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://github.com",
        resource_server_url="http://localhost:3001",
        required_scopes=["user"],
    ),
)
```

**Problems:**
- ❌ Still need to implement OAuth flow
- ❌ Still need callback handling
- ❌ Still need session management
- ❌ Still need web UI
- ❌ Adds MCP SDK layer for minimal benefit

**Conclusion**: More complexity, no real gain

---

## The Real Question: What Are You Buying?

### MCP SDK OAuth Gives You:
- ✅ A **framework** for token verification
- ✅ A **pattern** to follow (RFC 9728)
- ✅ A **structure** for auth settings
- ❌ **NOT** a complete auth solution

### Custom GitHub OAuth Gives You:
- ✅ A **complete working system**
- ✅ **Everything** needed for auth
- ✅ **User-friendly** experience
- ✅ **Zero external dependencies** (except GitHub)

**Analogy:**
- MCP SDK OAuth = IKEA instruction manual (you still build it)
- Custom OAuth = Fully assembled furniture (ready to use)

---

## The Decision Matrix

### Criteria for Choosing:

```
Use MCP SDK OAuth IF:
✅ You have an existing authorization server
✅ You're in an enterprise environment
✅ You need custom token formats
✅ You have time to implement OAuth flow
✅ You need centralized auth across services

Use Custom GitHub OAuth IF:
✅ You're building a public application
✅ You want rapid development
✅ You don't have auth infrastructure
✅ Your users are developers (have GitHub)
✅ You want GitHub-specific features
✅ You want a complete solution
```

### Our Project:
- ✅ Public application
- ✅ Developer users
- ✅ No auth infrastructure
- ✅ Need it fast
- ✅ Want GitHub features

**Conclusion**: Custom GitHub OAuth 🎯

---

## Architecture Comparison

### Using MCP SDK OAuth:

```
┌─────────┐                                    ┌──────────────┐
│  User   │──(1)──▶ Need token ───────────────▶│    Auth0     │
└─────────┘         How to get it?             │ (External)   │
     │                                          └──────┬───────┘
     │                                                 │
     │              (2) Implement OAuth flow           │
     │              - Authorization endpoint           │
     │              - Callback handling                │
     │              - Token exchange                   │
     │              - Session management               │
     │              - Web UI                           │
     │                                                 │
     │◀─────────────────── Token ─────────────────────┘
     │
     │              (3) Pass token in request
     ▼
┌────────────────────────────────────────┐
│         Your MCP Server                │
│  + MCP SDK OAuth (TokenVerifier)       │
│  + Your OAuth flow code                │
│  + Your session management             │
│  + Your web UI                         │
└────────────────────────────────────────┘
```

### Using Custom GitHub OAuth:

```
┌─────────┐
│  User   │──(1)──▶ Call 'github_login' tool
└────┬────┘
     │
     │              (2) Click authorization URL
     ▼
┌─────────────┐    (3) Authorize
│   GitHub    │◀──────────┐
│   OAuth     │           │
└──────┬──────┘           │
       │                  │
       │ (4) Callback     │
       ▼                  │
┌────────────────────────────────┐
│      Your MCP Server           │
│  + Complete OAuth flow ✅      │
│  + Callback handling ✅        │
│  + Session management ✅       │
│  + Web UI ✅                   │
│  + User profile ✅             │
│  + Everything included         │
└────────────────────────────────┘
```

**Simplicity winner**: Custom GitHub OAuth

---

## Final Answer

### Why NOT MCP SDK OAuth?

1. **Not a Complete Solution**: It's a framework, not a working system
2. **Requires External Service**: Need Auth0, Keycloak, or build your own
3. **More Implementation Work**: Still need to build OAuth flow, sessions, UI
4. **Additional Complexity**: Extra layer without clear benefit
5. **Cost**: External auth servers cost money
6. **Time**: Days/weeks to set up vs 5 minutes

### Why Custom GitHub OAuth?

1. **Complete Solution**: Everything included, just works
2. **No External Dependencies**: Just GitHub (free, ubiquitous)
3. **Zero Implementation Needed**: All code already written
4. **Simple**: Direct integration, clear flow
5. **Free**: No monthly costs
6. **Fast**: 5-minute setup

---

## The Bottom Line

**MCP SDK OAuth is designed for enterprises with existing auth infrastructure.**

**Custom GitHub OAuth is designed for rapid development of public applications.**

For this project:
- ✅ Public application for developers
- ✅ No existing auth infrastructure
- ✅ Need rapid development
- ✅ Want GitHub integration
- ✅ Want complete solution

**Custom GitHub OAuth was the RIGHT choice.** ✅

---

## Could This Change?

### If the project evolves to:
- Multiple OAuth providers (Google, Microsoft, etc.)
- Enterprise customers with SSO requirements
- Complex token requirements
- Centralized auth across multiple services

**Then**: MCP SDK OAuth framework might make sense

**Until then**: Custom GitHub OAuth is simpler, faster, and complete

---

## Summary

| Question | Answer |
|----------|--------|
| Does MCP SDK have OAuth? | ✅ Yes (RFC 9728) |
| Is it a complete solution? | ❌ No, it's a framework |
| Do you still need OAuth flow? | ✅ Yes, build it yourself |
| Do you need external auth server? | ✅ Yes (Auth0, etc.) |
| Is custom GitHub OAuth easier? | ✅ Yes, complete solution |
| Was custom OAuth the right choice? | ✅ Yes, for this use case |

**MCP SDK OAuth = Framework to integrate existing auth**  
**Custom GitHub OAuth = Complete working auth system**

Different tools for different needs. We picked the right one. ✅
