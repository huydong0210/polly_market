# Polymarket WebSocket API Documentation

## Tổng quan
Polymarket CLOB API cung cấp các kênh WebSocket (WSS) để client có thể nhận cập nhật theo thời gian thực. Các endpoint này cho phép client duy trì view gần như real-time về orders, trades và thị trường nói chung.

## WebSocket URL
```
wss://ws-subscriptions-clob.polymarket.com
```

## Các kênh có sẵn
- **User Channel**: Cập nhật liên quan đến hoạt động người dùng (orders, trades)
- **Market Channel**: Cập nhật liên quan đến thị trường (level 2 price data)

---

## 1. WSS Overview - Tổng quan WebSocket

### Subscription - Đăng ký kênh

Để đăng ký, gửi message bao gồm thông tin xác thực và ý định khi mở kết nối:

#### Cấu trúc message đăng ký:
```json
{
  "auth": {
    "apiKey": "your_api_key",
    "secret": "your_secret", 
    "passphrase": "your_passphrase"
  },
  "markets": ["condition_id_1", "condition_id_2"],
  "assets_ids": ["token_id_1", "token_id_2"],
  "type": "USER" | "MARKET",
  "custom_feature_enabled": true
}
```

#### Các trường:
- `auth`: Thông tin xác thực (chỉ cần cho User channel)
- `markets`: Mảng condition IDs để nhận events (cho User channel)
- `assets_ids`: Mảng token IDs để nhận events (cho Market channel)
- `type`: Loại kênh ("USER" hoặc "MARKET")
- `custom_feature_enabled`: Bật/tắt tính năng tùy chỉnh

### Subscribe/Unsubscribe động

Sau khi kết nối, có thể đăng ký/hủy đăng ký assets:

```json
{
  "assets_ids": ["token_id_1", "token_id_2"],
  "markets": ["condition_id_1", "condition_id_2"],
  "operation": "subscribe" | "unsubscribe",
  "custom_feature_enabled": true
}
```

---

## 2. WSS Quickstart - Hướng dẫn nhanh

### Lấy API Keys

#### Python - Tạo API Keys
```python
from py_clob_client.client import ClobClient

host = "https://clob.polymarket.com"
key = ""  # Private Key của bạn
chain_id = 137
POLYMARKET_PROXY_ADDRESS = ''  # Địa chỉ proxy để fund account

# Chọn một trong 3 cách khởi tạo:

# 1. Email/Magic account
client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

# 2. Browser Wallet (Metamask, Coinbase Wallet, etc)
client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

# 3. EOA trực tiếp
client = ClobClient(host, key=key, chain_id=chain_id)

print(client.derive_api_key())
```

### Kết nối WebSocket

#### Python Implementation
```python
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

    asset_ids = ["109681959945973300464568698402968596289258214226684818748321941747028805721376"]
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
```

---

## 3. WSS Authentication - Xác thực

Chỉ kết nối đến `user` channel cần xác thực.

### Cấu trúc Auth Object:
```json
{
  "apikey": "your_api_key",
  "secret": "your_secret",
  "passphrase": "your_passphrase"
}
```

### Các trường:
- `apikey`: CLOB API key của tài khoản Polygon
- `secret`: CLOB API secret của tài khoản Polygon  
- `passphrase`: CLOB API passphrase của tài khoản Polygon

---

## 4. User Channel - Kênh người dùng

Kênh xác thực cho cập nhật liên quan đến hoạt động người dùng (orders, trades), được lọc theo API key.

**SUBSCRIBE**: `user`

### Trade Message - Thông báo giao dịch

#### Khi nào được phát:
- Khi market order được khớp ("MATCHED")
- Khi limit order của user được bao gồm trong trade ("MATCHED")
- Thay đổi trạng thái tiếp theo của trade ("MINED", "CONFIRMED", "RETRYING", "FAILED")

