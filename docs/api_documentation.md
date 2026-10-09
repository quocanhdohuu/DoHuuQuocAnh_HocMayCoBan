# TÀI LIỆU KỸ THUẬT VÀ ĐẶC TẢ BACKEND API (PROJECT 16)
## Phân Loại Khối U Vú Wisconsin Diagnostic Breast Cancer (WDBC)

---

### 1. TỔNG QUAN HỆ THỐNG (SYSTEM OVERVIEW)
Tài liệu này đặc tả toàn bộ giao diện lập trình ứng dụng (**Application Programming Interface - API**) của Backend FastAPI phục vụ bài toán phân loại khối u vú FNA (Fine Needle Aspirate) từ tập dữ liệu Wisconsin Diagnostic Breast Cancer (WDBC), thuộc khuôn khổ học phần **Học máy cơ bản** (Trường Đại học Thủy Lợi).

- **Kiến trúc dịch vụ**: Web API chuẩn **ASGI (Asynchronous Server Gateway Interface)** xây dựng bằng **FastAPI**, nạp mô hình học máy theo cơ chế **Lifespan Singleton** (nạp đúng 1 lần duy nhất khi khởi động vào bộ nhớ RAM).
- **Mô hình phục vụ suy luận**: Scikit-Learn Pipeline (`StandardScaler` + `RandomForestClassifier`, 100 cây quyết định, `max_depth=8`, `max_features=0.3`, `random_state=42`) đã huấn luyện và đóng băng tham số.
- **An toàn & Toàn vẹn**: Tự động xác thực mã băm SHA-256 của tệp binary `.joblib` trước khi nạp vào bộ nhớ; kiểm định schema 30 đặc trưng đầu vào nghiêm ngặt bằng **Pydantic v2** (`extra="forbid"`, cấm `NaN`, cấm `Infinity`, cấm giá trị âm $< 0$, cấm giá trị cực đoan phi lý).
- **Địa chỉ phục vụ cục bộ (Base URL)**: `http://127.0.0.1:8000`
- **Tài liệu tương tác tự động**:
  - Swagger UI: `http://127.0.0.1:8000/docs`
  - ReDoc: `http://127.0.0.1:8000/redoc`
- **Cấu hình CORS (Cross-Origin Resource Sharing)**: Hỗ trợ kết nối từ các cổng phát triển cục bộ của Frontend (`http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:5173`, `http://127.0.0.1:5173`).

---

### 2. DANH MỤC CÁC ENDPOINT (API ENDPOINTS SUMMARY)

| Phương thức HTTP | Đường dẫn (Path) | Thẻ phân loại | Mục đích & Chức năng | Mã trạng thái HTTP |
| :---: | :--- | :---: | :--- | :---: |
| `GET` | `/` | General | Thông tin tổng quan dịch vụ, phiên bản, tác giả | `200 OK` |
| `GET` | `/api/health` | Health | Kiểm tra sức khỏe dịch vụ, trạng thái mô hình và SHA-256 | `200 OK` / `503 Service Unavailable` |
| `POST` | `/api/demo-classify` | Classification | Phân loại khối u vú từ 30 đặc trưng số FNA (Endpoint chính) | `200 OK` / `422 Unprocessable` / `503 Unavailable` |
| `POST` | `/api/predict` | Classification | Alias tương thích cho `/api/demo-classify` | `200 OK` / `422 Unprocessable` / `503 Unavailable` |

---

### 3. ĐẶC TẢ CHI TIẾT CÁC ENDPOINTS

#### 3.1. Endpoint Gốc: `GET /`
- **Mô tả**: Trả về thông tin giới thiệu dự án, tác giả, trạng thái hoạt động và liên kết nhanh tới tài liệu API.
- **Mã phản hồi thành công**: `200 OK`
- **Ví dụ Response Body**:
```json
{
  "app_name": "WDBC Breast Cancer Classification API",
  "project": "Project 16 - Học máy cơ bản",
  "version": "1.0.0",
  "status": "online",
  "documentation": "/docs",
  "health_check": "/api/health",
  "classification_endpoint": "/api/demo-classify",
  "author": "Do Huu Quoc Anh"
}
```

---

#### 3.2. Endpoint Kiểm Tra Sức Khỏe: `GET /api/health`
- **Mô tả**: Cung cấp báo cáo toàn diện về tình trạng sẵn sàng của hệ thống và mô hình ML, phục vụ giám sát vận hành (Health Check / Readiness Probe).
- **Mã phản hồi**:
  - `200 OK`: Dịch vụ hoạt động bình thường, mô hình và schema đã nạp thành công, mã băm SHA-256 khớp tuyệt đối.
  - `503 Service Unavailable`: Dịch vụ chuyển sang chế độ "Degraded" khi thiếu tệp artifact hoặc mô hình không thể nạp (không làm sập server).
