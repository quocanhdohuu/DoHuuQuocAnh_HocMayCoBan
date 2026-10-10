# Thẻ Dữ Liệu (Data Card) - Bộ Dữ Liệu WDBC
**Học phần**: Học máy cơ bản (12523W.1)  
**Đề tài**: Project 16 — Minh họa phân loại khối u vú bằng cây và rừng  
**Phiên bản dữ liệu**: `1.0.0` (UCI Frozen Snapshot)  
**Tiêu chuẩn định dạng**: Tuân theo khuôn mẫu *Datasheets for Datasets* (Gebru et al., 2021)

---

## 1. Động Lực Thu Thập Dữ Liệu (Motivation)

- **Mục đích thu thập gốc**:
  Bộ dữ liệu Wisconsin Diagnostic Breast Cancer (WDBC) được thu thập bởi Tiến sĩ William H. Wolberg, W. Nick Street và Olvi L. Mangasarian tại Bệnh viện Đại học Wisconsin (Madison, Hoa Kỳ) nhằm hỗ trợ chẩn đoán không xâm lấn bản chất khối u vú (lành tính vs ác tính) từ hình ảnh số hóa tế bào học chọc hút kim nhỏ (Fine Needle Aspirate - FNA).
- **Đơn vị tài trợ và quản lý nguồn**:
  Viện Ung thư Quốc gia Hoa Kỳ (NCI), Quỹ Khoa học Quốc gia Hoa Kỳ (NSF) và lưu trữ chính thức tại UCI Machine Learning Repository.
- **Mục đích sử dụng trong Project 16**:
  Huấn luyện, kiểm chứng và đánh giá năng lực phân loại của Cây quyết định (Decision Tree - CART), Cây tỉa cành (Cost-Complexity Pruning) và Rừng ngẫu nhiên (Random Forest) trong khuôn khổ học phần Học máy cơ bản tại Đại Học Công Nghệ Kỹ Thuật Hưng Yên.

---

## 2. Thành Phần Dữ Liệu (Dataset Composition)

- **Quy mô tập dữ liệu**:
  Tổng cộng $569$ mẫu bệnh phẩm sinh thiết (hàng) và $32$ thuộc tính (cột).
- **Phân loại thuộc tính**:
  1. `id`: Mã định danh số nguyên của mẫu bệnh phẩm (`int64`, không có ý nghĩa tiên lượng).
  2. `diagnosis`: Nhãn chẩn đoán mục tiêu (`object` / `string`):
     - `B` (Benign - Lành tính): $357$ mẫu ($62.74\%$).
     - `M` (Malignant - Ác tính): $212$ mẫu ($37.26\%$).
     - Tỷ lệ mất cân bằng: $1.68 : 1$.
  3. $30$ đặc trưng số thực liên tục (`float64`):
     Đo đạc $10$ đặc tính hình thái học nhân tế bào trích xuất qua thuật toán xử lý ảnh Snakes/Active Contours, mỗi đặc tính được tính toán theo $3$ thống kê:
     - Giá trị trung bình (Mean - 10 đặc trưng): `radius_mean`, `texture_mean`, `perimeter_mean`, `area_mean`, `smoothness_mean`, `compactness_mean`, `concavity_mean`, `concave points_mean`, `symmetry_mean`, `fractal_dimension_mean`.
     - Sai số chuẩn (Standard Error - 10 đặc trưng): `radius_se`, `texture_se`, ..., `fractal_dimension_se`.
     - Giá trị xấu nhất / Lớn nhất (Worst / Largest - 10 đặc trưng): `radius_worst`, `texture_worst`, ..., `fractal_dimension_worst`.
