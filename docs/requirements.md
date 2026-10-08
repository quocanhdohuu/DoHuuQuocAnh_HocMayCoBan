# TÀI LIỆU ĐẶC TẢ YÊU CẦU DỰ ÁN (PROJECT REQUIREMENTS)
## Đề tài: Project 16 — Minh họa phân loại khối u vú bằng cây và rừng
**Học phần**: Học máy cơ bản (Bài 6 — Cây quyết định, cắt tỉa và rừng ngẫu nhiên)  
**Giảng viên hướng dẫn**: PGS.TS. Nguyễn Văn Hậu — Lớp: 12523W.1  
**Nhóm thực hiện**: 02 sinh viên  
**Bộ dữ liệu**: Breast Cancer Wisconsin (Diagnostic) — UCI Machine Learning Repository  

---

## 1. TỔNG QUAN VÀ BỐI CẢNH DỰ ÁN

### 1.1. Bối cảnh bài toán
Dự án tập trung vào việc nghiên cứu và ứng dụng hai thuật toán học máy kinh điển là **Cây quyết định (Decision Tree)** và **Rừng ngẫu nhiên (Random Forest)** trên bộ dữ liệu ảnh tế bào học chọc hút kim nhỏ (Fine Needle Aspirate - FNA) của khối u vú Wisconsin Diagnostic Breast Cancer (WDBC).  
Mục đích cốt lõi là **minh họa học thuật** về cơ chế hoạt động, khả năng giải thích (interpretability), hiện tượng quá khớp (overfitting), vai trò của cắt tỉa (pruning) và cơ chế giảm phương sai của mô hình rừng tập hợp.

> **CẢNH BÁO BẮT BUỘC (NON-CLINICAL DISCLAIMER):**  
> Dự án hoàn toàn phục vụ mục đích nghiên cứu học thuật trong khuôn khổ môn học Học máy cơ bản. Mô hình và ứng dụng **tuyệt đối không được sử dụng cho chẩn đoán y tế lâm sàng thực tế**, không sử dụng dữ liệu bệnh nhân thực chưa kiểm duyệt, và không đưa ra bất kỳ khuyến nghị y khoa nào.

### 1.2. Mục tiêu học thuật cốt lõi
1. Vận dụng kiến thức Bài 6: Xây dựng, huấn luyện và trực quan hóa cây quyết định, cắt tỉa trước/sau (pre/post-pruning) và rừng ngẫu nhiên.
2. Xây dựng pipeline học máy chuẩn mực, có khả năng tái lập hoàn toàn (reproducibility), loại bỏ 100% rò rỉ dữ liệu (data leakage) và giữ tập kiểm thử độc lập tuyệt đối.
3. Thực hiện và phân tích sâu sắc 4 thí nghiệm bắt buộc thay vì chỉ báo cáo một con số điểm số đơn lẻ.
4. Đóng gói mô hình thành dịch vụ API (FastAPI) và ứng dụng Web tương tác (ReactJS) có khả năng giải thích đường đi quyết định (decision path).

---

## 2. TRÍCH XUẤT CÁC YÊU CẦU BẮT BUỘC (MANDATORY REQUIREMENTS)

### 2.1. Yêu cầu về Dữ liệu (Data Requirements)
- **Quy mô & Định dạng**: 569 mẫu bệnh phẩm, 30 đặc trưng số (numerical features) trích xuất từ 10 đặc tính hình thái học của nhân tế bào FNA (mean, standard error `se`, worst/largest). Cột định danh `id` phải bị loại bỏ trước khi huấn luyện.
- **Nhãn mục tiêu (`diagnosis`)**: Nhị phân gồm `B` (Benign - Lành tính: 357 mẫu ~62.74%) và `M` (Malignant - Ác tính: 212 mẫu ~37.26%).
- **Bản quyền & Xuất xứ**: Nguồn chính thức UCI Machine Learning Repository (DOI: 10.24432/C5DW2B), tuân thủ giấy phép Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Hồ sơ dữ liệu (Data Artifacts)**: Phải có `data/README.md` (metadata, checksum, trích dẫn), `data_dictionary.md` (tên, kiểu, đơn vị, ngưỡng hợp lệ), và báo cáo kiểm tra chất lượng (missing values, duplicates, outliers).

