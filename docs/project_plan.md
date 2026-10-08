# KẾ HOẠCH TRIỂN KHAI VÀ QUẢN LÝ DỰ ÁN (PROJECT PLAN)
## Đề tài: Project 16 — Minh họa phân loại khối u vú bằng cây và rừng
**Học phần**: Học máy cơ bản (12523W.1) — **Giảng viên**: PGS.TS. Nguyễn Văn Hậu  
**Quy mô**: 06 tuần — **Nhân sự**: Nhóm 02 sinh viên (SV1 & SV2)  

---

## 1. KẾ HOẠCH CHI TIẾT 06 TUẦN VÀ CÁC CỔNG KIỂM SOÁT (GATES)

```
       TUẦN 1                  TUẦN 2                  TUẦN 3
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Khởi tạo, Đề cương│───>│ Làm sạch, Split  │───>│ Huấn luyện Model,│
│  & Hồ sơ dữ liệu │    │ & EDA trên Train │    │ Tối ưu & Cắt tỉa │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
      [Gate 1]                [Gate 2]                [Gate 3]
         │                       │                       │
         v                       v                       v
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  4 Thí nghiệm &  │───>│ Đóng gói Serving │───>│ Hoàn thiện Docs, │
│ Đóng băng Test   │    │  FastAPI & Web   │    │ Slide & Rehearsal│
└──────────────────┘    └──────────────────┘    └──────────────────┘
       TUẦN 4                  TUẦN 5                  TUẦN 6
```

### TUẦN 1: KHỞI TẠO DỰ ÁN, ĐẶC TẢ BÀI TOÁN & THIẾT LẬP DỮ LIỆU
- **Mục tiêu**: Chốt phạm vi bài toán, thiết lập cấu trúc mã nguồn chuẩn mực, lập hồ sơ dữ liệu ban đầu và thống nhất kế hoạch thực hiện.
- **Công việc chi tiết**:
  - **SV1**: Thiết lập kho mã nguồn Git, xây dựng cấu trúc thư mục phân tầng (`data/`, `src/`, `models/`, `app/`, `frontend/`, `reports/`, `docs/`); cấu hình `requirements.txt`.
  - **SV2**: Viết `docs/requirements.md` và `docs/project_plan.md`; lập `data/README.md` ghi nhận nguồn gốc, giấy phép CC BY 4.0 và trích dẫn chuẩn UCI.
  - **Cả hai**: Soạn thảo bảng từ điển dữ liệu `data_dictionary.md` cho 30 đặc trưng nhân tế bào FNA; thống nhất biến toàn cục `RANDOM_STATE = 42`.
- **Minh chứng đầu ra (Artifacts)**:
  - Tài liệu đặc tả yêu cầu `docs/requirements.md` và kế hoạch `docs/project_plan.md`.
  - Hồ sơ dữ liệu `data/README.md` và `docs/data_dictionary.md`.
  - Khung thư mục dự án và `requirements.txt`.
- **Cổng kiểm soát 1 (Gate 1 — Data & Scope Check)**:
  - *Tiêu chí*: Nguồn dữ liệu hợp pháp, schema 30 đặc trưng đầy đủ, quy tắc chia tập và chống rò rỉ dữ liệu được cam kết bằng văn bản.

---

### TUẦN 2: LÀM SẠCH, CHIA TẬP STRATIFIED & EDA TRÊN TẬP HUẤN LUYỆN
- **Mục tiêu**: Kiểm tra chất lượng dữ liệu, thực hiện chia tập Stratified Train/Test độc lập, đóng băng tập Test và khám phá dữ liệu (EDA) trên tập Train.
- **Công việc chi tiết**:
  - **SV1**: Viết module `src/data.py` thực hiện: đọc `data.csv`, loại bỏ `id`, mã hóa nhãn $M=1, B=0$, kiểm tra trùng lặp/missing, thực hiện `train_test_split(..., stratify=y, test_size=0.2, random_state=42)`. Lưu `data/train.csv` và `data/test.csv`.
  - **SV2**: Thực hiện notebook/script EDA chỉ trên `data/train.csv`: phân tích thống kê mô tả, phân bố các đặc trưng giữa 2 nhóm B và M, biểu đồ ma trận tương quan giữa 10 đặc trưng cơ bản.
  - **Cả hai**: Xây dựng mô hình Baseline đầu tiên (`DummyClassifier`) và `DecisionTreeClassifier` chưa giới hạn độ sâu (Unpruned) trên tập Train để đo lường điểm cơ sở.
