from __future__ import annotations

from typing import Any, Literal

import httpx

# Type alias for the mode parameter
ClientMode = Literal["sync", "async"]


class HttpxClient:
    """
    A unified wrapper around httpx.Client / httpx.AsyncClient.

    Pass mode="sync"  → uses httpx.Client,        methods are regular callables.
    Pass mode="async" → uses httpx.AsyncClient,   methods are coroutines (await them).

    Both modes share:
    - Configurable base_url and default headers
    - set_header / set_headers / remove_header helpers
    - set_base_url helper
    - get, post, put, patch, delete methods
    - close() and context-manager support  (with / async with)
    """

    def __init__(
        self,
        base_url: str = "",
        headers: dict[str, str] | None = None,
        timeout: float | httpx.Timeout = 10.0,
        verify: bool = True,
        mode: ClientMode = "sync",
        **client_kwargs: Any,
    ) -> None:
        if mode not in ("sync", "async"):
            raise ValueError(f"mode must be 'sync' or 'async', got {mode!r}")

        self.mode: ClientMode = mode
        shared: dict[str, Any] = dict(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout,
            verify=verify,
            **client_kwargs,
        )

        self._client: httpx.Client | httpx.AsyncClient = (
            httpx.Client(**shared) if mode == "sync" else httpx.AsyncClient(**shared)
        )

    # ------------------------------------------------------------------
    # Header helpers
    # ------------------------------------------------------------------

    def set_header(self, key: str, value: str) -> None:
        """Add or update a single default header."""
        self._client.headers[key] = value

    def set_headers(self, headers: dict[str, str]) -> None:
        """Merge multiple headers into the default headers."""
        self._client.headers.update(headers)

    def remove_header(self, key: str) -> None:
        """Remove a default header by key (no-op if not present)."""
        self._client.headers.pop(key, None)

    # ------------------------------------------------------------------
    # Base URL helper
    # ------------------------------------------------------------------

    def set_base_url(self, base_url: str) -> None:
        """Update the base URL of the underlying client."""
        self._client.base_url = httpx.URL(base_url)

    # ------------------------------------------------------------------
    # CRUD methods
    # In sync mode  → return httpx.Response directly.
    # In async mode → return a coroutine; the caller must `await` it.
    # ------------------------------------------------------------------

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        return self._client.get(path, params=params, headers=headers, **kwargs)

    def post(
        self,
        path: str,
        *,
        json: Any | None = None,
        data: dict[str, Any] | None = None,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        return self._client.post(
            path, json=json, data=data, content=content, headers=headers, **kwargs
        )

    def put(
        self,
        path: str,
        *,
        json: Any | None = None,
        data: dict[str, Any] | None = None,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        return self._client.put(
            path, json=json, data=data, content=content, headers=headers, **kwargs
        )

    def patch(
        self,
        path: str,
        *,
        json: Any | None = None,
        data: dict[str, Any] | None = None,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        return self._client.patch(
            path, json=json, data=data, content=content, headers=headers, **kwargs
        )

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        return self._client.delete(path, params=params, headers=headers, **kwargs)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> Any:
        """Close the underlying client and release connections."""
        if self.mode == "sync":
            return self._client.close()
        return self._client.aclose()  # type: ignore[union-attr]

    # ------------------------------------------------------------------
    # Sync context manager  (with HttpxClient(..., mode="sync") as c)
    # ------------------------------------------------------------------

    def __enter__(self) -> "HttpxClient":
        if self.mode != "sync":
            raise TypeError("Use 'async with' for async mode, not 'with'.")
        return self

    def __exit__(self, *_: Any) -> None:
        self._client.close()

    # ------------------------------------------------------------------
    # Async context manager  (async with HttpxClient(..., mode="async") as c)
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "HttpxClient":
        if self.mode != "async":
            raise TypeError("Use 'with' for sync mode, not 'async with'.")
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._client.aclose()  # type: ignore[union-attr]

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"HttpxClient("
            f"mode={self.mode!r}, "
            f"base_url={str(self._client.base_url)!r}, "
            f"timeout={self._client.timeout!r})"
        )