### 2.2. Yêu cầu về Machine Learning & Quy trình Pipeline (ML Pipeline Requirements)
- **Tập mô hình bắt buộc**:
  1. `DummyClassifier`: Mô hình cơ sở (baseline) sử dụng chiến lược xác suất hoặc phân lớp đa số (`most_frequent` / `stratified`).
  2. `DecisionTreeClassifier (Unpruned)`: Cây quyết định phát triển tự do không giới hạn độ sâu nhằm quan sát hiện tượng quá khớp (overfitting).
  3. `DecisionTreeClassifier (Pruned)`: Cây quyết định có cắt tỉa (kết hợp pre-pruning qua `max_depth` và post-pruning qua tham số độ phức tạp chi phí `ccp_alpha`).
  4. `RandomForestClassifier`: Rừng ngẫu nhiên gồm tập hợp nhiều cây nhằm chứng minh cơ chế giảm phương sai (variance reduction).
- **Phân chia tập dữ liệu (Data Splitting)**:
  - Bắt buộc phân chia có phân tầng (**Stratified Train/Test Split**) để bảo toàn tỷ lệ nhãn 357B : 212M.
  - Tách tập Test hoàn toàn độc lập ngay từ đầu; chỉ đánh giá một lần duy nhất trên tập Test sau khi đã đóng băng toàn bộ mô hình và ngưỡng.
  - Toàn bộ quá trình chọn siêu tham số (`max_depth`, `ccp_alpha`, `n_estimators`,...) phải thực hiện qua K-Fold Cross-Validation (Stratified K-Fold) trên tập Train.
- **Chống rò rỉ dữ liệu (Zero Data Leakage)**: Mọi thao tác tiền xử lý, scaling (nếu có so sánh), feature selection hoặc tính toán thống kê chỉ được fit trên tập Train, sau đó transform sang Test.
- **Đóng gói Offline**: Mô hình và pipeline phải được huấn luyện offline, xuất artifact (`.joblib` hoặc `.pkl`) cùng file metadata cấu hình và thông số phân bố. Serving không được huấn luyện lại ở từng request.

### 2.3. Yêu cầu về 4 Thí nghiệm bắt buộc (Experimental Requirements)
1. **Thí nghiệm 1 (Train/CV curve theo độ sâu)**: Vẽ đồ thị độ chính xác/Recall trên tập Train vs Cross-Validation theo sự gia tăng của `max_depth` để minh họa rõ nét ranh giới giữa underfitting, điểm tối ưu và overfitting.
2. **Thí nghiệm 2 (So sánh 3 mô hình cây và rừng)**: Đánh giá so sánh trực tiếp trên cùng một phân vùng dữ liệu giữa Cây chưa cắt, Cây có cắt tỉa và Rừng ngẫu nhiên trên các metric chuẩn.
3. **Thí nghiệm 3 (Confusion Matrix & Phân tích False Negative)**: Lập ma trận nhầm lẫn, phân tích chuyên sâu các trường hợp lỗi False Negative (ca ung thư ác tính nhưng dự đoán lành tính) và đánh giá chi phí rủi ro trong y tế.
4. **Thí nghiệm 4 (Kiểm tra độ ổn định Feature Importance)**: Huấn luyện qua nhiều `random_state` (ví dụ 10 seeds khác nhau) để đánh giá độ biến thiên mức độ quan trọng của đặc trưng; tuyệt đối không diễn giải tương quan hay importance thành quan hệ nhân quả.

### 2.4. Thang đo đánh giá (Evaluation Metrics)
- `Recall (Malignant)`: Thang đo ưu tiên cao nhất nhằm tối thiểu hóa False Negative.
- `Precision`, `F1-score` (Macro & Malignant), `ROC-AUC`.
- `Confusion Matrix` trực quan hóa dạng nhiệt (Heatmap).