- **Minh chứng đầu ra**:
  - Module `src/data.py` và hai tệp dữ liệu đã phân chia `data/train.csv`, `data/test.csv`.
  - Báo cáo chất lượng dữ liệu và biểu đồ EDA (lưu tại `reports/figures/eda_*.png`).
  - Báo cáo kết quả sơ bộ của Baseline Dummy và Unpruned Tree trên tập Validation/CV.
- **Cổng kiểm soát 2 (Gate 2 — Split & Baseline Check)**:
  - *Tiêu chí*: Tập Test bị cô lập hoàn toàn, không có tính toán tiền xử lý nào chạm vào Test, tỷ lệ phân bố nhãn 357B : 212M được giữ nguyên trên cả 2 tập.

---

### TUẦN 3: XÂY DỰNG PIPELINE, HUẤN LUYỆN MÔ HÌNH VÀ CẮT TỈA CÂY
- **Mục tiêu**: Hoàn thiện pipeline huấn luyện, tối ưu hóa siêu tham số bằng Stratified K-Fold CV, thực hiện cắt tỉa cây (pruning) và huấn luyện Rừng ngẫu nhiên.
- **Công việc chi tiết**:
  - **SV1**: Viết module `src/train.py`. Xây dựng hàm tìm kiếm siêu tham số cho Cây quyết định: khảo sát dải `max_depth` (pre-pruning) và trích xuất đường dẫn độ phức tạp chi phí `cost_complexity_pruning_path` để tìm $\alpha$ tối ưu (`ccp_alpha` - post-pruning) thông qua 5-Fold Stratified CV.
  - **SV2**: Triển khai huấn luyện `RandomForestClassifier` trong `src/train.py`: thiết lập `n_estimators`, `max_features='sqrt'`, khảo sát điểm số CV qua OOB (Out-of-Bag) hoặc Stratified K-Fold.
  - **Cả hai**: Đóng gói các mô hình tốt nhất vào `models/` (`baseline_dummy.joblib`, `dt_unpruned.joblib`, `dt_pruned.joblib`, `rf_model.joblib`) kèm tệp metadata `models/train_stats.json` lưu giá trị min, max, mean phục vụ validation API sau này.
- **Minh chứng đầu ra**:
  - Module huấn luyện hoàn chỉnh `src/train.py`.
  - Các artifact mô hình trong thư mục `models/`.
  - Nhật ký ghi nhận kết quả Cross-Validation vòng 1 của các mô hình ứng viên.
- **Cổng kiểm soát 3 (Gate 3 — Candidate Models & Pipeline Check)**:
  - *Tiêu chí*: Pipeline tự động hóa, lưu trữ mô hình chuẩn định dạng, siêu tham số được chọn 100% bằng Cross-Validation trên Train, tập Test vẫn chưa được đụng đến.

---

