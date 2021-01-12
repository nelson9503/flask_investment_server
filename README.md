# flask_investment_server - Methods

**func |** `RunServer` `(` `flaskhost`: *str*, `flaskport`: *int*, `host`: *str*, `port`: *int*, `user`: *str*, `password`: *str* `)`

---

## URL Requests

`/update/price` **POST** symbol, price
`/update/dividend` **POST** symbol, dividend
`/update/stocksplit` **POST** symbol, stocksplit
`/update/commit` **GET**

`/query/price` **GET** symbol
`/query/dividend` **GET** symbol
`/query/stocksplit` **GET** symbol

`/shutdown` **GET**