- **Ví dụ Response Body (`200 OK`)**:
```json
{
  "status": "ok",
  "message": "Dịch vụ hoạt động bình thường, mô hình sẵn sàng phục vụ suy luận.",
  "app_name": "WDBC Breast Cancer Classification API",
  "version": "1.0.0",
  "model_loaded": true,
  "model_name": "WDBC_RandomForest_Classifier_Pipeline",
  "sha256_verified": true,
  "input_features_count": 30,
  "decision_threshold": 0.5,
  "target_positive_class": "Malignant",
  "startup_time": "2026-10-09T01:10:16.887000+00:00",
  "timestamp": "2026-10-09T01:16:38.120000+00:00",
  "error": null
}
```

---

#### 3.3. Endpoint Phân Loại: `POST /api/demo-classify` (và Alias `POST /api/predict`)
- **Mô tả**: Nhận 30 giá trị đặc trưng đo lường tế bào FNA, kiểm định dữ liệu nghiêm ngặt qua Pydantic, đưa vào Scikit-Learn Pipeline để tính toán xác suất và phân loại nhãn Lành tính (Benign - B) hoặc Ác tính (Malignant - M).

##### A. Cấu trúc Request Body
Hệ thống linh hoạt hỗ trợ 2 định dạng gửi dữ liệu:
1. **Định dạng trực tiếp (Direct Object)**: Một đối tượng JSON chứa đủ 30 trường đặc trưng ở cấp cao nhất.
2. **Định dạng gói (Wrapped Object)**: Đối tượng chứa object con `"features"` và tùy chọn ngưỡng phân loại `"threshold"`.

**Danh sách 30 đặc trưng bắt buộc (Kiểu `float`, không âm, không `NaN`, không `Inf`):**
- **Nhóm Mean (10 đặc trưng trung bình)**: `radius_mean`, `texture_mean`, `perimeter_mean`, `area_mean`, `smoothness_mean`, `compactness_mean`, `concavity_mean`, `concave points_mean` (hoặc `concave_points_mean`), `symmetry_mean`, `fractal_dimension_mean`.
- **Nhóm SE (10 đặc trưng sai số chuẩn)**: `radius_se`, `texture_se`, `perimeter_se`, `area_se`, `smoothness_se`, `compactness_se`, `concavity_se`, `concave points_se` (hoặc `concave_points_se`), `symmetry_se`, `fractal_dimension_se`.
- **Nhóm Worst (10 đặc trưng giá trị lớn nhất)**: `radius_worst`, `texture_worst`, `perimeter_worst`, `area_worst`, `smoothness_worst`, `compactness_worst`, `concavity_worst`, `concave points_worst` (hoặc `concave_points_worst`), `symmetry_worst`, `fractal_dimension_worst`.

##### B. Cấu trúc Response Body (`200 OK`)
| Trường dữ liệu | Kiểu | Ý nghĩa lâm sàng & Kỹ thuật |
| :--- | :---: | :--- |
| `status` | string | Trạng thái thực thi (`"success"`) |
| `predicted_class` | integer | Mã số lớp dự đoán: `0` (Lành tính) hoặc `1` (Ác tính) |
| `predicted_code` | string | Mã nhãn y khoa viết tắt: `"B"` hoặc `"M"` |
| `predicted_label` | string | Tên nhãn lâm sàng đầy đủ: `"Benign"` hoặc `"Malignant"` |
| `probabilities` | object | Xác suất cho từng lớp: `benign`, `malignant`, `B`, `M` (tổng xấp xỉ 1.0) |
| `decision_threshold` | float | Ngưỡng xác suất phân loại lớp Ác tính đang được áp dụng (mặc định `0.50`) |
| `confidence_score` | float | Độ tin cậy của mô hình tính theo tỷ lệ phần trăm (0% - 100%) |
| `is_high_risk` | boolean | Cờ cảnh báo nguy cơ cao: `true` nếu ca bệnh ác tính |
| `model_info` | object | Tên mô hình, phiên bản, thuật toán và số lượng đặc trưng |
| `explanation` | object | Phân tích phiếu bầu 100 cây (`votes_breakdown`), top 5 đặc trưng và tuyên bố giới hạn phương pháp |
| `warnings` | array | Danh sách cảnh báo Out-Of-Distribution nếu đặc trưng nằm ngoài dải tập huấn luyện |
| `clinical_disclaimer` | string | Tuyên bố miễn trừ trách nhiệm y khoa bắt buộc |
| `timestamp` | string | Thời gian hoàn tất suy luận chuẩn ISO 8601 UTC |