### TUẦN 4: THỰC HIỆN 4 THÍ NGHIỆM BẮT BUỘC & ĐÁNH GIÁ TẬP TEST
- **Mục tiêu**: Thực thi trọn vẹn 4 thí nghiệm bắt buộc theo yêu cầu của giảng viên, mở khóa tập Test một lần duy nhất để kết luận hiệu năng, và phân tích chuyên sâu các ca lỗi False Negative.
- **Công việc chi tiết**:
  - **SV1**: Viết `src/evaluate.py` và sinh kết quả:
    - **Thí nghiệm 1**: Vẽ đồ thị đường cong học tập Train vs CV Score theo `max_depth` từ 1 đến 20 (`exp1_depth_curve.png`).
    - **Thí nghiệm 2**: Lập bảng so sánh 4 mô hình (Dummy, Unpruned DT, Pruned DT, Random Forest) trên tập Test độc lập: Recall(M), Precision(M), F1-Score, ROC-AUC (`exp2_model_comparison.png`).
  - **SV2**: Viết kịch bản thí nghiệm và phân tích lỗi:
    - **Thí nghiệm 3**: Trực quan hóa Ma trận nhầm lẫn (Confusion Matrix) của các mô hình; trích xuất chi tiết từng mẫu thử nghiệm bị dự đoán sai (đặc biệt là False Negative), đối chiếu các đặc trưng của mẫu đó với ngưỡng phân chia của cây (`exp3_confusion_matrix.png`).
    - **Thí nghiệm 4**: Khảo sát độ ổn định của Feature Importance qua 10 random seeds khác nhau đối với cả Cây quyết định và Rừng ngẫu nhiên; vẽ biểu đồ Boxplot độ biến thiên (`exp4_feature_stability.png`).
  - **Cả hai**: Đóng băng toàn bộ số liệu đánh giá vào `reports/metrics_summary.json`; hoàn thiện nháp tài liệu Model Card (`docs/model_card.md`).
- **Minh chứng đầu ra**:
  - 4 biểu đồ thí nghiệm chất lượng cao tại `reports/figures/`.
  - Tệp kết quả đóng băng `reports/metrics_summary.json`.
  - Tài liệu phân tích lỗi False Negative và dự thảo Model Card.
- **Cổng kiểm soát 4 (Gate 4 — Experiments & Error Analysis Freeze)**:
  - *Tiêu chí*: 4 thí nghiệm có đủ bằng chứng thực nghiệm, số liệu trung thực, không suy diễn quan hệ nhân quả từ feature importance, tập Test chỉ chạy 1 lần duy nhất để chốt kết quả.

---

### TUẦN 5: ĐÓNG GÓI API FASTAPI VÀ PHÁT TRIỂN GIAO DIỆN REACTJS
- **Mục tiêu**: Xây dựng dịch vụ phục vụ dự đoán API hoàn chỉnh và giao diện Web tương tác đáp ứng đầy đủ yêu cầu của môn học.
- **Công việc chi tiết**:
  - **SV1 (Backend Serving)**: Xây dựng ứng dụng FastAPI trong `app/`:
    - `app/schemas.py`: Khai báo Pydantic BaseModel cho 30 đặc trưng với kiểm tra kiểu và miền giá trị (boundary validation).
    - `app/main.py`: Endpoint `POST /api/predict` nhận 30 đặc trưng, nạp model từ `models/`, tính toán nhãn, xác suất và trích xuất đường đi quyết định (Decision Path: danh sách các nút, điều kiện $\le$ hoặc $>$, và kết quả rẽ nhánh).
    - Viết unit tests kiểm thử API trong `tests/test_api.py`.
  - **SV2 (Frontend UI)**: Xây dựng ứng dụng ReactJS trong `frontend/`:
    - Tạo Banner cảnh báo phi lâm sàng (Non-clinical Disclaimer) cố định.
    - Xây dựng 3 màn hình:
      1. *Giới thiệu & Phạm vi*: Bối cảnh, mô tả đặc trưng tế bào, thông tin bộ dữ liệu WDBC và Model Card.
      2. *Thao tác chính & Vết phân nhánh*: Cho phép nạp mẫu có sẵn (Benign demo / Malignant demo) hoặc tự nhập 30 thông số; hiển thị xác suất và sơ đồ tương tác Decision Path.
      3. *Dashboard Thực nghiệm*: Trực quan hóa kết quả 4 thí nghiệm và ma trận nhầm lẫn.
  - **Cả hai**: Tích hợp Frontend - Backend qua Axios/Fetch, xử lý hiển thị thông báo lỗi khi API trả về mã lỗi 422/400.
- **Minh chứng đầu ra**:
  - Mã nguồn Backend FastAPI (`app/`) và Frontend ReactJS (`frontend/`).
  - Kịch bản chạy một lệnh (ví dụ `run_demo.bat` hoặc hướng dẫn trong `README.md`).
  - Bộ test API tự động chạy qua `pytest`.
