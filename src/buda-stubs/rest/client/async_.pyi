import sys
from types import TracebackType
from typing import Any, Literal, TypeVar, overload

from httpx import AsyncClient
from pydantic import BaseModel
from typing_extensions import deprecated

from buda.core.limiter import AsyncRateLimiter
from buda.core.providers import BudaCredentials
from buda.core.settings import BudaSettings
from buda.rest.client.base import BaseClient
from buda.rest.endpoints.base import Endpoint, RequestMethod
from buda.rest.endpoints.orders import QuotationPayload, TradesParams
from buda.rest.models.account import Balance, BalanceList, UserInfo
from buda.rest.models.markets import Market, MarketList, MarketTicker, TickerList
from buda.rest.models.orders import (
    OrderBook,
    OrderCancelAllResponse,
    OrderCancelResponse,
    OrderCreate,
    OrderCreateResponse,
    OrderDetail,
    Quotation,
    Trades,
)

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

T = TypeVar("T", bound=BaseModel)

class AsyncPublicAPI:
    """Public API endpoints for the Buda API."""

    __slots__ = ("_client",)

    _client: AsyncBudaClient
    """The AsyncBudaClient instance used to make API requests."""

    def __init__(self, client: AsyncBudaClient) -> None:
        """
        Initialize the AsyncPublicAPI instance.

        Parameters
        ----------
        client : AsyncBudaClient
            The AsyncBudaClient instance used to make API requests.
        """
        ...

    @overload
    async def markets(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> Market: ...
    @overload
    async def markets(
        self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> MarketList: ...
    @overload
    async def markets(
        self, market_id: str | None = ..., *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...
    async def markets(
        self, market_id: str | None = ..., *, raw: bool = ..., authenticated: bool = ...
    ) -> Market | MarketList | dict[str, Any]:
        """
        Fetch market information from the Buda API.

        Parameters
        ----------
        market_id : str | None, optional
            The ID of the market to fetch. If None, fetches all markets.
            By default, None.
        raw : bool, optional
            Whether to return the raw API response. By default, False.
        authenticated : bool, optional
            Whether to use authenticated requests. By default, False.

        Returns
        -------
        Market | MarketList | dict[str, Any]
            The market information, either as a :class:`Market` object,
            a :class:`MarketList`, or the raw API response as a dictionary.
        """
        ...

    @overload
    async def tickers(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> MarketTicker: ...
    @overload
    async def tickers(
        self, market_id: None = ..., *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> TickerList: ...
    @overload
    async def tickers(
        self, market_id: str | None = ..., *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...
    async def tickers(
        self, market_id: str | None = ..., *, raw: bool = ..., authenticated: bool = ...
    ) -> MarketTicker | TickerList | dict[str, Any]:
        """
        Fetch ticker information from the Buda API.

        Parameters
        ----------
        market_id : str | None, optional
            The ID of the market to fetch tickers for. If None,
            fetches all tickers. By default, None.
        raw : bool, optional
            Whether to return the raw API response. By default, False.
        authenticated : bool, optional
            Whether to use authenticated requests. By default, False.

        Returns
        -------
        MarketTicker | TickerList | dict[str, Any]
            The ticker information, either as a :class:`MarketTicker` object,
            a :class:`TickerList`, or the raw API response as a dictionary.
        """
        ...

    @overload
    async def order_book(
        self, market_id: str, *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> OrderBook: ...
    @overload
    async def order_book(
        self, market_id: str, *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...
    async def order_book(
        self, market_id: str, *, raw: bool = ..., authenticated: bool = ...
    ) -> OrderBook | dict[str, Any]:
        """
        Fetch the order book for a specific market from the Buda API.

        Parameters
        ----------
        market_id : str
            The ID of the market to fetch the order book for.
        raw : bool, optional
            Whether to return the raw API response. By default, False.
        authenticated : bool, optional
            Whether to use authenticated requests. By default, False.

        Returns
        -------
        OrderBook | dict[str, Any]
            The order book information, either as an :class:`OrderBook`
            object or the raw API response as a dictionary.
        """
        ...

    @overload
    @deprecated(
        "Authenticated trades requests with query params return 401. "
        "Use authenticated=False (default) when passing params."
    )
    async def trades(
        self,
        market_id: str,
        *,
        params: TradesParams,
        authenticated: Literal[True],
        raw: Literal[False] = ...,
    ) -> Trades: ...
    @overload
    @deprecated(
        "Authenticated trades requests with query params return 401. "
        "Use authenticated=False (default) when passing params."
    )
    async def trades(
        self,
        market_id: str,
        *,
        params: TradesParams,
        authenticated: Literal[True],
        raw: Literal[True],
    ) -> dict[str, Any]: ...
    @overload
    async def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = ...,
        raw: Literal[False] = ...,
        authenticated: bool = ...,
    ) -> Trades: ...
    @overload
    async def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = ...,
        raw: Literal[True],
        authenticated: bool = ...,
    ) -> dict[str, Any]: ...
    async def trades(
        self,
        market_id: str,
        *,
        params: TradesParams | None = ...,
        raw: bool = ...,
        authenticated: bool = ...,
    ) -> Trades | dict[str, Any]: ...
    @overload
    async def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: Literal[False] = ...,
        authenticated: bool = ...,
    ) -> Quotation: ...
    @overload
    async def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: Literal[True],
        authenticated: bool = ...,
    ) -> dict[str, Any]: ...
    async def quotations(
        self,
        market_id: str,
        *,
        payload: QuotationPayload,
        raw: bool = ...,
        authenticated: bool = ...,
    ) -> Quotation | dict[str, Any]:
        """
        Fetch quotations for a specific market from the Buda API.

        Parameters
        ----------
        market_id : str
            The ID of the market to fetch quotations for.
        payload : QuotationPayload
            The payload containing the quotation parameters.
        raw : bool, optional
            Whether to return the raw API response. By default, False.
        authenticated : bool, optional
            Whether to use authenticated requests. By default, False.

        Returns
        -------
        Quotation | dict[str, Any]
            The quotation information, either as a :class:`Quotation`
            object or the raw API response as a dictionary.
        """
        ...

class AsyncPrivateAPI:
    """Private API endpoints for the Buda API."""

    __slots__ = ("_client",)

    _client: AsyncBudaClient
    """The AsyncBudaClient instance used to make API requests."""

    def __init__(self, client: AsyncBudaClient) -> None:
        """
        Initialize the AsyncPrivateAPI instance.

        Parameters
        ----------
        client : AsyncBudaClient
            The AsyncBudaClient instance used to make API requests.
        """
        ...

    @overload
    async def me(self, *, raw: Literal[False] = ...) -> UserInfo: ...
    @overload
    async def me(self, *, raw: Literal[True]) -> dict[str, Any]: ...
    async def me(self, *, raw: bool = ...) -> UserInfo | dict[str, Any]:
        """
        Fetch information about the authenticated user from the Buda API.

        Parameters
        ----------
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        UserInfo | dict[str, Any]
            The user information, either as a :class:`UserInfo` object
            or the raw API response as a dictionary.
        """
        ...

    @overload
    async def balances(self, currency: str, *, raw: Literal[False] = ...) -> Balance: ...
    @overload
    async def balances(self, currency: None = ..., *, raw: Literal[False] = ...) -> BalanceList: ...
    @overload
    async def balances(
        self, currency: str | None = ..., *, raw: Literal[True]
    ) -> dict[str, Any]: ...
    async def balances(
        self, currency: str | None = ..., *, raw: bool = ...
    ) -> Balance | BalanceList | dict[str, Any]:
        """
        Fetch the balances for the authenticated user from the Buda API.

        Parameters
        ----------
        currency : str | None, optional
            The currency to fetch the balance for. If None,
            fetches all balances. By default, None.
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        Balance | BalanceList | dict[str, Any]
            The balance information, either as a :class:`Balance` or
            :class:`BalanceList` object or the raw API response as a dictionary.
        """
        ...

    @overload
    async def create_order(
        self, market_id: str, *, payload: OrderCreate, raw: Literal[False] = ...
    ) -> OrderCreateResponse: ...
    @overload
    async def create_order(
        self, market_id: str, *, payload: OrderCreate, raw: Literal[True]
    ) -> dict[str, Any]: ...
    async def create_order(
        self, market_id: str, *, payload: OrderCreate, raw: bool = ...
    ) -> OrderCreateResponse | dict[str, Any]:
        """
        Create a new order in the specified market.

        Parameters
        ----------
        market_id : str
            The ID of the market where the order will be placed.
        payload : OrderCreate
            The payload containing the order details.
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        OrderCreateResponse | dict[str, Any]
            The response from the API, either as an :class:`OrderCreateResponse`
            object or the raw API response as a dictionary.
        """
        ...

    @overload
    async def order_detail(self, order_id: int, *, raw: Literal[False] = ...) -> OrderDetail: ...
    @overload
    async def order_detail(self, order_id: int, *, raw: Literal[True]) -> dict[str, Any]: ...
    async def order_detail(self, order_id: int, *, raw: bool = ...) -> OrderDetail | dict[str, Any]:
        """
        Fetch the details of a specific order from the Buda API.

        Parameters
        ----------
        order_id : int
            The ID of the order to fetch.
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        OrderDetail | dict[str, Any]
            The order details, either as an :class:`OrderDetail` object
            or the raw API response as a dictionary.
        """
        ...

    @overload
    async def cancel_order(
        self, order_id: int, *, raw: Literal[False] = ...
    ) -> OrderCancelResponse: ...
    @overload
    async def cancel_order(self, order_id: int, *, raw: Literal[True]) -> dict[str, Any]: ...
    async def cancel_order(
        self, order_id: int, *, raw: bool = ...
    ) -> OrderCancelResponse | dict[str, Any]:
        """
        Cancel a specific order in the Buda API.

        Parameters
        ----------
        order_id : int
            The ID of the order to cancel.
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        OrderCancelResponse | dict[str, Any]
            The response from the API, either as an :class:`OrderCancelResponse`
            object or the raw API response as a dictionary.
        """
        ...

    @overload
    async def cancel_all_orders(
        self, market_id: str | None = ..., type: str | None = ..., *, raw: Literal[False] = ...
    ) -> OrderCancelAllResponse: ...
    @overload
    async def cancel_all_orders(
        self, market_id: str | None = ..., type: str | None = ..., *, raw: Literal[True]
    ) -> dict[str, Any]: ...
    async def cancel_all_orders(
        self, market_id: str | None = ..., type: str | None = ..., *, raw: bool = ...
    ) -> OrderCancelAllResponse | dict[str, Any]:
        """
        Cancel all orders in the Buda API.

        Parameters
        ----------
        market_id : str | None, optional
            The ID of the market where the orders will be canceled. If None,
            orders in all markets will be canceled. By default, None.
        type : str | None, optional
            The type of orders to cancel. By default, None.
        raw : bool, optional
            Whether to return the raw API response. By default, False.

        Returns
        -------
        OrderCancelAllResponse | dict[str, Any]
            The response from the API, either as an :class:`OrderCancelAllResponse`
            object or the raw API response as a dictionary.
        """
        ...

class AsyncBudaClient(BaseClient[AsyncClient]):
    """Asynchronous client for the Buda API."""

    __slots__ = ("_rate_limiter", "private", "public")

    _rate_limiter: AsyncRateLimiter
    """The rate limiter instance used to manage API request rates."""
    private: AsyncPrivateAPI
    """The private API endpoints for the Buda API."""
    public: AsyncPublicAPI
    """The public API endpoints for the Buda API."""

    def __init__(
        self, settings: BudaSettings | None = ..., provider: BudaCredentials | None = ...
    ) -> None:
        """
        Initialize the AsyncBudaClient instance.

        Parameters
        ----------
        settings : BudaSettings | None, optional
            The settings for the AsyncBudaClient, by default None.
        provider : BudaCredentials | None, optional
            The credentials provider for the AsyncBudaClient, by default None.
        """
        ...

    async def __aenter__(self) -> AsyncBudaClient: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    async def close(self) -> None:
        """Close the AsyncBudaClient instance and release any resources."""
        ...

    @overload
    async def _request(
        self, endpoint: Endpoint[T], *, raw: Literal[False] = ..., authenticated: bool = ...
    ) -> T: ...
    @overload
    async def _request(
        self, endpoint: Endpoint[T], *, raw: Literal[True], authenticated: bool = ...
    ) -> dict[str, Any]: ...
    async def _request(
        self, endpoint: Endpoint[T], *, raw: bool = ..., authenticated: bool = ...
    ) -> T | dict[str, Any]:
        """
        Make an API request to the specified endpoint.

        Parameters
        ----------
        endpoint : Endpoint[T]
            The API endpoint to make the request to.
        raw : bool, optional
            Whether to return the raw API response. By default, False.
        authenticated : bool, optional
            Whether to use authenticated requests. By default, False.

        Returns
        -------
        T | dict[str, Any]
            The response from the API, either as a parsed object
            of type T or the raw API response as a dictionary.
        """
        ...

    async def _raw_request(
        self, method: RequestMethod, path: str, *, authenticated: bool = ..., **kwargs: Any
    ) -> dict[str, Any]:
        """
        Make a raw API request to the specified path.

        Parameters
        ----------
        method : RequestMethod
            The HTTP method to use for the request.
        path : str
            The API path to make the request to.
        authenticated : bool, optional
            Whether to use authenticated requests.
            By default, False.
        **kwargs : Any
            Additional keyword arguments to pass to the HTTP
            client's request method.

        Returns
        -------
        dict[str, Any]
            The raw API response as a dictionary.
        """
        ...
