# HTTPx Client

A unified HTTPX wrapper (`HttpxClient`) that supports both sync and async modes via a single `mode` parameter.

**Location:** `src/mcp_server/lib/httpx_client.py`  
**ADR:** [002 – Why HTTPX](adr/002-choose-httpx.md)

## Constructor

```python
from mcp_server.lib.httpx_client import HttpxClient

client = HttpxClient(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer <token>"},
    timeout=10.0,
    verify=True,
    mode="sync",  # or "async"
)
```

| Parameter        | Type                        | Default  | Description                              |
| ---------------- | --------------------------- | -------- | ---------------------------------------- |
| `base_url`       | `str`                       | `""`     | Base URL prepended to every request path |
| `headers`        | `dict[str, str] \| None`    | `None`   | Default headers sent with every request  |
| `timeout`        | `float \| httpx.Timeout`    | `10.0`   | Request timeout in seconds               |
| `verify`         | `bool`                      | `True`   | Whether to verify SSL certificates       |
| `mode`           | `"sync" \| "async"`         | `"sync"` | Client mode                              |
| `**client_kwargs`| `Any`                       | —        | Extra kwargs forwarded to httpx           |

## Sync Usage

```python
client = HttpxClient(base_url="https://api.example.com", mode="sync")

response = client.get("/users", params={"page": 1})
response = client.post("/users", json={"name": "Alice"})
response = client.put("/users/1", json={"name": "Alice Updated"})
response = client.patch("/users/1", json={"name": "Alice Patched"})
response = client.delete("/users/1")

client.close()
```

With context manager:

```python
with HttpxClient(base_url="https://api.example.com", mode="sync") as client:
    response = client.get("/health")
```

## Async Usage

```python
client = HttpxClient(base_url="https://api.example.com", mode="async")

response = await client.get("/users")
response = await client.post("/users", json={"name": "Alice"})
response = await client.put("/users/1", json={"name": "Alice Updated"})
response = await client.patch("/users/1", json={"name": "Alice Patched"})
response = await client.delete("/users/1")

await client.close()
```

With context manager:

```python
async with HttpxClient(base_url="https://api.example.com", mode="async") as client:
    response = await client.get("/health")
```

## Header Helpers

```python
client.set_header("X-Request-Id", "abc-123")
client.set_headers({"X-Foo": "bar", "X-Baz": "qux"})
client.remove_header("X-Foo")
```

## Base URL

```python
client.set_base_url("https://staging.example.com")
```

## HTTP Methods

All methods accept `**kwargs` forwarded to httpx.

| Method   | Signature                                                       |
| -------- | --------------------------------------------------------------- |
| `get`    | `get(path, *, params=None, headers=None, **kwargs)`             |
| `post`   | `post(path, *, json=None, data=None, content=None, headers=None, **kwargs)` |
| `put`    | `put(path, *, json=None, data=None, content=None, headers=None, **kwargs)`  |
| `patch`  | `patch(path, *, json=None, data=None, content=None, headers=None, **kwargs)`|
| `delete` | `delete(path, *, params=None, headers=None, **kwargs)`          |