### 2.5. Yêu cầu Ứng dụng Web & API (System & Interface Requirements)
- **Kiến trúc phân tầng**: Tách biệt rõ Backend Serving (FastAPI) và Frontend Giao diện (ReactJS).
- **Backend API (FastAPI)**:
  - Endpoint `POST /api/predict` hoặc `POST /api/demo-classify`.
  - Schema validation chặt chẽ bằng Pydantic: kiểm tra kiểu số thực, số lượng đủ 30 đặc trưng, kiểm tra chặn trên/dưới theo miền giá trị vật lý (min/max của bộ dữ liệu).
  - Trả về mã lỗi HTTP chuẩn (400 Bad Request, 422 Unprocessable Entity) kèm thông báo chi tiết khi đầu vào bất thường; không âm thầm thế giá trị mặc định.
  - Phản hồi JSON chứa: Nhãn dự đoán, xác suất dự đoán các lớp, và chuỗi vết quyết định (**Decision Path**) của cây quyết định.
- **Frontend (ReactJS)**:
  - **Banner cảnh báo lâm sàng** luôn hiển thị cố định ở đầu trang.
  - **Màn hình 1 — Giới thiệu & Phạm vi**: Trình bày bối cảnh bài toán, mô tả 30 đặc trưng tế bào, thông tin bộ dữ liệu WDBC và model card.
  - **Màn hình 2 — Không gian thao tác chính**: Cho phép chọn mẫu thử nghiệm demo có sẵn (Preset Benign / Preset Malignant) hoặc nhập tay 30 đặc trưng; hiển thị kết quả xác suất, nhãn và sơ đồ/vết phân nhánh quyết định (Decision Path step-by-step).
  - **Màn hình 3 — Dashboard thực nghiệm & So sánh**: Trình bày biểu đồ 4 thí nghiệm bắt buộc, bảng so sánh metrics và ma trận nhầm lẫn.

### 2.6. Yêu cầu Sản phẩm bàn giao (Deliverables)
- Mã nguồn có tổ chức, chạy độc lập từ máy tính mới không phụ thuộc đường dẫn tuyệt đối.
- Tệp `requirements.txt` ghi rõ phiên bản dependencies.
- Báo cáo kết thúc học phần định dạng DOCX/PDF từ 15–25 trang chuẩn đề cương.
- Bộ slide thuyết trình 10–12 slide.

---

## 3. PHÂN BIỆT YÊU CẦU BẮT BUỘC VÀ PHẦN MỞ RỘNG TÙY CHỌN

| Hạng mục | Yêu cầu bắt buộc (Mandatory - Phải có) | Phần mở rộng tùy chọn (Optional Extensions) |
| :--- | :--- | :--- |
| **Dữ liệu** | 569 mẫu WDBC, 30 đặc trưng, bỏ ID, phân tích missing/duplicate, Stratified Split. | Bổ sung phân tích tương quan đa biến (VIF/PCA để khảo sát đa cộng tuyến mà không làm mất tính nguyên bản của cây). |
| **Mô hình** | DummyClassifier, DecisionTree (unpruned), DecisionTree (pruned via depth/ccp_alpha), RandomForest. | Thử nghiệm Gradient Boosting (XGBoost/LightGBM) để đối chiếu hiệu năng với Random Forest. |
| **Thực nghiệm** | Đủ 4 thí nghiệm bắt buộc theo mô tả của giảng viên. | Khảo sát ảnh hưởng của số lượng cây (`n_estimators` từ 10 đến 300) và cơ chế chọn đặc trưng (`max_features`). |
| **Web / UI** | 3 màn hình, banner y tế, chọn mẫu demo, xem xác suất, xem Decision Path cơ bản, validation lỗi. | Thanh trượt tùy chỉnh ngưỡng phân loại (Threshold Tuning Slider: từ 0.1 đến 0.9) để quan sát sự đánh đổi Precision-Recall trực tiếp trên UI; xuất báo cáo kết quả sang PDF. |
| **API** | Schema Pydantic 30 trường, trả nhãn + xác suất + decision path, test đơn vị (unit tests). | Tích hợp Swagger UI tùy biến, ghi log dự đoán (in-memory hoặc file log). |

---

## 4. MA TRẬN TRUY XUẤT YÊU CẦU (REQUIREMENT TRACEABILITY MATRIX - RTM)

