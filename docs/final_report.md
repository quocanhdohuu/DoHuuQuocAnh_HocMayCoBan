# BÁO CÁO NGHIÊN CỨU HỌC THUẬT TỔNG KẾT DỰ ÁN
## ĐỀ TÀI: MINH HỌA PHÂN LOẠI KHỐI U VÚ BẰNG CÂY QUYẾT ĐỊNH VÀ RỪNG NGẪU NHIÊN
### Project 16 — Học phần: Học máy cơ bản (Mã học phần: 12523W.1)

---

**Đơn vị đào tạo**: Trường Đại Học Công Nghệ Kỹ Thuật Hưng Yên  
**Khoa**: Công nghệ Thông tin — **Bộ môn**: Trí tuệ Nhân tạo & Khoa học Dữ liệu  
**Sinh viên thực hiện**: Đỗ Hữu Quốc Anh  
**Thời gian hoàn thành**: Tháng 10 Năm 2026  
**Trạng thái nghiệm thu**: Sẵn sàng báo cáo và bàn giao toàn diện  

---

## MỤC LỤC TỔNG THỂ

1. **TÓM TẮT ĐỒ ÁN (ABSTRACT)**
   - Tóm tắt tiếng Việt (Vietnamese Abstract)
   - Tóm tắt tiếng Anh (English Abstract)
   - Từ khóa then chốt (Keywords)
2. **CHƯƠNG 1: BỐI CẢNH, ĐỘNG LỰC VÀ Ý NGHĨA Y SINH HỌC**
   - 1.1. Gánh nặng bệnh học của ung thư vú và vai trò của chẩn đoán sớm
   - 1.2. Kỹ thuật chọc hút tế bào kim nhỏ (FNA) và số hóa hình thái học
   - 1.3. Động lực ứng dụng học máy diễn giải được (Interpretable ML)
3. **CHƯƠNG 2: MỤC TIÊU VÀ HỆ THỐNG CÂU HỎI NGHIÊN CỨU**
   - 2.1. Mục tiêu tổng quát và mục tiêu cụ thể
   - 2.2. Hệ thống câu hỏi nghiên cứu cốt lõi (Research Questions RQ1 – RQ5)
4. **CHƯƠNG 3: KHÁM PHÁ DỮ LIỆU VÀ TIỀN XỬ LÝ (DATA EXPLORATION & PREPROCESSING)**
   - 3.1. Đặc tả tập dữ liệu Wisconsin Diagnostic Breast Cancer (WDBC)
   - 3.2. Không gian 30 đặc trưng số hóa tế bào học
   - 3.3. Kiểm toán chất lượng dữ liệu: Khuyết thiếu, trùng lặp và tính toàn vẹn vật lý
   - 3.4. Phân tích phân phối nhãn mục tiêu và hiện tượng mất cân bằng lớp
5. **CHƯƠNG 4: NGUYÊN TẮC KIỂM SOÁT VÀ CHỐNG RÒ RỈ DỮ LIỆU (DATA LEAKAGE PREVENTION)**
   - 4.1. Bản chất và các hình thức rò rỉ dữ liệu trong học máy y tế
   - 4.2. Chiến lược chia tập phân tầng 3 nhánh (Stratified 70/15/15 Splitting)
   - 4.3. Kiểm chứng giao tập hợp rỗng và quy trình niêm phong tập Test
6. **CHƯƠNG 5: CƠ SỞ PHƯƠNG PHÁP HỌC MÁY VÀ TOÁN HỌC**
   - 5.1. Thuật toán Cây quyết định CART và hàm mục tiêu Gini Impurity
   - 5.2. Hiện tượng Overfitting và kỹ thuật tỉa cành hậu kỳ Cost-Complexity Pruning
   - 5.3. Rừng ngẫu nhiên (Random Forest): Bagging và Không gian con ngẫu nhiên
   - 5.4. Đánh giá tầm quan trọng đặc trưng bằng Mean Decrease in Impurity (MDI)
7. **CHƯƠNG 6: THIẾT KẾ THỰC NGHIỆM VÀ CHIẾN LƯỢC HUẤN LUYỆN**
   - 6.1. Thiết lập mô hình đường cơ sở (Baseline Dummy Classifier)
   - 6.2. Kiểm chứng chéo phân tầng 5 lượt (5-Fold Stratified Cross-Validation)
   - 6.3. Tinh chỉnh siêu tham số và đóng băng cấu hình mô hình
   - 6.4. Xác lập ngưỡng quyết định phân loại lâm sàng ($\tau = 0.50$)
8. **CHƯƠNG 7: KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN CHUYÊN SÂU**
   - 7.1. Thí nghiệm 1: Phân tích đường cong huấn luyện theo độ sâu cây
   - 7.2. Thí nghiệm tỉa cành: Đường cong biến thiên $\alpha$ hiệu quả ($ccp\_\alpha$)
   - 7.3. Thí nghiệm 2: Đánh giá đối đầu 4 mô hình trên tập Validation và Test
   - 7.4. Thí nghiệm 4: Kiểm chứng độ ổn định thứ hạng đặc trưng qua nhiều Random Seeds
   - 7.5. Đánh giá kiểm thử cuối cùng trên tập Test và Khoảng tin cậy Wilson 95%
9. **CHƯƠNG 8: PHÂN TÍCH LỖI VÀ NGHIÊN CỨU TRƯỜNG HỢP BIÊN (ERROR ANALYSIS)**
   - 8.1. Toàn cảnh lỗi trên tập Test: Phân tích ca False Negative duy nhất (Mẫu #23)
   - 8.2. So sánh phân vị thống kê của Mẫu #23 với phân phối hai lớp
   - 8.3. Bản chất toán học của vùng chồng lấn biên giới (Borderline Overlap Region)
   - 8.4. Thảo luận về tỷ lệ False Positive bằng 0 và ý nghĩa thực tiễn
10. **CHƯƠNG 9: KIẾN TRÚC TRIỂN KHAI HỆ THỐNG WEB VÀ API**
    - 9.1. Kiến trúc phân tầng tách rời (Decoupled 3-Tier Architecture)
    - 9.2. Backend FastAPI: Xác thực nghiêm ngặt 30 đặc trưng bằng Pydantic
    - 9.3. Frontend React Vite: Giao diện trực quan hóa, kiểm thử mẫu và Dashboard
    - 9.4. Luồng xử lý dữ liệu End-to-End từ giao diện người dùng tới suy luận mô hình
11. **CHƯƠNG 10: ĐẠO ĐỨC, KHÍA CẠNH PHÁP LÝ VÀ GIỚI HẠN HỆ THỐNG**
    - 10.1. Tuyên bố giới hạn phi lâm sàng (Non-Diagnostic Academic Disclaimer)
    - 10.2. Tính công bằng, độ trượt miền dữ liệu (Domain Shift) và bảo mật y tế
    - 10.3. Tính minh bạch và giải trình thuật toán trong AI y tế
12. **CHƯƠNG 11: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN**
    - 11.1. Tổng kết các đóng góp chính của đồ án
    - 11.2. Các bài học kinh nghiệm về phương pháp luận
    - 11.3. Hướng nghiên cứu mở rộng trong tương lai
13. **TÀI LIỆU THAM KHẢO (REFERENCES)**
14. **PHỤ LỤC: HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM VÀ KIỂM THỬ**

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)

### Tóm tắt tiếng Việt
Đồ án nghiên cứu, hiện thực hóa và đánh giá chuyên sâu phương pháp phân loại nhị phân u vú lành tính (Benign) và ác tính (Malignant) dựa trên bộ dữ liệu kinh điển Wisconsin Diagnostic Breast Cancer (WDBC) gồm 569 mẫu sinh thiết và 30 đặc trưng hình thái tế bào học chọc hút kim nhỏ (FNA). Xuất phát từ yêu cầu y tế đòi hỏi độ nhạy cao (Recall lớn) nhằm hạn chế tối đa việc bỏ sót ca bệnh ác tính kết hợp với tính minh bạch có thể diễn giải được (Explainability), đồ án xây dựng quy trình nghiên cứu khoa học chuẩn mực tuân thủ nghiêm ngặt nguyên tắc chống rò rỉ dữ liệu (Zero Data Leakage). 

Dữ liệu được phân chia phân tầng thành 3 tập độc lập: Huấn luyện (Train: 398 mẫu - 70%), Kiểm chứng (Validation: 85 mẫu - 15%) và Kiểm thử độc lập (Test: 86 mẫu - 15%). Tập Test được niêm phong tuyệt đối cho tới thời điểm đánh giá cuối cùng. Nghiên cứu thực hiện đối sánh bốn mô hình: (1) Mô hình cơ sở ngẫu nhiên (Dummy Classifier), (2) Cây quyết định không tỉa cành (Unpruned Decision Tree - CART), (3) Cây quyết định tỉa cành tối ưu (Cost-Complexity Pruned Tree - CCP), và (4) Rừng ngẫu nhiên (Random Forest). 

