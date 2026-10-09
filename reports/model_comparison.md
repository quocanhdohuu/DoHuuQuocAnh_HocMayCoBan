# Báo Cáo Tổng Hợp và So Sánh Mô Hình Phân Loại Khối U Vú (WDBC)
**Học phần**: Học máy cơ bản (12523W.1) - Đại Học Công Nghệ Kỹ Thuật Hưng Yên  
**Đề tài**: Project 16 - Minh họa phân loại khối u vú bằng cây và rừng  
**Tác giả**: Đỗ Hữu Quốc Anh  
**Thời điểm lập báo cáo**: 08/10/2026  

---

## 1. Mục Tiêu và Nguyên Tắc So Sánh

Báo cáo này tổng hợp và đối chiếu toàn diện hiệu năng của 4 mô hình học máy đã được huấn luyện qua các nhiệm vụ thực nghiệm:
1. **DummyClassifier (Baseline)**: Chiến lược dự đoán lớp đa số (`most_frequent`), làm chuẩn mốc tối thiểu.
2. **Decision Tree Chưa Cắt Tỉa (Unpruned DT)**: Cây quyết định phát triển tự do không giới hạn độ sâu, minh họa hiện tượng ghi nhớ mẫu (Overfitting).
3. **Decision Tree Đã Cắt Tỉa (Pruned DT)**: Cây quyết định được kiểm soát độ phức tạp thông qua Post-pruning (`ccp_alpha = 0.00408`) và Pre-pruning (`max_depth = 8`).
4. **Random Forest (Ensemble Candidate)**: Rừng ngẫu nhiên gồm 100 cây con được tối ưu siêu tham số (`n_estimators = 100`, `max_depth = 8`, `max_features = 0.3`, `min_samples_leaf = 1`).

### Nguyên tắc thực nghiệm cốt lõi:
- **Tính công bằng dữ liệu**: Tất cả mô hình được huấn luyện trên cùng tập **Train ($N = 398$)** và kiểm thử trên cùng tập **Validation ($N = 85$)** theo phân tầng Stratified 70/15/15 (`random_state = 42`).
- **Định nghĩa nhãn nhất quán**: Lớp dương tính (Positive Class, $y = 1$) là **Malignant (Ác tính)**; Lớp âm tính (Negative Class, $y = 0$) là **Benign (Lành tính)**.
- **Tính liêm chính thực nghiệm**: **Tuyệt đối KHÔNG sử dụng tập Test ($N = 86$)** trong quá trình so sánh và lựa chọn ứng viên này. Tập Test tiếp tục được đóng băng cho đến giai đoạn đánh giá độc lập cuối cùng.

---

## 2. Bảng Tổng Hợp Kết Quả Thực Nghiệm Định Lượng

Dưới đây là bảng tổng hợp các chỉ số định lượng được trích xuất trực tiếp từ các tệp nhật ký thực nghiệm: `baseline_results.json`, `unpruned_tree_results.json`, `pruning_search_results.json`, và `random_forest_results.json`.

### 2.1. Bảng Hiệu Năng Chi Tiết (Train vs Validation vs Cross-Validation)

| Mô hình | Không gian đánh giá | Accuracy | Precision (M) | Recall (M) | F1-Score (M) | ROC-AUC | Ma trận nhầm lẫn (Confusion Matrix) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. DummyClassifier** | **Validation (85)** | **62.35%** | **0.00%** | **0.00%** | **0.00%** | **0.5000** | TN=53, FP=0, **FN=32**, TP=0 |
| *(Baseline)* | Train (398) | 62.81% | 0.00% | 0.00% | 0.00% | 0.5000 | TN=250, FP=0, FN=148, TP=0 |
| | 5-Fold CV (Train) | 62.81% | 0.00% | 0.00% | 0.00% | 0.5000 | Zero-division handle: 0.0 |
| **2. Unpruned Tree** | **Validation (85)** | **89.41%** | **89.66%** | **81.25%** | **85.25%** | **0.8779** | TN=50, FP=3, **FN=6**, TP=26 |
| *(max_depth=8, leaves=19)* | Train (398) | 100.00% | 100.00% | 100.00% | 100.00% | 1.0000 | TN=250, FP=0, FN=0, TP=148 |
| | 5-Fold CV (Train) | 92.46% | 90.46% | 89.84% | 89.90% | 0.8800 | Phản ánh Overfitting cục bộ |
| **3. Pruned Tree** | **Validation (85)** | **87.06%** | **92.00%** | **71.88%** | **80.70%** | **0.8499** | TN=51, FP=2, **FN=9**, TP=23 |
| *(ccp_alpha=0.00408, leaves=12)* | Train (398) | 98.74% | 100.00% | 96.62% | 98.28% | 0.9874 | TN=250, FP=0, FN=5, TP=143 |
| | **5-Fold CV (Train)** | **92.96%** | **91.62%** | **89.84%** | **90.50%** | **0.8850** | Giảm 37.8% số nút, tăng CV F1 |
| **4. Random Forest** | **Validation (85)** | **96.47%** | **100.00%** | **90.62%** | **95.08%** | **0.9941** | **TN=53, FP=0, FN=3, TP=29** |
| *(100 cây, max_feat=0.3)* | Train (398) | 100.00% | 100.00% | 100.00% | 100.00% | 1.0000 | TN=250, FP=0, FN=0, TP=148 |
| | **5-Fold CV (Train)** | **94.22%** | **92.69%** | **92.51%** | **92.37%** | **0.9820** | **Đỉnh cao ổn định & tổng quát** |

