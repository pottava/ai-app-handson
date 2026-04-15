"""ユーザー API ツール関数のユニットテスト"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from app.tools.apis import get_user_by_id, get_users


class TestGetUsers:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        mock_users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_users)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_users()

        assert result["status"] == "success"
        assert result["users"] == mock_users

    @pytest.mark.asyncio
    async def test_client_error(self) -> None:
        mock_session = AsyncMock()
        mock_session.get = MagicMock(
            side_effect=aiohttp.ClientError("connection failed")
        )
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_users()

        assert "エラー" in result["status"]

    @pytest.mark.asyncio
    async def test_timeout(self) -> None:
        mock_session = AsyncMock()
        mock_session.get = MagicMock(side_effect=asyncio.TimeoutError())
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_users()

        assert "タイムアウト" in result["status"]

    @pytest.mark.asyncio
    async def test_returns_dict(self) -> None:
        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value=[])
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_users()

        assert isinstance(result, dict)


class TestGetUserById:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        mock_user = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value=mock_user)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_user_by_id(1)

        assert result["status"] == "success"
        assert result["user"] == mock_user

    @pytest.mark.asyncio
    async def test_invalid_type(self) -> None:
        result = await get_user_by_id("abc")  # type: ignore[arg-type]
        assert "エラー" in result["status"]

    @pytest.mark.asyncio
    async def test_client_error(self) -> None:
        mock_session = AsyncMock()
        mock_session.get = MagicMock(
            side_effect=aiohttp.ClientError("connection failed")
        )
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_user_by_id(1)

        assert "エラー" in result["status"]

    @pytest.mark.asyncio
    async def test_timeout(self) -> None:
        mock_session = AsyncMock()
        mock_session.get = MagicMock(side_effect=asyncio.TimeoutError())
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_user_by_id(1)

        assert "タイムアウト" in result["status"]

    @pytest.mark.asyncio
    async def test_returns_dict(self) -> None:
        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value={})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            result = await get_user_by_id(1)

        assert isinstance(result, dict)
