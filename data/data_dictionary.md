# TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY)
## Bộ dữ liệu Breast Cancer Wisconsin (Diagnostic) - WDBC

---

## 1. NGUYÊN LÝ TRÍCH XUẤT ĐẶC TRƯNG HÌNH THÁI HỌC
Các đặc trưng trong bộ dữ liệu được tính toán tự động từ ảnh kỹ thuật số chụp mẫu bệnh phẩm chọc hút tế bào bằng kim nhỏ (**Fine Needle Aspirate - FNA**) của khối u vú.  
Hệ thống xử lý ảnh nhận diện đường viền của các nhân tế bào trong ảnh và đo lường **10 đặc tính hình học và cấu trúc**:

| STT | Đặc tính hình thái | Ký hiệu gốc | Ý nghĩa sinh học & toán học |
| :---: | :--- | :--- | :--- |
| 1 | **Bán kính (Radius)** | `radius` | Khoảng cách trung bình từ trọng tâm đến các điểm trên đường viền nhân tế bào. |
| 2 | **Kết cấu (Texture)** | `texture` | Độ lệch chuẩn của các giá trị cường độ xám (grayscale) trong nhân tế bào. |
| 3 | **Chu vi (Perimeter)** | `perimeter` | Tổng chiều dài chu vi đường bao của nhân tế bào. |
| 4 | **Diện tích (Area)** | `area` | Số lượng pixel bên trong đường viền của nhân tế bào. |
| 5 | **Độ mịn (Smoothness)** | `smoothness` | Sự biến thiên cục bộ của độ dài các bán kính xung quanh nhân. |
| 6 | **Độ nén chặt (Compactness)**| `compactness` | Được tính bằng công thức: $\frac{\text{perimeter}^2}{\text{area}} - 1.0$. |
| 7 | **Độ lõm (Concavity)** | `concavity` | Mức độ nghiêm trọng của các chỗ khuyết lõm vào trong của đường bao. |
| 8 | **Điểm lõm (Concave points)**| `concave points` | Số lượng điểm lõm trên đường bao của nhân tế bào. |
| 9 | **Độ đối xứng (Symmetry)** | `symmetry` | Mức độ cân đối, đối xứng của hình dạng nhân tế bào. |
| 10 | **Chiều fractal (Fractal dim)**| `fractal_dimension` | Đo lường độ gồ ghề của đường viền theo hình học fractal ("xấp xỉ bờ biển" - 1). |

---

## 2. BA NHÓM ĐO LƯỜNG (30 ĐẶC TRƯNG SỐ)
Mỗi đặc tính trong 10 đặc tính trên được thống kê thành 3 giá trị khác nhau trên cùng một mẫu bệnh phẩm, tạo thành $10 \times 3 = 30$ đặc trưng:
1. **Giá trị trung bình (`_mean`)**: Giá trị trung bình của toàn bộ các nhân tế bào quan sát được trên lam kính của mẫu FNA đó.
2. **Sai số chuẩn (`_se` - Standard Error)**: Độ biến thiên / sai số chuẩn của phép đo giữa các nhân tế bào trong mẫu.
3. **Giá trị lớn nhất / xấu nhất (`_worst`)**: Giá trị trung bình của **3 nhân tế bào có kích thước lớn nhất hoặc biến dạng nặng nhất** trong mẫu (đây là chỉ dấu lâm sàng rất nhạy với tế bào ung thư ác tính).

---

## 3. BẢNG ĐẶC TẢ CHI TIẾT 32 THUỘC TÍNH

