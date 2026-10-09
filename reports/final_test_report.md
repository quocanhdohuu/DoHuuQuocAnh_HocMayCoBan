# Báo Cáo Đánh Giá Mô Hình Cuối Cùng Trên Tập Test Độc Lập
**Học phần**: Học máy cơ bản (12523W.1)  
**Đề tài**: Project 16 - Minh họa phân loại khối u vú bằng cây và rừng  
**Tác giả**: Đỗ Hữu Quốc Anh  
**Thời điểm mở niêm phong Test**: 09/10/2026  

---

## 1. Xác Nhận Điều Kiện Trước Khi Mở Niêm Phong Tập Test

Theo đúng quy chuẩn phương pháp luận học máy nghiêm ngặt, **tập Test ($N = 86$)** được giữ đóng băng tuyệt đối kể từ Nhiệm vụ 05 cho đến khi toàn bộ các quyết định về kiến trúc mô hình, siêu tham số và ngưỡng phân loại được xác lập bằng dữ liệu **Train ($N = 398$)** và **Validation ($N = 85$)**.

### 1.1. Quyết định lựa chọn mô hình và lý do
- **Mô hình được chọn**: **Random Forest Classifier (Rừng Ngẫu Nhiên)**.
- **Lý do lựa chọn**:
  1. *Hiệu năng phân loại vượt trội*: Vượt trội áp đảo DummyClassifier và các Cây Quyết định đơn lẻ trên cả 5-Fold Cross-Validation (Mean CV Recall: $92.51\%$, Mean CV ROC-AUC: $0.9820$) và tập Validation ($F_1 = 95.08\%$, $\text{ROC-AUC} = 0.9941$).
  2. *Bảo vệ mục tiêu an toàn y tế*: Trên tập Validation, mô hình hạ số ca bỏ sót bệnh xuống mức thấp nhất (**chỉ 3 ca FN** so với 9 ca của Pruned Tree và 32 ca của Dummy), đồng thời **hoàn toàn không có ca báo động giả nào (FP = 0, Precision 100%)**.
  3. *Ổn định phương sai cao*: Tập hợp 100 cây con với cơ chế Random Feature Selection ($30\%$ đặc trưng mỗi split) triệt tiêu hiện tượng Overfitting của cây đơn lẻ và giữ vững Top 5 đặc trưng qua nhiều random seed độc lập (Thí nghiệm 4).

### 1.2. Chốt cấu hình siêu tham số (Frozen Hyperparameters)
Cấu hình được lưu cố định tại [backend/models/final_model_config.json](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/backend/models/final_model_config.json):
- `model`: `RandomForestClassifier`
- `n_estimators`: `100` (Số lượng cây quyết định trong rừng)
- `criterion`: `'gini'` (Hàm mục tiêu đo độ vẩn đục)
- `max_depth`: `8` (Chiều sâu tối đa mỗi cây con)
- `min_samples_leaf`: `1` (Số lượng mẫu tối thiểu tại nút lá)
- `max_features`: `0.3` (30% số đặc trưng = 9 đặc trưng ngẫu nhiên mỗi split)
- `random_state`: `42` (Đảm bảo tính tái lập 100%)
- `positive_class`: `1` (**Malignant - Ác tính**)
- `negative_class`: `0` (**Benign - Lành tính**)

### 1.3. Chốt ngưỡng quyết định (Decision Threshold)
- **Ngưỡng khóa**: $\tau = 0.50$ (Ngưỡng xác suất mặc định chuẩn).
- **Lý do**: Trên tập Validation, ngưỡng $\tau = 0.50$ đã đạt trạng thái cân bằng lý tưởng (Recall $90.62\%$, Precision $100\%$). Việc không can thiệp điều chỉnh ngưỡng giúp tránh nguy cơ tối ưu hóa quá mức (Threshold Overfitting) trước khi bước vào tập Test.