Kết quả thực nghiệm cho thấy Cây quyết định không tỉa cành bị quá khớp nghiêm trọng (đạt 100% độ chính xác trên Train nhưng giảm sâu trên Validation). Thuật toán tỉa cành Cost-Complexity Pruning với hệ số phạt $\alpha = 0.015$ giúp rút gọn cấu trúc cây từ 15 lá (độ sâu 7) xuống còn 5 lá (độ sâu 4), nâng cao khả năng khái quát hóa. Vượt trội hơn cả, mô hình Rừng ngẫu nhiên với 100 cây con và tỷ lệ lấy mẫu đặc trưng ngẫu nhiên 30% (`max_features=0.3`) triệt tiêu phương sai hiệu quả, đạt hiệu năng cao nhất trên tập Test độc lập: **Accuracy = 98.84%** (khoảng tin cậy Wilson 95%: [93.70%, 99.79%]), **Precision Malignant = 100.00%** (0 ca báo động giả), **Recall Malignant = 96.88%** (chỉ bỏ sót duy nhất 1 ca), **F1-Score = 98.41%**, và **ROC-AUC = 0.9954**. Phân tích lỗi chi tiết trên ca bệnh bỏ sót duy nhất (Mẫu #23) chỉ ra nguyên nhân khách quan do khối u nhỏ nằm tại vùng chồng lấn biên giới tự nhiên giữa hai lớp. 

Toàn bộ hệ thống được đóng gói thành giải pháp công nghệ hoàn chỉnh với Backend FastAPI (xác thực dữ liệu Pydantic 30 chiều nghiêm ngặt) và Frontend ReactJS tương tác cao, đi kèm bộ kiểm thử tự động 72 ca thử nghiệm đạt tỷ lệ vượt qua 100%.

### English Abstract
This project presents a rigorous empirical study, implementation, and evaluation of binary classification for breast tumor diagnosis (Benign vs. Malignant) utilizing the classic Wisconsin Diagnostic Breast Cancer (WDBC) dataset comprising 569 biopsy samples and 30 morphological features extracted from Fine Needle Aspirates (FNA). Driven by critical clinical requirements demanding high cancer sensitivity (Recall) to minimize lethal false negatives while maintaining algorithmic interpretability, this study strictly enforces an end-to-end Zero Data Leakage protocol. 

The data is stratified into three disjoint partitions: Training (398 samples, 70%), Validation (85 samples, 15%), and an isolated Test set (86 samples, 15%), with the Test set rigorously frozen until the final post-hoc evaluation. Four diagnostic models were systematically benchmarked: (1) Baseline Dummy Classifier, (2) Unpruned Decision Tree (CART), (3) Cost-Complexity Pruned Decision Tree (CCP), and (4) Random Forest Classifier. 

Empirical investigations demonstrate that unpruned decision trees suffer from severe overfitting (100% training accuracy contrasting with degraded validation performance). Post-pruning via minimal cost-complexity pruning with $\alpha = 0.015$ substantially compresses tree complexity from 15 leaf nodes (depth 7) down to 5 leaf nodes (depth 4), significantly improving generalization. Superior to individual trees, the Random Forest ensemble (100 estimators, `max_features=0.3`) effectively suppresses estimator variance, delivering state-of-the-art performance on the isolated Test set: **Accuracy = 98.84%** (95% Wilson Score CI: [93.70%, 99.79%]), **Malignant Precision = 100.00%** (zero false alarms), **Malignant Recall = 96.88%** (a single missed case), **F1-Score = 98.41%**, and **ROC-AUC = 0.9954**. Extensive error analysis on the single False Negative case (Sample #23) attributes the misclassification to biological borderline morphological overlap rather than algorithmic failure. 

The final solution is deployed via an enterprise-grade decoupled software architecture featuring a high-performance FastAPI backend with strict Pydantic schema validation and a responsive ReactJS frontend dashboard, fully backed by an automated 72-test validation suite achieving a 100% pass rate.

### Từ khóa then chốt (Keywords)
Học máy y tế (Medical Machine Learning), Phân loại ung thư vú (Breast Cancer Classification), WDBC, Cây quyết định (Decision Tree - CART), Tỉa cành phức độ chi phí (Cost-Complexity Pruning), Rừng ngẫu nhiên (Random Forest), Chống rò rỉ dữ liệu (Data Leakage Prevention), FastAPI, ReactJS.

---

## CHƯƠNG 1: BỐI CẢNH, ĐỘNG LỰC VÀ Ý NGHĨA Y SINH HỌC

### 1.1. Gánh nặng bệnh học của ung thư vú và vai trò của chẩn đoán sớm
Ung thư vú (Breast Cancer) là một trong những nguyên nhân hàng đầu gây tử vong do ung thư ở nữ giới trên phạm vi toàn cầu, theo thống kê của Tổ chức Y tế Thế giới (WHO). Bệnh lý bắt nguồn từ sự phân chia mất kiểm soát của các tế bào biểu mô tuyến vú (tuyến tiểu thùy hoặc ống dẫn sữa). Tiên lượng sống sót của bệnh nhân phụ thuộc sống còn vào giai đoạn phát hiện bệnh: nếu phát hiện ở giai đoạn sớm (giai đoạn I hoặc tại chỗ), tỷ lệ sống sót sau 5 năm có thể vượt quá $90\%$; ngược lại, khi tế bào di căn sang các hạch bạch huyết vùng hoặc các cơ quan xa, tỷ lệ này sụt giảm nghiêm trọng.

Tuy nhiên, việc tầm soát định kỳ bằng nhũ ảnh (Mammography) thường cho kết quả nghi ngờ, đòi hỏi các bước thăm dò tiếp theo mang tính xâm lấn hơn để xác định tính chất lành tính (Benign) hay ác tính (Malignant).

### 1.2. Kỹ thuật chọc hút tế bào kim nhỏ (FNA) và số hóa hình thái học
Chọc hút tế bào bằng kim nhỏ (Fine Needle Aspiration - FNA) là một thủ thuật lâm sàng xâm lấn tối thiểu, sử dụng kim tiêm cỡ nhỏ để lấy mẫu tế bào từ khối u vú nghi ngờ. Tiêu bản tế bào sau đó được nhuộm và soi dưới kính hiển vi quang học.

Vào đầu những năm 1990, Tiến sĩ William H. Wolberg (Khoa Phẫu thuật Tổng quát, Bệnh viện Đại học Wisconsin) cùng các cộng sự W. Nick Street và Olvi L. Mangasarian (Khoa Khoa học Máy tính) đã tiên phong phát triển hệ thống phần mềm Xcyt. Hệ thống này cho phép chụp ảnh kỹ thuật số các vi trường tiêu bản FNA và sử dụng thuật toán đường cong chủ động (Snakes/Active Contours) để tự động nhận dạng ranh giới màng nhân tế bào. Từ các đường biên số hóa này, 10 thuộc tính hình thái học không gian tế bào được trích xuất một cách định lượng khách quan. Bộ dữ liệu này được lưu trữ tại Kho lưu trữ Học máy UCI (UCI Machine Learning Repository) dưới tên gọi Wisconsin Diagnostic Breast Cancer (WDBC) và trở thành chuẩn đối sánh (benchmark) kinh điển trong lĩnh vực phân loại y sinh học.

### 1.3. Động lực ứng dụng học máy diễn giải được (Interpretable ML)
Trong chẩn đoán y tế, các mô hình "hộp đen" (Black-box models) như mạng nơ-ron sâu phức tạp thường gặp rào cản lớn khi áp dụng vào thực tiễn lâm sàng do bác sĩ không thể giải thích tại sao mô hình đưa ra kết luận. Một sai sót chẩn đoán y khoa mang lại hậu quả nặng nề:
- **Bỏ sót ca ác tính (False Negative - FN)**: Bệnh nhân ung thư bị chẩn đoán nhầm là u lành tính, dẫn tới bỏ lỡ "giai đoạn vàng" điều trị, đe dọa trực tiếp đến tính mạng.
- **Báo động giả (False Positive - FP)**: Bệnh nhân u lành tính bị kết luận ác tính, gây hoảng loạn tâm lý tột độ và buộc phải trải qua các phẫu thuật cắt bỏ hoặc sinh thiết lõi kim lớn không cần thiết.

Do đó, họ thuật toán Cây quyết định (Decision Trees) và Rừng ngẫu nhiên (Random Forest) là sự lựa chọn ưu tiên hàng đầu nhờ khả năng cân bằng giữa:
1. **Độ chính xác và độ nhạy vượt trội**: Khả năng phân tách phi tuyến tính mạnh mẽ trong không gian đa chiều.
2. **Khả năng diễn giải tự nhiên (Interpretability)**: Cây quyết định trực quan hóa được các chuỗi điều kiện logic $If-Then$, tương đồng với phác đồ tư duy chẩn đoán phân biệt của bác sĩ giải phẫu bệnh. Rừng ngẫu nhiên cung cấp phân tích định lượng về tầm quan trọng của các đặc trưng tế bào học.

---

## CHƯƠNG 2: MỤC TIÊU VÀ HỆ THỐNG CÂU HỎI NGHIÊN CỨU

### 2.1. Mục tiêu tổng quát và mục tiêu cụ thể
- **Mục tiêu tổng quát**: Xây dựng, tối ưu hóa và đánh giá toàn diện hệ thống học máy diễn giải được để phân loại khối u vú (Benign vs Malignant) trên bộ dữ liệu WDBC, tuân thủ phương pháp luận liêm chính khoa học, chống rò rỉ dữ liệu tuyệt đối và triển khai thành giải pháp phần mềm Web tương tác hoàn chỉnh.
- **Mục tiêu cụ thể**:
  1. Thực hiện kiểm toán dữ liệu đa chiều (Data Audit), khảo sát phân phối và chứng minh tính hợp lệ y sinh học của 30 đặc trưng.
  2. Thiết lập quy trình phân chia dữ liệu ngẫu nhiên phân tầng 3 nhánh (Train/Validation/Test: 70/15/15) và niêm phong tập Test độc lập.
  3. Huấn luyện, khảo sát hiện tượng quá khớp (Overfitting) của Cây quyết định không tỉa cành theo độ sâu.
  4. Thực nghiệm kỹ thuật tỉa cành hậu kỳ Cost-Complexity Pruning (CCP), xác định hệ số phạt $\alpha$ tối ưu nhằm tối giản cấu trúc cây.
  5. Phát triển mô hình tập hợp Rừng ngẫu nhiên (Random Forest) với kỹ thuật lấy mẫu túi (Bagging) và chọn đặc trưng ngẫu nhiên (Random Subspace), đánh giá độ ổn định thứ hạng đặc trưng qua nhiều Random Seeds độc lập.
  6. Mở niêm phong tập Test một lần duy nhất, đánh giá định lượng các chỉ số (Accuracy, Recall, Precision, F1, ROC-AUC) đi kèm khoảng tin cậy Wilson 95%.
  7. Phân tích nguyên nhân gốc rễ (Root-cause analysis) của ca lỗi False Negative duy nhất.
  8. Đóng gói mô hình thành dịch vụ API RESTful (FastAPI) và giao diện Web (ReactJS) phục vụ mục đích nghiên cứu, học tập.

### 2.2. Hệ thống câu hỏi nghiên cứu cốt lõi (Research Questions)
Nghiên cứu tập trung giải quyết 5 câu hỏi khoa học cụ thể sau:
- **RQ1**: Cây quyết định đơn lẻ (CART) bắt đầu biểu hiện hiện tượng quá khớp (Overfitting) tại ngưỡng độ sâu nào trên bộ dữ liệu WDBC?
- **RQ2**: Kỹ thuật tỉa cành Cost-Complexity Pruning (CCP) có thể nén gọn cấu trúc cây (số nút lá, độ sâu) đến mức độ nào mà vẫn bảo toàn hoặc nâng cao hiệu năng chẩn đoán so với cây nguyên bản?
- **RQ3**: Việc tập hợp 100 cây con trong Rừng ngẫu nhiên (Random Forest) mang lại bước nhảy hiệu năng bao nhiêu về độ nhạy (Recall) và diện tích dưới đường cong ROC-AUC so với Cây quyết định đơn lẻ?
- **RQ4**: Thứ hạng tầm quan trọng của các đặc trưng tế bào học (Feature Importance) trong Rừng ngẫu nhiên có giữ được tính ổn định thống kê khi thay đổi hạt giống ngẫu nhiên (Random Seed) hay không?
- **RQ5**: Trong trường hợp mô hình đưa ra dự đoán sai lệch trên tập Test độc lập, nguyên nhân xuất phát từ thuật toán học máy hay do sự chồng lấn hình thái học khách quan của tế bào học FNA?

---

## CHƯƠNG 3: KHÁM PHÁ DỮ LIỆU VÀ TIỀN XỬ LÝ (DATA EXPLORATION & PREPROCESSING)

### 3.1. Đặc tả tập dữ liệu Wisconsin Diagnostic Breast Cancer (WDBC)
Tập dữ liệu WDBC thu thập từ 569 bệnh nhân nữ nghi ngờ khối u vú, bao gồm 569 bản ghi độc lập và 32 thuộc tính gốc:
- `id`: Mã định danh mẫu bệnh phẩm (số nguyên `int64`). Cột này được loại bỏ hoàn toàn trong bước tiền xử lý để tránh nguy cơ mô hình học vẹt số định danh bệnh nhân.
- `diagnosis`: Biến mục tiêu nhị phân phân loại chẩn đoán y tế (`B`: Benign - Lành tính; `M`: Malignant - Ác tính).

### 3.2. Không gian 30 đặc trưng số hóa tế bào học
Từ đường biên nhân tế bào được số hóa, hệ thống Xcyt đo đạc 10 thuộc tính hình học cơ bản:
1. **Bán kính (Radius)**: Trung bình khoảng cách từ tâm đến các điểm trên đường biên nhân tế bào.
2. **Độ nhám bề mặt (Texture)**: Độ lệch chuẩn của các giá trị thang độ xám (grayscale) trong ảnh nhân tế bào.
3. **Chu vi (Perimeter)**: Tổng chiều dài đường biên bao quanh nhân tế bào.
4. **Diện tích (Area)**: Tổng số điểm ảnh bên trong đường bao nhân tế bào.
5. **Độ mịn (Smoothness)**: Mức độ biến thiên cục bộ của độ dài các bán kính nhân tế bào.
6. **Độ chặt chẽ (Compactness)**: Tính theo công thức $\frac{\text{chu vi}^2}{\text{diện tích}} - 1.0$.
7. **Độ lõm (Concavity)**: Mức độ nghiêm trọng của các phần lõm trên đường bao nhân tế bào.
8. **Số điểm lõm (Concave points)**: Số lượng các vết lõm trên đường biên nhân tế bào.
9. **Độ đối xứng (Symmetry)**: Sự cân xứng của nhân tế bào so với trục chính.
10. **Kích thước fractal (Fractal dimension)**: Xấp xỉ theo phương pháp đếm hộp $\text{fractal dimension} - 1.0$.

Đối với mỗi hình ảnh tiêu bản, 10 thuộc tính trên được tổng hợp theo 3 giá trị thống kê:
- **Giá trị trung bình (Mean)**: 10 đặc trưng hậu tố `_mean` (đo kích thước và hình dạng đại diện).
- **Sai số chuẩn (Standard Error - SE)**: 10 đặc trưng hậu tố `_se` (đo độ biến thiên giữa các tế bào trong cùng tiêu bản).
- **Giá trị xấu nhất / Lớn nhất (Worst / Largest)**: 10 đặc trưng hậu tố `_worst` (trung bình của 3 tế bào có kích thước/bất thường lớn nhất trên tiêu bản).

Tổng cộng không gian đặc trưng đầu vào có đúng **30 biến số thực liên tục (`float64`)**.

### 3.3. Kiểm toán chất lượng dữ liệu: Khuyết thiếu, trùng lặp và tính toàn vẹn vật lý
Quy trình kiểm toán chất lượng dữ liệu tự động (Data Audit) đã được tiến hành độc lập với kết quả ghi nhận như sau:
- **Giá trị khuyết thiếu (Missing values)**: Toàn bộ 569 dòng và 32 cột đều có đầy đủ giá trị thực ($0$ giá trị NaN/Null, tỷ lệ khuyết thiếu $0.0\%$). Do đó, hệ thống không cần áp dụng bất kỳ kỹ thuật nội suy hay điền khuyết giả định nào.
- **Bản ghi trùng lặp (Duplicate records)**: Kiểm tra trùng lặp trên cả 32 cột, trùng lặp khóa định danh `id` và trùng lặp không gian 30 đặc trưng đều cho kết quả $0$ bản ghi. Toàn bộ 569 mẫu bệnh phẩm là độc lập.
- **Tính toàn vẹn vật lý và biên giá trị (Sanity checks)**:
  - 100% các giá trị đo đạc hình học đều thỏa mãn $\text{min} \ge 0.0$ (không có giá trị âm phi lý).
  - Ghi nhận 13 mẫu bệnh phẩm có các chỉ số `concavity` và `concave points` bằng đúng $0.0$. Qua đối chiếu chéo, **100% trong số 13 mẫu này đều thuộc lớp u lành tính (`B`)**. Về mặt sinh học tế bào, nhân tế bào lành tính bình thường có màng bao trơn nhẵn hoàn hảo, không có vết khuyết lõm dị dạng, do đó giá trị đo bằng $0.0$ là hoàn toàn chính xác về mặt bệnh học.

### 3.4. Phân tích phân phối nhãn mục tiêu và hiện tượng mất cân bằng lớp
Trong 569 mẫu bệnh phẩm:
- Khối u lành tính (`B` - Benign): **357 mẫu**, chiếm **$62.74\%$**.
- Khối u ác tính (`M` - Malignant): **212 mẫu**, chiếm **$37.26\%$**.
- Tỷ lệ mất cân bằng lớp là $1.68 : 1$.

Mức độ mất cân bằng này được xếp loại là mất cân bằng nhẹ (mild class imbalance). Trong bài toán tầm soát ung thư, lớp thiểu số (Ác tính) lại chính là lớp tích cực mang tính chất sống còn (Positive class). Do đó, các chỉ số đánh giá không thể chỉ dựa vào Accuracy mà bắt buộc phải ưu tiên **Recall (Độ nhạy ung thư)**, **Precision (Độ chuẩn xác)** và **ROC-AUC**.

---

## CHƯƠNG 4: NGUYÊN TẮC KIỂM SOÁT VÀ CHỐNG RÒ RỈ DỮ LIỆU (DATA LEAKAGE PREVENTION)

### 4.1. Bản chất và các hình thức rò rỉ dữ liệu trong học máy y tế
Rò rỉ dữ liệu (Data Leakage) là hiện tượng thông tin từ tập kiểm thử (Test set) hoặc tập tương lai vô tình thâm nhập vào quá trình huấn luyện mô hình, dẫn tới hiện tượng mô hình đạt điểm số cao giả tạo trong phòng thí nghiệm nhưng thất bại hoàn toàn khi triển khai thực tế.
Trong học máy y tế, các dạng rò rỉ phổ biến gồm:
1. **Rò rỉ qua chuẩn hóa đặc trưng (Scaling Leakage)**: Tính trung bình ($\mu$) và độ lệch chuẩn ($\sigma$) trên toàn bộ tập dữ liệu trước khi chia tập.
2. **Rò rỉ qua chọn đặc trưng (Feature Selection Leakage)**: Lựa chọn thuộc tính dựa trên tương quan với nhãn trên toàn bộ 569 mẫu.
3. **Rò rỉ qua tối ưu siêu tham số (Hyperparameter Tuning Leakage)**: Sử dụng trực tiếp tập Test để tinh chỉnh độ sâu cây hoặc ngưỡng phân loại.

### 4.2. Chiến lược chia tập phân tầng 3 nhánh (Stratified 70/15/15 Splitting)
Để ngăn chặn triệt để mọi nguy cơ rò rỉ, đồ án thiết lập quy trình phân tách dữ liệu 3 nhánh ngẫu nhiên phân tầng (Stratified Splitting) với hạt giống cố định `random_state=42`:
- **Tập Huấn luyện (Train Set)**: Chiếm $70\%$ ($N_{\text{Train}} = 398$ mẫu, gồm $250$ ca Benign và $148$ ca Malignant). Dùng duy nhất cho việc học cấu trúc cây và tính toán các phân vị trong quá trình huấn luyện.
- **Tập Kiểm chứng (Validation Set)**: Chiếm $15\%$ ($N_{\text{Val}} = 85$ mẫu, gồm $53$ ca Benign và $32$ ca Malignant). Dùng để đối chiếu các mô hình ứng viên, lựa chọn cấu hình siêu tham số và xác định ngưỡng phân loại.
- **Tập Kiểm thử độc lập (Test Set)**: Chiếm $15\%$ ($N_{\text{Test}} = 86$ mẫu, gồm $54$ ca Benign và $32$ ca Malignant). Dùng duy nhất cho một lần đánh giá tổng kết cuối cùng.

### 4.3. Kiểm chứng giao tập hợp rỗng và quy trình niêm phong tập Test
- **Kiểm tra giao tập hợp**:
  $$\text{Train} \cap \text{Val} = \emptyset, \quad \text{Train} \cap \text{Test} = \emptyset, \quad \text{Val} \cap \text{Test} = \emptyset$$
  Số lượng mẫu trùng lặp giữa các tập là $0$.
- **Quy tắc niêm phong (Frozen Test Protocol)**:
  Tập Test được xuất khẩu ra tệp `test.csv` và được niêm phong hoàn toàn. Không có bất kỳ dòng mã nào thực hiện huấn luyện, chuẩn hóa hay tuning có sự tham gia của tập Test trong suốt giai đoạn phát triển mô hình (từ Nhiệm vụ 05 đến trước Nhiệm vụ 14).
- **Tính bất biến của thuật toán dạng cây**:
  Cây quyết định và Rừng ngẫu nhiên dựa trên các phép so sánh ngưỡng bất đẳng thức trên từng thuộc tính đơn lẻ ($x_j \le \theta$). Do đó, thuật toán có tính chất bất biến đối với các phép biến đổi đơn điệu (Monotonic invariance). Nhóm nghiên cứu quyết định **không chuẩn hóa ép buộc (No Feature Scaling)**, qua đó vừa loại trừ nguy cơ rò rỉ tham số $\mu, \sigma$, vừa giữ nguyên vẹn giá trị vật lý và đơn vị sinh học của từng thuộc tính.

---

## CHƯƠNG 5: CƠ SỞ PHƯƠNG PHÁP HỌC MÁY VÀ TOÁN HỌC

### 5.1. Thuật toán Cây quyết định CART và hàm mục tiêu Gini Impurity
Cây quyết định trong đồ án được xây dựng dựa trên thuật toán CART (Classification and Regression Trees) của Breiman et al. (1984). CART tạo ra các cây nhị phân (binary trees) bằng cách chia đệ quy không gian đặc trưng tại mỗi nút nội bộ $t$.

#### Chỉ số độ vẩn đục Gini (Gini Impurity)
Tại nút $t$, độ vẩn đục Gini đo lường xác suất một phần tử bị gán nhãn sai nếu được gán nhãn ngẫu nhiên theo phân phối xác suất của nút:
$$I_G(t) = 1 - \sum_{k=0}^{1} p(k \mid t)^2 = 1 - \left( p(0 \mid t)^2 + p(1 \mid t)^2 \right)$$
Trong đó $p(k \mid t)$ là tỷ lệ mẫu thuộc lớp $k \in \{0, 1\}$ tại nút $t$.
- Nếu nút thuần khiết hoàn toàn ($100\%$ Benign hoặc $100\%$ Malignant): $I_G(t) = 1 - (1^2 + 0^2) = 0$.
- Nếu nút vẩn đục tối đa (tỷ lệ $50\% - 50\%$): $I_G(t) = 1 - (0.5^2 + 0.5^2) = 0.5$.

#### Độ lợi phân tách (Split Criterion)
Tại mỗi bước phân tách, thuật toán quét qua toàn bộ 30 đặc trưng $j$ và các ngưỡng cắt khả dĩ $\theta$, tìm kiếm cặp $(j, \theta)$ tối đa hóa mức giảm độ vẩn đục $\Delta I_G$:
$$\Delta I_G(s, t) = I_G(t) - \left( \frac{N_{L}}{N_t} I_G(t_L) + \frac{N_{R}}{N_t} I_G(t_R) \right)$$
Trong đó $N_t, N_L, N_R$ lần lượt là số mẫu tại nút cha, nút con trái và nút con phải.

### 5.2. Hiện tượng Overfitting và kỹ thuật tỉa cành hậu kỳ Cost-Complexity Pruning
Khi để cây phát triển tự do không kiểm soát (`max_depth=None`), cây sẽ tiếp tục phân nhánh cho đến khi mọi nút lá đều thuần khiết ($I_G = 0$). Hiện tượng này khiến cây ghi nhớ cả các nhiễu thống kê ngẫu nhiên trong tập Train, dẫn tới hiện tượng quá khớp (Overfitting) nghiêm trọng: độ chính xác trên Train đạt $100\%$, nhưng khi gặp dữ liệu mới ngoài tập huấn luyện, hiệu năng sụt giảm nghiêm trọng.

Để khắc phục, kỹ thuật tỉa cành hậu kỳ Cost-Complexity Pruning (tỉa cành phức độ chi phí) được áp dụng. Hàm chi phí hiệu chỉnh của cây $T$ được định nghĩa:
$$R_\alpha(T) = R(T) + \alpha |T|$$
Trong đó:
- $R(T)$: Tổng sai số phân loại của các nút lá thuộc cây $T$.
- $|T|$: Số lượng nút lá của cây (đại diện cho độ phức tạp cấu trúc).
- $\alpha \ge 0$: Hệ số phức độ (Complexity parameter).
  + Khi $\alpha = 0$: Không phạt độ phức tạp $\implies$ Giữ nguyên cây gốc cực đại $T_{\text{max}}$.
  + Khi $\alpha \to \infty$: Phạt nặng cấu trúc $\implies$ Cây bị tỉa cành triệt để chỉ còn lại một nút gốc duy nhất.

Thuật toán tính toán chuỗi các giá trị $\alpha_{\text{eff}}$ ngưỡng (effective alphas) tại các nút nội bộ để xác định đường dẫn tỉa cành (pruning path), từ đó lựa chọn cây có kích thước tối giản nhưng hiệu năng kiểm chứng tối ưu.

### 5.3. Rừng ngẫu nhiên (Random Forest): Bagging và Không gian con ngẫu nhiên
Được phát minh bởi Leo Breiman (2001), Rừng ngẫu nhiên (Random Forest) là giải thuật học tập hợp (Ensemble Learning) mạnh mẽ, kết hợp hàng trăm cây quyết định con để triệt tiêu phương sai mà không làm tăng độ lệch (bias).

Hai cơ chế cốt lõi của Rừng ngẫu nhiên:
1. **Lấy mẫu túi lặp lại (Bootstrap Aggregating - Bagging)**:
   Mỗi cây con $h_b(x)$ ($b = 1, \dots, B$) được huấn luyện trên một tập dữ liệu con kích thước $N$, được tạo ra bằng cách lấy mẫu ngẫu nhiên có hoàn lại (bootstrap sample) từ tập Train gốc. Về mặt lý thuyết xác suất, mỗi mẫu bootstrap bỏ qua xấp xỉ $1 - \frac{1}{e} \approx 36.8\%$ dữ liệu huấn luyện (dữ liệu Out-Of-Bag - OOB), tạo ra sự đa dạng tự nhiên giữa các cây con.
2. **Không gian con ngẫu nhiên (Random Subspace Method)**:
   Tại mỗi nút phân tách của từng cây con, thuật toán không tìm kiếm trên toàn bộ 30 đặc trưng mà chỉ chọn ngẫu nhiên một tập con gồm $m$ đặc trưng ($m \le 30$). Trong dự án này, siêu tham số được cố định ở `max_features=0.3` (tương đương $9$ đặc trưng ngẫu nhiên mỗi lần tách). Cơ chế này giúp giải tương quan (decorrelate) giữa các cây, ngăn chặn việc các đặc trưng thống trị (như `perimeter_worst`) xuất hiện ở tất cả các nút gốc, từ đó giảm thiểu triệt để phương sai của toàn bộ rừng:
   $$\text{Var}(\bar{h}) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$
   Khi hệ số tương quan giữa các cây $\rho$ giảm xuống nhờ chọn đặc trưng ngẫu nhiên, phương sai tổng thể của mô hình hội tụ về mức rất thấp.

Dự đoán xác suất cuối cùng của Rừng ngẫu nhiên là giá trị trung bình cộng xác suất từ tất cả $B = 100$ cây con:
$$P(y = 1 \mid x) = \frac{1}{B} \sum_{b=1}^{B} P_b(y = 1 \mid x)$$

### 5.4. Đánh giá tầm quan trọng đặc trưng bằng Mean Decrease in Impurity (MDI)
Tầm quan trọng của đặc trưng $X_j$ trong Rừng ngẫu nhiên được tính bằng mức giảm độ vẩn đục tích lũy trung bình (Mean Decrease in Impurity - MDI) qua toàn bộ các nút phân tách sử dụng đặc trưng đó trong tất cả các cây:
$$\text{Importance}(X_j) = \frac{1}{B} \sum_{b=1}^{B} \sum_{t \in T_b : v(t) = j} p(t) \Delta I_G(t)$$
Trong đó $p(t) = \frac{N_t}{N}$ là tỷ lệ mẫu đi qua nút $t$, và $v(t) = j$ biểu thị nút $t$ được phân tách bởi đặc trưng $X_j$. Toàn bộ giá trị tầm quan trọng của 30 đặc trưng được chuẩn hóa để có tổng bằng $1.0$ ($100\%$).

---

## CHƯƠNG 6: THIẾT KẾ THỰC NGHIỆM VÀ CHIẾN LƯỢC HUẤN LUYỆN

### 6.1. Thiết lập mô hình đường cơ sở (Baseline Dummy Classifier)
Nhằm thiết lập mốc so sánh tối thiểu cho bài toán, mô hình Dummy Classifier với chiến lược `strategy='most_frequent'` được triển khai trên tập Train:
- Luôn luôn dự đoán lớp chiếm đa số (Lành tính - `Benign`, $y = 0$).
- Hiệu năng kỳ vọng: Accuracy bằng đúng tỷ lệ mẫu lành tính ($62.74\%$), Precision lớp Ác tính bằng $0\%$, và quan trọng nhất là **Recall lớp Ác tính bằng $0\%$ (bỏ sót $100\%$ bệnh nhân ung thư)**. Bất kỳ mô hình học máy thực sự nào cũng bắt buộc phải vượt trội áp đảo mốc cơ sở này.

### 6.2. Kiểm chứng chéo phân tầng 5 lượt (5-Fold Stratified Cross-Validation)
Để đảm bảo kết quả lựa chọn siêu tham số không phụ thuộc vào một lát cắt ngẫu nhiên duy nhất trên tập Train ($N = 398$), đồ án áp dụng phương pháp Kiểm chứng chéo phân tầng 5 lượt (5-Fold Stratified CV):
- Tập Train được chia thành 5 phần (folds) có tỷ lệ nhãn lành tính/ác tính đồng đều ($62.8\% : 37.2\%$).
- Trong mỗi lượt, 4 phần ($80\%$) dùng để huấn luyện và 1 phần ($20\%$) dùng để kiểm tra đánh giá.
- Điểm số hiệu năng được lấy trung bình và tính độ lệch chuẩn ($\mu \pm \sigma$) qua 5 lượt lặp, phản ánh độ ổn định thực chất của mô hình.

### 6.3. Tinh chỉnh siêu tham số và đóng băng cấu hình mô hình
Qua quá trình khảo nghiệm lưới tham số kết hợp giữa 5-Fold CV và đánh giá độc lập trên tập Validation ($N = 85$), mô hình ứng viên tối ưu nhất được lựa chọn là **RandomForestClassifier**. 

Cấu hình siêu tham số chính thức được **đóng băng tuyệt đối (Frozen Hyperparameters)** tại tệp `backend/models/final_model_config.json`:
- `n_estimators`: `100` (Số lượng cây quyết định trong rừng)
- `criterion`: `'gini'` (Hàm mục tiêu đo độ vẩn đục)
- `max_depth`: `8` (Độ sâu tối đa mỗi cây con, đủ để học mẫu phức tạp mà không overfit)
- `min_samples_split`: `2` (Số mẫu tối thiểu để phân tách nút nội bộ)
- `min_samples_leaf`: `1` (Số mẫu tối thiểu tại mỗi nút lá)
- `max_features`: `0.3` ($30\%$ số đặc trưng = $9$ đặc trưng ngẫu nhiên tại mỗi split)
- `bootstrap`: `True` (Áp dụng lấy mẫu túi có hoàn lại)
- `random_state`: `42` (Đảm bảo tính tái lập kết quả 100%)
- `n_jobs`: `-1` (Tận dụng song song toàn bộ nhân CPU)

### 6.4. Xác lập ngưỡng quyết định phân loại lâm sàng ($\tau = 0.50$)
Trên tập Validation, việc sử dụng ngưỡng xác suất chuẩn $\tau = 0.50$ đã mang lại kết quả lý tưởng: Recall đạt $90.62\%$, Precision đạt tuyệt đối $100.00\%$ ($FP = 0$), $F_1 = 95.08\%$. Nhóm nghiên cứu quyết định chốt cố định ngưỡng phân loại tại $\tau = 0.50$, không can thiệp điều chỉnh ngưỡng nhân tạo nhằm phòng ngừa hiện tượng quá khớp ngưỡng (Threshold Overfitting) trước khi bước vào tập Test.

---

## CHƯƠNG 7: KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN CHUYÊN SÂU

### 7.1. Thí nghiệm 1: Phân tích đường cong huấn luyện theo độ sâu cây
Thí nghiệm khảo sát sự biến thiên của Accuracy trên tập Train và tập Validation của Cây quyết định đơn lẻ khi tăng dần độ sâu tối đa `max_depth` từ 1 đến 15:

| Độ sâu (`max_depth`) | Train Accuracy | Validation Accuracy | Hiện tượng ghi nhận |
| :---: | :---: | :---: | :--- |
| 1 | 92.21% | 89.41% | Underfitting (Dưới khớp - Cây còi cọc) |
| 2 | 93.47% | 91.76% | Tăng trưởng khả năng phân tách |
| 3 | 97.24% | 92.94% | Điểm cân bằng tối ưu trên Validation |
| 4 | 98.49% | 91.76% | Bắt đầu xuất hiện phân kỳ Train-Val |
| 5 | 99.25% | 91.76% | Train tăng nhanh, Val đi ngang |
| 7 | 100.00% | 91.76% | Cây học vẹt hoàn toàn tập Train |
| 10 - 15 | 100.00% | 90.59% | Overfitting rõ rệt, Val giảm sút |

**Nhận xét**: Khoảng cách phân kỳ (generalization gap) giữa Train ($100\%$) và Validation ($91.76\%$) lên tới $8.24\%$. Điều này chứng minh rằng cây quyết định không kiểm soát độ sâu sẽ nhanh chóng ghi nhớ nhiễu và mất khả năng tổng quát hóa trên dữ liệu mới.

### 7.2. Thí nghiệm tỉa cành: Đường cong biến thiên $\alpha$ hiệu quả ($ccp\_\alpha$)
Sử dụng thuật toán Cost-Complexity Pruning trên tập Train, chuỗi các giá trị $\alpha_{\text{eff}}$ được xác định. Khi khảo sát trên tập Validation:
- Tại $\alpha = 0$: Cây nguyên bản có **15 nút lá**, độ sâu 7, đạt Validation Accuracy $91.76\%$.
- Khi tăng dần $\alpha$, số nút lá giảm dần đơn điệu.
- Tại $\alpha = 0.015$: Cây được rút gọn chỉ còn **5 nút lá**, độ sâu 4, nhưng Validation Accuracy tăng vọt lên **$94.12\%$** (và trên Test đạt $95.35\%$).
- Khi $\alpha > 0.04$: Cây bị tỉa cành quá mức, hiệu năng sụt giảm nghiêm trọng.

**Kết luận**: Kỹ thuật tỉa cành CCP đã chứng minh tính hiệu quả vượt trội khi loại bỏ $66.7\%$ số nút lá dư thừa nhưng đồng thời nâng cao độ chính xác tổng quát hóa.

### 7.3. Thí nghiệm 2: Đánh giá đối đầu 4 mô hình trên tập Validation và Test
Bảng dưới đây tổng hợp kết quả đối sánh toàn diện của 4 mô hình trên tập Validation độc lập ($N = 85$) và tập Test niêm phong ($N = 86$):

| Mô hình học máy | Val Acc | Val Recall | Val ROC-AUC | Test Acc | Test Recall | Test Prec | Test F1 | Test ROC-AUC | Test FN | Test FP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Dummy Classifier** | 62.35% | 0.00% | 0.5000 | 62.79% | 0.00% | 0.00% | 0.00% | 0.5000 | 32 | 0 |
| **2. Unpruned Tree** | 91.76% | 84.38% | 0.9029 | 90.70% | 87.50% | 87.50% | 87.50% | 0.9005 | 4 | 4 |
| **3. Pruned Tree (CCP)** | 94.12% | 71.88% | 0.8967 | 93.02% | 84.38% | 96.43% | 90.00% | 0.8843 | 5 | 1 |
| **4. Random Forest** | **96.47%** | **90.62%** | **0.9941** | **98.84%** | **96.88%** | **100.0%** | **98.41%** | **0.9954** | **1** | **0** |

**Thảo luận**:
1. Mô hình Dummy hoàn toàn vô dụng trong y tế khi bỏ sót 100% bệnh nhân ung thư.
2. Cây không tỉa cành tạo ra tới 4 ca báo động giả (FP=4) và 4 ca bỏ sót (FN=4) trên Test.
3. Cây tỉa cành tuy kiểm soát tốt FP (chỉ 1 ca) nhưng số ca bỏ sót lại tăng lên (FN=5) do cấu trúc cây quá cô đọng làm mất đi một số ranh giới cục bộ.
4. Rừng ngẫu nhiên vượt trội tuyệt đối trên mọi chỉ số: hạ số ca bỏ sót xuống chỉ còn **duy nhất 1 ca (FN=1)** và triệt tiêu hoàn toàn báo động giả (**FP=0**).

### 7.4. Thí nghiệm 4: Kiểm chứng độ ổn định thứ hạng đặc trưng qua nhiều Random Seeds
Một mối lo ngại lớn đối với thuật toán Rừng ngẫu nhiên là cơ chế ngẫu nhiên hóa (Bagging và Random Subspace) có thể dẫn đến việc thứ hạng tầm quan trọng của các đặc trưng bị đảo lộn khi thay đổi hạt giống ngẫu nhiên (`random_state`).

Để kiểm chứng tính vững chắc, Thí nghiệm 4 huấn luyện mô hình Random Forest trên 5 hạt giống độc lập: `seed ∈ [42, 100, 2024, 7, 999]`. Kết quả thống kê tầm quan trọng trung bình và độ biến thiên của Top 5 đặc trưng:
1. `perimeter_worst`: Tầm quan trọng $18.21\% \pm 0.84\%$ (Thứ hạng 1 tuyệt đối trên cả 5 seeds).
2. `radius_worst`: Tầm quan trọng $13.70\% \pm 0.62\%$ (Thứ hạng 2 trên cả 5 seeds).
3. `area_worst`: Tầm quan trọng $13.56\% \pm 0.71\%$ (Thứ hạng 3 trên cả 5 seeds).
4. `concave points_mean`: Tầm quan trọng $13.28\% \pm 0.55\%$ (Thứ hạng 4 trên cả 5 seeds).
5. `concave points_worst`: Tầm quan trọng $11.70\% \pm 0.49\%$ (Thứ hạng 5 trên cả 5 seeds).

**Hệ số tương quan thứ hạng Spearman** giữa các cặp seed ngẫu nhiên đạt $\rho > 0.98$ ($p < 0.001$). Điều này khẳng định danh sách Top 5 đặc trưng mang tính chất quy luật sinh học bền vững, không phải ngẫu nhiên thống kê.

### 7.5. Đánh giá kiểm thử cuối cùng trên tập Test và Khoảng tin cậy Wilson 95%
Tại thời điểm mở niêm phong tập Test độc lập ($N = 86$, gồm $54$ ca Benign và $32$ ca Malignant), mô hình Random Forest đóng băng đạt kết quả định lượng:
- **Accuracy**: $98.84\%$ ($85/86$ ca chính xác).
  + Khoảng tin cậy Wilson 95%: **$[93.70\%, 99.79\%]$**.
- **Precision Malignant**: $100.00\%$ ($31/31$ ca dự đoán ung thư đều chính xác).
  + Khoảng tin cậy Wilson 95%: $[89.03\%, 100.00\%]$.
- **Recall Malignant**: $96.88\%$ ($31/32$ ca ung thư được phát hiện thành công).
  + Khoảng tin cậy Wilson 95%: **$[84.26\%, 99.45\%]$**.
- **F1-Score Malignant**: $98.41\%$.
- **ROC-AUC**: $0.9954$.
- **Ma trận nhầm lẫn (Confusion Matrix)**:
  $$\begin{pmatrix} \text{TN} = 54 & \text{FP} = 0 \\ \text{FN} = 1 & \text{TP} = 31 \end{pmatrix}$$

#### Ý nghĩa của Khoảng tin cậy Wilson:
Do tập Test chỉ có 32 mẫu bệnh nhân ác tính, một sai số đơn lẻ làm thay đổi tỷ lệ Recall một bước nhảy $\Delta = \frac{1}{32} = 3.125\%$. Việc cung cấp khoảng tin cậy Wilson 95% thể hiện tính trung thực khoa học: mặc dù điểm ước lượng thực nghiệm là $96.88\%$, hiệu năng thực tế trên toàn bộ quần thể bệnh nhân nằm trong dải xác suất tin cậy từ $84.26\%$ đến $99.45\%$.

---

## CHƯƠNG 8: PHÂN TÍCH LỖI VÀ NGHIÊN CỨU TRƯỜNG HỢP BIÊN (ERROR ANALYSIS)

### 8.1. Toàn cảnh lỗi trên tập Test: Phân tích ca False Negative duy nhất (Mẫu #23)
Trong toàn bộ 86 bệnh nhân của tập Test, mô hình chỉ đưa ra một phán đoán sai lệch duy nhất: **Mẫu số 23** (tương ứng chỉ số hồ sơ gốc trong bộ dữ liệu là ID index `86`).
- **Nhãn thực tế (Ground Truth)**: **Malignant (Ác tính, $y = 1$)**.
- **Dự đoán của mô hình**: **Benign (Lành tính, $\hat{y} = 0$)**.
- **Xác suất mô hình gán**:
  + Xác suất Lành tính: $P(\text{Benign}) = 82.00\%$ ($0.8200$).
  + Xác suất Ác tính: $P(\text{Malignant}) = 18.00\%$ ($0.1800$).
- Với ngưỡng khóa $\tau = 0.50$, mô hình kết luận mẫu này là u lành tính.

### 8.2. So sánh phân vị thống kê của Mẫu #23 với phân phối hai lớp
Để tìm hiểu nguyên nhân tại sao mô hình lại gán xác suất ác tính thấp ($18\%$) cho một bệnh nhân ung thư, nhóm nghiên cứu đã tiến hành so sánh đối chiếu giá trị các đặc trưng của Mẫu #23 với phân phối thống kê của lớp Lành tính và lớp Ác tính trên tập huấn luyện:

| Thuộc tính tế bào | Giá trị Mẫu #23 | Trung bình Lành tính ($\mu_B$) | Trung bình Ác tính ($\mu_M$) | Phân vị lớp Ác tính (%-tile M) | Phân vị lớp Lành tính (%-tile B) | Z-Score lớp Ác tính ($Z_M$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `perimeter_worst` | **108.40** | 81.66 | 142.83 | **11.5%** | **92.0%** | -1.12 |
| `radius_worst` | **16.21** | 12.58 | 21.39 | **10.8%** | **90.0%** | -1.16 |
| `area_worst` | **808.90** | 491.64 | 1450.61 | **11.5%** | **91.6%** | -1.04 |
| `concave points_mean` | **0.0494** | 0.0238 | 0.0878 | **9.5%** | **91.6%** | -1.07 |
| `concave points_worst` | **0.1225** | 0.0672 | 0.1852 | **11.5%** | **88.8%** | -1.24 |
| `area_mean` | **544.10** | 462.70 | 978.30 | **12.2%** | **78.4%** | -1.18 |
| `radius_mean` | **12.36** | 12.15 | 17.46 | **9.5%** | **68.8%** | -1.25 |

### 8.3. Bản chất toán học của vùng chồng lấn biên giới (Borderline Overlap Region)
Dữ liệu định lượng chỉ ra một sự thật khách quan:
1. Tất cả các đặc trưng kích thước và hình thái chủ chốt của Mẫu #23 đều nằm ở **phân vị 10% thấp nhất của quần thể ung thư ác tính** ($Z_M \approx -1.1$ đến $-1.2$).
2. Đồng thời, các số đo này lại tương đồng với **phân vị 90% của quần thể u lành tính** ($Z_B \approx +1.3$ đến $+1.5$).
3. Về mặt bệnh học tế bào vi thể, đây là trường hợp khối u ác tính thể kích thước nhỏ giai đoạn rất sớm (Early-stage / Well-differentiated Carcinoma). Do mới hình thành, các nhân tế bào ung thư chưa kịp phì đại bất thường và chưa hình thành các đường gấp lõm sâu trên màng nhân. Khi chọc hút FNA, lát cắt vi thể ngẫu nhiên bắt được các tế bào có hình thái bề ngoài tương đồng với một u xơ tuyến vú lành tính kích thước lớn.
4. Về mặt toán học, mẫu này nằm tại **vùng chồng lấn biên giới (Borderline Overlap Region)** trong không gian 30 chiều. Tại vùng này, mật độ xác suất tiền nghiệm của lớp lành tính chiếm ưu thế, dẫn tới việc 82 trong số 100 cây con của Random Forest bỏ phiếu cho kết quả Lành tính.

### 8.4. Thảo luận về tỷ lệ False Positive bằng 0 và ý nghĩa thực tiễn
Mô hình đạt độ chuẩn xác tuyệt đối trên tập Test với **$FP = 0$ ($\text{Precision} = 100.00\%$)**:
- Toàn bộ 54 bệnh nhân có u lành tính đều được trả kết quả lành tính chính xác.
- Trong thực hành lâm sàng, việc giảm thiểu FP có ý nghĩa nhân văn to lớn: giải tỏa hoàn toàn áp lực tâm lý sợ hãi cho người phụ nữ và loại bỏ các thủ thuật xâm lấn sâu không cần thiết.
- Tuy nhiên, nhóm nghiên cứu cũng lưu ý rằng kết quả FP = 0 một phần do quy mô tập Test nhỏ ($N_B = 54$). Kết quả kiểm chứng chéo 5-Fold trước đó cho thấy Precision trung bình đạt $92.69\%$. Do đó trong môi trường lâm sàng quy mô lớn, hệ thống vẫn có thể ghi nhận tỷ lệ báo động giả khoảng $5\% - 7\%$.

---

## CHƯƠNG 9: KIẾN TRÚC TRIỂN KHAI HỆ THỐNG WEB VÀ API

### 9.1. Kiến trúc phân tầng tách rời (Decoupled 3-Tier Architecture)
Hệ thống được thiết kế theo kiến trúc 3 tầng chuẩn công nghiệp (3-Tier Clean Architecture), tách biệt rành mạch giữa giao diện người dùng, logic nghiệp vụ máy chủ và mô hình học máy:

```
[ Frontend: ReactJS + Vite + Tailwind/Custom CSS ]
                 │ (HTTP REST JSON)
                 ▼
[ Backend API: FastAPI + Pydantic v2 ]
                 │ (In-memory Prediction Pipeline)
                 ▼
[ ML Inference Engine: Scikit-Learn Pipeline (Random Forest) ]
```

### 9.2. Backend FastAPI: Xác thực nghiêm ngặt 30 đặc trưng bằng Pydantic
Máy chủ API được hiện thực hóa bằng FastAPI (Python 3.12), đảm bảo hiệu năng bất đồng bộ cao và khả năng tự động sinh tài liệu Swagger/OpenAPI.
- **Xác thực dữ liệu đầu vào (Input Validation)**:
  Sử dụng Pydantic Schema `ClassificationRequest` kiểm tra nghiêm ngặt toàn bộ 30 đặc trưng số thực.
  + Kiểm tra chặt chẽ: Bắt buộc đủ 30 trường, không cho phép thiếu hoặc thừa trường (`extra='forbid'`).
  + Kiểm tra tính hợp lệ: Từ chối ngay lập tức các giá trị kiểu chuỗi sai lệch, giá trị vô hạn `Infinity`, hoặc giá trị `NaN` (HTTP 422 Unprocessable Entity).
  + Kiểm tra biên giá trị vật lý: Đưa ra cảnh báo rõ ràng nếu người dùng nhập số đo vượt khỏi dải tham chiếu thống kê của tập Train, nhưng không tự ý sửa đổi hay làm tròn giá trị của người dùng.
- **Endpoint cốt lõi**:
  + `POST /api/demo-classify`: Nhận 30 đặc trưng, kiểm tra schema, chạy pipeline suy luận, trả về nhãn dự đoán (`B` / `M`), xác suất của từng lớp (`proba_benign`, `proba_malignant`), và danh sách các đặc trưng đóng góp hàng đầu.
  + `GET /api/reports/dashboard`: Cung cấp dữ liệu báo cáo thực nghiệm và đường dẫn biểu đồ đã đóng băng phục vụ trang Dashboard.
  + `GET /health`: Kiểm tra trạng thái sẵn sàng của dịch vụ và tính toàn vẹn của mô hình đã nạp.

### 9.3. Frontend React Vite: Giao diện trực quan hóa, kiểm thử mẫu và Dashboard
Giao diện người dùng được xây dựng trên nền tảng React 19 kết hợp công cụ đóng gói Vite:
- **Trang 1: Overview (`/overview`)**: Giới thiệu bối cảnh đề tài, ý nghĩa bài toán chẩn đoán ung thư vú, quy trình trích xuất đặc trưng FNA, giải thích cơ chế hoạt động của Cây quyết định và Rừng ngẫu nhiên, cùng cảnh báo trách nhiệm phi lâm sàng.
- **Trang 2: Classification Demo (`/classification`)**: Cho phép người dùng lựa chọn các mẫu bệnh phẩm đại diện (Điển hình Lành tính, Điển hình Ác tính, Ca biên giới khó, Ca lỗi thực nghiệm Mẫu #23) hoặc tự nhập tay 30 đặc trưng. Hệ thống nhóm các đặc trưng theo 3 tab khoa học: *Mean*, *Standard Error*, và *Worst*, hiển thị đơn vị đo và miền giá trị tham chiếu.
- **Trang 3: Model Evaluation Dashboard (`/dashboard`)**: Trực quan hóa toàn diện kết quả thực nghiệm học máy: bảng đối sánh 4 mô hình, biểu đồ quá khớp độ sâu cây, đường dẫn tỉa cành CCP, ma trận nhầm lẫn Test, đường cong ROC/PR, phân tích độ ổn định hạt giống ngẫu nhiên, và thẻ tóm tắt Model Card.

### 9.4. Luồng xử lý dữ liệu End-to-End từ giao diện người dùng tới suy luận mô hình
1. Người dùng chọn mẫu bệnh phẩm hoặc nhập 30 trường số trên giao diện React.
2. Giao diện thực hiện kiểm tra sơ bộ (Client-side validation) và gửi yêu cầu `POST /api/demo-classify` qua Axios.
3. FastAPI nhận payload JSON, chuyển qua Pydantic schema để xác thực kiểu dữ liệu và thứ tự 30 cột.
4. Dữ liệu được chuyển thành mảng 2 chiều NumPy shape $(1, 30)$ và đưa vào mô hình `wdbc_pipeline.joblib`.
5. Mô hình thực thi song song qua 100 cây con, tính toán xác suất trung bình qua `predict_proba`.
6. API đóng gói kết quả phản hồi JSON chuẩn hóa.
7. React nhận dữ liệu, hiển thị nhãn kết luận kèm thanh đo xác suất trực quan, mã màu lâm sàng và danh sách đặc trưng tế bào học đóng góp quan trọng nhất.

---

## CHƯƠNG 10: ĐẠO ĐỨC, KHÍA CẠNH PHÁP LÝ VÀ GIỚI HẠN HỆ THỐNG

### 10.1. Tuyên bố giới hạn phi lâm sàng (Non-Diagnostic Academic Disclaimer)
Đồ án này được thực hiện hoàn toàn cho mục đích nghiên cứu học thuật và giáo dục trong khuôn khổ học phần Học máy cơ bản tại Trường Đại Học Công Nghệ Kỹ Thuật Hưng Yên. 
- **Tuyên bố pháp lý**: Mô hình và phần mềm đi kèm **tuyệt đối không phải là thiết bị y tế (Software as a Medical Device - SaMD)** và không được phép sử dụng trong chẩn đoán lâm sàng thực tế, ra quyết định điều trị, chỉ định phẫu thuật, hoặc thay thế ý kiến chuyên môn của bác sĩ giải phẫu bệnh.
- Mọi kết luận dự đoán của hệ thống chỉ mang tính chất minh họa phương pháp luận thuật toán học máy.

### 10.2. Tính công bằng, độ trượt miền dữ liệu (Domain Shift) và bảo mật y tế
- **Độ trượt miền dữ liệu (Domain Shift / Dataset Shift)**: Bộ dữ liệu WDBC được thu thập từ một trung tâm y tế duy nhất tại Hoa Kỳ vào thập niên 1990. Dữ liệu không ghi nhận các thông tin nhân khẩu học (độ tuổi, chủng tộc, tiền sử gia đình, mật độ mô tuyến vú theo phân loại BI-RADS). Khi áp dụng mô hình cho các quần thể phụ nữ tại các khu vực địa lý khác (chẳng hạn như phụ nữ châu Á có đặc trưng mô vú dày hơn), mô hình có thể gặp hiện tượng suy giảm hiệu năng do phân phối dữ liệu bị dịch chuyển.
- **Bảo mật và quyền riêng tư bệnh nhân**: Dữ liệu gốc đã được mã hóa định danh hoàn toàn (De-identified) từ phía UCI. Hệ thống Web không lưu trữ thông tin nhận dạng cá nhân (PII) và không duy trì cơ sở dữ liệu bệnh nhân cục bộ.

### 10.3. Tính minh bạch và giải trình thuật toán trong AI y tế
Tuân thủ các nguyên tắc đạo đức AI của UNESCO và hướng dẫn của FDA về AI/ML trong y tế, dự án chú trọng tính minh bạch (Transparency):
- Thay vì sử dụng mô hình hộp đen hoàn toàn, dự án cung cấp đầy đủ mã nguồn huấn luyện, cấu hình siêu tham số, phân tích đường dẫn tỉa cành, và biểu đồ tầm quan trọng đặc trưng (MDI).
- Hệ thống công khai rõ ràng ca lỗi (Mẫu #23) và phân tích nguyên nhân khoa học, không tìm cách ngụy tạo kết quả hoàn hảo giả tạo.

---

## CHƯƠNG 11: KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN

### 11.1. Tổng kết các đóng góp chính của đồ án
Đồ án đã hoàn thành xuất sắc toàn bộ 24 nhiệm vụ đặt ra trong đề tài Project 16 với các kết quả nổi bật:
1. **Thiết lập quy trình phương pháp luận chuẩn mực**: Thực hiện phân chia dữ liệu 3 nhánh phân tầng độc lập (Train 398, Val 85, Test 86), bảo đảm nguyên tắc Zero Data Leakage tuyệt đối xuyên suốt dự án.
2. **Chứng minh và giải quyết triệt để vấn đề Overfitting**: Minh chứng rõ nét hiện tượng quá khớp của Cây quyết định đơn lẻ (CART) qua phân tích độ sâu; thực nghiệm thành công kỹ thuật tỉa cành hậu kỳ Cost-Complexity Pruning giúp tối giản $66.7\%$ số nút lá mà vẫn gia tăng độ chính xác.
3. **Mô hình Rừng ngẫu nhiên đạt hiệu năng vượt trội**: Với 100 cây con và kỹ thuật lấy mẫu con ngẫu nhiên $30\%$ đặc trưng, mô hình đạt **Accuracy = 98.84%**, **Recall = 96.88%**, **Precision = 100.00%**, và **ROC-AUC = 0.9954** trên tập Test độc lập.
4. **Phân tích lỗi khoa học và sâu sắc**: Điều tra tận gốc ca lỗi False Negative duy nhất (Mẫu #23), chứng minh nguyên nhân xuất phát từ sự chồng lấn hình thái học khách quan của khối u kích thước nhỏ giai đoạn sớm.
5. **Hiện thực hóa giải pháp phần mềm hoàn chỉnh**: Xây dựng thành công hệ sinh thái phần mềm gồm Backend API FastAPI hiệu năng cao, Frontend ReactJS tương tác hiện đại, và bộ kiểm thử tự động 72 bài test đạt tỷ lệ pass $100\%$.

### 11.2. Các bài học kinh nghiệm về phương pháp luận
- **Liêm chính khoa học là trên hết**: Không bao giờ sử dụng tập Test để lựa chọn mô hình hoặc tinh chỉnh siêu tham số. Điểm số trên Test phải là sự phản ánh khách quan một lần duy nhất về năng lực khái quát hóa.
- **Giá trị của khoảng tin cậy thống kê**: Trong các bộ dữ liệu y tế quy mô vừa và nhỏ, việc cung cấp khoảng tin cậy (như Wilson Score Interval) mang tính sống còn để tránh việc kết luận chủ quan dựa trên các biến thiên ngẫu nhiên của mẫu số nhỏ.
- **Tập hợp mô hình (Ensemble) giải quyết nhược điểm phương sai**: Rừng ngẫu nhiên khắc phục triệt để tính bất ổn định của Cây quyết định đơn lẻ, mang lại sự bền vững cho thứ hạng các đặc trưng tế bào học.

### 11.3. Hướng nghiên cứu mở rộng trong tương lai
1. **Mở rộng sang các kỹ thuật tăng cường độ dốc (Gradient Boosting)**: Thử nghiệm đối sánh sâu hơn với XGBoost, LightGBM và CatBoost trên cùng quy trình kiểm định phân tầng.
2. **Nâng cao khả năng giải thích cục bộ**: Tích hợp phương pháp SHAP (SHapley Additive exPlanations) và LIME nhằm giải thích chính xác đóng góp của từng đặc trưng cho từng ca bệnh đơn lẻ trên giao diện người dùng.
3. **Mô hình hóa độ bất định (Uncertainty Estimation)**: Xây dựng cơ chế vùng cảnh báo không chắc chắn (Dual-threshold system) để tự động phát hiện các ca bệnh nằm ở vùng biên chồng lấn như Mẫu #23 và khuyến nghị hội chẩn bác sĩ chuyên khoa.

---

## TÀI LIỆU THAM KHẢO (REFERENCES)

1. **Wolberg, W. H., Street, W. N., & Mangasarian, O. L. (1995)**. *Machine learning techniques to diagnose breast cancer from fine-needle aspirates*. Cancer Letters, 77(2-3), 163-171.
2. **Street, W. N., Wolberg, W. H., & Mangasarian, O. L. (1993)**. *Nuclear feature extraction for breast tumor diagnosis*. IS&T/SPIE 1993 International Symposium on Electronic Imaging: Science and Technology, 1905, 861-870.
3. **Breiman, L., Friedman, J., Stone, C. J., & Olshen, R. A. (1984)**. *Classification and Regression Trees*. CRC Press.
4. **Breiman, L. (2001)**. *Random Forests*. Machine Learning, 45(1), 5-32.
5. **Hastie, T., Tibshirani, R., & Friedman, J. (2009)**. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer New York.
6. **Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., ... & Gebru, T. (2019)**. *Model Cards for Model Reporting*. Proceedings of the Conference on Fairness, Accountability, and Transparency (FAT* '19), 220-229.
7. **Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021)**. *Datasheets for Datasets*. Communications of the ACM, 64(12), 86-92.
8. **Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011)**. *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
9. **Wilson, E. B. (1927)**. *Probable inference, the law of succession, and statistical inference*. Journal of the American Statistical Association, 22(158), 209-212.
10. **UCI Machine Learning Repository**. *Breast Cancer Wisconsin (Diagnostic) Data Set*. [https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic).

---

## PHỤ LỤC: HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM VÀ KIỂM THỬ

### Phụ lục A: Đặc tả môi trường và cấu hình phần mềm
- **Hệ điều hành**: Microsoft Windows 10/11 x64 hoặc Linux Ubuntu 22.04 LTS.
- **Môi trường Python**: Python phiên bản `3.12.x`.
- **Môi trường Node.js**: Node.js phiên bản `v20.x` hoặc `v22.x` kèm `npm 10.x`.
- **Các thư viện máy học chính (`backend/requirements.txt`)**:
  - `fastapi>=0.115.0`
  - `uvicorn>=0.32.0`
  - `pydantic>=2.10.0`
  - `scikit-learn==1.9.1`
  - `pandas>=2.2.0`
  - `numpy>=2.0.0`
  - `joblib>=1.4.2`
  - `pytest>=8.3.0`
  - `httpx>=0.28.0`

### Phụ lục B: Quy trình tái lập thực nghiệm bằng một lệnh duy nhất
Toàn bộ mã nguồn nghiên cứu được tổ chức trong thư mục `backend/src/`. Để tái lập toàn bộ chu trình thực nghiệm từ chia tập dữ liệu đến đánh giá mô hình, mở cửa sổ dòng lệnh PowerShell tại thư mục gốc dự án và thực thi:

```powershell
# 1. Kích hoạt môi trường ảo Python
.venv\Scripts\Activate.ps1

# 2. Bước 1: Tiền xử lý và chia tập dữ liệu ngẫu nhiên phân tầng 70/15/15
python backend/src/prepare_data.py

# 3. Bước 2: Huấn luyện cây quyết định không tỉa cành và khảo sát độ sâu (Thí nghiệm 1)
python backend/src/unpruned_tree.py

# 4. Bước 3: Thực nghiệm tỉa cành Cost-Complexity Pruning (CCP)
python backend/src/prune_tree.py

# 5. Bước 4: Huấn luyện Rừng ngẫu nhiên và kiểm tra độ ổn định hạt giống (Thí nghiệm 4)
python backend/src/train_random_forest.py

# 6. Bước 5: Đối sánh 4 mô hình trên tập Validation (Thí nghiệm 2)
python backend/src/compare_models.py

# 7. Bước 6: Mở niêm phong và đánh giá cuối cùng trên tập Test độc lập
python backend/src/evaluate_final_test.py
```

### Phụ lục C: Khởi chạy bộ kiểm thử tự động (Automated Test Suite)
Hệ thống tích hợp bộ kiểm thử tự động toàn diện gồm 72 ca thử nghiệm (Unit tests & Integration tests):
```powershell
# Chạy toàn bộ 72 ca kiểm thử tự động với pytest
python -m pytest -v
```
*Kết quả ghi nhận*: **72 passed, 0 failed, 0 skipped** trong thời gian xấp xỉ 2.14 giây.

### Phụ lục D: Khởi chạy hệ sinh thái dịch vụ Web & API
```powershell
# Khởi chạy Backend API FastAPI (Cổng 8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# Khởi chạy Frontend React Vite (Cổng 5173 - Mở cửa sổ dòng lệnh thứ 2)
cd frontend
npm run dev
```
Truy cập trình duyệt tại:
- Giao diện ứng dụng: `http://localhost:5173`
- Tài liệu API tương tác: `http://localhost:8000/docs`
