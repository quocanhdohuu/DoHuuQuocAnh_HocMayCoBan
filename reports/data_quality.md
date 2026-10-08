# BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY REPORT)
## Đề tài: Project 16 — Phân loại khối u vú bằng cây và rừng (WDBC)
**Tập dữ liệu**: Breast Cancer Wisconsin (Diagnostic) — UCI Machine Learning Repository  
**Thời điểm thực hiện**: 08/10/2026  
**Công cụ kiểm toán**: Python 3.12, pandas 3.0.6, numpy 2.5.3  

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM TOÁN CHẤT LƯỢNG

| Hạng mục kiểm tra | Tiêu chuẩn đánh giá | Kết quả thực tế | Đánh giá chất lượng |
| :--- | :--- | :--- | :---: |
| **Quy mô tập dữ liệu** | Đúng 569 mẫu bệnh phẩm | 569 dòng, 32 cột | **ĐẠT (Hoàn hảo)** |
| **Giá trị khuyết thiếu (Missing)** | 0 giá trị NaN/Null | **0** trên toàn bộ 32 cột (0.0%) | **ĐẠT (Hoàn hảo)** |
| **Bản ghi trùng lặp (Duplicates)** | Không có dòng trùng lặp | **0** dòng trùng (trùng ID: 0, trùng 30 features: 0) | **ĐẠT (Hoàn hảo)** |
| **Kiểu dữ liệu (Data types)** | 30 features float, ID int, label string | 30 float64, 1 int64, 1 object/string | **ĐẠT (Hoàn hảo)** |
| **Giá trị phi lý / Vi phạm vật lý** | Kích thước, chu vi, diện tích $\ge 0$ | 0 giá trị âm (< 0) trên cả 30 đặc trưng | **ĐẠT (Hoàn hảo)** |
| **Phân bố nhãn mục tiêu** | Nhị phân B và M | 357 Lành tính (62.74%), 212 Ác tính (37.26%) | **ĐẠT (Mất cân bằng nhẹ 1.68:1)** |
| **Ngoại lệ thống kê (Outliers)** | Phát hiện bằng IQR (Tukey's fences) | 171 mẫu có $\ge 1$ ngoại lệ (chiếm 30.05%) | **CẦN GIỮ NGUYÊN (Tín hiệu sinh học)** |

---

## 2. CHI TIẾT KIỂM TRA GIÁ TRỊ KHUYẾT THIẾU (MISSING VALUES)
- Toàn bộ 569 dòng và 32 thuộc tính đều chứa đầy đủ dữ liệu thực.
- Không phát hiện bất kỳ giá trị khuyết thiếu nào ở dạng `NaN`, `None`, khoảng trắng rỗng (`""`), hoặc các giá trị mã hóa thiếu quy ước (như `-999`, `?`, `NA`).
- **Kết luận**: Không cần áp dụng bất kỳ kỹ thuật điền khuyết (Imputation) nào như Mean/Median Imputer hay KNNImputer.

---

## 3. CHI TIẾT KIỂM TRA BẢN GHI TRÙNG LẶP (DUPLICATE RECORDS)
Việc kiểm tra trùng lặp được tiến hành đa tầng với các tiêu chí chặt chẽ:
1. **Trùng lặp toàn bộ bản ghi (Full-row duplicate)**: So sánh cả 32 cột $\rightarrow$ **0 bản ghi** trùng lặp.
2. **Trùng lặp khóa định danh (`id`)**: Kiểm tra `df.duplicated(subset=['id'])` $\rightarrow$ **0 trường hợp**. Tất cả 569 mẫu đều sở hữu mã ID duy nhất.
3. **Trùng lặp không gian đặc trưng (Feature-vector duplicate)**: So sánh 30 đặc trưng số để tìm khả năng hai bệnh nhân khác nhau nhưng có số đo giống hệt nhau $\rightarrow$ **0 trường hợp**.
- **Kết luận**: Tập dữ liệu hoàn toàn độc lập, không bị thổi phồng giả tạo (Artificial data duplication).

---

## 4. KIỂM TRA KIỂU DỮ LIỆU VÀ TÍNH HỢP LỆ VẬT LÝ
- Cột `id`: Kiểu số nguyên `int64` (mã hồ sơ bệnh phẩm).
- Cột `diagnosis`: Kiểu chuỗi ký tự chứa đúng 2 giá trị nhị phân `['B', 'M']`.
- 30 cột đặc trưng hình thái nhân tế bào: Đều là số thực liên tục `float64`.
- **Kiểm tra biên vật lý (Boundary Sanity Check)**:
  - Các chỉ số bán kính, chu vi, diện tích, độ mịn, độ đối xứng không thể nhận giá trị âm. Kết quả: Toàn bộ 30 đặc trưng đều có $\text{min} \ge 0$.
  - Phát hiện **13 mẫu bệnh phẩm có các giá trị concavity và concave points bằng đúng 0.0**:
    - `concavity_mean`: 13 mẫu
    - `concave points_mean`: 13 mẫu
    - `concavity_worst`: 13 mẫu
    - `concave points_worst`: 13 mẫu
  - **Phân tích bản chất y sinh**: Khi lọc 13 mẫu này, **100% đều thuộc lớp Lành tính (`B`: 13, `M`: 0)**. Về mặt tế bào học, tế bào lành tính bình thường có màng nhân tròn đều, trơn láng hoàn hảo và không xuất hiện các góc khuyết hay vết lõm dị dạng. Do đó, giá trị đo được bằng $0.0$ là hoàn toàn chính xác về mặt bệnh học, phản ánh đúng tín hiệu của mô lành.

---

## 5. THỐNG KÊ PHÂN BỐ NHÃN MỤC TIÊU VÀ MỨC ĐỘ MẤT CÂN BẰNG

| Nhãn (`diagnosis`) | Ý nghĩa bệnh học | Số lượng mẫu | Tỷ lệ phần trăm |
| :---: | :--- | :---: | :---: |
| **B (Benign)** | Khối u lành tính (Không phải ung thư) | **357** | **62.74%** |
| **M (Malignant)** | Khối u ác tính (Ung thư vú) | **212** | **37.26%** |
| **Tổng cộng** | | **569** | **100.00%** |

- **Tỷ lệ mất cân bằng lớp (Imbalance Ratio)**:
  $$\frac{N_{\text{Benign}}}{N_{\text{Malignant}}} = \frac{357}{212} \approx 1.68 : 1$$
- **Nhận định**: Mức độ mất cân bằng ở mức nhẹ (Mild Imbalance). Tuy nhiên, trong y tế, việc chẩn đoán sai ca Ác tính thành Lành tính (False Negative) để lại hậu quả nghiêm trọng hơn rất nhiều so với False Positive.
- **Quyết định phương pháp luận**:
  - Bắt buộc áp dụng **Stratified Splitting** khi chia tập Train/Test để giữ nguyên tỷ lệ 62.74% : 37.26%.
  - Áp dụng **Stratified K-Fold Cross-Validation** khi tinh chỉnh siêu tham số.
  - Sử dụng các thước đo đánh giá tập trung vào lớp ác tính: `Recall(M)`, `Precision(M)`, `F1-Score`, `ROC-AUC`, và Ma trận nhầm lẫn (Confusion Matrix).

---

## 6. KIỂM TRA GIÁ TRỊ NGOẠI LỆ (OUTLIERS) VÀ PHÂN TÍCH CHUYÊN SÂU

### 6.1. Thống kê ngoại lệ theo phương pháp IQR (Tukey's Fences)
Giá trị ngoại lệ được xác định khi nằm ngoài khoảng $[Q_1 - 1.5 \times IQR, \; Q_3 + 1.5 \times IQR]$:

| STT | Tên đặc trưng | Q1 (25%) | Q3 (75%) | IQR | Giới hạn trên (Upper) | Giá trị Max | Số lượng ngoại lệ | Tỷ lệ (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `area_se` | 17.85 | 45.19 | 27.34 | 86.20 | 542.20 | **65** | 11.42% |
| 2 | `radius_se` | 0.232 | 0.479 | 0.246 | 0.849 | 2.873 | **38** | 6.68% |
| 3 | `perimeter_se` | 1.606 | 3.357 | 1.751 | 5.984 | 21.980 | **38** | 6.68% |
| 4 | `area_worst` | 515.30 | 1084.00 | 568.70 | 1937.05 | 4254.00 | **35** | 6.15% |
| 5 | `smoothness_se`| 0.0052 | 0.0081 | 0.0030 | 0.0126 | 0.0311 | **30** | 5.27% |
| 6 | `fractal_dimension_se`| 0.0022 | 0.0046 | 0.0023 | 0.0080 | 0.0298 | **28** | 4.92% |
| 7 | `compactness_se`| 0.0131 | 0.0325 | 0.0194 | 0.0615 | 0.1354 | **28** | 4.92% |
| 8 | `symmetry_se` | 0.0152 | 0.0235 | 0.0083 | 0.0360 | 0.0790 | **27** | 4.75% |
| 9 | `area_mean` | 420.30 | 782.70 | 362.40 | 1326.30 | 2501.00 | **25** | 4.39% |
| 10 | `fractal_dimension_worst`| 0.0715 | 0.0921 | 0.0206 | 0.1230 | 0.2075 | **24** | 4.22% |

### 6.2. Phân tích phân bố mẫu có ngoại lệ
- Tổng số mẫu bệnh phẩm có ít nhất 1 đặc trưng là ngoại lệ IQR: **171 / 569 mẫu (chiếm 30.05%)**.
- Phân bố nhãn của 171 mẫu ngoại lệ này:
  - **Lớp Ác tính (`M`)**: **114 mẫu** (chiếm tới **53.77%** trên tổng số 212 ca ác tính của toàn bộ tập dữ liệu!).
  - **Lớp Lành tính (`B`)**: **57 mẫu** (chỉ chiếm 15.97% số ca lành tính).

---

## 7. PHÂN BIỆT NGOẠI LỆ THỐNG KÊ VS DỮ LIỆU THỰC SỰ SAI: VÌ SAO TUYỆT ĐỐI KHÔNG XÓA OUTLIER?

### 7.1. Bản chất sinh học của các giá trị ngoại lệ trong ung thư vú
- **Dữ liệu thực sự sai (Data Errors / Artefacts)**: Là các giá trị phát sinh do lỗi nhập liệu của con người (như gõ nhầm thêm số 0), cảm biến camera kính hiển vi bị lỗi chập cháy, hoặc mẫu bị tráo đổi. Các giá trị này mang tính phi lý vật lý (ví dụ: bán kính tế bào âm, hoặc diện tích gấp một triệu lần bình thường). Trong tập WDBC, **hoàn toàn không có dữ liệu sai loại này**.
- **Ngoại lệ thống kê (Statistical Outliers / Extreme Biological Phenotypes)**: Các giá trị `area_worst = 4254` hay `perimeter_worst = 251.2` không phải là lỗi! Tế bào ung thư ác tính có cơ chế phân chia nhân vô tổ chức, nhân phình to cực đại và biến dạng dữ dội. Do đó, các khối u ác tính tiến triển nhanh tự nhiên sẽ sở hữu các số đo hình học vượt xa phân bố Gauss thông thường của tế bào lành tính.

### 7.2. Hậu quả tai hại nếu xóa bỏ ngoại lệ
Nếu áp dụng quy tắc cơ học "loại bỏ mẫu nằm ngoài 1.5 IQR", chúng ta sẽ:
1. **Xóa mất hơn 53% các ca ung thư ác tính (114 ca M)**, làm mất đi chính các mẫu hình bệnh học mà mô hình cần học nhất!
2. Khiến mô hình bị mù trước các ca ung thư kích thước lớn ngoài thực tế.

### 7.3. Tính chất kháng ngoại lệ bẩm sinh của Cây quyết định và Rừng ngẫu nhiên
- Các thuật toán dạng cây (Tree-based algorithms) như Decision Tree hay Random Forest **hoàn toàn không bị ảnh hưởng tiêu cực bởi độ lớn của ngoại lệ** (Monotonic transformation invariant).
- Thuật toán CART chỉ quan tâm đến **thứ tự sắp xếp (ranks)** của dữ liệu để tìm điểm cắt (split point) tối ưu:
  $$\text{Điều kiện rẽ nhánh: } \text{feature} \le \text{threshold}$$
- Một giá trị diện tích là $2000$ hay $4000$ thì nó đều nằm về phía $> 1300$, dẫn đến cùng một quyết định phân nhánh mà không làm dịch chuyển ranh giới quyết định giống như trong Hồi quy tuyến tính hay Support Vector Machines (SVM).
- **QUYẾT ĐỊNH**: **Giữ nguyên 100% các giá trị ngoại lệ, không xóa bỏ hay biến đổi bất kỳ mẫu nào.**

---

## 8. ĐỀ XUẤT PHƯƠNG ÁN LÀM SẠCH VÀ TIỀN XỬ LÝ (CHỐNG DATA LEAKAGE)
1. **Trạng thái hiện tại**: Dữ liệu thô từ UCI đã đạt độ sạch tuyệt đối (0 missing, 0 duplicate, 0 invalid types, 0 negative values). Do đó, **không cần bước imputation hay lọc nhiễu thô bạo**.
2. **Quy tắc chia tập**:
   - Tách tập Stratified Train/Test (80% Train : 20% Test) cố định bằng `RANDOM_STATE = 42`.
   - Đóng băng tập Test độc lập ngay lập tức.
3. **Quy tắc tiền xử lý**:
   - Thuật toán Decision Tree và Random Forest **không yêu cầu chuẩn hóa thang đo (Feature Scaling)**.
   - Nếu trong các bài toán so sánh mở rộng cần chuẩn hóa (ví dụ `StandardScaler` hay `MinMaxScaler`), mọi thao tác học tham số ($\mu, \sigma, \min, \max$) **bắt buộc chỉ được fit trên tập Train**, sau đó áp dụng phép biến đổi (`transform`) sang tập Test để chống rò rỉ dữ liệu (Zero Data Leakage).
   - **Tuyệt đối không thực hiện scaling, PCA, resampling hay feature selection trên toàn bộ dữ liệu 569 mẫu.**
