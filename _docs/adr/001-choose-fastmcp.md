# ADR-001 – Use FastMCP as the MCP Server Framework

**Status:** Accepted  
**Date:** 2025-06-01  
**Authors:** code4mk  

---

## 1. Context

We are building a production-ready Model Context Protocol (MCP) server template for the MCP boilerplate project. The MCP specification defines how AI models interact with external tools, resources, and prompts. We needed a Python framework that:

- Implements the MCP specification fully and correctly
- Supports multiple transport layers (stdio, HTTP/SSE, Streamable HTTP)
- Provides a clean, Pythonic developer experience with minimal boilerplate
- Offers built-in support for tools, resources, and prompts registration
- Supports middleware (rate limiting, authentication) out of the box
- Is actively maintained and aligned with the evolving MCP spec
- Can serve as a reliable foundation for a reusable boilerplate/template

---

## 2. Decision

> We will use **FastMCP** (`fastmcp>=3.0.0b1`) as the core framework to build and serve our MCP server.

---

## 3. Rationale (Why)

- **High-level API**: FastMCP provides a decorator-based, Flask/FastAPI-like API for registering tools, resources, and prompts — drastically reducing boilerplate compared to the low-level `mcp` SDK.
- **Multi-transport support**: A single codebase can serve over stdio (for Claude Desktop), SSE, or Streamable HTTP — configurable at runtime via environment variables.
- **FileSystemProvider**: Auto-discovers and registers MCP components from directory structures, enabling a clean modular architecture (`handlers/tools/`, `handlers/resources/`, `handlers/prompts/`).
- **Built-in middleware**: Ships with `RateLimitingMiddleware` and supports custom middleware, removing the need to build infrastructure plumbing from scratch.
- **OAuth / Auth support**: Native integration with auth providers (e.g., GitHub OAuth), toggled via configuration.
- **Pydantic integration**: Works naturally with Pydantic models for input validation (`strict_input_validation=True`), aligning with modern Python best practices.
- **Active development**: FastMCP is actively maintained and tracks the latest MCP specification changes, ensuring forward compatibility.

---

## 4. Consequences

### Positive
- Rapid development with minimal boilerplate for tools, resources, and prompts
- Clean project structure using `FileSystemProvider` for auto-registration
- Easy transport switching (stdio ↔ HTTP/SSE) without code changes
- Built-in rate limiting and auth middleware reduce custom infrastructure code
- Pydantic-based input validation provides type safety and clear error messages
- Strong community adoption in the MCP ecosystem

### Negative / Risks
- **Beta dependency**: Using `>=3.0.0b1` means relying on a pre-release version; breaking changes may occur before stable release
- **Abstraction lock-in**: The high-level API abstracts away low-level MCP protocol details, which could limit flexibility for edge cases
- **Ecosystem maturity**: The MCP ecosystem is still evolving; framework APIs may shift as the spec matures
- **Debugging complexity**: Auto-registration via `FileSystemProvider` can make it harder to trace which handlers are loaded and in what order

---

## 5. Alternatives Considered

### Option A – Low-level `mcp` Python SDK
- Pros:
  - Direct control over the MCP protocol
  - No additional abstraction layer
  - Minimal dependency footprint
- Cons:
  - Significant boilerplate for server setup, tool/resource registration
  - No built-in middleware support
  - Manual transport handling required
  - Slower development velocity

### Option B – Custom MCP implementation from scratch
- Pros:
  - Full control over every aspect
  - No external dependencies
- Cons:
  - Extremely high development effort
  - Must track MCP spec changes manually
  - No community support or shared bug fixes
  - Not practical for a template/boilerplate project

### Option C – TypeScript-based MCP SDK
- Pros:
  - First-class MCP SDK support from Anthropic
  - Mature TypeScript ecosystem
- Cons:
  - Project requirement is Python
  - Team expertise is Python-focused
  - Would not serve the goal of a Python MCP template

---

## 6. Related Decisions
There have been no related decisions yet.

---

## 7. References

- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

## 8. Status Notes

- FastMCP v3.x is currently in beta; we should monitor releases and upgrade to stable when available
- Re-evaluate this decision if the official `mcp` Python SDK introduces a comparable high-level API
- Review annually or when major MCP spec changes occur

---

