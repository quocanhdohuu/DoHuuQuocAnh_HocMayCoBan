# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA REPORT)
## Đề tài: Project 16 — Minh họa phân loại khối u vú bằng cây và rừng (WDBC)
**Phạm vi dữ liệu**: **CHỈ SỬ DỤNG TẬP HUẤN LUYỆN (Train Set — 398 mẫu)**  
**Nguyên tắc cốt lõi**: **Bảo toàn tuyệt đối tính độc lập của Validation và Test Set (Zero Data Leakage)**  
**Thời điểm thực hiện**: 08/10/2026  
**Công cụ thực hiện**: Python 3.12, pandas, matplotlib, seaborn  

---

## 1. NGUYÊN TẮC HỌC MÁY TRONG QUY TRÌNH EDA
1. **Cô lập tập Validation và Test**: Toàn bộ các phân tích thống kê, đồ thị phân bố, tính toán tương quan trong báo cáo này **chỉ được tiến hành trên 398 mẫu của tập Train** (`data/train.csv`). Tập Validation (85 mẫu) và tập Test (86 mẫu) được giữ nguyên vẹn và không tham gia vào bất kỳ quyết định tiền xử lý nào.
2. **Không suy diễn nhân quả**: Mọi hệ số tương quan ($r$) được tính toán chỉ phản ánh mức độ đồng biến thiên thống kê tuyến tính giữa các phép đo hình thái học nhân tế bào; tuyệt đối không khẳng định mối quan hệ nhân quả (Causality).

---

## 2. BẢNG THỐNG KÊ MÔ TẢ TOÀN DIỆN 30 ĐẶC TRƯNG (TẬP TRAIN, N=398)

| Đặc trưng | Trung bình (Mean) | Độ lệch chuẩn (Std) | Tối thiểu (Min) | Trung vị (Median) | Tối đa (Max) | Độ lệch (Skewness) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `radius_mean` | 14.1265 | 3.5532 | 6.9810 | 13.3550 | 28.1100 | 0.96 |
| `texture_mean` | 19.4382 | 4.3224 | 9.7100 | 19.0300 | 39.2800 | 0.65 |
| `perimeter_mean` | 91.9044 | 24.4477 | 43.7900 | 86.3650 | 188.5000 | 1.00 |
| `area_mean` | 655.3254 | 353.6835 | 143.5000 | 548.7500 | 2499.0000 | 1.64 |
| `smoothness_mean` | 0.0959 | 0.0144 | 0.0625 | 0.0951 | 0.1634 | 0.60 |
| `compactness_mean` | 0.1026 | 0.0535 | 0.0194 | 0.0909 | 0.3454 | 1.31 |
| `concavity_mean` | 0.0885 | 0.0812 | 0.0000 | 0.0596 | 0.4268 | 1.48 |
| `concave points_mean` | 0.0485 | 0.0393 | 0.0000 | 0.0333 | 0.2012 | 1.22 |
| `symmetry_mean` | 0.1814 | 0.0271 | 0.1060 | 0.1798 | 0.2906 | 0.69 |
| `fractal_dimension_mean` | 0.0626 | 0.0071 | 0.0502 | 0.0613 | 0.0974 | 1.32 |
| `radius_se` | 0.4068 | 0.2786 | 0.1115 | 0.3191 | 2.8730 | 2.92 |
| `texture_se` | 1.2174 | 0.5570 | 0.3602 | 1.1095 | 4.8850 | 1.82 |
| `perimeter_se` | 2.8676 | 2.0150 | 0.7570 | 2.3050 | 21.9800 | 3.33 |
| `area_se` | 40.2961 | 43.5622 | 6.8020 | 24.6100 | 525.6000 | 4.76 |
| `smoothness_se` | 0.0069 | 0.0029 | 0.0017 | 0.0063 | 0.0311 | 2.57 |
| `compactness_se` | 0.0251 | 0.0179 | 0.0023 | 0.0198 | 0.1064 | 1.79 |
| `concavity_se` | 0.0323 | 0.0331 | 0.0000 | 0.0259 | 0.3960 | 5.39 |
| `concave points_se` | 0.0116 | 0.0063 | 0.0000 | 0.0109 | 0.0528 | 1.61 |
| `symmetry_se` | 0.0204 | 0.0084 | 0.0079 | 0.0187 | 0.0790 | 2.34 |
| `fractal_dimension_se` | 0.0038 | 0.0027 | 0.0009 | 0.0031 | 0.0298 | 4.24 |
| `radius_worst` | 16.2966 | 4.8525 | 7.9300 | 14.9750 | 33.1300 | 1.08 |
| `texture_worst` | 25.9209 | 6.1146 | 12.0200 | 25.4800 | 49.5400 | 0.49 |
| `perimeter_worst` | 107.4012 | 33.7110 | 50.4100 | 97.7350 | 229.3000 | 1.09 |
| `area_worst` | 883.1176 | 566.8742 | 185.2000 | 684.5500 | 3432.0000 | 1.74 |
| `smoothness_worst` | 0.1322 | 0.0238 | 0.0712 | 0.1311 | 0.2226 | 0.43 |
| `compactness_worst` | 0.2524 | 0.1575 | 0.0273 | 0.2118 | 1.0580 | 1.49 |
| `concavity_worst` | 0.2739 | 0.2109 | 0.0000 | 0.2290 | 1.2520 | 1.15 |
| `concave points_worst` | 0.1147 | 0.0665 | 0.0000 | 0.0994 | 0.2910 | 0.47 |
| `symmetry_worst` | 0.2911 | 0.0642 | 0.1565 | 0.2820 | 0.6638 | 1.58 |
| `fractal_dimension_worst` | 0.0839 | 0.0182 | 0.0550 | 0.0801 | 0.2075 | 1.82 |

