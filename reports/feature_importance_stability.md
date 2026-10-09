# Báo Cáo Thí Nghiệm 4: Khảo Sát Độ Ổn Định Của Feature Importance
**Học phần**: Học máy cơ bản (12523W.1)
**Đề tài**: Project 16 - Minh họa phân loại khối u vú bằng cây và rừng  
**Tác giả**: Đỗ Hữu Quốc Anh  
**Thời điểm lập báo cáo**: 09/10/2026  

---

## 1. Mục Tiêu và Thiết Kế Thí Nghiệm

Trong học máy y tế, việc mô hình đưa ra dự đoán chính xác là chưa đủ; các đặc trưng mà mô hình dựa vào để ra quyết định cần phải thể hiện **tính ổn định vững chắc (Stability / Robustness)** trước các yếu tố ngẫu nhiên trong quá trình huấn luyện.

### 1.1. Mục tiêu thí nghiệm
1. Đánh giá mức độ ổn định của chỉ số đo tầm quan trọng đặc trưng (Mean Decrease in Impurity - MDI Gini Importance) khi thay đổi hạt giống ngẫu nhiên (`random_state`).
2. Xác định nhóm đặc trưng cốt lõi đóng vai trò "trụ cột" trong việc phân biệt khối u lành tính và ác tính.
3. Phân tích tác động của hiện tượng **đa cộng tuyến (Multicollinearity)** giữa các nhóm đặc trưng hình học đến sự phân bổ trọng số trong rừng ngẫu nhiên.
4. Làm rõ ranh giới phương pháp luận giữa **Liên kết thống kê (Feature Importance / Correlation)** và **Quan hệ nhân quả sinh học (Causality)**.

### 1.2. Thiết kế thực nghiệm
- **Mô hình khảo sát**: `RandomForestClassifier` ứng viên tối ưu từ Nhiệm vụ 11 (`n_estimators = 100`, `max_depth = 8`, `min_samples_leaf = 1`, `max_features = 0.3`).
- **Tập dữ liệu**: **Tập Train ($N = 398$)** theo phân tầng Stratified. **Tuyệt đối KHÔNG sử dụng tập Test ($N = 86$)** trong thí nghiệm này.
- **Tập hạt giống ngẫu nhiên**: 5 seed độc lập được cố định trước: $\mathcal{S} = \{42, 123, 456, 789, 999\}$.
- **Chỉ số đo lường**:
  + Giá trị trung bình ($\mu$) và độ lệch chuẩn ($\sigma$) của Gini Importance qua 5 seeds.
  + Hệ số biến thiên phần trăm ($CV\% = \frac{\sigma}{\mu} \times 100\%$).
  + Thứ hạng trung bình ($\text{Mean Rank}$) và độ biến động thứ hạng ($\text{Std Rank}$).

---

## 2. Bảng Số Liệu Thực Nghiệm: Top 10 Đặc Trưng Qua 5 Seeds

Dưới đây là bảng thống kê chi tiết của Top 10 đặc trưng quan trọng nhất được trích xuất từ tệp nhật ký thực nghiệm [reports/exp4_feature_stability_results.json](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/exp4_feature_stability_results.json):