---

## 3. Biểu Đồ Trực Quan Hóa So Sánh

### 3.1. So Sánh Các Chỉ Số Hiệu Năng Trên Tập Validation
Biểu đồ cột nhóm dưới đây thể hiện sự bứt phá vượt bậc của mô hình tập hợp (Random Forest) so với các cây quyết định đơn lẻ và mô hình cơ sở:

![So Sánh Hiệu Năng Validation](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/model_comparison_metrics.png)

### 3.2. Lưới Ma Trận Nhầm Lẫn (Confusion Matrix Grid)
Ma trận nhầm lẫn làm nổi bật hai sai số sống còn trong y tế: **Số ca bỏ sót bệnh (False Negatives - FN)** và **Số ca chẩn đoán nhầm ác tính (False Positives - FP)**:

![Ma Trận Nhầm Lẫn 4 Mô Hình](file:///c:/Ôn tập/Năm 4/Học máy cơ bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/model_confusion_matrices.png)

### 3.3. Đồ Thị Đánh Đổi Recall vs Precision
Vị trí của 4 mô hình trên không gian Precision - Recall:

![Đánh Đổi Recall vs Precision](file:///c:/Ôn tập/Năm 4/Học máy cơ bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/model_tradeoff_pr.png)

---

## 4. Phân Tích Chuyên Sâu Các Khía Cạnh Kỹ Thuật

### 4.1. Sự Đánh Đổi (Trade-off) Giữa Recall và Precision Trong Bài Toán Ung Thư
Trong bài toán chẩn đoán ung thư vú, mục tiêu tối thượng là **bảo vệ tính mạng bệnh nhân**:
- **False Negative (FN - Bỏ sót ung thư)**: Hậu quả đặc biệt nguy hiểm. Bệnh nhân có khối u ác tính nhưng bị kết luận là lành tính, dẫn đến mất đi "thời gian vàng" điều trị, tế bào ung thư di căn và đe dọa trực tiếp tính mạng. Do đó, **Recall Malignant ($\frac{\text{TP}}{\text{TP} + \text{FN}}$) là chỉ số ưu tiên số 1**.
- **False Positive (FP - Báo động giả)**: Bệnh nhân có u lành tính nhưng bị chẩn đoán nhầm là ác tính. Hậu quả là gây lo lắng tâm lý, tốn kém chi phí làm thêm sinh thiết hoặc phẫu thuật không cần thiết.
- **Sự chuyển dịch qua các mô hình**:
  + *DummyClassifier*: Bỏ sót **32/32 ca (FN = 32)**, hoàn toàn vô dụng.
  + *Pruned Tree*: Do cắt tỉa các nhánh lá cô lập, số ca FP giảm từ 3 xuống 2 (Precision tăng lên 92.0%), nhưng trên tập Val 85 mẫu lại bị tăng 3 ca bỏ sót (FN từ 6 lên 9).
  + *Random Forest*: Đạt trạng thái cân bằng lý tưởng nhất: **FN giảm xuống chỉ còn 3 ca** (Recall đạt 90.62%), đồng thời **FP bằng đúng 0** (Precision đạt 100.00%).

### 4.2. So Sánh Độ Phức Tạp, Khả Năng Giải Thích và Hiện Tượng Overfitting

| Đặc tính so sánh | DummyClassifier | Unpruned Tree | Pruned Tree | Random Forest |
| :--- | :---: | :---: | :---: | :---: |
| **Quy mô cấu trúc** | 0 tham số | 37 nút, 19 lá, độ sâu 8 | 23 nút, 12 lá, độ sâu 6 | 100 cây con, TB 15 lá/cây |
| **Thời gian suy luận (Latency)** | < 0.01 ms | ~ 0.05 ms | **~ 0.03 ms (Cực nhanh)** | ~ 1.5 ms |
| **Tính giải thích (Interpretability)** | Tầm thường | Tốt (Vẽ được cây) | **Xuất sắc (Trực quan, dễ hiểu)** | Hộp đen (Giải thích qua Feature Importance) |
| **Mức độ Overfitting** | Không (Underfitting nặng) | **Nặng (Gap Acc: 10.6%, Gap Rec: 18.8%)** | Kiểm soát tốt trên CV | **Rất thấp (Khoảng cách Train-Val nhỏ nhất)** |
| **Độ ổn định phương sai (Variance)** | Phương sai = 0 | Phương sai cao (High Variance) | Phương sai trung bình | **Phương sai thấp nhất (Low Variance)** |

- **Cây Chưa Cắt (Unpruned Tree)**: Bị Overfitting nghiêm trọng do học thuộc lòng từng điểm ngoại lai của tập Train ($100\%$ hoàn hảo), dẫn đến giảm sút khi gặp dữ liệu mới.
- **Cây Đã Cắt Tỉa (Pruned Tree)**: Thành công trong việc giảm **37.8% số nút** và **36.8% số lá**, giữ lại bộ khung quy tắc chẩn đoán ngắn gọn, có giá trị sư phạm và lâm sàng cực kỳ cao.
- **Rừng Ngẫu Nhiên (Random Forest)**: Nhờ cơ chế lấy mẫu hoàn lại (Bootstrap) và ngẫu nhiên hóa đặc trưng (Random Feature Selection), 100 cây con triệt tiêu phương sai lẫn nhau, mang lại độ phân tách lớp vượt trội (ROC-AUC đạt **0.9941**).

---

## 5. Giải Thích Vì Sao Accuracy Cao Nhất Chưa Chắc Là Lựa Chọn Phù Hợp Nhất

Trong các bài toán phân loại học máy y tế, **Accuracy (Độ chính xác tổng thể)** là chỉ số dễ gây ngộ nhận nhất (The Accuracy Paradox) vì 3 lý do:

1. **Mất cân bằng lớp (Class Imbalance)**:
   - Dữ liệu WDBC có 62.7% ca lành tính (357 ca) và 37.3% ca ác tính (212 ca).
   - Mô hình `DummyClassifier` chỉ cần dự đoán toàn bộ là "Lành tính" đã tự động đạt **Accuracy = 62.35%**. Tuy nhiên, mô hình này không phát hiện được bất kỳ một ca ung thư nào (Recall = 0%). Nếu chỉ nhìn vào con số 62.35% mà kết luận mô hình hoạt động ở mức trung bình khá là hoàn toàn sai lầm.
2. **Chi phí bất đối xứng của sai lầm (Asymmetric Misclassification Costs)**:
   - Trong chẩn đoán y khoa, cái giá của một ca **False Negative** (bệnh nhân ung thư bị bỏ sót tử vong) đắt hơn gấp hàng chục đến hàng trăm lần so với một ca **False Positive** (bệnh nhân lành tính làm thêm xét nghiệm sinh thiết kiểm tra lại).
   - Accuracy đối xử với lỗi FN và FP hoàn toàn bình đẳng ($1 \text{ lỗi FN} = 1 \text{ lỗi FP}$). Một mô hình có Accuracy 95% nhưng toàn bộ 5% lỗi sai rơi vào lớp Ác tính sẽ nguy hiểm hơn rất nhiều so với một mô hình có Accuracy 92% nhưng bắt trúng 100% ca ác tính.
3. **Độ tin cậy của xác suất (Probability Calibration)**:
   - Accuracy chỉ tính trên nhãn cứng sau khi áp ngưỡng 0.5. Nó không phản ánh được mức độ tự tin của mô hình. Ngược lại, **ROC-AUC** và **F1-Score** cho cái nhìn toàn diện về chất lượng phân tách và sự cân đối giữa độ nhạy và độ chính xác thực tế.

---

## 6. Đề Xuất Mô Hình Tốt Nhất Dựa Trên Kết Quả Thực Nghiệm

Dựa trên kết quả tổng hợp thực nghiệm khách quan trên cả 5-Fold Cross-Validation và tập Validation độc lập:

1. **Mô hình có hiệu năng dự đoán tốt nhất**: **Random Forest**
   - Đạt **ROC-AUC = 0.9941** và **F1-Score = 0.9508** trên Validation.
   - Giảm số ca bỏ sót nguy hiểm xuống mức thấp nhất (**chỉ còn 3 ca FN** trên tập Validation), đồng thời **không mắc bất kỳ lỗi báo động giả nào (FP = 0)**.
   - Thể hiện tính ổn định cao nhất trên Cross-Validation (Mean CV Recall = 92.51%, Mean CV ROC-AUC = 98.20%).
2. **Mô hình có tính giải thích và minh họa tốt nhất**: **Pruned Decision Tree**
   - Đạt cấu trúc tinh gọn (độ sâu 6, 12 lá), phù hợp để bác sĩ theo dõi từng nhánh quyết định logic dạng if-else.
3. **Trạng thái phê duyệt**:
   - Theo đúng nguyên tắc của dự án học phần, kết quả này **chỉ ghi nhận Random Forest là mô hình ứng viên sáng giá nhất (Candidate Model)**.
   - **Chưa tự ý chốt mô hình cuối cùng để triển khai Web hay đánh giá trên Test** tại bước này. Quyết định chính thức sẽ được đưa ra sau khi thực hiện đầy đủ các thí nghiệm so sánh chuyên sâu (Thí nghiệm 2, 3, 4) và được người dùng phê duyệt nghiệm thu.

---

*Báo cáo được tạo tự động bởi quy trình thực nghiệm Project 16. Dữ liệu Test ($N = 86$) vẫn được bảo lưu độc lập nguyên vẹn.*
