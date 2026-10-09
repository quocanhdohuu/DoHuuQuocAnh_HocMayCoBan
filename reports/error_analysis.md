# Báo Cáo Phân Tích Lỗi (Error Analysis) Trên Tập Test Độc Lập
**Học phần**: Học máy cơ bản (12523W.1)  
**Đề tài**: Project 16 - Minh họa phân loại khối u vú bằng cây và rừng  
**Tác giả**: Đỗ Hữu Quốc Anh  
**Thời điểm lập báo cáo**: 09/10/2026  

---

## 1. Tổng Quan Kết Quả Phân Loại Trên Tập Test ($N = 86$)

Trên tập dữ liệu kiểm thử độc lập gồm **86 mẫu** ($54$ ca Lành tính - Benign và $32$ ca Ác tính - Malignant), mô hình Random Forest ứng viên tối ưu đạt hiệu năng chẩn đoán phân loại ở mức cao:
- **True Negatives (TN)**: $54 / 54$ ca lành tính được dự đoán chính xác.
- **False Positives (FP)**: **$0$ ca báo động giả** ($\text{Precision} = 100.00\%$).
- **True Positives (TP)**: $31 / 32$ ca ác tính được phát hiện chính xác.
- **False Negatives (FN)**: **$1$ ca ung thư duy nhất bị bỏ sót** ($\text{Recall} = 96.88\%$).

Báo cáo này tập trung phân tích sâu về trường hợp sai lệch duy nhất này nhằm hiểu rõ ranh giới quyết định của mô hình và rút ra bài học thực tiễn cho việc triển khai lâm sàng.

---

## 2. Truy Vết Ca Bỏ Sót Duy Nhất (False Negative: Sample #23)

### 2.1. Thông Tin Chi Tiết Ca Bệnh
- **Vị trí trong tập Test**: Mẫu thứ 23 (Index $23$, tương ứng chỉ số gốc trong bộ dữ liệu là ID index `86`).
- **Nhãn thực tế (Ground Truth)**: **Malignant (Ác tính, $y = 1$)**.
- **Xác suất mô hình gán**:
  + $P(\text{Benign}) = 82.00\%$ ($0.8200$)
  + $P(\text{Malignant}) = 18.00\%$ ($0.1800$)
- **Ngưỡng quyết định**: $\tau = 0.50 \implies$ Mô hình kết luận **Benign (Lành tính, $\hat{y} = 0$)**.

### 2.2. So Sánh Định Lượng Giá Trị Đặc Trưng Của Mẫu #23 Với Phân Phối Quần Thể
Bảng dưới đây so sánh các đặc trưng quan trọng nhất của Mẫu #23 với phân phối của hai lớp trên tập huấn luyện:

| Đặc trưng quan trọng | Giá trị Mẫu #23 | Trung bình Lành tính ($\mu_B$) | Trung bình Ác tính ($\mu_M$) | Phân vị trong lớp Ác tính (%-tile M) | Phân vị trong lớp Lành tính (%-tile B) | Z-Score lớp Ác tính ($Z_M$) | Z-Score lớp Lành tính ($Z_B$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `perimeter_worst` | **108.40** | 81.66 | 142.83 | **11.5%** | **92.0%** | -1.12 | +1.53 |
| `radius_worst` | **16.21** | 12.58 | 21.39 | **10.8%** | **90.0%** | -1.16 | +1.39 |
| `area_worst` | **808.90** | 491.64 | 1450.61 | **11.5%** | **91.6%** | -1.04 | +1.47 |
| `concave points_mean` | **0.0494** | 0.0238 | 0.0878 | **9.5%** | **91.6%** | -1.07 | +1.51 |
| `concave points_worst` | **0.1225** | 0.0672 | 0.1852 | **11.5%** | **88.8%** | -1.24 | +1.27 |
| `area_mean` | **544.10** | 462.70 | 978.30 | **12.2%** | **78.4%** | -1.18 | +0.72 |
| `perimeter_mean` | **82.98** | 78.08 | 115.36 | **10.1%** | **76.0%** | -1.21 | +0.68 |
| `radius_mean` | **12.36** | 12.15 | 17.46 | **9.5%** | **68.8%** | -1.25 | +0.48 |

---

## 3. Biểu Đồ Minh Họa Mẫu Sai So Với Phân Phối Dữ Liệu

Biểu đồ hàm mật độ xác suất (KDE Plot) dưới đây trực quan hóa vị trí của Mẫu #23 (ngôi sao vàng) đặt giữa hai phân phối Lành tính (xanh) và Ác tính (đỏ):

![Phân Tích Mẫu False Negative](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/error_analysis_fn_comparison.png)

---

## 4. Giả Thuyết Khoa Học Giải Thích Nguyên Nhân Lỗi

Dựa trên các phân tích thống kê định lượng ở Mục 2 và Mục 3, ta rút ra các nhận định khách quan:

