# PROJECT 16: MINH HỌA PHÂN LOẠI KHỐI U VÚ BẰNG CÂY VÀ RỪNG

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Framework](https://img.shields.io/badge/Backend-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-ReactJS-cyan.svg)](https://react.dev/)

> **CẢNH BÁO PHI LÂM SÀNG (NON-CLINICAL DISCLAIMER):**  
> Dự án này hoàn toàn phục vụ mục đích nghiên cứu học thuật trong khuôn khổ môn học **Học máy cơ bản** (Đại Học Công Nghệ Kỹ Thuật Hưng Yên / PGS.TS. Nguyễn Văn Hậu).  
> **TUYỆT ĐỐI KHÔNG SỬ DỤNG CHO MỤC ĐÍCH CHẨN ĐOÁN Y TẾ LÂM SÀNG THỰC TẾ.** Không sử dụng dữ liệu bệnh nhân thực chưa kiểm duyệt.

---

## 1. GIỚI THIỆU DỰ ÁN
Dự án tập trung minh họa cách các thuật toán **Cây quyết định (Decision Tree)**, kỹ thuật **Cắt tỉa (Pruning - Pre-pruning & Post-pruning via `ccp_alpha`)** và **Rừng ngẫu nhiên (Random Forest)** xử lý các đặc trưng hình học nhân tế bào từ bộ dữ liệu **Breast Cancer Wisconsin (Diagnostic) - WDBC**.

### Câu hỏi nghiên cứu:
1. Việc cắt tỉa cây quyết định (Decision Tree Pruning) giúp cải thiện khả năng tổng quát hóa (Generalization) và giảm hiện tượng quá khớp (Overfitting) như thế nào?
2. Cơ chế lấy mẫu có hoàn lại (Bootstrap) và không gian đặc trưng ngẫu nhiên (Random Feature Subspace) của Rừng ngẫu nhiên (Random Forest) giúp giảm phương sai (Variance Reduction) và tăng độ ổn định ra sao?

---

## 2. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
DoHuuQuocAnh_HocMayCoBan/
├── .gitignore                     # Cấu hình bỏ qua venv, cache, file tạm, node_modules
├── requirements.txt               # Danh sách thư viện và phiên bản tương thích
├── README.md                      # Tài liệu tổng quan và hướng dẫn vận hành
├── data.csv                       # Tệp dữ liệu gốc WDBC từ UCI (569 dòng, 32 cột)
│
├── data/                          # Dữ liệu phục vụ huấn luyện và kiểm thử
│   ├── .gitkeep
│   ├── train.csv                  # Tập huấn luyện (80%, Stratified Split) - Sinh ở Nhiệm vụ 03
│   └── test.csv                   # Tập kiểm thử độc lập (20%) - Đóng băng tuyệt đối
│
├── backend/                       # Toàn bộ mã nguồn phía máy chủ và mô hình hóa
│   ├── src/                       # Pipeline Học máy (Xử lý dữ liệu, Train, Đánh giá)
│   │   ├── __init__.py
│   │   ├── config.py              # Cấu hình seed toàn cục (42), đường dẫn, danh sách đặc trưng
│   │   ├── data.py                # Xử lý, làm sạch và chia tách dữ liệu Stratified (Nhiệm vụ 03)
│   │   ├── train.py               # Pipeline huấn luyện, K-Fold CV & Cắt tỉa (Nhiệm vụ 04)
│   │   └── evaluate.py            # Thực hiện 4 thí nghiệm bắt buộc & Phân tích FN (Nhiệm vụ 05)
│   ├── app/                       # Dịch vụ API Serving (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py                # Endpoints phục vụ dự đoán và giải thích Decision Path
│   │   └── schemas.py             # Pydantic schemas kiểm tra kiểu và miền giá trị
│   └── models/                    # Lưu trữ artifacts mô hình đã đóng băng
│       ├── .gitkeep
│       ├── baseline_dummy.joblib
│       ├── dt_unpruned.joblib
│       ├── dt_pruned.joblib
│       ├── rf_model.joblib
│       └── train_stats.json       # Thống kê min/max/mean phục vụ validation
│
├── frontend/                      # Giao diện người dùng Web (ReactJS)
│   ├── .gitkeep
│   ├── public/
│   └── src/                       # Các components: Banner, DecisionPathView, Dashboard
│
├── reports/                       # Báo cáo thực nghiệm và trực quan hóa
│   ├── figures/                   # 4 biểu đồ thí nghiệm bắt buộc (300 DPI)
│   │   ├── .gitkeep
│   │   ├── exp1_depth_curve.png
│   │   ├── exp2_model_comparison.png
│   │   ├── exp3_confusion_matrix.png
│   │   └── exp4_feature_stability.png
│   └── metrics_summary.json       # Bảng số liệu hiệu năng đóng băng trên Test set
│
├── docs/                          # Hồ sơ tài liệu kỹ thuật và học thuật
│   ├── requirements.md            # Đặc tả yêu cầu dự án, RTM, phân tích rủi ro kỹ thuật
│   ├── project_plan.md            # Kế hoạch 6 tuần, phân công 2 thành viên, rubric 100 điểm
│   └── data_dictionary.md         # Bảng mô tả 30 đặc trưng nhân tế bào FNA WDBC
│
└── tests/                         # Kiểm thử tự động (Unit Tests & Integration Tests)
    ├── __init__.py
    ├── test_data.py               # Kiểm tra không rò rỉ dữ liệu, đúng schema
    ├── test_models.py             # Kiểm tra kích thước output, tính xác suất
    └── test_api.py                # Kiểm tra endpoint FastAPI, mã lỗi 400/422
```

---

## 3. THIẾT LẬP MÔI TRƯỜNG VÀ CÀI ĐẶT

### 3.1. Yêu cầu hệ thống
- Hệ điều hành: Windows / Linux / macOS
- Python: Phiên bản **3.10 trở lên** (Khuyến nghị 3.12)
- Node.js: Phiên bản **18.x trở lên** (cho Frontend ReactJS)

### 3.2. Cài đặt môi trường Python (Backend)
1. **Tạo môi trường ảo:**
   ```powershell
   python -m venv .venv
   ```

2. **Kích hoạt môi trường ảo:**
   - Trên Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Trên Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```

3. **Cài đặt các gói phụ thuộc:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## 4. HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM (REPRODUCIBILITY)
Dự án cố định biến `RANDOM_STATE = 42` xuyên suốt toàn bộ pipeline để đảm bảo kết quả có thể tái lập 100%:

```powershell
# Bước 1: Tiền xử lý dữ liệu và chia tập Stratified
python backend/src/data.py

# Bước 2: Huấn luyện Baseline, Cây quyết định cắt tỉa và Rừng ngẫu nhiên
python backend/src/train.py

# Bước 3: Chạy 4 thí nghiệm bắt buộc và xuất biểu đồ
python backend/src/evaluate.py

# Bước 4: Khởi chạy API Serving FastAPI
uvicorn backend.app.main:app --reload --port 8000
```

```powershell
# Bước 5: Khởi chạy ứng dụng ReactJS (Frontend)
cd frontend
npm run dev
```
---

## 5. THÀNH VIÊN VÀ PHÂN CÔNG THỰC HIỆN
- **Lớp**: 12523W.1 — Môn: Học máy cơ bản
- **Giảng viên hướng dẫn**: PGS.TS. Nguyễn Văn Hậu
- **Sinh viên 1**: Đỗ Hữu Quốc Anh (Dữ liệu, Pipeline Huấn luyện, Backend API FastAPI)
- **Sinh viên 2**: Thành viên phối hợp (EDA, 4 Thí nghiệm & Phân tích lỗi, Frontend ReactJS)
