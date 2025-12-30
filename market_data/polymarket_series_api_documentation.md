# Polymarket Series API Documentation

## Tổng quan
Series API của Polymarket cho phép truy xuất thông tin về các chuỗi sự kiện (series) trên nền tảng. Series là tập hợp các sự kiện liên quan đến nhau, thường có tính chất định kỳ hoặc thuộc cùng một chủ đề.

## Base URL
```
https://gamma-api.polymarket.com
```

---

## 1. List Series - Lấy danh sách tất cả series

### Endpoint
```
GET /series
```

### Mô tả
API này trả về danh sách tất cả các series có sẵn trên Polymarket, bao gồm thông tin chi tiết về từng series và các sự kiện liên quan.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Giới hạn số lượng kết quả trả về (≥ 0) |
| `offset` | integer | No | Bỏ qua số lượng kết quả từ đầu (≥ 0) |
| `order` | string | No | Danh sách các trường để sắp xếp (phân cách bằng dấu phẩy) |
| `ascending` | boolean | No | Sắp xếp tăng dần (true) hoặc giảm dần (false) |
| `slug` | string[] | No | Lọc theo slug của series |
| `categories_ids` | integer[] | No | Lọc theo ID danh mục |
| `categories_labels` | string[] | No | Lọc theo nhãn danh mục |
| `closed` | boolean | No | Lọc series đã đóng (true) hoặc đang mở (false) |
| `include_chat` | boolean | No | Bao gồm thông tin chat |
| `recurrence` | string | No | Lọc theo tính định kỳ |

### Response Fields

#### Series Object
- `id`: ID duy nhất của series
- `ticker`: Mã ticker của series
- `slug`: URL slug của series
- `title`: Tiêu đề series
- `subtitle`: Phụ đề
- `seriesType`: Loại series
- `recurrence`: Tính định kỳ (daily, weekly, monthly, etc.)
- `description`: Mô tả chi tiết
- `image`: URL hình ảnh chính
- `icon`: URL icon
- `active`: Series có đang hoạt động không
- `closed`: Series đã đóng chưa
- `featured`: Series có được đặc sắc không
- `volume24hr`: Khối lượng giao dịch 24h
- `volume`: Tổng khối lượng giao dịch
- `liquidity`: Thanh khoản hiện tại
- `startDate`: Ngày bắt đầu
- `events[]`: Mảng các sự kiện trong series
- `categories[]`: Danh mục của series
- `tags[]`: Các thẻ gắn với series

### Ví dụ Request
```bash
curl --request GET \
  --url "https://gamma-api.polymarket.com/series?limit=10&order=volume24hr&ascending=false"
```

### Ví dụ Response
```json
[
  {
    "id": "123",
    "ticker": "ELECTION2024",
    "slug": "us-election-2024",
    "title": "US Presidential Election 2024",
    "subtitle": "Who will win the 2024 US Presidential Election?",
    "seriesType": "election",
    "recurrence": "quadrennial",
    "description": "Markets related to the 2024 United States Presidential Election",
    "image": "https://example.com/election2024.jpg",
    "icon": "https://example.com/election-icon.png",
    "active": true,
    "closed": false,
    "featured": true,
    "volume24hr": 1500000,
    "volume": 25000000,
    "liquidity": 5000000,
    "startDate": "2023-01-01T00:00:00Z",
    "events": [
      {
        "id": "456",
        "title": "Republican Primary Winner",
        "slug": "republican-primary-2024",
        "active": true,
        "volume": 8000000,
        "markets": [...]
      }
    ],
    "categories": [
      {
        "id": "politics",
        "label": "Politics",
        "slug": "politics"
      }
    ],
    "tags": [
      {
        "id": "election",
        "label": "Election",
        "slug": "election"
      }
    ]
  }
]
```

### Use Cases
- Hiển thị danh sách tất cả series trên trang chủ
- Lọc series theo danh mục hoặc thẻ
- Phân trang kết quả series
- Sắp xếp series theo khối lượng giao dịch hoặc thanh khoản

---

## 2. Get Series by ID - Lấy thông tin chi tiết một series

### Endpoint
```
GET /series/{id}
```

