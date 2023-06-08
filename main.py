# importing necessary packages
import datetime as dt
from typing import Optional
from fastapi import FastAPI, Path, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
# from fastapi_pagination import Page, add_pagination, paginate


# pydantic model representing a trade
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None,
                                       description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None,
                                        description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId",
                               description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails",
                                        description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


# creating fastapi instance
app = FastAPI()
# add_pagination(app)

# mock database interaction layer
trades = {
    '1': {
        "asset_class": "Bond",
        "counterparty": "ABC Bank",
        "instrument_id": "TSLA",
        "instrument_name": "Tesla Inc",
        "trade_date_time": dt.datetime.fromisoformat("2023-06-01T09:30:00"),
        "trade_details": {
            "buySellIndicator": "BUY",
            "price": 750.0,
            "quantity": 10,
        },
        "trade_id": "1",
        'trader': "Alex",
    },
    '2': {
        "asset_class": "Equity",
        "counterparty": "DEF Bank",
        "instrument_id": "AAPL",
        "instrument_name": "US Dollar",
        "trade_date_time": dt.datetime.fromisoformat("2023-06-02T15:45:00"),
        "trade_details": {
            "buySellIndicator": "SELL",
            "price": 250.0,
            "quantity": 100,
        },
        "trade_id": "2",
        "trader": "Bob",
    },
    '3': {
        "asset_class": "FX",
        "counterparty": "XYZ Bank",
        "instrument_id": "AMZN",
        "instrument_name": "US Dollar",
        "trade_date_time": dt.datetime.fromisoformat("2023-06-03T11:15:00"),
        "trade_details": {
            "buySellIndicator": "BUY",
            "price": 1200,
            "quantity": 50,
        },
        "trade_id": "3",
        "trader": "Charles",
    },
    '4': {
        "asset_class": "Bond",
        "counterparty": "UWU Bank",
        "instrument_id": "GOOGL",
        "instrument_name": "Tesla Inc",
        "trade_date_time": dt.datetime.fromisoformat("2023-06-09T14:20:00"),
        "trade_details": {
            "buySellIndicator": "BUY",
            "price": 1500.0,
            "quantity": 25,
        },
        "trade_id": "4",
        'trader': "Daniel",
    },
}


# redirecting to swagger-ui docs
@app.get("/")
def docs_redirect():
    return RedirectResponse(url='/docs')


# fetching list of all trades
# if parameters provided as described, filters trades accordingly
@app.get("/trades")
def list_trades(
        asset_class: Optional[str] = Query(None, description="Asset class of the trades to be filtered"),
        end: Optional[dt.datetime] = Query(None, description="Date before which trades to filter."),
        max_price: Optional[float] = Query(None, description="Maximum price of trades to filter."),
        min_price: Optional[float] = Query(None, description="Minimum price of trades to filter."),
        start: Optional[dt.datetime] = Query(None, description="Date after which trades to filter"),
        trade_type: Optional[str] = Query(None, description="tradeDetails.buySellIndicator is BUY or SELL"),
):
    # list to contain trades to be shown
    filtered_trades = []

    # filters and retrieves trades if optional parameters given
    # returns all trades if no parameters given
    # trade added when either no parameters given or when condition on parameters satisfied
    for trade_id, trade in trades.items():
        if (
            (not asset_class or trade['asset_class'] == asset_class) and
            (not end or trade['trade_date_time'] <= end) and
            (not max_price or trade['trade_details']['price'] <= max_price) and
            (not min_price or trade['trade_details']['price'] >= min_price) and
            (not start or trade['trade_date_time'] >= start) and
            (not trade_type or trade['trade_details']['buySellIndicator'] == trade_type.upper())
        ):
            filtered_trades.append(trade)
    return filtered_trades


# endpoint to fetch a trade by its trade_id
# trade_id taken as path parameter
@app.get("/get-trade/{trade_id}")
def get_trade(trade_id: str = Path(description="The Trade ID to be fetched.")):
    return trades[trade_id]


# endpoint for fetching list of trades
# supports searching by: counterparty, instrumentId, instrumentName, trader
@app.get("/search-trade")
def search_trade(
    counterparty: Optional[str] = Query(None, description="Counterparty for the trade to be searched."),
    instrument_id: Optional[str] = Query(None, description="Instrument ID for the trade to be searched."),
    instrument_name: Optional[str] = Query(None, description="Instrument name of the trade to be searched."),
    trader: Optional[str] = Query(None, description="Enter trader name")
):
    found_trades = []

    # adds to list when any condition matches and if parameter exists
    for trade_id, trade in trades.items():
        if (trader and trade["trader"] == trader) \
                or (counterparty and trade["counterparty"] == counterparty) \
                or (instrument_id and trade["instrument_id"] == instrument_id.upper()) \
                or (instrument_name and trade["instrument_name"] == instrument_name):
            found_trades.append(trade)
    if found_trades:
        return found_trades
    return {"Data": "Not found."}


# adding pagination to data
# @app.get("/trades")
# def list_trades():
#     return paginate(trades)