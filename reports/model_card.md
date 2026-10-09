# Thẻ Mô Hình (Model Card) - Phân Loại Khối U Vú WDBC
**Học phần**: Học máy cơ bản (12523W.1)  
**Đề tài**: Project 16 - Minh họa phân loại khối u vú bằng cây và rừng  
**Phiên bản mô hình**: `1.0.0`  
**Ngày phát hành**: 09/10/2026  
**Định dạng chuẩn hóa**: Tuân theo khuôn mẫu Model Card for Model Reporting (Mitchell et al., 2019)  

---

## 1. Thông Tin Chi Tiết Về Mô Hình (Model Details)

- **Tên mô hình**: `WDBC_RandomForest_Classifier_Pipeline`
- **Tác giả phát triển**: Đỗ Hữu Quốc Anh
- **Cơ sở đào tạo**: Đại Học Công Nghệ Kỹ Thuật Hưng Yên (Bộ môn Trí tuệ Nhân tạo - Khoa CNTT)
- **Kiến trúc mô hình**: Rừng ngẫu nhiên (Random Forest Classifier) kết hợp trong `sklearn.pipeline.Pipeline`.
- **Framework & Thư viện**: Python 3.12, scikit-learn 1.9.1, numpy 2.x, pandas 2.x, joblib 1.4.x.
- **Tệp đóng gói nhị phân**: `backend/models/wdbc_pipeline.joblib`
- **Mã băm toàn vẹn SHA-256**: `1f5c3bc820674e6911d07fd1a372d592bc696e280470903a51276dc4a83451d1`
- **Giấy phép phần mềm (License)**: MIT License (Dành cho mã nguồn học thuật).

---

## 2. Mục Đích Sử Dụng (Intended Use)

### 2.1. Mục đích được phép (Intended Uses)
- **Nghiên cứu học thuật và giáo dục**: Minh họa thuật toán Cây quyết định (CART) và Rừng ngẫu nhiên (Random Forest) cho học phần Học máy cơ bản.
- **Thử nghiệm đối sánh thuật toán**: Cung cấp mã nguồn chuẩn mực, có khả năng tái lập 100%, đối chiếu hiệu năng giữa các kỹ thuật Pre-pruning, Post-pruning (Cost-Complexity Pruning) và Ensemble Learning.
- **Trực quan hóa và trình diễn**: Cung cấp giao diện tương tác Web (FastAPI + ReactJS) cho sinh viên và giảng viên quan sát quá trình suy luận và tầm quan trọng của các đặc trưng tế bào học.

### 2.2. Mục đích nghiêm cấm (Out-of-Scope & Prohibited Uses)
- **Tuyệt đối KHÔNG sử dụng trong chẩn đoán y tế tự động (Autonomous Clinical Diagnosis)**.
- **Tuyệt đối KHÔNG sử dụng làm căn cứ duy nhất để ra chỉ định phẫu thuật, hóa trị, xạ trị hoặc từ chối điều trị cho bệnh nhân**.
- Không sử dụng ngoài môi trường nghiên cứu khi chưa qua các thử nghiệm lâm sàng ngẫu nhiên có đối chứng (RCTs) và chưa được cơ quan quản lý y tế (như Bộ Y tế / FDA) cấp phép thiết bị y tế kỹ thuật số (SaMD).

---

## 3. Dữ Liệu Huấn Luyện và Kiểm Thử (Data & Splitting)

- **Nguồn dữ liệu gốc**: UCI Machine Learning Repository - Breast Cancer Wisconsin (Diagnostic) Dataset (WDBC).
- **Quy mô tập dữ liệu**: $569$ mẫu sinh thiết chọc hút kim nhỏ (FNA), $30$ đặc trưng số liên tục đo đạc hình thái học nhân tế bào.
- **Phân chia dữ liệu (Stratified 70/15/15)**:
  + **Tập Huấn luyện (Train)**: $398$ mẫu ($250$ Lành tính, $148$ Ác tính). Dùng để học trọng số và tuning qua 5-Fold Cross-Validation.
  + **Tập Kiểm chứng (Validation)**: $85$ mẫu ($53$ Lành tính, $32$ Ác tính). Dùng để đối chiếu 4 mô hình và chốt siêu tham số.
  + **Tập Kiểm thử (Test)**: $86$ mẫu ($54$ Lành tính, $32$ Ác tính). Đóng băng nguyên vẹn đến bước đánh giá cuối cùng.
  + **Mô hình triển khai sản xuất (Production)**: Khớp trên $483$ mẫu (Train + Validation) với đúng cấu hình đã chốt.