- **Kiểm toán chất lượng dữ liệu**:
  - Tỷ lệ khuyết thiếu (Missing values): **$0.0\%$** ($0$ giá trị NaN/Null trên toàn bộ $569 \times 32$ ô dữ liệu).
  - Bản ghi trùng lặp (Duplicates): **$0$** dòng trùng lặp hoàn toàn, $0$ dòng trùng ID, $0$ dòng trùng không gian 30 đặc trưng.
  - Vi phạm vật lý: $0$ giá trị âm. $13$ mẫu có giá trị concavity = 0.0 đều thuộc lớp Lành tính (phản ánh đặc tính màng nhân trơn nhẵn sinh học).

---

## 3. Quy Trình Thu Thập và Tiền Xử Lý (Collection & Preprocessing)

- **Phương pháp thu thập gốc**:
  Mẫu tế bào được lấy từ khối u vú của bệnh nhân bằng bơm tiêm kim nhỏ (FNA), nhuộm tiêu bản và quét ảnh phóng đại qua kính hiển vi. Hệ thống phần mềm Xcyt số hóa đường biên nhân tế bào và tự động tính toán các chỉ số hình học.
- **Tiền xử lý trong dự án**:
  - Loại bỏ cột `id` khỏi không gian đặc trưng học máy để ngăn ngừa rò rỉ dữ liệu hoặc học vẹt định danh.
  - Mã hóa biến mục tiêu: `B` $\rightarrow 0$ (Lành tính), `M` $\rightarrow 1$ (Ác tính).
  - **Không áp dụng Data Imputation**: Do dữ liệu không có giá trị khuyết.
  - **Không áp dụng Feature Scaling ép buộc**: Cây quyết định và Rừng ngẫu nhiên là các thuật toán bất biến với phép biến đổi đơn điệu (monotonic invariance), việc giữ nguyên đơn vị gốc giúp mô hình bảo toàn khả năng giải thích sinh học.

---

## 4. Phân Chia Dữ Liệu và Chống Rò Rỉ (Data Splits & Leakage Prevention)

Để ngăn chặn tuyệt đối hiện tượng Data Leakage, phân chia dữ liệu được thực hiện ngẫu nhiên phân tầng (Stratified Splitting) với `random_state=42`:
- **Tập Huấn luyện (Train Set)**: $398$ mẫu ($70\%$) — $250$ Benign, $148$ Malignant.
- **Tập Kiểm chứng (Validation Set)**: $85$ mẫu ($15\%$) — $53$ Benign, $32$ Malignant.
- **Tập Kiểm thử độc lập (Test Set)**: $86$ mẫu ($15\%$) — $54$ Benign, $32$ Malignant.

**Quy tắc kiểm soát**:
- Tập Test được niêm phong hoàn toàn (Freeze). Không tham gia vào quá trình tiền xử lý, trích xuất đặc trưng, hay tinh chỉnh siêu tham số.
- Giao tập hợp giữa các tập: $\text{Train} \cap \text{Val} = \emptyset$, $\text{Train} \cap \text{Test} = \emptyset$, $\text{Val} \cap \text{Test} = \emptyset$.

---

## 5. Giới Hạn và Cân Nhắc Đạo Đức (Limitations & Ethical Considerations)

1. **Giới hạn nhân khẩu học và phân bổ quần thể**:
   Dữ liệu được thu thập tại một trung tâm y tế duy nhất (Bệnh viện Madison, Wisconsin) từ những năm 1990. Không có thông tin về độ tuổi, chủng tộc, tiền sử gia đình, hay giai đoạn mãn kinh. Do đó, mô hình có thể gặp hiện tượng Domain Shift (trượt phân phối) khi áp dụng cho các quần thể phụ nữ tại khu vực địa lý khác (ví dụ: phụ nữ châu Á).
2. **Kích thước mẫu khiêm tốn ($N = 569$)**:
   Tập Test chỉ có 32 ca ác tính, khiến khoảng tin cậy của Recall dao động trong khoảng $[84.26\%, 99.45\%]$.
3. **Mục đích phi lâm sàng**:
   Bộ dữ liệu và mô hình huấn luyện chỉ dùng cho mục đích học thuật và giáo dục, tuyệt đối không sử dụng trong chẩn đoán lâm sàng tự động.