### 4.1. Bản chất toán học: Mẫu nằm ở vùng ranh giới chồng lấn (Borderline Overlap Region)
- Mẫu #23 là một trường hợp ngoại lai thống kê đối với phân phối lớp Ác tính:
  + Cả 5 đặc trưng quyết định nhất của nó (`perimeter_worst`, `radius_worst`, `area_worst`, `concave points_mean`, `concave points_worst`) đều nằm ở **phân vị ~10% thấp nhất của lớp Ác tính** ($Z_M \approx -1.1$ đến $-1.2$).
  + Đồng thời, các giá trị này lại nằm ở **phân vị ~90% của lớp Lành tính** ($Z_B \approx +1.3$ đến $+1.5$).
- Do Random Forest sử dụng cơ chế bỏ phiếu từ 100 cây con được huấn luyện dựa trên ranh giới phân tách tối ưu, đại đa số các cây con (82/100 cây) khi kiểm tra ngưỡng split (ví dụ: `concave points_mean <= 0.049` hay `radius_worst <= 16.82`) đều xếp mẫu này vào nhánh phân phối u lành tính.

### 4.2. Giả thuyết về mặt tế bào học lâm sàng
- Trong bệnh học khối u vú, các khối u ác tính thể biệt hóa rất cao (Well-differentiated Carcinoma) hoặc ung thư biểu mô tại chỗ giai đoạn rất sớm (Carcinoma in situ / T1a-T1b) có thể có nhân tế bào chưa kịp phình to bất thường và chưa hình thành các đường lõm màng nhân sâu như các khối u tiến triển nặng.
- Kết quả chọc hút kim nhỏ (FNA) của mẫu này chỉ phản ánh hình thái học bề ngoài ở một lát cắt vi thể cục bộ, khiến các chỉ số số hóa tế bào học của nó tương đồng với các u xơ tuyến vú lành tính kích thước lớn.

### 4.3. Cảnh báo phương pháp luận: Không suy diễn nhân quả (No Causal Inference)
- Báo cáo này **tuyệt đối không suy diễn** rằng các kích thước nhỏ của mẫu này là "nguyên nhân" trực tiếp khiến nó trở nên lành tính hay ác tính.
- Sự sai lệch ở đây thuần túy là do giới hạn của mô hình học máy dựa trên dữ liệu hình thái học quan sát tĩnh (Observational Morphological Data), khi mà ranh giới giữa hai lớp trong không gian 30 chiều có một vùng chồng lấn tự nhiên.

---

## 5. Thảo Luận Về Tỷ Lệ False Positive Bằng 0 (Zero FP Rate)

Một điểm sáng đặc biệt trong kết quả Test là mô hình đạt **$FP = 0$ (Precision = 100%)**:
- **Ý nghĩa thực tiễn**: Trong bối cảnh tầm soát ung thư, việc không có ca báo động giả nào giúp loại bỏ hoàn toàn các chỉ định can thiệp phẫu thuật mở hoặc sinh thiết lõi kim lớn không cần thiết, bảo vệ sức khỏe và tâm lý cho bệnh nhân có u lành tính.
- **Tính ổn định**: Mặc dù trên tập Test nhỏ ($54$ ca lành tính) mô hình đạt FP = 0, kết quả 5-Fold Cross-Validation trước đó trên tập Train cho thấy Mean Precision đạt **$92.69\%$**. Do đó, khi triển khai vào môi trường sản xuất thực tế, hệ thống vẫn phải dự liệu một tỷ lệ nhỏ ca báo động giả (~7%) trên các biến thể mô bệnh học hiếm gặp.

---

## 6. Bài Học Kinh Nghiệm Cho Thiết Kế Hệ Thống AI Y Tế

Từ phân tích trường hợp lỗi trên, nhóm phát triển đúc kết 3 nguyên tắc cho hệ thống AI hỗ trợ chẩn đoán khối u vú:
1. **Thiết kế ngưỡng kép (Dual-Threshold Alert System)**:
   - Thay vì chỉ có 2 trạng thái nhị phân (Lành tính vs Ác tính tại $\tau = 0.50$), hệ thống nên bổ sung **Vùng Cảnh Báo Không Chắc Chắn (Uncertainty Zone)**:
     + $P(\text{Malignant}) \ge 0.50$: Nguy cơ cao $\implies$ Khuyến nghị hội chẩn chuyên khoa ngay.
     + $0.15 \le P(\text{Malignant}) < 0.50$: **Vùng nghi ngờ / Ranh giới** (như mẫu #23 với $P = 18\%$) $\implies$ Đưa ra cảnh báo cho bác sĩ làm thêm xét nghiệm hóa mô miễn dịch hoặc chụp cộng hưởng từ (MRI).
     + $P(\text{Malignant}) < 0.15$: Nguy cơ thấp.
2. **AI là công cụ hỗ trợ, không thay thế con người**:
   - Trường hợp mẫu #23 chứng minh rằng không một thuật toán học máy nào có thể đạt độ nhạy tuyệt đối 100% trên dữ liệu hình ảnh tế bào học đơn thuần. Quyết định điều trị cuối cùng bắt buộc phải thuộc về bác sĩ chuyên khoa lâm sàng.

---

*Báo cáo phân tích lỗi hoàn tất, lưu trữ tại `reports/error_analysis.md`.*
