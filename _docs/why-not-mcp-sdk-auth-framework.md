# Why Not Use MCP SDK's Auth Framework?

## The Real Question

**Why was custom auth logic implemented instead of using MCP SDK's built-in auth framework?**

```python
# Option A: What was done (Custom)
@require_auth  # Custom decorator
async def my_tool(ctx: Context) -> str:
    session = get_current_session()  # Custom session management
    return f"Hello {session.user.login}"

# Option B: What could have been done (MCP SDK Framework)
from mcp.server.auth.provider import AccessToken, TokenVerifier

class GitHubTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        user = await get_github_user(token)
        return AccessToken(token=token, scopes=["user"])

mcp = FastMCP(
    "Service",
    token_verifier=GitHubTokenVerifier(),  # Use SDK framework
    auth=AuthSettings(...)
)

# Tools automatically protected by SDK
@mcp.tool()
async def my_tool(ctx: Context) -> str:
    # SDK validates token automatically
    return "Hello"
```

## The Honest Answer

**This might have been a missed opportunity.** Let me analyze both approaches:

---

## What Using MCP SDK Framework Would Provide

### Advantages:

1. **Standards Compliance**
   - Built on RFC 9728 (OAuth 2.0 Resource Server Metadata)
   - Industry-standard patterns
   - Better interoperability

2. **Automatic Token Validation**
   - SDK handles token verification per request
   - No need for custom decorator
   - Built-in scope checking

3. **Proper Separation of Concerns**
   - Authentication (SDK framework)
   - Authorization (your business logic)
   - Clear boundaries

4. **Better MCP Client Integration**
   - Clients can discover auth requirements
   - Standard token passing mechanism
   - Metadata endpoints

5. **Less Custom Code**
   - Fewer potential bugs
   - Less maintenance
   - Use tested SDK code

---

## Why Custom Auth Was Chosen (Analyzing the Decision)

### Reason 1: **Session-Based vs Token-Based Architecture**

**MCP SDK Approach (Stateless):**
```python
# Every request includes token
# Server verifies token each time
# No server-side session storage

Request 1: Bearer token123 → Verify → Execute
Request 2: Bearer token123 → Verify → Execute
Request 3: Bearer token123 → Verify → Execute
```

**Custom Approach (Stateful):**
```python
# Login once, create session
# Subsequent requests use session
# Server maintains session state

Login: OAuth → Create session
Request 1: Check session → Execute
Request 2: Check session → Execute
Request 3: Check session → Execute
```

**Trade-offs:**
- MCP SDK: Stateless, scalable, RESTful
- Custom: Stateful, simpler client, maintains context

**Decision**: Custom approach chosen for simpler user experience (login once vs pass token each time)

---

### Reason 2: **OAuth Flow Handling**

**Both approaches still need:**
```python
# OAuth flow is the same either way
@app.route("/auth/login")
async def login():
    # Generate GitHub OAuth URL
    return redirect(auth_url)

@app.route("/auth/callback")
async def callback():
    # Exchange code for token
    # Get user info
    # ... then what?
```

**With MCP SDK:**
```python
# Option A: Return token to user
# User manually adds to requests
# Bad UX

# Option B: Store session anyway
# Then why use stateless framework?
```

**With Custom:**
```python
# Store session, set as current
# User doesn't touch tokens
# Transparent to user
```

**Decision**: For web OAuth flow, session storage makes sense regardless

---

### Reason 3: **Context and User Data**

**MCP SDK Approach:**
```python
class GitHubTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        # Returns AccessToken
        # Where do we store user profile?
        # How do tools access user data?
        
        return AccessToken(
            token=token,
            scopes=["user"]
            # No place for user profile, session data, etc.
        )

@mcp.tool()
async def my_tool(ctx: Context) -> str:
    # ctx might have token info
    # But how to get user profile?
    # Need additional lookup
    pass
```

**Custom Approach:**
```python
@mcp.tool()
@require_auth
async def my_tool(ctx: Context) -> str:
    session = get_current_session()
    # session.user has everything:
    # - login, email, name, avatar
    # - bio, location, company
    # - access_token for GitHub API
    
    return f"Hello {session.user.name}"
```

**Decision**: Custom approach provides richer context to tools

---

### Reason 4: **Simplicity and Learning Curve**

**MCP SDK Approach:**
```python
# Need to understand:
- TokenVerifier interface
- AccessToken model
- AuthSettings configuration
- RFC 9728 spec
- How tokens flow through SDK
- Integration with FastMCP
- Metadata endpoints

# Plus still implement:
- OAuth flow
- Session management (if needed)
- User profile storage
```