- **Định nghĩa biến mục tiêu**:
  + Lớp 1 (Positive): **Malignant (Ác tính)**
  + Lớp 0 (Negative): **Benign (Lành tính)**

---

## 4. Đặc Tả Siêu Tham Số Cố Định (Model Parameters)

```json
{
  "n_estimators": 100,
  "criterion": "gini",
  "max_depth": 8,
  "min_samples_split": 2,
  "min_samples_leaf": 1,
  "max_features": 0.3,
  "bootstrap": true,
  "random_state": 42,
  "decision_threshold": 0.50
}
```

---

## 5. Kết Quả Đánh Giá Hiệu Năng Định Lượng (Quantitative Performance)

### 5.1. Kết Quả Kiểm Thử Độc Lập Trên Tập Test ($N = 86$)
- **Accuracy**: **$98.84\%$** ($85 / 86$ mẫu đúng) [95% CI: $93.70\% - 99.79\%$]
- **Precision Malignant**: **$100.00\%$** ($31 / 31$ ca chuẩn xác) [95% CI: $89.03\% - 100.00\%$]
- **Recall Malignant**: **$96.88\%$** ($31 / 32$ ca phát hiện) [95% CI: $84.26\% - 99.45\%$]
- **F1-Score Malignant**: **$98.41\%$**
- **ROC-AUC Score**: **$0.9954$**
- **Ma trận nhầm lẫn (Confusion Matrix)**: $\text{TN} = 54, \text{FP} = 0, \text{FN} = 1, \text{TP} = 31$

### 5.2. So Sánh Đối Trọng Với Các Mô Hình Cùng Nghiên Cứu Trên Test
| Mô hình | Accuracy | Precision (M) | Recall (M) | F1-Score (M) | ROC-AUC | Ca bỏ sót (FN) | Báo động giả (FP) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| DummyClassifier (Baseline) | 62.79% | 0.00% | 0.00% | 0.00% | 0.5000 | 32 (100%) | 0 |
| Unpruned Decision Tree | 90.70% | 87.50% | 87.50% | 87.50% | 0.9005 | 4 | 4 |
| Pruned Decision Tree | 93.02% | 96.43% | 84.38% | 90.00% | 0.8843 | 5 | 1 |
| **Random Forest (Mô hình này)** | **98.84%** | **100.00%** | **96.88%** | **98.41%** | **0.9954** | **1** | **0** |

---

## 6. Yêu Cầu Về Đầu Vào và Thứ Tự 30 Đặc Trưng (Input Schema & Feature Ordering)

Mô hình yêu cầu đầu vào nghiêm ngặt gồm đúng **30 đặc trưng số liên tục** (`float64`) theo đúng thứ tự đã lưu trong [backend/models/feature_schema.json](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/backend/models/feature_schema.json):

1. `radius_mean`
2. `texture_mean`
3. `perimeter_mean`
4. `area_mean`
5. `smoothness_mean`
6. `compactness_mean`
7. `concavity_mean`
8. `concave points_mean`
9. `symmetry_mean`
10. `fractal_dimension_mean`
11. `radius_se`
12. `texture_se`
13. `perimeter_se`
14. `area_se`
15. `smoothness_se`
16. `compactness_se`
17. `concavity_se`
18. `concave points_se`
19. `symmetry_se`
20. `fractal_dimension_se`
21. `radius_worst`
22. `texture_worst`
23. `perimeter_worst`
24. `area_worst`
25. `smoothness_worst`
26. `compactness_worst`
27. `concavity_worst`
28. `concave points_worst`
29. `symmetry_worst`
30. `fractal_dimension_worst`

