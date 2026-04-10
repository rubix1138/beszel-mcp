"""PocketBase client for interacting with Beszel's backend."""

import httpx
from typing import Any, Optional
from datetime import datetime


class PocketBaseClient:
    """Client for interacting with PocketBase API."""

    def __init__(self, base_url: str, email: Optional[str] = None, password: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.client = httpx.AsyncClient(timeout=30.0)

    async def authenticate(self) -> None:
        """Authenticate with PocketBase using user credentials."""
        if not self.email or not self.password:
            return

        try:
            response = await self.client.post(
                f"{self.base_url}/api/collections/users/auth-with-password",
                json={"identity": self.email, "password": self.password},
            )
            response.raise_for_status()
            self.token = response.json().get("token")
        except Exception as e:
            raise Exception(f"Failed to authenticate with Beszel: {e}")

    async def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        """Make an authenticated request, re-authing once on 401."""
        for attempt in range(2):
            headers = {"Content-Type": "application/json"}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            response = await self.client.request(method, f"{self.base_url}{path}", headers=headers, **kwargs)

            if response.status_code == 401 and attempt == 0 and self.email:
                # Token expired — re-authenticate and retry once
                self.token = None
                await self.authenticate()
                continue

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Beszel API error ({path}): {e.response.text}")

            return response.json()

        raise Exception("Authentication failed after retry")

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_list(
        self,
        collection: str,
        page: int = 1,
        per_page: int = 50,
        filter: Optional[str] = None,
        sort: Optional[str] = None,
        expand: Optional[str] = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "perPage": per_page}
        if filter:
            params["filter"] = filter
        if sort:
            params["sort"] = sort
        if expand:
            params["expand"] = expand

        return await self._request("GET", f"/api/collections/{collection}/records", params=params)

    async def get_one(
        self,
        collection: str,
        record_id: str,
        expand: Optional[str] = None,
    ) -> dict[str, Any]:
        params = {}
        if expand:
            params["expand"] = expand
        return await self._request("GET", f"/api/collections/{collection}/records/{record_id}", params=params)

    async def query_stats(
        self,
        collection: str,
        filter: str,
        page: int = 1,
        per_page: int = 100,
        sort: str = "-created",
    ) -> dict[str, Any]:
        return await self.get_list(
            collection=collection,
            page=page,
            per_page=per_page,
            filter=filter,
            sort=sort,
        )

    async def close(self) -> None:
        await self.client.aclose()

    def build_time_filter(
        self,
        field: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> str:
        filters = []
        if start_time:
            filters.append(f"{field} >= '{start_time}'")
        if end_time:
            filters.append(f"{field} <= '{end_time}'")
        return " && ".join(filters) if filters else ""