#### Cấu trúc:
```json
{
  "asset_id": "string",
  "event_type": "trade",
  "id": "string",
  "last_update": "string",
  "maker_orders": [
    {
      "asset_id": "string",
      "matched_amount": "string",
      "order_id": "string",
      "outcome": "string",
      "owner": "string",
      "price": "string"
    }
  ],
  "market": "string",
  "matchtime": "string",
  "outcome": "string",
  "owner": "string",
  "price": "string",
  "side": "BUY|SELL",
  "size": "string",
  "status": "string",
  "taker_order_id": "string",
  "timestamp": "string",
  "trade_owner": "string",
  "type": "TRADE"
}
```

#### Ví dụ Trade Message:
```json
{
  "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
  "event_type": "trade",
  "id": "28c4d2eb-bbea-40e7-a9f0-b2fdb56b2c2e",
  "last_update": "1672290701",
  "maker_orders": [
    {
      "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
      "matched_amount": "10",
      "order_id": "0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
      "outcome": "YES",
      "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
      "price": "0.57"
    }
  ],
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "matchtime": "1672290701",
  "outcome": "YES",
  "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "price": "0.57",
  "side": "BUY",
  "size": "10",
  "status": "MATCHED",
  "taker_order_id": "0x06bc63e346ed4ceddce9efd6b3af37c8f8f440c92fe7da6b2d0f9e4ccbc50c42",
  "timestamp": "1672290701",
  "trade_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "type": "TRADE"
}
```

### Order Message - Thông báo lệnh

#### Khi nào được phát:
- Khi order được đặt (PLACEMENT)
- Khi order được cập nhật (một phần được khớp) (UPDATE)
- Khi order bị hủy (CANCELLATION)

#### Cấu trúc:
```json
{
  "asset_id": "string",
  "associate_trades": ["string"],
  "event_type": "order",
  "id": "string",
  "market": "string",
  "order_owner": "string",
  "original_size": "string",
  "outcome": "string",
  "owner": "string",
  "price": "string",
  "side": "BUY|SELL",
  "size_matched": "string",
  "timestamp": "string",
  "type": "PLACEMENT|UPDATE|CANCELLATION"
}
```

#### Ví dụ Order Message:
```json
{
  "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
  "associate_trades": null,
  "event_type": "order",
  "id": "0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "order_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "original_size": "10",
  "outcome": "YES",
  "owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
  "price": "0.57",
  "side": "SELL",
  "size_matched": "0",
  "timestamp": "1672290687",
  "type": "PLACEMENT"
}
```

---

## 5. Market Channel - Kênh thị trường

Kênh công khai cho cập nhật liên quan đến thị trường (level 2 price data).

**SUBSCRIBE**: `market`

### Book Message - Thông báo sổ lệnh

#### Khi nào được phát:
- Lần đầu đăng ký thị trường
- Khi có trade ảnh hưởng đến sổ lệnh

#### Cấu trúc:
```json
{
  "event_type": "book",
  "asset_id": "string",
  "market": "string",
  "timestamp": "string",
  "hash": "string",
  "buys": [
    {
      "price": "string",
      "size": "string"
    }
  ],
  "sells": [
    {
      "price": "string", 
      "size": "string"
    }
  ]
}
```

#### Ví dụ Book Message:
```json
{
  "event_type": "book",
  "asset_id": "65818619657568813474341868652308942079804919287380422192892211131408793125422",
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "bids": [
    { "price": ".48", "size": "30" },
    { "price": ".49", "size": "20" },
    { "price": ".50", "size": "15" }
  ],
  "asks": [
    { "price": ".52", "size": "25" },
    { "price": ".53", "size": "60" },
    { "price": ".54", "size": "10" }
  ],
  "timestamp": "123456789000",
  "hash": "0x0...."
}
```

### Price Change Message - Thông báo thay đổi giá

⚠️ **Breaking Change Notice**: Schema sẽ được cập nhật vào 15/9/2025 lúc 11 PM UTC.

#### Khi nào được phát:
- Order mới được đặt
- Order bị hủy

#### Cấu trúc:
```json
{
  "event_type": "price_change",
  "market": "string",
  "price_changes": [
    {
      "asset_id": "string",
      "price": "string",
      "size": "string",
      "side": "BUY|SELL",
      "hash": "string",
      "best_bid": "string",
      "best_ask": "string"
    }
  ],
  "timestamp": "string"
}
```