- **Cổng kiểm soát 5 (Gate 5 — Web & Serving Integration Check)**:
  - *Tiêu chí*: Luồng hoạt động end-to-end trơn tru; API từ chối dữ liệu ngoài miền hợp lệ; banner cảnh báo hiển thị rõ ràng; đường đi của cây được minh họa chính xác.

---

### TUẦN 6: KIỂM THỬ TÁI LẬP, HOÀN THIỆN BÁO CÁO VÀ SLIDE THUYẾT TRÌNH
- **Mục tiêu**: Kiểm chứng khả năng chạy lại trên môi trường sạch, hoàn thiện báo cáo học thuật từ 15–25 trang, chuẩn bị slide và tập dượt thuyết trình.
- **Công việc chi tiết**:
  - **SV1**: Kiểm thử tái lập (Reproducibility check) trên một máy tính hoặc môi trường ảo hoàn toàn mới; hoàn thiện `README.md` với hướng dẫn cài đặt và chạy từng bước; hỗ trợ viết phần Kỹ thuật & Thực nghiệm trong báo cáo.
  - **SV2**: Chủ trì soạn thảo Báo cáo kết thúc học phần (15–25 trang theo chuẩn đề cương bắt buộc); thiết kế bộ slide thuyết trình (10–12 slide tóm lược bài toán, phương pháp, 4 thí nghiệm và demo).
  - **Cả hai**: Soạn thảo biên bản phân công công việc, nhật ký thực hiện 6 tuần; chuẩn bị và tập dượt thuyết trình vấn đáp cá nhân (rehearsal 5–7 phút demo, 5–7 phút phản biện).
- **Minh chứng đầu ra**:
  - Báo cáo chính thức định dạng DOCX và PDF (`docs/Bao_cao_Project_16.pdf`).
  - Slide thuyết trình (`docs/Slide_Project_16.pptx`).
  - Kho mã nguồn hoàn thiện, sạch sẽ, tài liệu hướng dẫn đầy đủ.
- **Cổng kiểm soát 6 (Gate 6 — Final Acceptance & Submission)**:
  - *Tiêu chí*: Đáp ứng 100% checklist theo rubric đánh giá 100 điểm của giảng viên; sẵn sàng cho buổi bảo vệ chính thức.

---

## 2. BẢNG PHÂN CÔNG TRÁCH NHIỆM CÂN BẰNG GIỮA HAI THÀNH VIÊN

Theo yêu cầu nghiêm ngặt của giảng viên: *Mỗi người phải có đóng góp đáng kể ở cả phần dữ liệu/mô hình và phần web/báo cáo; không chia cứng một người chỉ viết báo cáo.*

| Hạng mục công việc | Trách nhiệm chính (Lead) | Trách nhiệm phối hợp / Review | Tỷ trọng ước tính |
| :--- | :---: | :---: | :---: |
| **Hồ sơ dữ liệu & Quản lý Git** | SV1 | SV2 | 50% - 50% |
| **Xử lý dữ liệu & Chống Leakage (`src/data.py`)** | SV1 | SV2 | 60% - 40% |
| **Khám phá dữ liệu EDA & Baseline** | SV2 | SV1 | 60% - 40% |
| **Pipeline Mô hình hóa & Cắt tỉa (`src/train.py`)** | SV1 | SV2 | 60% - 40% |
| **Thiết kế & Chạy 4 Thí nghiệm (`src/evaluate.py`)** | SV2 | SV1 | 60% - 40% |
| **Xây dựng API Backend (FastAPI, Serving, Validation)** | SV1 | SV2 | 65% - 35% |
| **Xây dựng Frontend Giao diện (ReactJS, UI/UX, Chart)** | SV2 | SV1 | 65% - 35% |
| **Tài liệu học thuật (Báo cáo 15–25 trang)** | SV2 | SV1 | 50% - 50% |
| **Slide thuyết trình & Tập dượt Rehearsal** | Cả hai | Cả hai | 50% - 50% |

