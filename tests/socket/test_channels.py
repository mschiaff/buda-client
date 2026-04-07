from __future__ import annotations

import pytest

from buda.socket.channels import Channel


class TestChannelFactoryMethods:
    def test_book(self):
        ch = Channel.book("btcclp")
        assert ch.name == "book"
        assert ch.param == "btcclp"
        assert ch.private is False

    def test_trades(self):
        ch = Channel.trades("btcclp")
        assert ch.name == "trades"
        assert ch.param == "btcclp"
        assert ch.private is False

    def test_balances(self):
        ch = Channel.balances()
        assert ch.name == "balances"
        assert ch.param == ""
        assert ch.private is True

    def test_orders(self):
        ch = Channel.orders()
        assert ch.name == "orders"
        assert ch.param == ""
        assert ch.private is True

    def test_deposits(self):
        ch = Channel.deposits()
        assert ch.name == "deposits"
        assert ch.param == ""
        assert ch.private is True


class TestChannelResolve:
    def test_public_channel_resolve(self):
        ch = Channel.book("btcclp")
        assert ch.resolve() == "book@btcclp"

    def test_public_channel_resolve_ignores_pubsub_key(self):
        ch = Channel.trades("btcclp")
        assert ch.resolve(pubsub_key="some-key") == "trades@btcclp"

    def test_private_channel_resolve_with_key(self):
        ch = Channel.balances()
        assert ch.resolve(pubsub_key="pk-123") == "balances@pk-123"

    def test_private_channel_resolve_without_key_raises(self):
        ch = Channel.orders()
        with pytest.raises(ValueError, match="private"):
            ch.resolve()

    def test_private_channel_resolve_empty_key_raises(self):
        ch = Channel.deposits()
        with pytest.raises(ValueError, match="private"):
            ch.resolve(pubsub_key="")


class TestChannelFrozen:
    def test_immutable(self):
        ch = Channel.book("btcclp")
        with pytest.raises(AttributeError):
            ch.name = "other"  # type: ignore[misc]