#### Ví dụ Price Change Message:
```json
{
  "market": "0x5f65177b394277fd294cd75650044e32ba009a95022d88a0c1d565897d72f8f1",
  "price_changes": [
    {
      "asset_id": "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      "price": "0.5",
      "size": "200",
      "side": "BUY",
      "hash": "56621a121a47ed9333273e21c83b660cff37ae50",
      "best_bid": "0.5",
      "best_ask": "1"
    }
  ],
  "timestamp": "1757908892351",
  "event_type": "price_change"
}
```

### Tick Size Change Message - Thông báo thay đổi tick size

#### Khi nào được phát:
- Tick size tối thiểu của thị trường thay đổi (khi giá > 0.96 hoặc < 0.04)

#### Cấu trúc:
```json
{
  "event_type": "tick_size_change",
  "asset_id": "string",
  "market": "string",
  "old_tick_size": "string",
  "new_tick_size": "string",
  "side": "string",
  "timestamp": "string"
}
```

### Last Trade Price Message - Thông báo giá giao dịch cuối

#### Khi nào được phát:
- Khi maker và taker order được khớp tạo trade event

#### Ví dụ:
```json
{
  "asset_id": "114122071509644379678018727908709560226618148003371446110114509806601493071694",
  "event_type": "last_trade_price",
  "fee_rate_bps": "0",
  "market": "0x6a67b9d828d53862160e470329ffea5246f338ecfffdf2cab45211ec578b0347",
  "price": "0.456",
  "side": "BUY",
  "size": "219.217767",
  "timestamp": "1750428146322"
}
```

### Best Bid Ask Message - Thông báo bid/ask tốt nhất

Cần bật `custom_feature_enabled` flag.

#### Khi nào được phát:
- Giá bid và ask tốt nhất của thị trường thay đổi

#### Cấu trúc:
```json
{
  "event_type": "best_bid_ask",
  "market": "string",
  "asset_id": "string",
  "best_bid": "string",
  "best_ask": "string",
  "spread": "string",
  "timestamp": "string"
}
```

### New Market Message - Thông báo thị trường mới

Cần bật `custom_feature_enabled` flag.

#### Khi nào được phát:
- Thị trường mới được tạo

#### Cấu trúc:
```json
{
  "id": "string",
  "question": "string",
  "market": "string",
  "slug": "string",
  "description": "string",
  "assets_ids": ["string"],
  "outcomes": ["string"],
  "event_message": {
    "id": "string",
    "ticker": "string",
    "slug": "string",
    "title": "string",
    "description": "string"
  },
  "timestamp": "string",
  "event_type": "new_market"
}
```

### Market Resolved Message - Thông báo thị trường được giải quyết

Cần bật `custom_feature_enabled` flag.

#### Khi nào được phát:
- Thị trường được giải quyết

#### Cấu trúc:
```json
{
  "id": "string",
  "question": "string",
  "market": "string",
  "slug": "string",
  "description": "string",
  "assets_ids": ["string"],
  "outcomes": ["string"],
  "winning_asset_id": "string",
  "winning_outcome": "string",
  "event_message": {
    "id": "string",
    "ticker": "string",
    "slug": "string",
    "title": "string",
    "description": "string"
  },
  "timestamp": "string",
  "event_type": "market_resolved"
}
```

---

## Ví dụ Implementation hoàn chỉnh