---

## 3. RUBRIC ĐÁNH GIÁ 100 ĐIỂM VÀ ĐỐI CHIẾU NỘI BỘ

| Tiêu chí | Trọng số | Yêu cầu đạt điểm tối đa | Chiến lược đảm bảo điểm của Nhóm |
| :--- | :---: | :--- | :--- |
| **1. Bài toán & phạm vi** | 8 điểm | Định nghĩa câu hỏi đo được; đơn vị quan sát, đầu vào, đầu ra, tiêu chí thành công rõ. | Xác lập rõ 30 đặc trưng FNA, phân loại nhị phân M/B, tiêu chí ưu tiên Recall(M) tránh sót ca bệnh. |
| **2. Dữ liệu & EDA** | 12 điểm | Nguồn/giấy phép rõ; data dictionary; chất lượng dữ liệu; EDA định hướng quyết định. | Bổ sung đầy đủ license CC BY 4.0, data dictionary, báo cáo missing=0, phân bố B:357 / M:212. |
| **3. Split, leakage & tái lập** | 15 điểm | Stratified split; pipeline đúng; seed cố định; test độc lập; không có shortcut. | Tách tập Test ngay từ đầu; dùng Pipeline Scikit-learn; cố định `random_state=42`; test chỉ chạy 1 lần. |
| **4. Mô hình & thí nghiệm** | 18 điểm | Baseline Dummy, Unpruned Tree, Pruned Tree, Random Forest; thiết kế công bằng; tuning K-Fold. | Chạy đủ 4 mô hình; tuning `ccp_alpha` và `max_depth` qua K-Fold CV; so sánh trên cùng phân vùng dữ liệu. |
| **5. Đánh giá & phân tích lỗi** | 18 điểm | Metric đúng (Recall, Precision, ROC-AUC); biểu đồ chuẩn; phân tích sâu False Negative; không suy diễn nhân quả. | Báo cáo chi tiết ma trận nhầm lẫn; phân tích từng ca False Negative; kiểm tra độ ổn định đa seed. |
| **6. Web & API** | 12 điểm | Luồng end-to-end; validation chặt; mã lỗi hợp lý; UI 3 màn hình; disclaimer y tế; decision path. | FastAPI + ReactJS; Pydantic validation chặn ngoài miền; Banner cảnh báo; trích xuất vết rẽ nhánh. |
| **7. Mã nguồn & bàn giao** | 7 điểm | Cấu trúc chuẩn; README chạy được từ máy mới; `requirements.txt`; unit tests. | Cấu trúc phân tầng; kịch bản cài đặt tự động 1 lệnh; unit tests cho pipeline và API. |
| **8. Báo cáo, trình bày & nhóm** | 10 điểm | Báo cáo logic 15–25 trang; slide đẹp; trả lời vấn đáp cá nhân tốt; commit cân bằng. | Phân công đều; tài liệu DOCX/PDF chỉn chu; slide trực quan; nắm vững bản chất toán học của cây & rừng. |
| **TỔNG ĐIỂM** | **100** | **Mục tiêu đạt từ 90–100 điểm (Xuất sắc)** | **Tuân thủ tuyệt đối quy tắc không có rò rỉ dữ liệu để tránh bị giới hạn trần 50 điểm.** |

---

## 4. QUY TRÌNH KIỂM THỬ VÀ TÁI LẬP (REPRODUCIBILITY PROTOCOL)

1. **Khởi tạo môi trường ảo sạch**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. **Chạy pipeline dữ liệu và huấn luyện từ đầu**:
   ```powershell
   python src/data.py
   python src/train.py
   python src/evaluate.py
   ```
3. **Kiểm tra tính tương thích của kết quả**:
   - Tệp `reports/metrics_summary.json` phải tạo ra đúng các chỉ số đã lưu.
   - Các biểu đồ trong `reports/figures/` được sinh mới hoàn toàn nhưng không thay đổi hình dạng xu hướng.
4. **Khởi động ứng dụng phục vụ**:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