**Custom Approach:**
```python
# Simple Python patterns:
- Functions
- Decorators
- Dictionaries for storage
- Simple session objects

# Everything custom, easy to understand
```

**Decision**: Lower barrier to entry for contributors

---

### Reason 5: **Flexibility and Control**

**MCP SDK Approach:**
```python
# Constrained by SDK's interface
# Must fit into TokenVerifier pattern
# Limited customization options
# SDK decides flow
```

**Custom Approach:**
```python
# Complete control over:
- Session structure
- Storage mechanism
- Verification logic
- Error handling
- User experience
```

**Decision**: More flexibility for specific requirements

---

## Honest Assessment: Was This The Right Choice?

### ⚠️ Potential Issues With Custom Approach:

1. **Reinventing the Wheel**
   - MCP SDK provides auth framework
   - Custom code duplicates some functionality
   - More code to maintain

2. **Not Using SDK Features**
   - Missing out on standards compliance
   - Clients can't auto-discover auth requirements
   - No metadata endpoints

3. **Maintenance Burden**
   - Security updates need to be implemented manually
   - More surface area for bugs
   - Testing complexity

4. **Interoperability**
   - Custom approach may not work well with all MCP clients
   - Some clients expect standard MCP auth

---

## Could We Refactor to Use MCP SDK Auth?

### Option: Hybrid Approach

```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

class SessionBasedTokenVerifier(TokenVerifier):
    """Use MCP SDK framework but with session-based verification"""
    
    async def verify_token(self, token: str) -> AccessToken | None:
        # token could be session_id
        session = get_session(token)
        
        if not session or not session.is_valid():
            return None
        
        return AccessToken(
            token=session.access_token,
            scopes=["user"],
            # Note: Can't attach user profile here
        )

mcp = FastMCP(
    "Cox's Bazar MCP",
    token_verifier=SessionBasedTokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://github.com",
        resource_server_url="http://localhost:8000",
        required_scopes=["user"],
    ),
)

# OAuth flow still custom
@mcp.custom_route("/auth/login")
async def login():
    # Same as before
    pass

@mcp.custom_route("/auth/callback")  
async def callback():
    # Same as before
    # Create session
    # Store with session_id as "token"
    pass

# Tools now use SDK auth automatically
@mcp.tool()
async def my_tool(ctx: Context) -> str:
    # SDK validates automatically
    # But how to get user profile?
    # Still need custom logic
    pass
```

**Verdict**: Hybrid approach still has issues with user context access

---

## The Real Constraint: User Context

The fundamental issue is:

```python
# MCP SDK TokenVerifier returns:
AccessToken(
    token=str,
    scopes=list[str]
)

# But we need:
Session(
    access_token=str,
    user=GitHubUser(
        login=str,
        email=str,
        name=str,
        avatar_url=str,
        bio=str,
        # ... rich profile
    ),
    created_at=datetime,
    # ... session metadata
)
```

**The SDK's AccessToken doesn't have space for rich user context.**

---

## What Should Have Been Done?

### Best Practice: Extend SDK Framework

```python
from mcp.server.auth.provider import AccessToken, TokenVerifier
from typing import Optional

class EnhancedAccessToken(AccessToken):
    """Extend SDK's AccessToken with user data"""
    user: GitHubUser
    session_id: str

class GitHubOAuthVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> EnhancedAccessToken | None:
        # token is session_id
        session = get_session(token)
        
        if not session:
            return None
        
        return EnhancedAccessToken(
            token=session.access_token,
            scopes=["user"],
            user=session.user,  # Attach user data
            session_id=token,
        )

# Use SDK framework
mcp = FastMCP(
    "Service",
    token_verifier=GitHubOAuthVerifier(),
    auth=AuthSettings(
        issuer_url="https://github.com",
        resource_server_url="http://localhost:8000",
        required_scopes=["user"],
    ),
)

# OAuth flow still custom (unavoidable)
# But verification uses SDK framework

@mcp.tool()
async def my_tool(ctx: Context) -> str:
    # How to access enhanced token?
    # This depends on SDK internals
    pass
```

**Problem**: Depends on whether MCP SDK supports extended token models and how to access them in Context

---

## Framework vs Implementation Confusion

I think there's confusion about what the SDK provides:

