# SteelEye - API Developer Assessment

Problem Statement: Writing a functional API in Python using FastAPI framework to provide a set of endpoints for retrieving a list of Trades, retrieving a single Trade by ID, searching against Trades, and filtering Trades

## Requirements:
- Python 3.9
- fastapi 
- uvicorn[standard]

## Prerequisites:
- Created a virtual environment
```console
PS python -m venv apienv
```
- Activate virtual environment
```console
PS .\apienv\Scripts\activate
```
- Install necessary packages
```console
(apienv) PS pip install fastapi
(apienv) PS pip install uvicorn[standard]
```
## API endpoints created:
1. GET /trades: List Trades
   - Endpoint to fetch a list of all trades.
   - Also supports filtering using the following query parameters:
 ```console
    asset_class: Asset class of the trades to be filtered
    end: Date before which trades to filter.
    max_price: Maximum price of trades to filter.
    min_price: Minimum price of trades to filter.
    start: Date after which trades to filter
    trade_type: tradeDetails.buySellIndicator is BUY or SELL
```

2. GET /get-trade/{trade_id} Get Trade
   - Endpoint to fetch a single trade by its trade_id from the API

3. GET /search-trade Search Trade
   - Endpoint to search across all trades 
   - Supports following parameters:
```console
    counterparty: Counterparty for the trade to be searched.
    instrument_id: Instrument ID for the trade to be searched.
    instrument_name: Instrument name of the trade to be searched.
    trader: Trader name to be searched
```

## Testing endpoints:
- Open the terminal to execute:
```console
uvicorn main:app --reload
```
- Click on the local host url generated. eg.:
```console
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20720] using WatchFiles
INFO:     Started server process [23084]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
- Clicking on the URL will be redirected to Swagger UI docs automatically
- Check endpoints 