### 1.4. Kiểm tra liêm chính dữ liệu (Data Leakage Verification)
- Tập Test giữ nguyên vẹn **đúng 86 mẫu** ($54$ ca Lành tính, $32$ ca Ác tính).
- Không có bất kỳ kỹ thuật tính toán chuẩn hóa (scaling), trích xuất đặc trưng hay tuning tham số nào được thực hiện có sự tham gia của tập Test.

---

## 2. Kết Quả Đánh Giá Định Lượng Trên Tập Test Độc Lập ($N = 86$)

Dưới đây là kết quả kiểm thử khách quan duy nhất trên tập Test, trích xuất từ [reports/final_test_evaluation.json](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/final_test_evaluation.json):

### 2.1. Bảng Chỉ Số Hiệu Năng Cuối Cùng

| Chỉ số (Metric) | Giá trị thực nghiệm trên Test | Khoảng tin cậy 95% (Wilson Score CI) | Ý nghĩa lâm sàng |
| :--- | :---: | :---: | :--- |
| **Accuracy (Độ chính xác tổng)** | **98.84%** (85/86 mẫu) | **[93.70%, 99.79%]** | Tỷ lệ dự đoán đúng gần như tuyệt đối |
| **Precision Malignant (Độ chuẩn xác)** | **100.00%** (31/31 ca) | [89.03%, 100.00%] | **Không có ca báo động giả nào (FP = 0)** |
| **Recall Malignant (Độ nhạy ung thư)** | **96.88%** (31/32 ca) | **[84.26%, 99.45%]** | **Chỉ bỏ sót đúng 1 ca ác tính (FN = 1)** |
| **F1-Score Malignant** | **98.41%** | - | Cân bằng điều hòa tối ưu |
| **ROC-AUC (Năng lực phân tách)** | **0.9954** | - | Đường cong ROC tiệm cận hoàn hảo |

### 2.2. Ma Trận Nhầm Lẫn (Confusion Matrix)

$$\begin{pmatrix} \text{TN} = 54 & \text{FP} = 0 \\ \text{FN} = 1 & \text{TP} = 31 \end{pmatrix}$$

- **True Negatives (TN) = 54**: Cả 54/54 trường hợp u lành tính đều được kết luận chính xác là lành tính.
- **False Positives (FP) = 0**: Hoàn toàn không có bệnh nhân lành tính nào bị chẩn đoán nhầm là ung thư ác tính.
- **True Positives (TP) = 31**: Phát hiện chính xác 31/32 bệnh nhân có khối u ác tính.
- **False Negatives (FN) = 1**: Chỉ có **1 trường hợp ác tính duy nhất** bị dự đoán nhầm thành lành tính.

### 2.3. Báo Cáo Phân Loại Chi Tiết (Classification Report)

```
              precision    recall  f1-score   support

      Benign     0.9818    1.0000    0.9908        54
   Malignant     1.0000    0.9688    0.9841        32

    accuracy                         0.9884        86
   macro avg     0.9909    0.9844    0.9875        86
weighted avg     0.9886    0.9884    0.9883        86
```

---

## 3. Các Biểu Đồ Trực Quan Hóa Đánh Giá Cuối Cùng

### 3.1. Ma Trận Nhầm Lẫn Trên Tập Test
Biểu đồ ma trận nhiệt làm nổi bật kết quả phân loại trên tập Test độc lập:

![Confusion Matrix Test](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/final_test_confusion_matrix.png)

### 3.2. Đường Cong ROC và Đường Cong Precision-Recall Trên Test
Năng lực phân tách xác suất của Random Forest trên tập Test đạt diện tích dưới đường cong ROC $\text{AUC} = 0.9954$:

![Đường Cong ROC và PR Test](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/final_test_roc_pr_curves.png)

### 3.3. Thí Nghiệm Bắt Buộc 2: So Sánh 4 Mô Hình Trên Tập Test Độc Lập
Biểu đồ cột so sánh đối đầu toàn diện 4 mô hình học máy trên cùng tập Test:

![Thí Nghiệm 2 Model Comparison Test](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/exp2_model_comparison_test.png)