---

### 4. VÍ DỤ MINH HỌA REQUEST VÀ RESPONSE THỰC TẾ

#### 4.1. Ví dụ Ca Bệnh Lành Tính (Preset Benign - Test Sample #1)
**HTTP Request:**
```http
POST /api/demo-classify HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "radius_mean": 10.17,
  "texture_mean": 14.88,
  "perimeter_mean": 64.55,
  "area_mean": 311.9,
  "smoothness_mean": 0.1134,
  "compactness_mean": 0.08061,
  "concavity_mean": 0.01084,
  "concave points_mean": 0.0129,
  "symmetry_mean": 0.2743,
  "fractal_dimension_mean": 0.0696,
  "radius_se": 0.5158,
  "texture_se": 1.441,
  "perimeter_se": 3.312,
  "area_se": 34.62,
  "smoothness_se": 0.007514,
  "compactness_se": 0.01099,
  "concavity_se": 0.007665,
  "concave points_se": 0.008193,
  "symmetry_se": 0.04183,
  "fractal_dimension_se": 0.005953,
  "radius_worst": 11.02,
  "texture_worst": 17.45,
  "perimeter_worst": 69.86,
  "area_worst": 368.6,
  "smoothness_worst": 0.1275,
  "compactness_worst": 0.09866,
  "concavity_worst": 0.02168,
  "concave points_worst": 0.02579,
  "symmetry_worst": 0.3557,
  "fractal_dimension_worst": 0.0802
}
```

**HTTP Response (`200 OK`):**
```json
{
  "status": "success",
  "predicted_class": 0,
  "predicted_code": "B",
  "predicted_label": "Benign",
  "probabilities": {
    "benign": 0.97,
    "malignant": 0.03,
    "B": 0.97,
    "M": 0.03
  },
  "decision_threshold": 0.5,
  "confidence_score": 97.0,
  "is_high_risk": false,
  "model_info": {
    "model_name": "WDBC_RandomForest_Classifier_Pipeline",
    "version": "1.0.0",
    "algorithm": "RandomForestClassifier",
    "decision_threshold": 0.5,
    "input_features_count": 30
  },
  "explanation": {
    "model_type": "RandomForestClassifier",
    "explanation_method": "Ensemble Voting & Global Feature Importance",
    "total_trees": 100,
    "votes_breakdown": {
      "benign_votes": 97,
      "malignant_votes": 3,
      "B": 97,
      "M": 3
    },
    "vote_percentage": {
      "Benign": 97.0,
      "Malignant": 3.0,
      "B": 97.0,
      "M": 3.0
    },
    "top_influential_features": [
      {"rank": 1, "feature": "area_worst", "importance_score": 0.1903, "sample_value": 368.6},
      {"rank": 2, "feature": "concave points_worst", "importance_score": 0.1763, "sample_value": 0.0258},
      {"rank": 3, "feature": "concave points_mean", "importance_score": 0.1355, "sample_value": 0.0129},
      {"rank": 4, "feature": "radius_worst", "importance_score": 0.1188, "sample_value": 11.02},
      {"rank": 5, "feature": "perimeter_worst", "importance_score": 0.1033, "sample_value": 69.86}
    ],
    "aggregation_mechanism": "Soft-Voting (Trung bình cộng xác suất dự đoán qua 100 cây quyết định ngẫu nhiên)",
    "methodological_limitation": "GIẢI THÍCH VÀ GIỚI HẠN PHƯƠNG PHÁP: Mô hình hiện tại là Random Forest gồm 100 cây quyết định độc lập. Quyết định phân loại là kết quả tổng hợp của TOÀN BỘ 100 CÂY thông qua cơ chế soft-voting. KHÔNG CÓ một đường đi rẽ nhánh đơn lẻ nào đại diện cho toàn bộ mô hình rừng. Mọi nỗ lực lấy đường đi của 1 cây đơn lẻ trong rừng để giải thích là SAI BẢN CHẤT thuật toán ensemble và gây hiểu nhầm lâm sàng."
  },
  "warnings": [],
  "clinical_disclaimer": "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA: Mô hình này được phát triển phục vụ mục đích nghiên cứu học thuật và giáo dục trong học phần Học máy cơ bản. Mô hình TUYỆT ĐỐI KHÔNG ĐƯỢC SỬ DỤNG cho mục đích chẩn đoán y tế, tự động ra phác đồ điều trị lâm sàng hoặc thay thế ý kiến chuyên môn của bác sĩ giải phẫu bệnh.",
  "timestamp": "2026-10-09T01:10:16.988870+00:00"
}
```

