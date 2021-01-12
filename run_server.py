from flask import Flask
from flask import request, jsonify
from . import mysqloo
import json, ast


def RunServer(flaskhost: str, flaskport: int, host: str, port: int, user: str, password: str):
    """
    Start runnung flask server.
    """
    server = Flask(__name__)

    global sql
    sql = mysqloo.NewConnection(
        host=str(host),
        port=int(port),
        user=str(user),
        password=str(password)
    )

    if not "investdb" in sql.list_database():
        sql.create_database("investdb")

    global investdb
    investdb = sql.Database("investdb")

    @server.route("/update/price", methods=["POST"])
    def updatePrice():
        symbol = request.values.get("symbol")
        price = request.values.get("price")
        price = ast.literal_eval(price)
        tbName = symbol.lower() + "_price"
        if not tbName in investdb.list_table():
            investdb.create_table(
                tbName,
                {
                    "date": "DATE NOT NULL PRIMARY KEY",
                    "open": "FLOAT",
                    "high": "FLOAT",
                    "low": "FLOAT",
                    "close": "FLOAT",
                    "adjclose": "FLOAT",
                    "volume": "BIGINT"
                }
            )
        investdb.Table(tbName).update(price)
        return "success"

    @server.route("/update/dividend", methods=["POST"])
    def updateDividend():
        symbol = request.values.get("symbol")
        dividend = request.values.get("dividend")
        dividend = ast.literal_eval(dividend)
        tbName = symbol.lower() + "_divid"
        if not tbName in investdb.list_table():
            investdb.create_table(
                tbName,
                {
                    "date": "DATE NOT NULL PRIMARY KEY",
                    "dividend": "FLOAT"
                }
            )
        investdb.Table(tbName).update(dividend)
        return "success"

    @server.route("/update/stocksplit", methods=["POST"])
    def updateStockSplit():
        symbol = request.values.get("symbol")
        split = request.values.get("stocksplit")
        split = ast.literal_eval(split)
        tbName = symbol.lower() + "_split"
        if not tbName in investdb.list_table():
            investdb.create_table(
                tbName,
                {
                    "date": "DATE NOT NULL PRIMARY KEY",
                    "stocksplit": "CHAR(20)"
                }
            )
        investdb.Table(tbName).update(split)
        return "success"

    # No use, not complete design function.
    @server.route("/update/info", methods=["POST"])
    def updateInfo():
        symbol = request.values.get("symbol")
        info = request.values.get("info")
        tbName = symbol.lower() + "_info"
        if not tbName in investdb.list_table():
            investdb.create_table(
                tbName,
                {
                    "item": "CHAR(200)",
                    "info": "CHAR(200)"
                }
            )
        data = [{"symbol": symbol, "info": info}]
        investdb.Table(tbName).update(data)
        return "success"

    @server.route("/update/commit", methods=["GET"])
    def commit():
        sql.commit()
        return "committed"

    @server.route("/query/price", methods=["GET"])
    def queryPrice():
        symbol = request.values.get("symbol")
        tbName = symbol.lower() + "_price"
        if not tbName in investdb.list_table():
            return "symbol not exists"
        data = investdb.Table(tbName).query("*", "")
        return jsonify(data)

    @server.route("/query/dividend", methods=["GET"])
    def queryDividend():
        symbol = request.values.get("symbol")
        tbName = symbol.lower() + "_divid"
        if not tbName in investdb.list_table():
            return "symbol not exists"
        data = investdb.Table(tbName).query("*", "")
        return jsonify(data)

    @server.route("/query/stocksplit", methods=["GET"])
    def queryStockSplit():
        symbol = request.values.get("symbol")
        tbName = symbol.lower() + "_split"
        if not tbName in investdb.list_table():
            return "symbol not exists"
        data = investdb.Table(tbName).query("*", "")
        return jsonify(data)

    # not use
    @server.route("/query/info", methods=["GET"])
    def queryInfo():
        symbol = request.values.get("symbol")
        tbName = "symbol_info"
        if not tbName in investdb.list_table():
            return "no records"
        data = investdb.Table(tbName).query(
            "*", 'WHERE symbol = "{}"'.format(symbol))
        if len(data) == 0:
            return "symbol not exists"
        data = json.loads(data[0]["info"])
        return jsonify(data)
    
    @server.route("/shutdown", methods=["GET"])
    def shutdownServer():
        sql.close()
        func = request.environ.get('werkzeug.server.shutdown') 
        if func is None: 
            raise RuntimeError('Not running with the Werkzeug Server') 
        func()

    server.run(host=flaskhost, port=flaskport)
