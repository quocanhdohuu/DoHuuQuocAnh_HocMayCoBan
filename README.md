# PROJECT 16: PHÂN LOẠI KHỐI U VÚ BẰNG CÂY QUYẾT ĐỊNH VÀ RỪNG NGẪU NHIÊN
## (Breast Cancer Wisconsin Diagnostic Classification with Decision Trees and Random Forests)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%2019%20+%20Vite-61DAFB.svg)](https://react.dev/)
[![Tests](https://img.shields.io/badge/Tests-72%2F72%20Passed-success.svg)](file:///tests)
[![Dataset](https://img.shields.io/badge/Dataset-UCI%20WDBC-orange.svg)](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)

> **CẢNH BÁO PHI LÂM SÀNG (NON-CLINICAL ACADEMIC DISCLAIMER):**  
> Dự án này hoàn toàn phục vụ mục đích nghiên cứu học thuật và giáo dục trong khuôn khổ học phần **Học máy cơ bản** (Mã học phần: 12523W.1) tại **Trường Đại Học Công Nghệ Kỹ Thuật Hưng Yên**.  
> **TUYỆT ĐỐI KHÔNG SỬ DỤNG CHO MỤC ĐÍCH CHẨN ĐOÁN Y TẾ LÂM SÀNG THỰC TẾ.** Hệ thống không thay thế các phán đoán chuyên môn của bác sĩ giải phẫu bệnh và chuyên gia y tế.

---

## 1. TỔNG QUAN DỰ ÁN

Dự án nghiên cứu, thực nghiệm và triển khai phân loại nhị phân u vú lành tính (Benign - `B`) và ác tính (Malignant - `M`) dựa trên bộ dữ liệu **Wisconsin Diagnostic Breast Cancer (WDBC)** gồm 569 mẫu sinh thiết chọc hút kim nhỏ (FNA) với 30 đặc trưng số hóa tế bào học.

### Điểm nhấn phương pháp luận & Kết quả:
1. **Chống rò rỉ dữ liệu tuyệt đối (Zero Data Leakage)**: Phân chia ngẫu nhiên phân tầng 3 nhánh độc lập (Train 398 mẫu - 70%, Validation 85 mẫu - 15%, Test 86 mẫu - 15%), niêm phong tập Test đến bước đánh giá cuối cùng.
2. **Khắc phục triệt để Overfitting của Cây quyết định**: Chứng minh hiện tượng quá khớp theo độ sâu cây (Thí nghiệm 1); ứng dụng tỉa cành Cost-Complexity Pruning ($ccp\_\alpha = 0.015$) giảm $66.7\%$ số nút lá mà tăng độ chính xác từ $91.76\%$ lên $94.12\%$.
3. **Mô hình tối ưu Rừng ngẫu nhiên (Random Forest)**: 100 cây con, `max_features=0.3`, triệt tiêu phương sai, duy trì thứ hạng đặc trưng ổn định qua nhiều random seeds ($\rho > 0.98$).
4. **Hiệu năng xuất sắc trên tập Test độc lập ($N=86$)**:
   - **Accuracy**: **$98.84\%$** ($85/86$ ca đúng) — Khoảng tin cậy Wilson 95%: **$[93.70\%, 99.79\%]$**.
   - **Precision Malignant**: **$100.00\%$** ($31/31$ ca đúng) — **$0$ ca báo động giả (FP = 0)**.
   - **Recall Malignant**: **$96.88\%$** ($31/32$ ca ung thư) — **Chỉ bỏ sót đúng 1 ca ác tính (FN = 1)**.
   - **ROC-AUC Score**: **$0.9954$**.
5. **Phân tích lỗi khoa học**: Điều tra tường tận ca FN duy nhất (Mẫu #23), chỉ ra nguyên nhân khách quan do khối u nhỏ nằm tại vùng chồng lấn biên giới hình thái học tự nhiên giữa hai lớp.

---

## 2. HỒ SƠ TÀI LIỆU TOÀN DIỆN (DOCUMENTATION LINKS)

- 📘 **Báo cáo học thuật chính thức (11 Chương, ~25 trang)**: [docs/final_report.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/docs/final_report.md)
- 🎤 **Hồ sơ thuyết trình & Bàn giao (Slides, Demo, Kịch bản, Vấn đáp, Rubric 100 điểm)**: [docs/presentation_and_handover.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/docs/presentation_and_handover.md)
- 🗂️ **Thẻ mô hình (Model Card - Mitchell et al., 2019)**: [reports/model_card.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/model_card.md)
- 📊 **Thẻ dữ liệu (Data Card - Gebru et al., 2021)**: [reports/data_card.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/data_card.md)
- 🔍 **Báo cáo phân tích lỗi chi tiết**: [reports/error_analysis.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/error_analysis.md)
- 🌐 **Tài liệu đặc tả API RESTful**: [docs/api_documentation.md](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/docs/api_documentation.md)

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
DoHuuQuocAnh_HocMayCoBan/
├── .venv/                         # Môi trường ảo Python 3.12
├── data/
│   ├── raw/                       # Dữ liệu gốc wdbc.data từ UCI
│   └── processed/                 # Dữ liệu phân tầng đã chia tách: train.csv, val.csv, test.csv
├── backend/
│   ├── app/                       # Ứng dụng máy chủ FastAPI
│   │   ├── main.py                # REST API Endpoints: /api/demo-classify, /api/reports/dashboard
│   │   └── schemas.py             # Pydantic schemas kiểm tra chặt chẽ 30 đặc trưng
│   ├── models/                    # Artifacts mô hình học máy đóng gói nhị phân (.joblib, .json)
│   │   ├── final_model_config.json# Cấu hình siêu tham số đóng băng
│   │   ├── wdbc_pipeline.joblib   # Pipeline sản xuất
│   │   └── rf_final.joblib        # Mô hình Random Forest chính thức
│   ├── src/                       # Các kịch bản huấn luyện, thí nghiệm độc lập
│   │   ├── prepare_data.py        # Tiền xử lý và chia tập 70/15/15
│   │   ├── unpruned_tree.py       # Huấn luyện cây tự do & Thí nghiệm 1 (Độ sâu)
│   │   ├── prune_tree.py          # Thí nghiệm tỉa cành Cost-Complexity Pruning
│   │   ├── train_random_forest.py # Huấn luyện Random Forest & Thí nghiệm 4 (Seed stability)
│   │   ├── compare_models.py      # Thí nghiệm 2 (Đối sánh 4 mô hình trên Val)
│   │   └── evaluate_final_test.py # Đánh giá mở niêm phong Test set độc lập
│   └── requirements.txt           # Danh mục thư viện Python
├── frontend/                      # Giao diện người dùng React 19 + Vite
│   ├── src/
│   │   ├── pages/                 # Overview, Classification, Dashboard
│   │   ├── components/            # Layout, Header, Navigation, StatCards, Charts
│   │   └── services/api.js        # Dịch vụ gọi REST API
│   └── package.json               # Cấu hình phụ thuộc Node.js
├── reports/                       # Báo cáo thực nghiệm, Model Card, Data Card
│   ├── figures/                   # 20 biểu đồ chất lượng cao trực quan hóa thực nghiệm
│   └── final_test_evaluation.json # Kết quả số liệu kiểm thử đóng băng
├── docs/                          # Báo cáo học thuật 11 chương và hồ sơ bàn giao
├── tests/                         # Bộ kiểm thử tự động (72 tests)
└── README.md                      # Hướng dẫn tổng thể
```

---

## 4. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH

### 4.1. Khởi tạo môi trường ảo Python
```powershell
# 1. Kích hoạt môi trường ảo
.venv\Scripts\Activate.ps1

# 2. Cài đặt các thư viện phụ thuộc
pip install -r backend/requirements.txt
```

### 4.2. Khởi chạy bộ kiểm thử tự động (Automated Test Suite)
Dự án tích hợp 72 ca kiểm thử tự động (Unit test, Validation test, Integration test):
```powershell
python -m pytest -v
```
*(Kết quả: 72 passed, 100% thành công)*

### 4.3. Khởi chạy hệ sinh thái Web & API
# Cửa sổ dòng lệnh 1: Khởi chạy Backend API FastAPI (Cổng 8000)
source .venv/Scripts/activate
uvicorn backend.app.main:app --reload --port 8000

# Cửa sổ dòng lệnh 2: Khởi chạy Frontend ReactJS (Cổng 5173)
cd frontend
npm run dev
```

Truy cập:
- **Giao diện Web**: [http://localhost:5173](http://localhost:5173)
- **Tài liệu Swagger API**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 5. QUY TRÌNH TÁI LẬP THỰC NGHIỆM TỪ ĐẦU (REPRODUCIBILITY)

Để tái lập toàn bộ kết quả nghiên cứu và xuất khẩu toàn bộ 20 biểu đồ thực nghiệm:
```powershell
.venv\Scripts\Activate.ps1

# 1. Chia tập ngẫu nhiên phân tầng 70/15/15
python backend/src/prepare_data.py

# 2. Thí nghiệm 1: Cây quyết định tự do và đường cong độ sâu
python backend/src/unpruned_tree.py

# 3. Thí nghiệm tỉa cành Cost-Complexity Pruning
python backend/src/prune_tree.py

# 4. Thí nghiệm 4: Huấn luyện Random Forest và kiểm tra ổn định qua 5 seeds
python backend/src/train_random_forest.py

# 5. Thí nghiệm 2: Đối sánh 4 mô hình trên tập Validation
python backend/src/compare_models.py

# 6. Đánh giá mở niêm phong trên tập Test độc lập
python backend/src/evaluate_final_test.py
```

---

## 6. THÔNG TIN THỰC HIỆN ĐỀ TÀI

- **Cơ sở đào tạo**: Trường Đại Học Công Nghệ Kỹ Thuật Hưng Yên
- **Khoa**: Công nghệ Thông tin — **Bộ môn**: Trí tuệ Nhân tạo
- **Học phần**: Học máy cơ bản (12523W.1)
- **Sinh viên thực hiện**: **Đỗ Hữu Quốc Anh**
- **Đóng góp**: Toàn bộ chu trình từ thu thập, kiểm toán dữ liệu, thiết kế thuật toán, huấn luyện mô hình, kiểm thử, phân tích lỗi, đến xây dựng API và giao diện Web.