| Req ID | Mô tả yêu cầu | Mức ưu tiên (MoSCoW) | Sản phẩm đầu ra | Phương pháp kiểm chứng |
| :--- | :--- | :---: | :--- | :--- |
| **REQ-DAT-01** | Làm sạch dữ liệu WDBC: loại bỏ `id`, kiểm tra missing/outlier, mã hóa nhãn $M=1, B=0$. | **Must Have** | `src/data.py`, `data/README.md` | Chạy test kiểm tra kích thước shape `(569, 31)`, 0 null. |
| **REQ-DAT-02** | Chia tập Stratified Train/Test (80:20 hoặc 75:25), cố định `random_state`. | **Must Have** | `src/data.py`, `data/train.csv`, `data/test.csv` | Kiểm tra tỷ lệ nhãn B/M ở Train và Test xấp xỉ nhau; không trùng lặp index. |
| **REQ-MOD-01** | Huấn luyện Baseline DummyClassifier. | **Must Have** | `src/train.py`, `models/baseline_dummy.joblib` | Điểm số Recall(M) = 0 nếu dùng chiến lược `most_frequent`. |
| **REQ-MOD-02** | Huấn luyện Decision Tree chưa cắt tỉa (unpruned). | **Must Have** | `src/train.py`, `models/dt_unpruned.joblib` | Độ chính xác tập Train đạt xấp xỉ 100%, độ sâu tối đa không bị chặn. |
| **REQ-MOD-03** | Tối ưu hóa siêu tham số và cắt tỉa cây (Pre-pruning `max_depth` & Post-pruning `ccp_alpha`) bằng K-Fold CV. | **Must Have** | `src/train.py`, `models/dt_pruned.joblib` | Tìm ra $\alpha$ tối ưu trên CV; cây có số lá ít hơn và tổng quát tốt hơn trên validation. |
| **REQ-MOD-04** | Huấn luyện Random Forest Classifier. | **Must Have** | `src/train.py`, `models/rf_model.joblib` | Điểm số CV ROC-AUC và Recall vượt trội so với cây đơn lẻ. |
| **REQ-EXP-01** | **Thí nghiệm 1**: Đường cong Train vs CV theo `max_depth`. | **Must Have** | `reports/figures/exp1_depth_curve.png` | Đồ thị thể hiện rõ Train score tăng dần lên 1.0 trong khi CV score bão hòa/giảm. |
| **REQ-EXP-02** | **Thí nghiệm 2**: Bảng so sánh hiệu năng 3 mô hình (Unpruned, Pruned, RF). | **Must Have** | `reports/figures/exp2_model_comparison.png`, `reports/metrics_summary.json` | So sánh công bằng trên cùng Test set: Recall, Precision, F1, ROC-AUC. |
| **REQ-EXP-03** | **Thí nghiệm 3**: Confusion Matrix và phân tích lỗi False Negative. | **Must Have** | `reports/figures/exp3_confusion_matrix.png`, tài liệu phân tích lỗi | Hiển thị rõ số lượng FN của từng mô hình; phân tích nguyên nhân các ca bị dự đoán sai. |
| **REQ-EXP-04** | **Thí nghiệm 4**: Phân tích độ ổn định Feature Importance qua $\ge 10$ random seeds. | **Must Have** | `reports/figures/exp4_feature_stability.png` | Boxplot hoặc errorbar biểu diễn độ lệch chuẩn của importance các đặc trưng top đầu. |
| **REQ-API-01** | Xây dựng API FastAPI phục vụ dự đoán và giải thích đường đi quyết định. | **Must Have** | `app/main.py`, `app/schemas.py` | Gửi request JSON qua Postman / pytest, nhận về 200 OK với label, proba, decision path. |
| **REQ-API-02** | Xác thực schema và xử lý ngoại lệ ngoài miền giá trị. | **Must Have** | `app/schemas.py`, `tests/test_api.py` | Gửi giá trị thiếu, chuỗi ký tự, hoặc số âm vô lý nhận về mã 422 hoặc 400 kèm chi tiết lỗi. |
| **REQ-WEB-01** | Giao diện ReactJS gồm 3 màn hình: Giới thiệu/Phạm vi, Dự đoán & Cây, Dashboard. | **Must Have** | `frontend/src/` | Kiểm thử giao diện trên trình duyệt: chuyển tab mượt mà, layout chuẩn responsive. |
| **REQ-WEB-02** | Banner cảnh báo miễn trừ trách nhiệm y tế (Medical Disclaimer). | **Must Have** | `frontend/src/components/DisclaimerBanner.jsx` | Banner đỏ/vàng cảnh báo hiển thị trên toàn bộ các trang giao diện. |
| **REQ-WEB-03** | Trực quan hóa đường đi quyết định (Decision Path Inspector). | **Must Have** | `frontend/src/components/DecisionPathView.jsx` | Hiển thị từng bước rẽ nhánh: đặc trưng, ngưỡng cắt, giá trị mẫu và chiều rẽ. |
| **REQ-EXT-01** | Thanh điều chỉnh ngưỡng quyết định xác suất (Threshold Slider). | **Should Have** | `frontend/src/components/ThresholdSlider.jsx` | Thay đổi ngưỡng từ 0.1 - 0.9 cập nhật tức thời nhãn dự đoán trên giao diện. |
| **REQ-DOC-01** | Báo cáo hoàn chỉnh 15–25 trang và Slide thuyết trình 10–12 trang. | **Must Have** | `docs/Bao_cao_Project_16.docx`, `docs/Slide_thuyet_trinh.pptx` | Đầy đủ 13 mục theo đề cương của giảng viên; biểu đồ rõ nét, trích dẫn chuẩn IEEE. |

