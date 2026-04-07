<h1 align="center">Buda Client</h1>

<h3 align="center">A typed Python client for the Buda.com REST and WebSocket APIs — sync and async.</h3>

<p align="center">
  <a href="https://github.com/mschiaff/buda-client/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/mschiaff/buda-client" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13">
  <img src="https://img.shields.io/badge/status-alpha-orange" alt="Alpha">
</p>

---

**Buda Client** is a Python library that wraps the [Buda.com](https://www.buda.com) API, giving you a clean, fully typed interface for querying markets, managing orders, checking balances, and streaming real-time data — all without having to deal with raw HTTP requests or WebSocket frames yourself. It works great for scripts, bots, data pipelines, or just poking around from a REPL.

> [!WARNING]
> **This is not an official Buda.com product.** It is an independent, community-driven project with no affiliation to or endorsement by Buda.com.
>
> The library is currently in **alpha** (`v0.1.0`). APIs may change, features may be incomplete, and bugs are expected. If you choose to use it in production or with real funds, you do so **entirely at your own risk**. The authors assume no responsibility for any financial loss, data issues, or other damages that may result from its use.

## Features

- **Sync and async REST clients** — `BudaClient` for synchronous code, `AsyncBudaClient` for `asyncio` workflows. Both expose the same intuitive API.
- **Real-time WebSocket streaming** — Subscribe to order book updates, trades, balances, orders, and deposits via `BudaWebSocketClient`.
- **HMAC-SHA384 authentication** — Secure request signing handled automatically when you provide credentials.
- **Proactive rate limiting** — A sliding-window limiter throttles requests *before* they hit the server, respecting per-second, per-minute (authenticated), and per-minute (unauthenticated) limits.
- **Automatic retries** — Failed requests on 429, 500, and 503 are retried with exponential backoff, honoring the server's `Retry-After` header when present.
- **Pydantic v2 models** — Every API response is parsed into a strict, typed Pydantic model. No more guessing what keys a dict has.
- **Flexible credential providers** — Pass credentials directly, read them from environment variables, or load them from a `.env` file.
- **Full type safety** — Developed with Pyright in strict mode. Your editor's autocomplete will thank you.

## Installation

> [!NOTE]
> Buda Client is not yet published on PyPI. Install it directly from GitHub:

```bash
uv add git+https://github.com/mschiaff/buda-client.git
```

or with pip:

```bash
pip install git+https://github.com/mschiaff/buda-client.git
```

**Requirements:** Python 3.13

## Quick Start

### Fetching public market data

No credentials needed — just create a client and go:

```python
from buda import BudaClient

with BudaClient() as client:
    # List all available markets
    markets = client.public.markets()
    for market in markets.root:
        print(f"{market.id}: {market.base_currency}/{market.quote_currency}")

    # Get the ticker for a specific market
    ticker = client.public.tickers("btc-clp")
    print(f"BTC-CLP last price: {ticker.last_price.value} {ticker.last_price.currency}")

    # Fetch the order book
    book = client.public.order_book("btc-clp")
    print(f"Best bid: {book.bids[0].price}, Best ask: {book.asks[0].price}")
```

The clients also work fine without a context manager — just remember to close them when you're done:

```python
from buda import BudaClient

client = BudaClient()
markets = client.public.markets()
client.close()
```

### Async usage

Same API, just `async`:

```python
import asyncio
from buda import AsyncBudaClient

async def main():
    async with AsyncBudaClient() as client:
        ticker = await client.public.tickers("btc-clp")
        print(f"Last price: {ticker.last_price.value}")

asyncio.run(main())
```

### Authentication

Choose the credential provider that fits your setup:

```python
from buda import BudaClient, StaticCredentials, EnvCredentials, DotEnvCredentials

# Option 1: Pass credentials directly
provider = StaticCredentials(api_key="your-key", api_secret="your-secret")

# Option 2: Read from BUDA_API_KEY and BUDA_API_SECRET environment variables
provider = EnvCredentials()

# Option 3: Load from a .env file
provider = DotEnvCredentials()  # looks for .env in the current directory

with BudaClient(provider=provider) as client:
    # Now you can access private endpoints
    balances = client.private.balances()
    for balance in balances.root:
        print(f"{balance.id}: {balance.available_amount.value} available")

    me = client.private.me()
    print(f"Logged in as: {me.email}")
```

### Creating an order

```python
from buda import BudaClient, DotEnvCredentials, OrderCreate

with BudaClient(provider=DotEnvCredentials()) as client:
    order = client.private.create_order(
        "btc-clp",
        payload=OrderCreate(
            type="Bid",
            price_type="limit",
            amount=0.001,
            limit={"price": 50_000_000},
        ),
    )
    print(f"Order {order.id} created — state: {order.state}")
```

### WebSocket streaming

Stream real-time data with an async handler:

```python
import asyncio
from buda import BudaWebSocketClient

async def on_event(data: dict) -> None:
    print(f"Event: {data}")

async def main():
    ws = BudaWebSocketClient()
    await ws.book("btcclp", handler=on_event)

asyncio.run(main())
```

For private channels (balances, orders, deposits), pass your `pubsub_key`:

```python
ws = BudaWebSocketClient(pubsub_key="your-pubsub-key")
await ws.orders(handler=on_event)
```

> [!TIP]
> You can get your `pubsub_key` from the `me()` endpoint: `client.private.me().pubsub_key`.

## Configuration

Customize client behavior through `BudaSettings`:

```python
from buda import BudaClient, BudaSettings

settings = BudaSettings(
    timeout=30.0,                   # Request timeout in seconds (default: 10)
    retry_max_attempts=5,           # Max retry attempts (default: 3)
    rate_limit_per_second=10,       # Per-second request limit (default: 20)
)

with BudaClient(settings=settings) as client:
    ...
```

See the `BudaSettings` class for the full list of configurable options, including retry backoff parameters, rate limit windows, and WebSocket timeouts.

## Contributing

Contributions are welcome! Whether it's a bug report, feature suggestion, or pull request — every bit helps.

Check out the [Contributing Guide](CONTRIBUTING.md) to get started.

## License

This project is licensed under the [Apache License 2.0](LICENSE).