---

## 3. PHÂN TÍCH CHI TIẾT CÁC BIỂU ĐỒ TRỰC QUAN HÓA

### 3.1. Biểu đồ 1: Phân bố Nhãn mục tiêu trên Tập Train
- **Tệp biểu đồ**: `reports/figures/eda_target_distribution.png`
- **Mô tả trực quan**: Biểu đồ cột (Bar chart) và biểu đồ tròn (Donut chart) thể hiện số lượng và tỷ lệ mẫu giữa hai lớp chẩn đoán trên tập Train:
  - Khối u Lành tính (`B`): **250 mẫu (62.8%)**.
  - Khối u Ác tính (`M`): **148 mẫu (37.2%)**.
- **Giải thích & Kết luận kỹ thuật**:
  - Tỷ lệ lớp được bảo toàn hoàn hảo so với tỷ lệ tổng thể ($37.26\%$) nhờ cơ chế Stratified Split.
  - Sự mất cân bằng ở mức $1.69 : 1$ không quá khắc nghiệt nhưng có tính chất bất đối xứng về chi phí y tế.
  - **Hệ quả cho huấn luyện**: Bắt buộc phải áp dụng **Stratified K-Fold Cross-Validation** (5 folds) khi tinh chỉnh siêu tham số và ưu tiên tối đa chỉ số **Recall của lớp Malignant** để triệt tiêu False Negative.

---

### 3.2. Biểu đồ 2: Histogram và Mật độ Xác suất (KDE) của 6 Đặc trưng Tiêu biểu
- **Tệp biểu đồ**: `reports/figures/eda_feature_histograms.png`
- **Mô tả trực quan**: Thể hiện phân bố tần suất và đường cong mật độ KDE của 6 đặc trưng then chốt: `radius_mean`, `texture_mean`, `area_mean`, `concave points_mean`, `perimeter_worst`, và `concave points_worst`. Mỗi ô đồ thị được bóc tách thành 2 màu: Xanh lam (Lành tính) và Cam (Ác tính).
- **Giải thích & Nhận định**:
  1. Hầu hết các đặc trưng đo kích thước (`area_mean`, `radius_mean`) và độ lõm (`concave points_mean`, `concave points_worst`) đều có phân bố **lệch phải dương (Positive/Right-skewed, Skewness > 1)** với đuôi dài hướng về phía các giá trị cao.
  2. Sự phân tách giữa hai phân bố Lành tính và Ác tính là **cực kỳ rõ nét**:
     - Phân bố Lành tính tập trung dày đặc ở vùng giá trị thấp (ví dụ: `concave points_worst` chủ yếu $< 0.10$).
     - Phân bố Ác tính dịch chuyển mạnh về phía bên phải với phương sai lớn hơn nhiều.
