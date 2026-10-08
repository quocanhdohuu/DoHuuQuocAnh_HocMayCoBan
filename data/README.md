# HỒ SƠ DỮ LIỆU: BREAST CANCER WISCONSIN (DIAGNOSTIC) - WDBC

## 1. THÔNG TIN XUẤT XỨ VÀ BẢN QUYỀN
- **Tên tập dữ liệu**: Breast Cancer Wisconsin (Diagnostic) Data Set (WDBC).
- **Cơ quan quản lý**: Đại học California tại Irvine (UCI Machine Learning Repository).
- **Trang dữ liệu chính thức**: [https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)
- **Đường dẫn tải tệp thô trực tiếp**: [https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data](https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data)
- **Định danh số (DOI)**: [10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B)
- **Tác giả nghiên cứu gốc**:
  - Dr. William H. Wolberg (Khoa Ngoại, Bệnh viện Đại học Wisconsin)
  - W. Nick Street (Khoa Khoa học Máy tính, Đại học Wisconsin)
  - Olvi L. Mangasarian (Khoa Khoa học Máy tính, Đại học Wisconsin)
- **Ngày công bố gốc**: 01/11/1995.
- **Giấy phép sử dụng**: Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
- **Trích dẫn khoa học bắt buộc**:
  > Street, W., Wolberg, W., & Mangasarian, O. (1995). *Breast Cancer Wisconsin (Diagnostic)*. UCI Machine Learning Repository. https://doi.org/10.24432/C5DW2B.

---

## 2. THỜI ĐIỂM TẢI VÀ TOÀN VẸN DỮ LIỆU
- **Thời điểm trích xuất / tải dữ liệu**: 08/10/2026.
- **Phương thức tải**: Tự động thông qua script `backend/src/data.py` kết nối trực tiếp với máy chủ UCI.
- **Tệp dữ liệu đã lưu**: `data/wdbc.csv`.
- **Mã băm kiểm tra tính toàn vẹn (SHA-256 Checksum)**:
  - `data/wdbc.csv`: `8eb50040833604b43dbf8ce129e32a5002d31d052e0477bd352d7886ff68f2ed` (Dữ liệu tải trực tiếp từ UCI).
  - `data.csv` (Bản dự phòng local): `6098db46b1707f93d653b025e0d078e98db25cdc9f24cad9d3a603318fb2493a`.

---

## 3. ĐẶC TẢ CẤU TRÚC VÀ QUY MÔ
- **Tổng số mẫu (Observations)**: Đúng 569 mẫu bệnh phẩm FNA.
- **Tổng số thuộc tính (Attributes)**: 32 thuộc tính:
  - 01 Thuộc tính định danh: `id` (Mã số bệnh phẩm — **Loại bỏ khỏi tập đặc trưng**).
  - 01 Thuộc tính nhãn mục tiêu: `diagnosis` (`M` = Malignant / Ác tính; `B` = Benign / Lành tính).
  - 30 Đặc trưng số (Continuous Features): Đo lường 10 đặc tính hình thái của nhân tế bào theo 3 góc độ: giá trị trung bình (`mean`), sai số chuẩn (`se`), và giá trị lớn nhất/xấu nhất (`worst`).
- **Phân bố nhãn lớp**:
  - `B` (Benign - Lành tính): 357 mẫu (62.74%).
  - `M` (Malignant - Ác tính): 212 mẫu (37.26%).
- **Chất lượng dữ liệu**:
  - Giá trị khuyết thiếu (Missing values): **0** (Hoàn toàn không có NaN/Null).
  - Bản ghi trùng lặp (Duplicates): **0**.

---

## 4. BẢO MẬT VÀ PHI LÂM SÀNG
- Bộ dữ liệu đã được ẩn danh hoàn toàn (de-identified), không chứa bất kỳ thông tin nhận dạng cá nhân nào (như tên tuổi, địa chỉ, số CMND/CCCD, hồ sơ bệnh án cá nhân).
- Bộ dữ liệu chỉ được sử dụng cho mục đích minh họa học thuật giải thuật Cây quyết định và Rừng ngẫu nhiên trong môn học **Học máy cơ bản**.
- Nghiêm cấm ứng dụng vào quy trình chẩn đoán y tế thực tế mà không có sự kiểm định lâm sàng.