| Hạng TB | Tên Đặc Trưng | Seed 42 | Seed 123 | Seed 456 | Seed 789 | Seed 999 | Mean Importance ($\mu$) | Std ($\sigma$) | CV (%) | Thứ hạng qua 5 seeds | Std Rank |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | `perimeter_worst` | 0.0964 | 0.2140 | 0.2131 | 0.2169 | 0.1703 | **0.1821** | 0.0462 | 25.4% | [5, 1, 1, 1, 2] | **1.55** |
| **2** | `radius_worst` | 0.1345 | 0.1225 | 0.0956 | 0.1277 | 0.2048 | **0.1370** | 0.0364 | 26.6% | [3, 3, 5, 3, 1] | **1.26** |
| **3** | `area_worst` | 0.2016 | 0.1233 | 0.1516 | 0.1177 | 0.0840 | **0.1356** | 0.0394 | 29.1% | [1, 2, 2, 4, 5] | **1.47** |
| **4** | `concave points_mean` | 0.1558 | 0.1125 | 0.1108 | 0.1680 | 0.1171 | **0.1328** | 0.0241 | **18.1%** | [2, 4, 4, 2, 4] | **0.98** |
| **5** | `concave points_worst` | 0.1158 | 0.1107 | 0.1283 | 0.0730 | 0.1572 | **0.1170** | 0.0273 | 23.3% | [4, 5, 3, 5, 3] | **0.89** |
| **6** | `area_mean` | 0.0380 | 0.0506 | 0.0361 | 0.0541 | 0.0115 | **0.0381** | 0.0150 | 39.4% | [7, 6, 7, 6, 14] | 3.03 |
| **7** | `perimeter_mean` | 0.0443 | 0.0316 | 0.0263 | 0.0358 | 0.0243 | **0.0324** | 0.0071 | **21.9%** | [6, 8, 9, 7, 7] | **1.02** |
| **8** | `radius_mean` | 0.0088 | 0.0181 | 0.0371 | 0.0209 | 0.0514 | **0.0273** | 0.0151 | 55.3% | [15, 12, 6, 9, 6] | 3.50 |
| **9** | `concavity_mean` | 0.0293 | 0.0372 | 0.0280 | 0.0178 | 0.0179 | **0.0260** | 0.0074 | 28.5% | [8, 7, 8, 11, 9] | 1.36 |
| **10** | `symmetry_worst` | 0.0151 | 0.0258 | 0.0233 | 0.0179 | 0.0178 | **0.0200** | 0.0039 | **19.5%** | [13, 9, 10, 10, 10] | 1.36 |

---

## 3. Biểu Đồ Trực Quan Hóa Thực Nghiệm

### 3.1. Phân Bố Trọng Số Top 10 Đặc Trưng Kèm Thanh Sai Số (Error Bars)
Biểu đồ thanh ngang thể hiện giá trị trung bình $\mu$, dải sai số $\pm 1\sigma$ và các điểm giá trị cụ thể tại từng seed:

![Top 10 Feature Importance Stability](file:///c:/Ôn%20tập/Năm%204/Học%20máy%20cơ%20bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/exp4_feature_stability.png)

### 3.2. Ma Trận Nhiệt Biến Thiên Thứ Hạng (Rank Heatmap)
Heatmap thể hiện thứ hạng của Top 10 đặc trưng qua 5 hạt giống độc lập (tô màu theo độ ưu tiên):

![Feature Rank Heatmap](file:///c:/Ôn%20tập/Năm 4/Học máy cơ bản/DoHuuQuocAnh_HocMayCoBan/reports/figures/exp4_feature_ranks_heatmap.png)

---

## 4. Phân Tích Chuyên Sâu Kết Quả Thực Nghiệm

### 4.1. Độ Ổn Định Tuyệt Đối Của Nhóm "Top 5 Trụ Cột"
Từ bảng số liệu và biểu đồ nhiệt, ta rút ra một quy luật nổi bật:
- **Tập hợp Top 5 hoàn toàn bất biến**: Bất kể hạt giống ngẫu nhiên nào được sử dụng (từ Seed 42 đến Seed 999), 5 vị trí dẫn đầu **luôn thuộc về đúng 5 đặc trưng**:
  1. `perimeter_worst` (Chu vi lớn nhất)
  2. `radius_worst` (Bán kính lớn nhất)
  3. `area_worst` (Diện tích lớn nhất)
  4. `concave points_mean` (Số điểm lõm trung bình)
  5. `concave points_worst` (Số điểm lõm lớn nhất)
- Tổng trọng số MDI của 5 đặc trưng này chiếm tới **khoảng 70.5% toàn bộ sức mạnh phân loại** của khu rừng ngẫu nhiên.
- Các đặc trưng về hình thái lõm nhân tế bào (`concave points_mean`, `concave points_worst`) có độ ổn định thứ hạng cực cao với độ lệch chuẩn thứ hạng $\text{Std Rank} < 1.0$ (luôn ổn định ở vị trí hạng 2 đến hạng 5).

### 4.2. Ảnh Hưởng Của Đa Cộng Tuyến (Collinearity) Đến Sự Hoán Đổi Thứ Hạng
Quan sát trong Top 3 (`perimeter_worst`, `radius_worst`, `area_worst`), ta thấy thứ hạng giữa chúng có sự hoán đổi qua lại giữa các seed (ví dụ: ở Seed 42 thì `area_worst` đứng đầu, nhưng ở Seed 123, 456, 789 thì `perimeter_worst` lại đứng đầu):

```
       [Nhóm Đặc Trưng Kích Thước - Size Dimension]
         r > 0.98 giữa perimeter_worst, radius_worst, area_worst
                            |
           +----------------+----------------+
           |                                 |
   [Cây Quyết Định Đơn Lẻ]           [Rừng Ngẫu Nhiên]
   - Phân chia tham lam              - Ngẫu nhiên hóa max_features=0.3
   - Chọn 1 đặc trưng ở gốc           - Mỗi split chỉ xét 9/30 đặc trưng
   - Chiếm độc quyền 75.8%            - Cơ hội chia đều cho cả 3
   => Triệt tiêu 2 biến còn lại       => Chia sẻ độ quan trọng (Dilution)
```

1. **Bản chất hình học**: Về mặt giải phẫu tế bào học, một nhân tế bào có dạng xấp xỉ hình cầu/hình elip. Do đó, bán kính ($R$), chu vi ($P \approx 2\pi R$) và diện tích ($A \approx \pi R^2$) là 3 đại lượng phụ thuộc toán học chặt chẽ, có hệ số tương quan tuyến tính $r > 0.98$.
2. **Hiệu ứng lấn át trong Cây Quyết định đơn lẻ**:
   - Khi chạy thử trên Cây quyết định cắt tỉa (Pruned Tree) qua 5 seeds, `perimeter_worst` được chọn ở nút gốc và chiếm tới **75.75% tổng importance**, trong khi `radius_worst` chỉ nhận vỏn vẹn **0.96%** và `area_worst` nhận **0%**. Cây đơn lẻ hoàn toàn triệt tiêu các đặc trưng đồng dạng.
3. **Hiệu ứng san sẻ trọng số trong Random Forest (Importance Dilution)**:
   - Trong Random Forest, siêu tham số `max_features = 0.3` quy định rằng tại mỗi nút phân tách, thuật toán chỉ được bốc ngẫu nhiên $9 / 30$ đặc trưng.
   - Nếu ở một nút cụ thể, `perimeter_worst` không may mắn nằm trong tập 9 đặc trưng được bốc, thì `radius_worst` hoặc `area_worst` sẽ được chọn để thay thế làm điểm cắt tối ưu.
   - Kết quả: Cả 3 biến kích thước đều nhận được mức trọng số tương đương nhau (~13.5% - 18.2%). Việc thứ hạng nội bộ của chúng dao động giữa vị trí 1 và 3 chỉ là hệ quả ngẫu nhiên của lượt rút mẫu đặc trưng chứ không phản ánh sự vượt trội sinh học của chu vi so với diện tích.

---

## 5. Phân Biệt Giữa Feature Importance và Correlation

Hai khái niệm này thường bị nhầm lẫn nhưng có bản chất toán học và ý nghĩa hoàn toàn khác nhau:

| Tiêu chí | Correlation (Hệ số tương quan Pearson) | Feature Importance (MDI Gini Importance) |
| :--- | :--- | :--- |
| **Bản chất toán học** | Đo lường mức độ liên kết tuyến tính chuẩn hóa giữa 2 biến: $\rho_{X, Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$. | Đo lường mức giảm độ vẩn đục Gini Impurity tích lũy trên tất cả các nút phân nhánh sử dụng biến đó trong rừng. |
| **Không gian xem xét** | **Đơn biến (Univariate)**: Xét từng cặp đặc trưng cô lập, bỏ qua hoàn toàn các biến còn lại. | **Đa biến (Multivariate)**: Đo lường đóng góp của biến trong cấu trúc phân nhánh có điều kiện kết hợp phức tạp. |
| **Tính phi tuyến** | Hoàn toàn mù quáng trước các mối quan hệ phi tuyến (ví dụ: quan hệ parabol hoặc cấu trúc logic XOR). | Bắt giữ xuất sắc các tương tác phi tuyến và ngưỡng cắt bậc thang. |
| **Phản ứng với đa cộng tuyến** | Cả hai biến tương quan cao đều có hệ số $\rho$ cao tương đương nhau với biến mục tiêu. | Bị phân tán (diluted): Tổng đóng góp bị chia nhỏ cho các biến cùng nhóm. |

> **Ví dụ điển hình**: Một đặc trưng có thể có Correlation với nhãn $y$ chỉ ở mức trung bình (~0.3), nhưng lại có Feature Importance rất cao trong Random Forest vì nó đóng vai trò "chìa khóa phân loại phụ" sau khi một đặc trưng chính đã chia tách không gian ở tầng trên.

---

## 6. Tại Sao Một Đặc Trưng Quan Trọng Không Đồng Nghĩa Nó Gây Ra Ung Thư?
### (Association is NOT Causation: Nguyên nhân vs Triệu chứng)

Đây là ranh giới đạo đức và khoa học quan trọng nhất khi áp dụng trí tuệ nhân tạo trong y học:

```
                  [ĐỘT BIẾN GEN / BIẾN ĐỔI BIỂU SINH]
                   (Nguyên nhân gốc rễ - True Causality)
                     BRCA1, BRCA2, TP53, Môi trường
                                   |
                                   v
                   [Tế bào phân chia mất kiểm soát]
                                   |
                                   v
             +---------------------+---------------------+
             |                                           |
             v                                           v
    [Nhân tế bào phình to]                     [Màng tế bào gồ ghề, lõm]
   radius_worst, area_worst               concave points_mean, concave points_worst
             |                                           |
             +---------------------+---------------------+
                                   |
                                   v
                     [Dữ liệu hình ảnh FNA (WDBC)]
                                   |
                                   v
                     [Mô hình Học máy nhận diện]
                       (Tương quan thống kê thuần túy)
```

1. **Bản chất của tập dữ liệu WDBC**:
   - Dữ liệu WDBC thu được từ kỹ thuật chọc hút kim nhỏ (Fine Needle Aspirate - FNA), số hóa hình ảnh tế bào học và đo lường các chỉ số **hình thái học (Morphological Features)** của nhân tế bào (bán kính, chu vi, độ lõm, độ mịn).
2. **Đặc trưng là Triệu chứng (Phenotype/Biomarker), không phải Nguyên nhân (Etiology)**:
   - Các đặc trưng như `area_worst` lớn hay `concave points_mean` cao là **hậu quả sinh học hiển thị ra bên ngoài (Phenotypic Manifestations)** khi tế bào đã chuyển sang trạng thái ác tính và phân bào vô tổ chức.
   - Nói rằng *"Diện tích nhân tế bào lớn gây ra ung thư vú"* là một ngụy biện đảo ngược nguyên nhân - kết quả. Ngược lại, chính quá trình ung thư hóa mới làm cho nhân tế bào bị biến dạng và phình to.
   - Nguyên nhân thực sự gây ra ung thư vú nằm ở tầng sâu sinh học phân tử: các đột biến gen sửa chữa DNA (như BRCA1, BRCA2), đột biến gen ức chế khối u TP53, rối loạn thụ thể estrogen/progesterone (ER/PR), hoặc các tác nhân phóng xạ/hóa chất sinh ung.
3. **Cảnh báo suy diễn nhân quả**:
   - Mô hình Random Forest chỉ là một bộ khớp hàm thống kê (Statistical Pattern Recognizer) có nhiệm vụ tìm ranh giới phân tách tối ưu trên dữ liệu số.
   - Tuyệt đối **không được suy luận quan hệ nhân quả** hay đưa ra bất kỳ kết luận điều trị y khoa nào (ví dụ: không thể suy diễn rằng làm giảm chu vi tế bào sẽ chữa khỏi ung thư) từ bảng xếp hạng Feature Importance của mô hình.

---

## 7. Kết Luận và Đề Xuất Nghiệm Thu

1. Thí nghiệm 4 đã chứng minh mô hình `RandomForestClassifier` đạt **độ ổn định đặc trưng xuất sắc**: Nhóm Top 5 đặc trưng (`perimeter_worst`, `radius_worst`, `area_worst`, `concave points_mean`, `concave points_worst`) giữ vững vị trí hàng đầu qua toàn bộ 5 hạt giống ngẫu nhiên.
2. Cơ chế `max_features` của Random Forest giúp khắc phục hoàn toàn nhược điểm triệt tiêu biến của Cây Quyết định đơn lẻ, phân bổ đồng đều trọng số giữa các biến kích thước đa cộng tuyến.
3. Toàn bộ thí nghiệm được bảo vệ nghiêm ngặt: **Chỉ chạy trên Train Set ($N = 398$), Test Set ($N = 86$) vẫn được đóng băng nguyên vẹn**.

---

*Báo cáo được tạo tự động bởi quy trình thực nghiệm Project 16. Mọi số liệu và biểu đồ đã được lưu trữ sẵn sàng.*