- **Hệ quả cho xử lý & mô hình**:
  - Không cần áp dụng các phép biến đổi chuẩn hóa (như Log transform hay Box-Cox) vì thuật toán Cây quyết định (Decision Tree) và Rừng ngẫu nhiên (Random Forest) là các mô hình phi tham số (Non-parametric), không giả định dữ liệu phải tuân theo phân bố chuẩn Gauss.

---

### 3.3. Biểu đồ 3: Boxplot So sánh Phân bố Đặc trưng giữa Hai Lớp
- **Tệp biểu đồ**: `reports/figures/eda_feature_boxplots.png`
- **Mô tả trực quan**: Biểu đồ hộp biểu diễn 5 số đo tóm tắt (Min, Q1, Median, Q3, Max) và các điểm ngoại lệ vượt ngoài $1.5 \times IQR$ của từng lớp.
- **Giải thích & Nhận định**:
  1. **Khoảng cách giữa hai trung vị (Median Gap)** là rất lớn. Ví dụ đối với `perimeter_worst`, trung vị của lớp Lành tính chỉ khoảng $87\,\mu m$, trong khi trung vị của lớp Ác tính lên tới hơn $125\,\mu m$.
  2. Toàn bộ hộp IQR ($Q_1 \rightarrow Q_3$) của lớp Lành tính gần như tách rời hoàn toàn khỏi hộp IQR của lớp Ác tính đối với các đặc trưng `concave points_mean` và `concave points_worst`.
  3. Các điểm ngoại lệ (Fliers) hầu hết tập trung ở phía đuôi trên của lớp Ác tính, phản ánh các trường hợp ung thư khối u phình to cực đại.
- **Hệ quả cho mô hình hóa**:
  - Dữ liệu có tín hiệu phân tách rất mạnh. Cây quyết định hoàn toàn có khả năng tìm được các điểm cắt đơn giản (Simple Thresholds) để phân loại với độ chính xác cao.
  - Giữ nguyên các ngoại lệ này vì cây quyết định miễn nhiễm với khoảng cách hình học của ngoại lệ.

---

### 3.4. Biểu đồ 4: Ma trận Tương quan Pearson (Correlation Heatmap)
- **Tệp biểu đồ**: `reports/figures/eda_correlation_heatmap.png`
- **Mô tả trực quan**: Bản đồ nhiệt thể hiện hệ số tương quan tuyến tính Pearson ($r \in [-1, 1]$) giữa các đặc trưng trung bình (`_mean`) và nhóm đặc trưng cực đại (`_worst`).
- **Giải thích & Nhận định**:
  1. **Đa cộng tuyến cực mạnh (Extreme Multicollinearity)** giữa các thuộc tính hình học:
     - Tương quan giữa `radius_mean` và `perimeter_mean`: $r = 0.998$ (gần như $1.0$).
     - Tương quan giữa `radius_mean` và `area_mean`: $r = 0.987$.
     - Tương quan giữa `radius_worst` và `perimeter_worst`: $r = 0.994$.
     - *Lý do hình học*: Chu vi tỷ lệ thuận với bán kính ($P = 2\pi r$) và diện tích tỷ lệ thuận với bình phương bán kính ($S = \pi r^2$).
  2. Tương quan mạnh giữa độ nén (`compactness`), độ lõm (`concavity`) và điểm lõm (`concave points`): $r \approx 0.85 - 0.92$.