### Mô tả
API này trả về thông tin chi tiết của một series cụ thể dựa trên ID, bao gồm tất cả các sự kiện và thị trường liên quan.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | ID của series cần lấy thông tin |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include_chat` | boolean | No | Bao gồm thông tin chat |

### Response
Trả về một object Series với cấu trúc tương tự như trong List Series, nhưng với thông tin chi tiết hơn về các events và markets.

### Ví dụ Request
```bash
curl --request GET \
  --url "https://gamma-api.polymarket.com/series/123?include_chat=true"
```

### Ví dụ Response
```json
{
  "id": "123",
  "ticker": "ELECTION2024",
  "slug": "us-election-2024",
  "title": "US Presidential Election 2024",
  "subtitle": "Who will win the 2024 US Presidential Election?",
  "seriesType": "election",
  "recurrence": "quadrennial",
  "description": "Comprehensive markets covering all aspects of the 2024 United States Presidential Election, including primaries, general election, and related political events.",
  "image": "https://example.com/election2024.jpg",
  "icon": "https://example.com/election-icon.png",
  "active": true,
  "closed": false,
  "featured": true,
  "volume24hr": 1500000,
  "volume": 25000000,
  "liquidity": 5000000,
  "startDate": "2023-01-01T00:00:00Z",
  "commentsEnabled": true,
  "commentCount": 1250,
  "events": [
    {
      "id": "456",
      "title": "Republican Primary Winner",
      "slug": "republican-primary-2024",
      "description": "Who will win the Republican primary for the 2024 presidential election?",
      "active": true,
      "volume": 8000000,
      "volume24hr": 500000,
      "liquidity": 2000000,
      "startDate": "2023-06-01T00:00:00Z",
      "endDate": "2024-07-15T00:00:00Z",
      "markets": [
        {
          "id": "789",
          "question": "Will Donald Trump win the Republican primary?",
          "slug": "trump-republican-primary-2024",
          "active": true,
          "volume": 3000000,
          "liquidity": 800000,
          "outcomes": "Yes,No",
          "outcomePrices": "0.65,0.35",
          "lastTradePrice": 0.65,
          "bestBid": 0.64,
          "bestAsk": 0.66
        }
      ]
    }
  ],
  "categories": [
    {
      "id": "politics",
      "label": "Politics",
      "slug": "politics"
    }
  ],
  "tags": [
    {
      "id": "election",
      "label": "Election",
      "slug": "election"
    },
    {
      "id": "usa",
      "label": "USA",
      "slug": "usa"
    }
  ],
  "chats": [
    {
      "id": "chat123",
      "channelId": "election2024",
      "channelName": "Election 2024 Discussion",
      "live": true,
      "startTime": "2023-01-01T00:00:00Z"
    }
  ]
}
```

### Use Cases
- Hiển thị trang chi tiết của một series
- Lấy thông tin đầy đủ về các events và markets trong series
- Hiển thị thông tin chat và bình luận
- Phân tích chi tiết về hiệu suất giao dịch của series

---

## Cấu trúc dữ liệu chi tiết

### Event Object (trong Series)
- `id`: ID của event
- `title`: Tiêu đề event
- `slug`: URL slug
- `description`: Mô tả
- `active`: Trạng thái hoạt động
- `volume`: Khối lượng giao dịch
- `liquidity`: Thanh khoản
- `startDate`: Ngày bắt đầu
- `endDate`: Ngày kết thúc
- `markets[]`: Các thị trường trong event

### Market Object (trong Event)
- `id`: ID của market
- `question`: Câu hỏi thị trường
- `slug`: URL slug
- `active`: Trạng thái hoạt động
- `volume`: Khối lượng giao dịch
- `liquidity`: Thanh khoản
- `outcomes`: Các kết quả có thể
- `outcomePrices`: Giá của các kết quả
- `lastTradePrice`: Giá giao dịch cuối
- `bestBid`: Giá mua tốt nhất
- `bestAsk`: Giá bán tốt nhất

### Category Object
- `id`: ID danh mục
- `label`: Tên hiển thị
- `slug`: URL slug
- `parentCategory`: Danh mục cha (nếu có)

### Tag Object
- `id`: ID thẻ
- `label`: Tên hiển thị
- `slug`: URL slug
- `forceShow`: Bắt buộc hiển thị
- `forceHide`: Bắt buộc ẩn

---

## Error Handling

### Common Error Codes
- `400 Bad Request`: Tham số không hợp lệ
- `404 Not Found`: Series không tồn tại
- `429 Too Many Requests`: Vượt quá giới hạn rate limit
- `500 Internal Server Error`: Lỗi server

### Error Response Format
```json
{
  "error": {
    "code": 404,
    "message": "Series not found",
    "details": "No series found with ID 999"
  }
}
```

---

## Rate Limiting
- Giới hạn: 100 requests/phút cho mỗi IP
- Header response bao gồm thông tin rate limit:
  - `X-RateLimit-Limit`: Giới hạn tối đa
  - `X-RateLimit-Remaining`: Số request còn lại
  - `X-RateLimit-Reset`: Thời gian reset (Unix timestamp)

---

## Best Practices

1. **Caching**: Cache kết quả để giảm số lượng API calls
2. **Pagination**: Sử dụng limit và offset để phân trang hiệu quả
3. **Filtering**: Sử dụng các tham số lọc để giảm dữ liệu không cần thiết
4. **Error Handling**: Luôn xử lý các trường hợp lỗi và retry logic
5. **Rate Limiting**: Tuân thủ giới hạn rate limit để tránh bị chặn

---

## Ví dụ Integration

### JavaScript/Node.js
```javascript
const axios = require('axios');