### JavaScript/Node.js
```javascript
const WebSocket = require('ws');

class PolymarketWebSocket {
  constructor(url = 'wss://ws-subscriptions-clob.polymarket.com') {
    this.url = url;
    this.ws = null;
    this.pingInterval = null;
  }

  // Kết nối Market Channel
  connectMarket(assetIds, onMessage) {
    const wsUrl = `${this.url}/ws/market`;
    this.ws = new WebSocket(wsUrl);

    this.ws.on('open', () => {
      console.log('Market WebSocket connected');
      
      // Subscribe to assets
      this.ws.send(JSON.stringify({
        assets_ids: assetIds,
        type: 'MARKET'
      }));

      // Start ping
      this.startPing();
    });

    this.ws.on('message', (data) => {
      const message = JSON.parse(data.toString());
      onMessage(message);
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.ws.on('close', () => {
      console.log('WebSocket closed');
      this.stopPing();
    });
  }

  // Kết nối User Channel
  connectUser(markets, auth, onMessage) {
    const wsUrl = `${this.url}/ws/user`;
    this.ws = new WebSocket(wsUrl);

    this.ws.on('open', () => {
      console.log('User WebSocket connected');
      
      // Subscribe with auth
      this.ws.send(JSON.stringify({
        markets: markets,
        type: 'USER',
        auth: auth
      }));

      this.startPing();
    });

    this.ws.on('message', (data) => {
      const message = JSON.parse(data.toString());
      onMessage(message);
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.ws.on('close', () => {
      console.log('WebSocket closed');
      this.stopPing();
    });
  }

  // Subscribe thêm assets
  subscribeAssets(assetIds) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        assets_ids: assetIds,
        operation: 'subscribe'
      }));
    }
  }

  // Unsubscribe assets
  unsubscribeAssets(assetIds) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        assets_ids: assetIds,
        operation: 'unsubscribe'
      }));
    }
  }

  startPing() {
    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send('PING');
      }
    }, 10000);
  }

  stopPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  close() {
    this.stopPing();
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Sử dụng
const polyWS = new PolymarketWebSocket();

// Market channel
const assetIds = ['109681959945973300464568698402968596289258214226684818748321941747028805721376'];
polyWS.connectMarket(assetIds, (message) => {
  console.log('Market message:', message);
  
  switch(message.event_type) {
    case 'book':
      console.log('Order book update:', message.bids, message.asks);
      break;
    case 'price_change':
      console.log('Price change:', message.price_changes);
      break;
    case 'last_trade_price':
      console.log('Last trade:', message.price, message.size);
      break;
  }
});

// User channel (cần auth)
const auth = {
  apiKey: 'your_api_key',
  secret: 'your_secret',
  passphrase: 'your_passphrase'
};
const markets = ['condition_id_1'];

polyWS.connectUser(markets, auth, (message) => {
  console.log('User message:', message);
  
  switch(message.event_type) {
    case 'trade':
      console.log('Trade executed:', message.price, message.size, message.side);
      break;
    case 'order':
      console.log('Order update:', message.type, message.price, message.size_matched);
      break;
  }
});
```

---

## Best Practices

### 1. Connection Management
- Luôn implement reconnection logic
- Xử lý các trường hợp connection drop
- Sử dụng ping/pong để maintain connection

### 2. Message Handling
- Parse JSON messages cẩn thận
- Implement error handling cho malformed messages
- Log messages để debug

### 3. Subscription Management
- Track các assets/markets đã subscribe
- Unsubscribe khi không cần thiết để giảm bandwidth
- Sử dụng custom_feature_enabled cho advanced features

### 4. Performance
- Batch subscribe/unsubscribe operations
- Implement message queuing nếu cần
- Monitor memory usage với high-frequency data

### 5. Security
- Bảo mật API credentials
- Sử dụng environment variables
- Implement proper authentication flow

---

## Error Handling

### Common Issues
- **Connection timeout**: Implement retry logic
- **Authentication failed**: Kiểm tra API credentials
- **Rate limiting**: Implement backoff strategy
- **Message parsing errors**: Validate JSON structure

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

---

## Kết luận

Polymarket WebSocket API cung cấp khả năng real-time mạnh mẽ cho:

1. **Market Channel**: 
   - Order book updates
   - Price changes
   - Trade notifications
   - Market lifecycle events

2. **User Channel**:
   - Personal trade notifications
   - Order status updates
   - Account-specific events

Với implementation đúng cách, bạn có thể xây dựng các ứng dụng trading real-time, monitoring dashboards, và automated trading systems hiệu quả.
