from websocket import WebSocketApp
import json
import time
import threading

MARKET_CHANNEL = "market"
USER_CHANNEL = "user"

class WebSocketOrderBook:
    def __init__(self, channel_type, url, data, auth, message_callback, verbose):
        self.channel_type = channel_type
        self.url = url
        self.data = data
        self.auth = auth
        self.message_callback = message_callback
        self.verbose = verbose
        furl = url + "/ws/" + channel_type
        self.ws = WebSocketApp(
            furl,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )

    def on_message(self, ws, message):
        print(message)
        # Xử lý message tại đây

    def on_error(self, ws, error):
        print("Error: ", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_open(self, ws):
        if self.channel_type == MARKET_CHANNEL:
            ws.send(json.dumps({"assets_ids": self.data, "type": MARKET_CHANNEL}))
        elif self.channel_type == USER_CHANNEL and self.auth:
            ws.send(json.dumps({
                "markets": self.data, 
                "type": USER_CHANNEL, 
                "auth": self.auth
            }))
        
        # Bắt đầu ping thread
        thr = threading.Thread(target=self.ping, args=(ws,))
        thr.start()

    def subscribe_to_tokens_ids(self, assets_ids):
        if self.channel_type == MARKET_CHANNEL:
            self.ws.send(json.dumps({
                "assets_ids": assets_ids, 
                "operation": "subscribe"
            }))

    def unsubscribe_to_tokens_ids(self, assets_ids):
        if self.channel_type == MARKET_CHANNEL:
            self.ws.send(json.dumps({
                "assets_ids": assets_ids, 
                "operation": "unsubscribe"
            }))

    def ping(self, ws):
        while True:
            ws.send("PING")
            time.sleep(10)

    def run(self):
        self.ws.run_forever()

# Sử dụng
if __name__ == "__main__":
    url = "wss://ws-subscriptions-clob.polymarket.com"
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    api_passphrase = "your_api_passphrase"

    asset_ids = ["97871895239823782023647783404652666876928114069545215397262234554268583084201", "98194334085313056512767271055295234282935238719687760373683666517277065140287"]
    condition_ids = []

    auth = {
        "apiKey": api_key, 
        "secret": api_secret, 
        "passphrase": api_passphrase
    }

    # Market connection
    market_connection = WebSocketOrderBook(
        MARKET_CHANNEL, url, asset_ids, auth, None, True
    )
    
    # User connection
    user_connection = WebSocketOrderBook(
        USER_CHANNEL, url, condition_ids, auth, None, True
    )

    market_connection.run()