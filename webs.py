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
    
try:
    while True:
        ws.send(json.dumps(params))
        result = ws.recv()
        converted = json.loads(result)
        if 'price' in converted:
            btc_price = float(converted['price'])
            date = dateutil.parser.isoparse(converted['time'])
            print(btc_price, date)
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