---

## 5. KẾ HOẠCH TRIỂN KHAI 6 TUẦN (MAPPING CHI TIẾT)

```
Tuần 1: Khởi tạo, Đặc tả & Chuẩn bị dữ liệu
├── Chốt bài toán, định nghĩa input/output
├── Thiết lập Git repository, cấu trúc thư mục
└── Viết data/README.md, data_dictionary.md

Tuần 2: EDA trên tập Train & Mô hình Baseline
├── Thực hiện Stratified Train/Test split (đóng băng Test)
├── EDA độc lập trên Train set (phân bố, tương quan)
└── Triển khai DummyClassifier & DecisionTree unpruned

Tuần 3: Huấn luyện Mô hình chính & Cắt tỉa
├── Tối ưu hóa max_depth và ccp_alpha qua Stratified K-Fold CV
├── Huấn luyện RandomForestClassifier
└── Lưu trữ các Pipeline và Artifacts vào models/

Tuần 4: Thực hiện 4 Thí nghiệm & Đóng băng kết quả Test
├── Thí nghiệm 1: Depth curve (Train vs CV)
├── Thí nghiệm 2: So sánh Unpruned vs Pruned vs Random Forest
├── Thí nghiệm 3: Confusion Matrix & Phân tích chuyên sâu False Negative
├── Thí nghiệm 4: Đánh giá độ ổn định Feature Importance qua đa seed
└── Đánh giá 1 lần duy nhất trên tập Test, đóng băng số liệu báo cáo

Tuần 5: Đóng gói API FastAPI & Phát triển Web ReactJS
├── Xây dựng FastAPI app: /api/predict, /api/demo-samples, /api/model-card
├── Kiểm thử schema validation và mã lỗi
└── Xây dựng Frontend ReactJS (3 màn hình, Banner, Decision Path)

Tuần 6: Hoàn thiện Báo cáo, Slide & Kiểm thử tái lập
├── Kiểm thử chạy lại toàn bộ quy trình trên môi trường sạch
├── Viết báo cáo học thuật (15-25 trang) và chuẩn bị Slide (10-12 trang)
└── Hoàn thiện hồ sơ bàn giao, model card và tài liệu hướng dẫn
```

---

## 6. NHẬN DIỆN VÀ CHIẾN LƯỢC QUẢN TRỊ RỦI RO KỸ THUẬT

### 6.1. Rủi ro Rò rỉ dữ liệu (Data Leakage)
- **Bản chất rủi ro**: Sử dụng toàn bộ 569 mẫu để tính min, max, mean, chuẩn hóa dữ liệu hoặc chọn siêu tham số trước khi chia tập. Dẫn đến việc thông tin tập Test bị rò rỉ vào quá trình học, làm kết quả đánh giá cao bất thường và không phản ánh đúng thực tế.
- **Biện pháp ngăn chặn triệt để**:
  1. Thực hiện chia tập `StratifiedShuffleSplit` hoặc `train_test_split(..., stratify=y)` ngay bước đầu tiên.
  2. Tập Test được lưu vào file riêng (`data/test.csv`) và **tuyệt đối không được mở ra** trong suốt quá trình EDA, Feature Engineering và Tuning siêu tham số.
  3. Mọi phép biến đổi phải nằm trong `Pipeline` của `scikit-learn`, đảm bảo chỉ gọi hàm `fit` trên tập Train và chỉ `transform` trên tập Test.