- **CẢNH BÁO QUAN HỆ NHÂN QUẢ**:
  > *Hệ số tương quan cao giữa `perimeter_mean` và `concave points_mean` ($r = 0.85$) chỉ cho thấy khi nhân tế bào to ra thì số điểm lõm có xu hướng tăng lên. Đây là sự đồng biến thiên hình học, không đồng nghĩa với việc "chu vi tăng gây ra điểm lõm tăng" theo quan hệ nhân quả sinh học.*
- **Hệ quả cho mô hình cây và rừng**:
  - Đối với Cây quyết định đơn lẻ (Single Tree): Khi có nhiều biến cộng tuyến, thuật toán sẽ chọn 1 biến có độ giảm Gini cao nhất (ví dụ `perimeter_worst`) làm nút phân chia, khiến các biến tương đương (`radius_worst`, `area_worst`) có thể nhận Feature Importance bằng 0.
  - Đối với Rừng ngẫu nhiên (Random Forest): Cơ chế chọn ngẫu nhiên tập con đặc trưng tại mỗi nút (`max_features = 'sqrt'`) sẽ buộc mô hình phải luân phiên chọn cả `radius`, `perimeter` và `area`, giúp phân bổ độ quan trọng đều đặn hơn và giảm phương sai của tổng thể.

---

### 3.5. Biểu đồ 5: Không gian Phân tách giữa 2 Đặc trưng Cốt lõi
- **Tệp biểu đồ**: `reports/figures/eda_discriminative_features.png`
- **Mô tả trực quan**: Biểu đồ tán xạ 2 chiều (Joint Scatter Plot) giữa `concave points_worst` (trục hoành) và `perimeter_worst` (trục tung) kèm đường cong phân bố biên (Marginal KDE) và các đường phân chia trực giao trực quan.
- **Giải thích & Nhận định**:
  1. Hai đám mây điểm Lành tính (xanh) và Ác tính (đỏ) phân tách nhau cực kỳ rõ rệt trong không gian 2D.
  2. Các mẫu Lành tính hầu như hoàn toàn nằm gọn trong góc phần tư phía dưới bên trái:
     $$\text{concave points\_worst} \le 0.135 \quad \text{VÀ} \quad \text{perimeter\_worst} \le 105.0\,\mu m$$
  3. Chỉ có một vùng chồng lấn rất hẹp xung quanh ranh giới này (khoảng 5–10 mẫu có kích thước trung gian).
- **Hệ quả cho mô hình hóa**:
  - Minh họa trực quan chính xác cách Cây quyết định cắt không gian: Cây quyết định tạo ra các ranh giới song song với các trục tọa độ (Axis-aligned decision boundaries).
  - Kết quả này dự báo rằng một Cây quyết định đã cắt tỉa (Pruned Tree) với độ sâu chỉ từ **3 đến 4 tầng** hoàn toàn có thể đạt hiệu năng phân loại vượt trội (Accuracy > 93%, Recall > 90%) mà vẫn giữ được tính minh bạch và khả năng giải thích (Interpretability) tối đa.

---

## 4. TỔNG KẾT VÀ QUYẾT ĐỊNH CHO BƯỚC TIẾP THEO
1. **Dữ liệu tập Train đạt độ sạch và tính phân tách lý tưởng**: Không cần thực hiện lọc ngoại lệ, không cần imputation.
2. **Không áp dụng Feature Scaling**: Thuật toán Decision Tree và Random Forest hoạt động độc lập với thang đo đặc trưng. Giữ nguyên đơn vị đo gốc ($\mu m, \mu m^2$) giúp đường đi quyết định (Decision Path) trên Web sau này dễ hiểu với người dùng.
3. **Mô hình mục tiêu**:
   - Baseline: `DummyClassifier` để đo mức sàn.
   - Mô hình 1: `DecisionTreeClassifier` unpruned để quan sát hiện tượng học vẹt các nhánh nhỏ.
   - Mô hình 2: `DecisionTreeClassifier` cắt tỉa bằng pre-pruning (`max_depth`) và post-pruning (`ccp_alpha`) để tìm cấu trúc cây tối ưu.
   - Mô hình 3: `RandomForestClassifier` để khử phương sai và nâng cao độ ổn định.