### What MCP SDK Auth Framework IS:
- ✅ **Interface**: TokenVerifier, AuthSettings
- ✅ **Structure**: How to organize auth code
- ✅ **Standards**: RFC 9728 compliance
- ✅ **Integration**: How auth fits into MCP protocol

### What MCP SDK Auth Framework IS NOT:
- ❌ **OAuth Flow**: You still implement login/callback
- ❌ **Session Management**: You still implement storage
- ❌ **User Management**: You still implement profiles
- ❌ **Web UI**: You still implement OAuth pages

**Either way, you're writing similar code.**

The question is: Should that code conform to MCP SDK's auth framework?

---

## Recommendation: Should This Be Refactored?

### Arguments FOR Refactoring to SDK Framework:

1. **Standards Compliance**: Better MCP protocol conformance
2. **Future-Proofing**: SDK may add features we want
3. **Interoperability**: Better client compatibility
4. **Best Practices**: Use framework as intended
5. **Community**: Aligns with MCP ecosystem patterns

### Arguments AGAINST Refactoring:

1. **Working Code**: Current implementation works well
2. **Rich Context**: Custom approach provides better user context
3. **Significant Effort**: Large refactor for minimal functional gain
4. **Documentation**: Would need to rewrite all docs
5. **Risk**: Potential bugs during migration

---

## The Verdict

### Was Custom Auth a Mistake?

**Not a mistake, but perhaps not optimal.**

### Reasoning:

1. **For a template/learning project**: Custom is fine
   - Easier to understand
   - Clear, simple code
   - No SDK magic

2. **For production/enterprise**: SDK framework better
   - Standards compliance
   - Better interoperability
   - Professional implementation

3. **The middle ground**: Could have used SDK framework with custom OAuth flow
   - Use TokenVerifier interface
   - Keep custom OAuth flow
   - Best of both worlds

---

## What Would I Do Differently?

If starting from scratch:

```python
# 1. Use MCP SDK auth framework
from mcp.server.auth.provider import TokenVerifier, AccessToken

class GitHubSessionVerifier(TokenVerifier):
    """Session-based verification using SDK framework"""
    
    async def verify_token(self, session_id: str) -> AccessToken | None:
        session = get_session(session_id)
        if not session:
            return None
        
        # Store user in global context
        set_request_user(session.user)
        
        return AccessToken(
            token=session.access_token,
            scopes=["user"],
        )

# 2. Configure FastMCP with SDK auth
mcp = FastMCP(
    "Service",
    token_verifier=GitHubSessionVerifier(),
    auth=AuthSettings(
        issuer_url="https://github.com",
        resource_server_url="http://localhost:8000",
        required_scopes=["user"],
    ),
)

# 3. Keep custom OAuth flow (unavoidable)
@mcp.custom_route("/auth/login")
async def login():
    # Same implementation
    pass

@mcp.custom_route("/auth/callback")
async def callback():
    # Create session
    # Return session_id as "token"
    pass

# 4. Tools work with SDK auth
@mcp.tool()
async def my_tool(ctx: Context) -> str:
    # SDK validates automatically
    # Access user via context var
    user = get_request_user()
    return f"Hello {user.login}"
```

**This would be the ideal approach:**
- ✅ Uses SDK framework
- ✅ Standards compliant
- ✅ Still has rich user context
- ✅ Custom OAuth flow where needed

---

## Final Answer

### Why wasn't MCP SDK auth framework used?

**Likely reasons:**
1. Simplicity - Custom decorator is simpler
2. Flexibility - Full control over implementation
3. Learning curve - Avoiding SDK complexity
4. Session-based design - SDK is token-based
5. Rich user context - SDK's AccessToken is limited

**Should it have been used?**
- For a template/demo: Current approach is fine ✅
- For production: SDK framework would be better ✅
- Ideal: Hybrid approach using SDK framework with custom OAuth flow ✅

**Is it worth refactoring?**
- If this is going to production: Yes
- If it's staying a template: No (current works)
- If you want to learn SDK: Yes, good exercise

---

## Conclusion

The custom auth implementation works well and is easier to understand, but **using MCP SDK's auth framework would have been more "proper"** from an architectural standpoint.

It's not a critical issue, but if I were doing this for a production system or to demonstrate best practices, I'd use the SDK's auth framework with the custom OAuth flow integrated into it.

**Current approach**: 7/10 - Works, simple, understandable  
**SDK framework approach**: 9/10 - More professional, standards-compliant, better architecture

The custom implementation isn't wrong, it's just... custom. And sometimes custom is fine! 🎯