### 6.2. Rủi ro Quá khớp (Overfitting)
- **Bản chất rủi ro**: Cây quyết định phát triển quá sâu để chia đúng tất cả các mẫu ngoại lai (outliers) hoặc nhiễu trong tập Train, dẫn đến phương sai cực lớn (High Variance).
- **Biện pháp ngăn chặn triệt để**:
  1. Đo lường khoảng cách giữa Train Score và Validation Score.
  2. Áp dụng kỹ thuật Cost-Complexity Pruning (tỉa hậu kỳ) với việc chọn tham số $\alpha$ (`ccp_alpha`) thông qua K-Fold CV.
  3. Giới hạn `max_depth`, `min_samples_leaf`, và sử dụng mô hình Random Forest để giảm phương sai.

### 6.3. Rủi ro Mất tính tái lập (Lack of Reproducibility)
- **Bản chất rủi ro**: Kết quả thay đổi sau mỗi lần chạy lại do các yếu tố ngẫu nhiên trong việc chia tập, lấy mẫu bootstrap của Random Forest, hoặc sự khác biệt giữa phiên bản thư viện.
- **Biện pháp ngăn chặn triệt để**:
  1. Cố định biến toàn cục `RANDOM_STATE = 42` (hoặc một seed thống nhất) cho toàn bộ các hàm chia tập, cây quyết định và rừng ngẫu nhiên.
  2. Cố định danh mục thư viện kèm phiên bản chính xác trong `requirements.txt`.
  3. Viết script chạy tự động từ đầu đến cuối (`run_pipeline.py`) cho phép một máy tính mới chỉ cần chạy 1 lệnh là tái hiện đúng 100% kết quả và đồ thị.

### 6.4. Rủi ro Ứng dụng y sinh sai mục đích (Misuse in Clinical Diagnosis)
- **Bản chất rủi ro**: Người dùng hiểu nhầm ứng dụng là công cụ chẩn đoán y tế chuyên nghiệp.
- **Biện pháp ngăn chặn triệt để**:
  1. Gắn Banner cảnh báo màu đỏ/vàng trên mọi trang giao diện Web: *"Hệ thống phục vụ mục đích minh họa học thuật. Tuyệt đối không dùng cho chẩn đoán lâm sàng."*
  2. Trong API response luôn trả về trường metadata `"disclaimer": "Academic demo only. Not for clinical diagnostic use."`.

---

## 7. ĐỀ XUẤT CÔNG NGHỆ VÀ LÝ DO KỸ THUẬT

1. **Ngôn ngữ cốt lõi: Python 3.10+**
   - Tiêu chuẩn công nghiệp cho Khoa học dữ liệu và Học máy; cộng đồng lớn, hỗ trợ phong phú.
2. **Xử lý & Phân tích: `pandas` & `numpy`**
   - Cấu trúc DataFrame mạnh mẽ, hỗ trợ đọc, làm sạch và tính toán vector hóa nhanh chóng.
3. **Mô hình hóa Học máy: `scikit-learn`**
   - Cung cấp triển khai chuẩn mực của DecisionTreeClassifier (hỗ trợ trích xuất decision tree structure, decision path và `cost_complexity_pruning_path`), RandomForestClassifier, K-Fold CV, Pipeline và các metrics đánh giá.
4. **Trực quan hóa Thực nghiệm: `matplotlib` & `seaborn`**
   - Đảm bảo chất lượng xuất ảnh đồ thị độ phân giải cao (300 DPI) cho báo cáo học thuật và slide.
5. **Backend Serving: `FastAPI` + `Uvicorn` + `Pydantic`**
   - Tốc độ thực thi cao (dựa trên ASGI), cú pháp khai báo hiện đại với Type Hints, tự động xác thực schema đầu vào bằng Pydantic và tự động sinh tài liệu chuẩn OpenAPI (Swagger UI).
6. **Frontend Giao diện: `ReactJS` + `Vanilla CSS`**
   - Khả năng xây dựng Single Page Application linh hoạt, tương tác mượt mà, quản lý trạng thái trực quan cho phép bóc tách chi tiết cây quyết định (decision path inspector) mà không cần reload trang.
