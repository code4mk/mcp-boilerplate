# ADR-002 – Use HTTPX as the HTTP Client Library

**Status:** Accepted  
**Date:** 2026-03-24  
**Authors:** code4mk  

---

## 1. Context

The MCP server needs to make outbound HTTP requests to external APIs (e.g., weather services, third-party integrations). We needed a Python HTTP client library that:

- Supports both synchronous and asynchronous usage from a single API
- Provides connection pooling and persistent sessions out of the box
- Offers a modern, Pythonic interface with type hints
- Handles timeouts, retries, and SSL verification cleanly
- Is actively maintained with strong community adoption
- Can serve as the foundation for a unified `HttpxClient` wrapper (see [http-client docs](../httpx-client.md))

---

## 2. Decision

> We will use **HTTPX** (`httpx`) as the HTTP client library for all outbound HTTP communication.

---

## 3. Rationale (Why)

- **Sync + Async in one library**: HTTPX provides both `httpx.Client` (sync) and `httpx.AsyncClient` (async) with identical method signatures. This allowed us to build a single `HttpxClient` wrapper that switches mode at construction time — no branching in request methods.
- **Drop-in replacement for requests**: The sync API mirrors the `requests` library, making it familiar to most Python developers while offering strictly more features.
- **HTTP/2 support**: HTTPX supports HTTP/2 out of the box (opt-in), which can improve performance for multiplexed API calls.
- **Built-in connection pooling**: Both sync and async clients maintain connection pools, reducing latency for repeated calls to the same host.
- **First-class timeout control**: Granular timeout configuration via `httpx.Timeout` (connect, read, write, pool) rather than a single flat value.
- **Type-annotated API**: Full type hints throughout, aligning with our Pydantic-based codebase and enabling better IDE support.
- **Active maintenance**: HTTPX is actively developed by Encode (the team behind Starlette and Uvicorn), ensuring compatibility with the modern Python async ecosystem.

---

## 4. Consequences

### Positive
- Single dependency covers both sync and async HTTP needs
- Unified `HttpxClient` wrapper with zero branching in CRUD methods — `httpx.Client` and `httpx.AsyncClient` share the same interface
- Connection pooling and keep-alive improve performance for repeated API calls
- HTTP/2 available when needed without switching libraries
- Clean integration with `asyncio` for the MCP server's async runtime

### Negative / Risks
- **Additional dependency**: HTTPX is not in the standard library; adds a dependency (though it has minimal transitive deps)
- **Less ubiquitous than requests**: While growing fast, HTTPX has a smaller ecosystem of plugins and middleware compared to `requests`
- **HTTP/2 requires optional dep**: Full HTTP/2 support requires installing `httpx[http2]` (adds `h2` dependency)
- **Slightly different edge-case behavior**: Some subtle differences from `requests` in redirect handling and encoding may surprise developers coming from `requests`

---

## 5. Alternatives Considered

### Option A – `requests`
- Pros:
  - Most widely used Python HTTP library
  - Massive ecosystem of adapters and plugins
  - Battle-tested in production at scale
- Cons:
  - Sync only — no native async support
  - Would require a separate async library (e.g., `aiohttp`) for async mode, doubling the dependency surface
  - No HTTP/2 support
  - Less granular timeout control

### Option B – `aiohttp`
- Pros:
  - Mature async HTTP client
  - Large community and ecosystem
  - WebSocket support built in
- Cons:
  - Async only — no sync client; would need `requests` or similar for sync usage
  - API is quite different from `requests`, steeper learning curve
  - Two libraries to maintain for sync + async

### Option C – `urllib3` / `http.client` (stdlib)
- Pros:
  - No external dependencies
  - Low-level control
- Cons:
  - No async support
  - Verbose API, significant boilerplate
  - No connection pooling in `http.client` (urllib3 has it, but no async)
  - Not practical for a developer-friendly template

---

## 6. Related Decisions

- [ADR-001](001-choose-fastmcp.md) – Use FastMCP as the MCP Server Framework

---

## 7. References

- [HTTPX Documentation](https://www.python-httpx.org)
- [HTTPX GitHub Repository](https://github.com/encode/httpx)
- [HTTP Client Usage Docs](../httpx-client.md)

---

## 8. Status Notes

- Monitor HTTPX releases for any breaking changes in major versions
- Consider enabling HTTP/2 (`httpx[http2]`) if multiplexed connections become a performance requirement
- Re-evaluate if `requests` adds native async support or if a better unified client emerges

---