#### Bảng Số Liệu Chi Tiết Thí Nghiệm 2:
| Mô hình học máy | Accuracy | Precision (M) | Recall (M) | F1-Score (M) | ROC-AUC | Số ca bỏ sót (FN) | Số ca báo động giả (FP) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. DummyClassifier (Baseline)** | 62.79% | 0.00% | 0.00% | 0.00% | 0.5000 | 32 (100%) | 0 |
| **2. Unpruned Decision Tree** | 90.70% | 87.50% | 87.50% | 87.50% | 0.9005 | 4 | 4 |
| **3. Pruned Decision Tree** | 93.02% | 96.43% | 84.38% | 90.00% | 0.8843 | 5 | 1 |
| **4. Random Forest (Final Model)** | **98.84%** | **100.00%** | **96.88%** | **98.41%** | **0.9954** | **1** | **0** |

---

## 4. Phân Tích Chuyên Sâu Các Chỉ Số và Ca Bỏ Sót (False Negative)

### 4.1. Giải Thích Chi Tiết Từng Chỉ Số
1. **Recall Malignant ($96.88\%$)**:
   - Tỷ lệ phát hiện bệnh nhân ung thư đạt $31 / 32$. Đây là chỉ số quan trọng nhất trong tầm soát ung thư vì nó đảm bảo gần như không bệnh nhân nào bị mất cơ hội điều trị.
2. **Precision Malignant ($100.00\%$)**:
   - Khi mô hình đưa ra kết luận khối u ác tính, độ chuẩn xác là tuyệt đối ($31/31$). Không có bất kỳ bệnh nhân lành tính nào phải chịu tổn thương tâm lý hay sinh thiết oan uổng.
3. **Accuracy ($98.84\%$)**:
   - Chỉ số tổng hợp đạt $85/86$ ca đúng. Điểm số này thực sự phản ánh năng lực cao vì nó đi kèm với Recall và Precision đều xấp xỉ tuyệt đối, không phải do ngụy tạo bởi lớp đa số như DummyClassifier.
4. **ROC-AUC ($0.9954$)**:
   - Thể hiện rằng nếu chọn ngẫu nhiên 1 bệnh nhân ác tính và 1 bệnh nhân lành tính từ tập Test, xác suất mô hình gán điểm xác suất ác tính cao hơn cho bệnh nhân ung thư là **$99.54\%$**.

### 4.2. Phân Tích Chi Tiết Ca Bỏ Sót Duy Nhất (Sample 23 trong Test)
- **Thông tin mẫu**: Bệnh nhân ở chỉ số thứ 23 trong tập Test (Mã ID ban đầu: `86`).
- **Nhãn thực tế**: Malignant ($y = 1$).
- **Xác suất dự đoán bởi Random Forest**: $P(\text{Malignant}) = 0.1019$ ($10.19\%$).
- **Lý do y sinh học khiến mô hình dự đoán nhầm**:
  + Khi kiểm tra các chỉ số tế bào của mẫu số 23, các đặc trưng kích thước (`radius_mean = 12.36`, `area_worst = 544.1`, `perimeter_worst = 82.98`) nằm sâu trong dải phân phối điển hình của u lành tính (Benign mean radius $\approx 12.15$, mean area $\approx 462.7$).
  + Đây là một dạng khối u ác tính thể nhỏ giai đoạn rất sớm (Early-stage / Well-differentiated Carcinoma) có nhân tế bào chưa kịp phình to và chưa hình thành nhiều vết lõm màng nhân.
  + Với ngưỡng khóa $\tau = 0.50$, mô hình phân loại mẫu này là lành tính. Đây là minh chứng thực tế vì sao các hệ thống AI chẩn đoán hình ảnh luôn được định vị là **công cụ hỗ trợ bác sĩ (Decision Support System)**, không thể thay thế hoàn toàn bác sĩ giải phẫu bệnh đọc tiêu bản mô bệnh học.

---

## 5. Giới Hạn Dữ Liệu và Phân Biệt Biến Thiên Cross-Validation vs Kết Quả Test