class PolymarketSeriesAPI {
  constructor() {
    this.baseURL = 'https://gamma-api.polymarket.com';
  }

  async getAllSeries(params = {}) {
    try {
      const response = await axios.get(`${this.baseURL}/series`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching series:', error.response?.data || error.message);
      throw error;
    }
  }

  async getSeriesById(id, includeChat = false) {
    try {
      const response = await axios.get(`${this.baseURL}/series/${id}`, {
        params: { include_chat: includeChat }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching series by ID:', error.response?.data || error.message);
      throw error;
    }
  }

  async getFeaturedSeries() {
    return this.getAllSeries({
      featured: true,
      active: true,
      limit: 10,
      order: 'volume24hr',
      ascending: false
    });
  }
}

// Sử dụng
const api = new PolymarketSeriesAPI();

// Lấy top 10 series có khối lượng giao dịch cao nhất
api.getFeaturedSeries()
  .then(series => console.log('Featured series:', series))
  .catch(error => console.error('Error:', error));

// Lấy chi tiết một series cụ thể
api.getSeriesById(123, true)
  .then(series => console.log('Series details:', series))
  .catch(error => console.error('Error:', error));
```

### Python
```python
import requests
from typing import Optional, Dict, Any, List

class PolymarketSeriesAPI:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
    
    def get_all_series(self, **params) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả series"""
        try:
            response = requests.get(f"{self.base_url}/series", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching series: {e}")
            raise
    
    def get_series_by_id(self, series_id: int, include_chat: bool = False) -> Dict[str, Any]:
        """Lấy thông tin chi tiết một series"""
        try:
            params = {"include_chat": include_chat} if include_chat else {}
            response = requests.get(f"{self.base_url}/series/{series_id}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching series {series_id}: {e}")
            raise
    
    def get_featured_series(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy các series nổi bật"""
        return self.get_all_series(
            featured=True,
            active=True,
            limit=limit,
            order="volume24hr",
            ascending=False
        )

# Sử dụng
api = PolymarketSeriesAPI()

# Lấy series nổi bật
featured = api.get_featured_series()
print(f"Found {len(featured)} featured series")

# Lấy chi tiết series đầu tiên
if featured:
    series_detail = api.get_series_by_id(featured[0]['id'], include_chat=True)
    print(f"Series: {series_detail['title']}")
    print(f"Volume 24h: ${series_detail['volume24hr']:,}")
```

---

## Kết luận

Series API của Polymarket cung cấp một cách mạnh mẽ và linh hoạt để truy xuất thông tin về các chuỗi sự kiện trên nền tảng. Với hai endpoint chính, bạn có thể:

1. **List Series**: Lấy danh sách tổng quan với khả năng lọc và sắp xếp
2. **Get Series by ID**: Lấy thông tin chi tiết của một series cụ thể

API này phù hợp cho việc xây dựng các ứng dụng phân tích thị trường, dashboard theo dõi, hoặc tích hợp dữ liệu Polymarket vào các hệ thống khác.