| STT | Tên thuộc tính | Kiểu dữ liệu | Vai trò | Mô tả & Ý nghĩa | Đơn vị / Ghi chú |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | `id` | `int64` | **Identifier (ID)** | Mã số hồ sơ định danh mẫu bệnh phẩm | **Loại khỏi mô hình học máy** |
| 2 | `diagnosis` | `string` / `int` | **Target (Nhãn)** | Chẩn đoán bản chất khối u | `M` (Malignant=1), `B` (Benign=0) |
| 3 | `radius_mean` | `float64` | Feature (Đặc trưng) | Bán kính trung bình các nhân | Micromet ($\mu m$) |
| 4 | `texture_mean` | `float64` | Feature | Độ biến thiên cường độ xám trung bình | Vô thứ nguyên (Grayscale std) |
| 5 | `perimeter_mean` | `float64` | Feature | Chu vi trung bình các nhân | Micromet ($\mu m$) |
| 6 | `area_mean` | `float64` | Feature | Diện tích trung bình các nhân | Micromet vuông ($\mu m^2$) |
| 7 | `smoothness_mean` | `float64` | Feature | Độ mịn trung bình | Vô thứ nguyên |
| 8 | `compactness_mean` | `float64` | Feature | Độ nén chặt trung bình | Vô thứ nguyên |
| 9 | `concavity_mean` | `float64` | Feature | Độ sâu các vết lõm trung bình | Vô thứ nguyên |
| 10 | `concave points_mean` | `float64` | Feature | Số lượng điểm lõm trung bình | Vô thứ nguyên |
| 11 | `symmetry_mean` | `float64` | Feature | Độ đối xứng trung bình | Vô thứ nguyên |
| 12 | `fractal_dimension_mean` | `float64` | Feature | Chiều fractal trung bình | Vô thứ nguyên |
| 13 | `radius_se` | `float64` | Feature | Sai số chuẩn của bán kính | Micromet ($\mu m$) |
| 14 | `texture_se` | `float64` | Feature | Sai số chuẩn của độ kết cấu | Vô thứ nguyên |
| 15 | `perimeter_se` | `float64` | Feature | Sai số chuẩn của chu vi | Micromet ($\mu m$) |
| 16 | `area_se` | `float64` | Feature | Sai số chuẩn của diện tích | Micromet vuông ($\mu m^2$) |
| 17 | `smoothness_se` | `float64` | Feature | Sai số chuẩn của độ mịn | Vô thứ nguyên |
| 18 | `compactness_se` | `float64` | Feature | Sai số chuẩn của độ nén | Vô thứ nguyên |
| 19 | `concavity_se` | `float64` | Feature | Sai số chuẩn của độ lõm | Vô thứ nguyên |
| 20 | `concave points_se` | `float64` | Feature | Sai số chuẩn của số điểm lõm | Vô thứ nguyên |
| 21 | `symmetry_se` | `float64` | Feature | Sai số chuẩn của độ đối xứng | Vô thứ nguyên |
| 22 | `fractal_dimension_se` | `float64` | Feature | Sai số chuẩn của chiều fractal | Vô thứ nguyên |
| 23 | `radius_worst` | `float64` | Feature | Bán kính của nhân dị thường nhất | Micromet ($\mu m$) |
| 24 | `texture_worst` | `float64` | Feature | Kết cấu của nhân dị thường nhất | Vô thứ nguyên |
| 25 | `perimeter_worst` | `float64` | Feature | Chu vi của nhân dị thường nhất | Micromet ($\mu m$) |
| 26 | `area_worst` | `float64` | Feature | Diện tích của nhân dị thường nhất | Micromet vuông ($\mu m^2$) |
| 27 | `smoothness_worst` | `float64` | Feature | Độ mịn của nhân dị thường nhất | Vô thứ nguyên |
| 28 | `compactness_worst` | `float64` | Feature | Độ nén của nhân dị thường nhất | Vô thứ nguyên |
| 29 | `concavity_worst` | `float64` | Feature | Độ lõm của nhân dị thường nhất | Vô thứ nguyên |
| 30 | `concave points_worst`| `float64` | Feature | Điểm lõm của nhân dị thường nhất | Vô thứ nguyên |
| 31 | `symmetry_worst` | `float64` | Feature | Độ đối xứng của nhân dị thường nhất | Vô thứ nguyên |
| 32 | `fractal_dimension_worst`| `float64` | Feature | Chiều fractal của nhân dị thường nhất | Vô thứ nguyên |

---

## 4. QUY TẮC RÀNG BUỘC KHI TIỀN XỬ LÝ VÀ HUẤN LUYỆN
1. **Loại bỏ `id`**: Thuộc tính `id` là mã số ngẫu nhiên do bệnh viện cấp. Nó không chứa tín hiệu y sinh và mang tính duy nhất, nếu đưa vào mô hình sẽ dẫn đến việc cây quyết định ghi nhớ thuộc lòng ID (Memorization / Overfitting giả tạo).
2. **Mã hóa nhãn (`diagnosis`)**:
   - `M` (Malignant - Ác tính) được mã hóa thành **1** (Lớp dương tính - Positive Class).
   - `B` (Benign - Lành tính) được mã hóa thành **0** (Lớp âm tính - Negative Class).
3. **Tính sẵn sàng của dữ liệu**: Toàn bộ 30 đặc trưng đều được đo lường đồng thời tại thời điểm phân tích ảnh sinh thiết FNA, không có biến nào xuất hiện sau thời điểm chẩn đoán, đảm bảo **không có rò rỉ dữ liệu theo thời gian (No Temporal Leakage)**.