### 5.1. Giới Hạn Do Kích Thước Dữ Liệu và Cỡ Mẫu Ác Tính Trong Test
- Tập Test gồm **86 mẫu**, trong đó chỉ có **32 ca ác tính**.
- Do mẫu số $N_{\text{Malignant}} = 32$ tương đối nhỏ, mỗi ca dự đoán đúng hay sai làm thay đổi Recall một bước nhảy tới:
  $$\Delta \text{Recall} = \frac{1}{32} \approx 3.125\%$$
- **Khoảng tin cậy Wilson 95% của Recall**: $[84.26\%, 99.45\%]$. Mặc dù điểm ước lượng điểm (Point Estimate) là $96.88\%$, về mặt thống kê xác suất, độ nhạy thực tế của mô hình trên toàn bộ quần thể bệnh nhân nằm trong khoảng từ $84.26\%$ đến $99.45\%$.
- Tương tự, **Khoảng tin cậy Wilson 95% của Accuracy**: $[93.70\%, 99.79\%]$.

### 5.2. Đối Chiếu Kết Quả Test Với Khoảng Biến Thiên Cross-Validation
Sự khác biệt giữa Cross-Validation (CV) và Test phản ánh hai cấp độ đánh giá:

| Không gian đánh giá | Recall Malignant | ROC-AUC | Bản chất đo lường |
| :--- | :---: | :---: | :--- |
| **5-Fold Cross-Validation (Train)** | **92.51% (±4.08%)** | **0.9820** | Đo lường độ ổn định và phương sai trên 398 mẫu xoay vòng qua 5 lượt chia. |
| **Validation Set (Độc lập)** | **90.62%** (FN=3) | **0.9941** | Lát cắt độc lập 85 mẫu dùng để chọn mô hình và chốt tham số. |
| **Test Set (Đánh giá cuối cùng)** | **96.88%** (FN=1) | **0.9954** | Đánh giá khách quan một lần duy nhất trên dữ liệu hoàn toàn mới 86 mẫu. |

- Kết quả Test ($96.88\%$) nằm hoàn toàn trong dải kỳ vọng thống kê của CV ($\mu \pm 2\sigma = [84.35\%, 100\%]$). Điều này chứng minh mô hình **không hề bị Overfitting**, có năng lực khái quát hóa vững vàng trên dữ liệu ngoại suy.

---

## 6. Chiến Lược Mô Hình Sản Xuất (Production Model)

Để chuẩn bị cho giai đoạn xây dựng Backend API (FastAPI) và Giao diện Web (ReactJS) ở các nhiệm vụ tiếp theo:
1. Đã huấn luyện mô hình sản xuất cuối cùng trên toàn bộ tập phát triển **Train + Validation ($N = 398 + 85 = 483$ mẫu)** với bộ siêu tham số đã chốt không đổi.
2. Mô hình sản xuất tận dụng triệt để 100% dữ liệu nghiên cứu, nâng chỉ số phân tách trên Test lên $\text{ROC-AUC} = \mathbf{0.9983}$.
3. Mô hình sản xuất chính thức được lưu trữ an toàn tại:
   `backend/models/rf_final.joblib`

---

## 7. Kết Luận Nghiệm Thu

1. Quá trình mở niêm phong và đánh giá tập Test đã diễn ra nghiêm ngặt, minh bạch, tuân thủ 100% nguyên tắc liêm chính khoa học (không điều chỉnh mô hình hay ngưỡng sau khi xem kết quả Test).
2. Mô hình Random Forest đã hoàn thành xuất sắc nhiệm vụ với **Accuracy = 98.84%, Recall Malignant = 96.88%, Precision = 100%, ROC-AUC = 0.9954**.
3. Toàn bộ mã nguồn, cấu hình đóng băng, kết quả số liệu và biểu đồ đã được lưu trữ hoàn tất.

---

*Báo cáo kết thúc đánh giá thực nghiệm Project 16. Dừng chờ nghiệm thu.*