---

#### 4.2. Ví dụ Ca Bệnh Ác Tính (Preset Malignant - Test Sample #0)
**Tóm tắt kết quả (`HTTP 200 OK`):**
- **Nhãn dự đoán**: `"M"` (`"Malignant"`), `predicted_class`: `1`.
- **Xác suất**: $P(\text{Benign}) = 0.00$, $P(\text{Malignant}) = 1.00$.
- **Đồng thuận Ensemble**: 100/100 cây trong Rừng Ngẫu Nhiên bỏ phiếu ác tính tuyệt đối (`votes_breakdown.malignant_votes = 100`).
- **Cờ rủi ro cao**: `is_high_risk: true`.

---

#### 4.3. Ví dụ Mẫu Có Cảnh Báo Out-Of-Distribution (OOD Soft Warning)
Khi giá trị đặc trưng hợp lệ về mặt vật lý nhưng vượt ra ngoài dải quan sát huấn luyện (ví dụ `radius_mean = 35.0` trong khi $\max_{\text{train}} = 28.11$):
**HTTP Response (`200 OK`):**
```json
{
  "status": "success",
  "predicted_class": 1,
  "predicted_code": "M",
  "predicted_label": "Malignant",
  "warnings": [
    "Đặc trưng 'radius_mean' = 35.0000 > max_train (28.1100). Mẫu nằm ngoài khoảng quan sát huấn luyện phía trên (Out-Of-Distribution)."
  ]
}
```

---

### 5. BẢNG MÃ LỖI HTTP VÀ CHÍNH SÁCH XỬ LÝ SỰ CỐ

| Mã trạng thái HTTP | Tên chuẩn RESTful | Nguyên nhân phát sinh | Cấu trúc phản hồi lỗi mẫu |
| :---: | :--- | :--- | :--- |
| **`200 OK`** | Success | Yêu cầu hợp lệ, xử lý và suy luận thành công | Trả về JSON theo `ClassificationResponse` |
| **`422`** | Unprocessable Content | Thiếu trường, thừa trường (`extra_forbidden`), sai kiểu dữ liệu, nhận `NaN`, `Infinity`, hoặc nhận giá trị âm $< 0$ | `{"detail": [{"loc": ["body", "radius_mean"], "msg": "Đặc trưng 'radius_mean' không thể nhận giá trị âm (-5.0 < 0)", "type": "value_error"}]}` |
| **`422`** | Unprocessable Content | Giá trị vượt quá giới hạn sinh học cực đoan khả dĩ ($> 15 \times \max_{\text{train}}$) | `{"detail": "Đặc trưng 'radius_mean' có giá trị 5000.0 vượt quá giới hạn sinh học cực đoan (ngưỡng tối đa cho phép: 421.65). Vui lòng kiểm tra lại thiết bị đo."}` |
| **`503`** | Service Unavailable | Mô hình chưa sẵn sàng, tệp artifact bị thiếu hoặc không thể giải nén nhị phân | `{"detail": "Mô hình phân loại chưa sẵn sàng phục vụ suy luận (Lỗi nạp mô hình: ...). Vui lòng kiểm tra GET /api/health."}` |
| **`500`** | Internal Server Error | Sự cố bất ngờ trong quá trình tính toán ma trận bên trong pipeline Scikit-Learn | `{"detail": "Lỗi nội bộ khi thực hiện suy luận mô hình: ..."}` |

---

### 6. QUY TRÌNH KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Hệ thống kiểm thử tự động sử dụng `pytest` kết hợp với `fastapi.testclient.TestClient`. Toàn bộ 72 test cases đều được chạy và xác thực trực tiếp trên môi trường máy chủ:

```powershell
# Chạy toàn bộ test suite dự án
.\.venv\Scripts\pytest.exe -v tests/

# Chạy riêng bộ kiểm thử Classification API
.\.venv\Scripts\pytest.exe -v tests/test_api_classification.py
```

**Bảng tổng kết trạng thái kiểm thử thực tế:**
- **Tổng số tests**: **72**
- **Passed**: **72 (100%)**
- **Failed**: **0**
- **Skipped**: **0**
- **Thời gian thực thi**: ~5.7 giây

---

### 7. HƯỚNG DẪN KHỞI CHẠY DỊCH VỤ BẰNG UVICORN

```powershell
# Chế độ phát triển (Tự động tải lại khi sửa mã nguồn - Hot Reload)
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Chế độ triển khai sản xuất (Production Multi-worker)
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 2
```
