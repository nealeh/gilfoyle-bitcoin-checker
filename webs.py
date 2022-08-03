from websocket import create_connection
import json
import time
from playsound import playsound
import sys
import dateutil.parser

URL = "wss://ws-feed.pro.coinbase.com"

ws = create_connection(URL)

params = {"type": "subscribe", "product_ids": ["BTC-USD"],
"channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]}

# {'type': 'ticker', 'sequence': 22868951000, 'product_id': 'BTC-USD', 'price': '58193.25', 'open_24h': '54839.16', 
# 'volume_24h': '22151.57398753', 'low_24h': '54138.01', 'high_24h': '59576.18', 'volume_30d': '734284.99591688', 
# 'best_bid': '58184.50', 'best_ask': '58193.25', 'side': 'buy', 'time': '2021-03-18T11:48:34.775847Z', 
# 'trade_id': 146606993, 'last_size': '0.0021167'}
    
try:
    while True:
        ws.send(json.dumps(params))
        result = ws.recv()
        converted = json.loads(result)
        if 'price' in converted:
            btc_price = float(converted['price'])
            date = dateutil.parser.isoparse(converted['time'])
            print(btc_price, date)
            playsound('You_Suffer.mp3')
            if 'open_24' in converted:
                opening_price = float(converted['open_24h'])
                ten_percent = opening_price * 0.10
                if btc_price <= (opening_price - ten_percent):
                    print("BTC price has dropped by at least 10%")
                    print("Opening price: ", opening_price)
                    print("Current price: ", btc_price) 
                    playsound('You_Suffer.mp3')
        time.sleep(5)
except KeyboardInterrupt:
        ws.close()

if ws.error:
    sys.exit(1)
else:
    sys.exit(0)