> **LƯU Ý KỸ THUẬT**: Tuyệt đối không tráo đổi vị trí các cột hoặc đưa nhầm cột định danh `id` vào đầu vào. Việc sai lệch thứ tự cột sẽ dẫn đến lỗi sai lệch thầm lặng (Silent Failure) khiến mô hình đưa ra dự đoán sai mà không báo lỗi runtime.

---

## 7. Các Hạn Chế và Thiên Lệch (Limitations & Biases)

1. **Giới hạn cỡ mẫu và phân bố địa lý**:
   - Dữ liệu thu thập tại Bệnh viện Đại học Wisconsin vào thập niên 1990 trên cỡ mẫu $569$ bệnh nhân. Mô hình chưa được kiểm chứng trên các nhóm dân số đa dạng chủng tộc hoặc thiết bị chụp tế bào học kỹ thuật số thế hệ mới.
2. **Khối u giai đoạn sớm ở vùng ranh giới**:
   - Phân tích lỗi (Error Analysis) cho thấy mô hình có thể phân loại nhầm các khối u ác tính thể biệt hóa rất cao ở giai đoạn khởi phát (như mẫu #23) do kích thước và độ lõm của chúng còn nhỏ và trùng lấn với vùng phân phối u xơ tuyến lành tính.
3. **Mô hình dạng hộp xám**:
   - Mặc dù cung cấp chỉ số Gini Feature Importance tổng thể, Random Forest không cho phép bác sĩ truy vết từng bước suy luận đơn lẻ cho từng bệnh nhân cụ thể như Cây Quyết định đơn.

---

## 8. Cảnh Báo Bảo Mật và Tuyên Bố Pháp Lý (Security & Legal Disclaimers)

### 8.1. Cảnh Báo Bảo Mật (Security Advisory)
> **CẢNH BÁO BẢO MẬT QUAN TRỌNG**:  
> Tệp mô hình được lưu dưới định dạng nhị phân Python (`.joblib` / `pickle`). Việc nạp các tệp joblib từ các nguồn không rõ ràng trên internet có nguy cơ bị tấn công thực thi mã tùy ý (Arbitrary Code Execution / Remote Code Execution).  
> **Chỉ tải và giải nén tệp mô hình từ nguồn tin cậy đã được kiểm chứng (Trusted Source)** và bắt buộc phải kiểm tra mã băm SHA-256 trùng khớp với giá trị:  
> `1f5c3bc820674e6911d07fd1a372d592bc696e280470903a51276dc4a83451d1`.

### 8.2. Tuyên Bố Miễn Trừ Trách Nhiệm Y Khoa (Clinical Disclaimer)
> **TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ**:  
> Mô hình học máy này là một sản phẩm phần mềm học thuật được phát triển phục vụ mục đích nghiên cứu, học tập và minh họa giáo dục trong khuôn khổ học phần Học máy cơ bản tại Đại Học Công Nghệ Kỹ Thuật Hưng Yên.  
> **HỆ THỐNG TUYỆT ĐỐI KHÔNG PHẢI LÀ MỘT THIẾT BỊ Y TẾ HOẶC HỆ THỐNG CHẨN ĐOÁN LÂM SÀNG CHÍNH THỨC**.  
> Mọi kết quả dự đoán (xác suất, phân lớp, cảnh báo nguy cơ) chỉ mang tính chất tham khảo thực nghiệm, **HOÀN TOÀN KHÔNG CÓ GIÁ TRỊ THAY THẾ Ý KIẾN CHẨN ĐOÁN CỦA BÁC SĨ CHUYÊN KHOA UNG BƯỚU VÀ BÁC SĨ GIẢI PHẪU BỆNH HỌC**. Nhóm tác giả không chịu bất kỳ trách nhiệm pháp lý nào đối với các quyết định y tế phát sinh từ việc sử dụng phần mềm này.

---

*Tài liệu Model Card hoàn tất, lưu trữ tại `reports/model_card.md`.*
