# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import urllib.parse
from contextlib import suppress
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from buda.core.settings import BudaSettings
from buda.socket.channels import Channel
from buda.socket.client import BudaWebSocketClient

FAST_SETTINGS = BudaSettings()


class TestBuildUrl:
    def test_single_public_channel(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        url = client._build_url(Channel.book("btcclp"))
        decoded = urllib.parse.unquote(url)
        assert "book@btcclp" in decoded
        assert "sub?channel=" in decoded

    def test_multiple_channels(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        url = client._build_url(Channel.book("btcclp"), Channel.trades("btcclp"))
        decoded = urllib.parse.unquote(url)
        assert "book@btcclp" in decoded
        assert "trades@btcclp" in decoded

    def test_private_channel_with_key(self):
        client = BudaWebSocketClient(pubsub_key="pk-123", settings=FAST_SETTINGS)
        url = client._build_url(Channel.balances())
        decoded = urllib.parse.unquote(url)
        assert "balances@pk-123" in decoded

    def test_private_channel_without_key_raises(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        with pytest.raises(ValueError, match="private"):
            client._build_url(Channel.orders())

    def test_no_channels_raises(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        with pytest.raises(ValueError, match="At least one channel"):
            client._build_url()

    def test_url_contains_base_uri(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        url = client._build_url(Channel.book("btcclp"))
        assert "realtime.buda.com" in url


class TestSubscribe:
    async def test_subscribe_calls_handler(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        handler = AsyncMock()

        mock_ws = AsyncMock()
        mock_ws.__aiter__ = lambda self: self # type: ignore
        messages = [json.dumps({"ev": "book-changed", "data": "test"})]
        mock_ws.__anext__ = AsyncMock(side_effect=[messages[0], StopAsyncIteration])

        mock_connect = MagicMock()
        mock_connect.__aiter__ = lambda self: iter([mock_ws]) # type: ignore

        with patch("buda.socket.client.connect", return_value=mock_connect):
            # Run subscribe but break after first ws connection
            mock_ws.__aiter__ = lambda self: self # type: ignore
            raw_messages = [json.dumps({"ev": "book-changed", "data": "test"})]

            async def async_iter_messages():
                for msg in raw_messages:
                    yield msg

            mock_ws.__aiter__ = lambda _: async_iter_messages() # type: ignore

            async def connect_iter():
                yield mock_ws
                return

            mock_connect_ctx = MagicMock()
            mock_connect_ctx.__aiter__ = lambda _: connect_iter() # type: ignore

            with patch("buda.socket.client.connect", return_value=mock_connect_ctx):
                # We need to cancel the infinite subscribe loop
                import asyncio
                task = asyncio.create_task(
                    client.subscribe(Channel.book("btcclp"), handler=handler)
                )
                await asyncio.sleep(0.1)
                task.cancel()
                with suppress(asyncio.CancelledError):
                    await task

                handler.assert_called()

    async def test_subscribe_filters_events(self):
        client = BudaWebSocketClient(settings=FAST_SETTINGS)
        handler = AsyncMock()

        raw_messages = [
            json.dumps({"ev": "book-changed", "data": "wanted"}),
            json.dumps({"ev": "other-event", "data": "unwanted"}),
        ]

        async def async_iter_messages():
            for msg in raw_messages:
                yield msg

        mock_ws = AsyncMock()
        mock_ws.__aiter__ = lambda _: async_iter_messages() # type: ignore

        async def connect_iter():
            yield mock_ws

        mock_connect_ctx = MagicMock()
        mock_connect_ctx.__aiter__ = lambda _: connect_iter() # type: ignore

        with patch("buda.socket.client.connect", return_value=mock_connect_ctx):
            import asyncio
            task = asyncio.create_task(
                client.subscribe(
                    Channel.book("btcclp"),
                    handler=handler,
                    events={"book-changed"},
                )
            )
            await asyncio.sleep(0.1)
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

            # Handler called only once (for "book-changed"), not for "other-event"
            assert handler.call_count == 1
            call_data = handler.call_args[0][0]
            assert call_data["ev"] == "book-changed"


class TestConvenienceMethods:
    async def test_book_delegates_to_subscribe(self):
        with patch.object(BudaWebSocketClient, "subscribe", new_callable=AsyncMock) as mock_sub:
            client = BudaWebSocketClient(settings=FAST_SETTINGS)
            await client.book("btcclp")
            mock_sub.assert_called_once()
            args, _ = mock_sub.call_args
            assert args[0].name == "book"
            assert args[0].param == "btcclp"

    async def test_trades_delegates_to_subscribe(self):
        with patch.object(BudaWebSocketClient, "subscribe", new_callable=AsyncMock) as mock_sub:
            client = BudaWebSocketClient(settings=FAST_SETTINGS)
            await client.trades("btcclp")
            mock_sub.assert_called_once()
            args, _ = mock_sub.call_args
            assert args[0].name == "trades"

    async def test_balances_delegates_to_subscribe(self):
        with patch.object(BudaWebSocketClient, "subscribe", new_callable=AsyncMock) as mock_sub:
            client = BudaWebSocketClient(pubsub_key="pk", settings=FAST_SETTINGS)
            await client.balances()
            mock_sub.assert_called_once()
            args, _ = mock_sub.call_args
            assert args[0].name == "balances"

    async def test_orders_delegates_to_subscribe(self):
        with patch.object(BudaWebSocketClient, "subscribe", new_callable=AsyncMock) as mock_sub:
            client = BudaWebSocketClient(pubsub_key="pk", settings=FAST_SETTINGS)
            await client.orders()
            mock_sub.assert_called_once()
            args, _ = mock_sub.call_args
            assert args[0].name == "orders"

    async def test_deposits_delegates_to_subscribe(self):
        with patch.object(BudaWebSocketClient, "subscribe", new_callable=AsyncMock) as mock_sub:
            client = BudaWebSocketClient(pubsub_key="pk", settings=FAST_SETTINGS)
            await client.deposits()
            mock_sub.assert_called_once()
            args, _ = mock_sub.call_args
            assert args[0].name == "deposits"
