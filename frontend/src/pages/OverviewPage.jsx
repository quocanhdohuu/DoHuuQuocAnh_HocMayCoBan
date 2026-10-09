import React from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Database,
  ShieldAlert,
  GitBranch,
  Scissors,
  Trees,
  Layers,
  ArrowRight,
  Activity,
  CheckCircle2,
  AlertOctagon,
  FileText,
  Server,
  Monitor,
  HeartPulse,
  Info,
  Cpu
} from 'lucide-react';

export default function OverviewPage() {
  return (
    <div className="overview-page animate-fade-in">
      {/* ==============================================================================
          1. HERO ACADEMIC CARD: TIÊU ĐỀ & MỤC TIÊU DỰ ÁN
          ============================================================================== */}
      <section className="hero-academic-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="badge badge-primary">Project 16</span>
          <span className="badge" style={{ background: '#f1f5f9', color: '#475569' }}>
            Học phần: Học máy cơ bản (12523W.1)
          </span>
        </div>

        <h1 style={{ fontSize: '2.1rem', color: '#0f172a', marginBottom: '0.75rem', lineHeight: '1.25' }}>
          Minh Họa Phân Loại Khối U Vú Bằng Cây Quyết Định và Rừng Ngẫu Nhiên
        </h1>

        <p style={{ fontSize: '1.05rem', color: '#475569', maxWidth: '980px', lineHeight: '1.6' }}>
          Xây dựng hệ thống học máy toàn diện (End-to-End) giải quyết bài toán phân loại khối u vú FNA từ bộ dữ liệu
          <strong> Wisconsin Diagnostic Breast Cancer (WDBC)</strong>. Khảo sát hiện tượng quá khớp (Overfitting), kỹ thuật
          cắt tỉa kiểm soát độ phức tạp (Cost-Complexity Pruning), phương pháp tập hợp Rừng ngẫu nhiên (Random Forest)
          và triển khai suy luận Web API thời gian thực.
        </p>

        <div className="hero-meta-bar">
          <div className="hero-meta-item">
            <span>Đơn vị:</span>
            <strong>Đại Học Công Nghệ Kỹ Thuật Hưng Yên</strong>
          </div>
          <span>&bull;</span>
          <div className="hero-meta-item">
            <span>Bộ môn:</span>
            <strong>Khoa học Dữ liệu & Trí tuệ Nhân tạo</strong>
          </div>
          <span>&bull;</span>
          <div className="hero-meta-item">
            <span>Giảng viên hướng dẫn:</span>
            <strong>PGS.TS. Nguyễn Văn Hậu</strong>
          </div>
          <span>&bull;</span>
          <div className="hero-meta-item">
            <span>Sinh viên thực hiện:</span>
            <strong>Đỗ Hữu Quốc Anh</strong>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          2. THỐNG KÊ NHANH BỘ DỮ LIỆU WDBC (4 STAT CARDS)
          ============================================================================== */}
      <section style={{ marginBottom: '2rem' }}>
        <div className="grid-4-col">
          <div className="stat-card-mini">
            <div className="stat-icon-wrapper" style={{ background: '#eff6ff', color: '#2563eb' }}>
              <Database size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-number">569</div>
              <div className="stat-label">Mẫu bệnh phẩm FNA</div>
            </div>
          </div>

          <div className="stat-card-mini">
            <div className="stat-icon-wrapper" style={{ background: '#f0fdf4', color: '#16a34a' }}>
              <Layers size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-number">30</div>
              <div className="stat-label">Đặc trưng nhân tế bào số thực</div>
            </div>
          </div>

          <div className="stat-card-mini">
            <div className="stat-icon-wrapper" style={{ background: '#fef2f2', color: '#dc2626' }}>
              <Activity size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-number">62.7% / 37.3%</div>
              <div className="stat-label">Tỷ lệ Lành tính / Ác tính</div>
            </div>
          </div>

          <div className="stat-card-mini">
            <div className="stat-icon-wrapper" style={{ background: '#faf5ff', color: '#9333ea' }}>
              <CheckCircle2 size={24} />
            </div>
            <div className="stat-content">
              <div className="stat-number">70 / 15 / 15</div>
              <div className="stat-label">Tỷ lệ chia Train / Val / Test</div>
            </div>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          3. GIỚI THIỆU BỘ DỮ LIỆU WDBC & 30 ĐẶC TRƯNG HÌNH HỌC TẾ BÀO
          ============================================================================== */}
      <section className="card">
        <div className="card-header">
          <span className="card-title">
            <Database size={20} color="#2563eb" />
            Bộ Dữ Liệu Wisconsin Diagnostic Breast Cancer (WDBC) & 30 Đặc Trưng
          </span>
          <span className="badge badge-primary">Nguồn: UCI Machine Learning Repository</span>
        </div>
        <div className="card-body">
          <p style={{ lineHeight: '1.65', marginBottom: '1.25rem' }}>
            Bộ dữ liệu <strong>WDBC</strong> được thu thập bởi các bác sĩ và nhà khoa học tại Bệnh viện Đại học Wisconsin
            (Dr. William H. Wolberg, W. Nick Street, Olvi L. Mangasarian, 1995). Các mẫu bệnh phẩm thu thập từ kỹ thuật
            <strong> chọc hút tế bào bằng kim nhỏ (Fine Needle Aspirate - FNA)</strong> từ khối u vú, sau đó quét hình ảnh kỹ thuật số
            và tính toán vector hình học của nhân tế bào qua phần mềm phân tích hình ảnh Xcyt.
          </p>

          <div style={{ background: '#f8fafc', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid #e2e8f0', marginBottom: '1.5rem' }}>
            <h4 style={{ fontSize: '0.95rem', color: '#1e293b', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Info size={16} color="#2563eb" /> 10 Thuộc tính hình học nhân tế bào gốc:
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.5rem', fontSize: '0.85rem' }}>
              <div>&bull; <strong>radius:</strong> Bán kính nhân</div>
              <div>&bull; <strong>texture:</strong> Độ nhám / xám bề mặt</div>
              <div>&bull; <strong>perimeter:</strong> Chu vi nhân tế bào</div>
              <div>&bull; <strong>area:</strong> Diện tích nhân</div>
              <div>&bull; <strong>smoothness:</strong> Độ nhẵn cục bộ</div>
              <div>&bull; <strong>compactness:</strong> Độ co cụm ($P^2/A - 1$)</div>
              <div>&bull; <strong>concavity:</strong> Mức độ lõm viền</div>
              <div>&bull; <strong>concave points:</strong> Số điểm lõm trên viền</div>
              <div>&bull; <strong>symmetry:</strong> Độ đối xứng hình học</div>
              <div>&bull; <strong>fractal dimension:</strong> Số chiều fractal</div>
            </div>
          </div>

          <h4 style={{ fontSize: '1rem', color: '#0f172a', marginBottom: '0.75rem' }}>
            Cơ cấu 30 đặc trưng đầu vào (chia thành 3 nhóm đo lường):
          </h4>
          <div className="grid-3-col">
            <div style={{ background: '#eff6ff', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid #bfdbfe' }}>
              <strong style={{ color: '#1d4ed8', fontSize: '0.9rem', display: 'block', marginBottom: '0.35rem' }}>
                1. Nhóm Mean (10 đặc trưng trung bình)
              </strong>
              <p style={{ fontSize: '0.8rem', color: '#475569', marginBottom: '0.5rem' }}>
                Giá trị trung bình của các nhân tế bào đo được trên toàn bộ tiêu bản bệnh phẩm FNA.
              </p>
              <div className="feature-tags-grid">
                <span className="feature-tag mean">radius_mean</span>
                <span className="feature-tag mean">texture_mean</span>
                <span className="feature-tag mean">perimeter_mean</span>
                <span className="feature-tag mean">area_mean</span>
                <span className="feature-tag mean">concave points_mean</span>
              </div>
            </div>

            <div style={{ background: '#fffbeb', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid #fde68a' }}>
              <strong style={{ color: '#b45309', fontSize: '0.9rem', display: 'block', marginBottom: '0.35rem' }}>
                2. Nhóm SE (10 sai số chuẩn)
              </strong>
              <p style={{ fontSize: '0.8rem', color: '#475569', marginBottom: '0.5rem' }}>
                Sai số chuẩn (Standard Error), biểu thị mức độ đa dạng và biến thiên kích thước giữa các tế bào.
              </p>
              <div className="feature-tags-grid">
                <span className="feature-tag se">radius_se</span>
                <span className="feature-tag se">texture_se</span>
                <span className="feature-tag se">perimeter_se</span>
                <span className="feature-tag se">area_se</span>
                <span className="feature-tag se">concavity_se</span>
              </div>
            </div>

            <div style={{ background: '#fff1f2', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid #fecdd3' }}>
              <strong style={{ color: '#be123c', fontSize: '0.9rem', display: 'block', marginBottom: '0.35rem' }}>
                3. Nhóm Worst (10 giá trị lớn nhất / tệ nhất)
              </strong>
              <p style={{ fontSize: '0.8rem', color: '#475569', marginBottom: '0.5rem' }}>
                Giá trị lớn nhất đo được (trung bình của 3 tế bào dị dạng nhất), phản ánh nguy cơ ác tính cao nhất.
              </p>
              <div className="feature-tags-grid">
                <span className="feature-tag worst">radius_worst</span>
                <span className="feature-tag worst">area_worst</span>
                <span className="feature-tag worst">perimeter_worst</span>
                <span className="feature-tag worst">concave points_worst</span>
                <span className="feature-tag worst">concavity_worst</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          4. BẢN CHẤT Y HỌC & Ý NGHĨA HAI LỚP BENIGN VS MALIGNANT
          ============================================================================== */}
      <section style={{ marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1.35rem', marginBottom: '0.5rem', color: '#0f172a' }}>
          Bản Chất Sinh Học & Ý Nghĩa Hai Lớp Khối U
        </h3>
        <p style={{ color: '#64748b', marginBottom: '1.25rem', fontSize: '0.95rem' }}>
          Hiểu rõ đặc tính tế bào và sự chênh lệch chi phí rủi ro y tế giữa hai lớp phân loại.
        </p>

        <div className="grid-2-col">
          {/* Lớp Lành tính */}
          <div className="class-card class-card-benign">
            <div className="class-card-header">
              <span className="class-title">
                <CheckCircle2 size={22} />
                Lớp Lành Tính (Benign - Mã 'B' / Lớp 0)
              </span>
              <span className="badge badge-benign">357 mẫu (62.74%)</span>
            </div>
            <ul className="class-feature-list">
              <li>
                <strong>Hình thái nhân tế bào:</strong> Tròn đều, kích thước đồng nhất, đường viền nhẵn nhụi, ranh giới rõ ràng với mô xung quanh.
              </li>
              <li>
                <strong>Hành vi sinh học:</strong> Tăng sinh có kiểm soát, khối u khu trú, không xâm lấn mô lành và không có khả năng di căn xa.
              </li>
              <li>
                <strong>Giá trị đặc trưng:</strong> Bán kính (`radius_mean`), diện tích (`area_worst`), và số điểm lõm (`concave points_mean`) đều ở mức thấp.
              </li>
              <li>
                <strong>Tiên lượng lâm sàng:</strong> Rất thuận lợi, thường không đe dọa tính mạng; bệnh nhân chỉ cần theo dõi định kỳ.
              </li>
            </ul>
          </div>

          {/* Lớp Ác tính */}
          <div className="class-card class-card-malignant">
            <div className="class-card-header">
              <span className="class-title">
                <AlertOctagon size={22} />
                Lớp Ác Tính (Malignant - Mã 'M' / Lớp 1)
              </span>
              <span className="badge badge-malignant">212 mẫu (37.26%)</span>
            </div>
            <ul className="class-feature-list">
              <li>
                <strong>Hình thái nhân tế bào:</strong> Đa hình thái, dị dạng, kích thước nhân phình to bất thường, đường viền nham nhở, răng cưa lõm sâu.
              </li>
              <li>
                <strong>Hành vi sinh học:</strong> Tăng sinh mất kiểm soát (Ung thư), có xu hướng xâm lấn mạch máu, phá vỡ màng đáy và di căn các cơ quan.
              </li>
              <li>
                <strong>Giá trị đặc trưng:</strong> Diện tích lớn (`area_worst` &gt; 1000), độ lõm cao (`concavity_worst`), số điểm lõm tăng vọt.
              </li>
              <li>
                <strong>Chi phí rủi ro y tế:</strong> Bỏ sót ca ác tính (lỗi <em>False Negative - FN</em>) là sai lầm nguy hiểm nhất, làm mất thời điểm vàng điều trị. Mô hình học máy bắt buộc phải ưu tiên tối đa chỉ số <strong>Recall Ác tính</strong>.
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          5. GIỚI THIỆU 3 THUẬT TOÁN: CÂY CHƯA TỈA, CẮT TỈA VÀ RỪNG NGẪU NHIÊN
          ============================================================================== */}
      <section style={{ marginBottom: '2rem' }}>
        <h3 style={{ fontSize: '1.35rem', marginBottom: '0.5rem', color: '#0f172a' }}>
          Ba Thuật Toán & Tiến Trình Tối Ưu Hóa Mô Hình
        </h3>
        <p style={{ color: '#64748b', marginBottom: '1.25rem', fontSize: '0.95rem' }}>
          Từ mô hình Cây Quyết Định đơn lẻ dễ quá khớp đến Rừng Ngẫu Nhiên bền vững có khả năng tổng quát hóa cao.
        </p>

        <div className="grid-3-col">
          {/* Cây chưa cắt tỉa */}
          <div className="algo-card">
            <div>
              <div className="algo-card-top">
                <div className="algo-icon-box" style={{ background: '#fef2f2', color: '#dc2626' }}>
                  <GitBranch size={24} />
                </div>
                <div>
                  <div className="algo-card-title">Cây Quyết Định Chưa Cắt</div>
                  <div className="algo-card-badge">Unpruned Decision Tree</div>
                </div>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: '1.5' }}>
                Xây dựng nhánh phân chia đệ quy tối đa dựa trên chỉ số tạp chất Gini mà không giới hạn độ sâu.
                Mô hình học thuộc lòng dữ liệu Train nhưng bị hiện tượng <strong>Quá khớp (Overfitting)</strong> nặng,
                phương sai cao khi gặp dữ liệu thực tế mới.
              </p>
            </div>
            <div className="algo-specs">
              <div className="algo-specs-row"><span>Độ sâu thực tế:</span><strong>8 tầng</strong></div>
              <div className="algo-specs-row"><span>Số nút lá:</span><strong>37 lá</strong></div>
              <div className="algo-specs-row"><span>Đặc tính:</span><span className="text-danger">Overfitting (Train 100%)</span></div>
            </div>
          </div>

          {/* Cây đã cắt tỉa */}
          <div className="algo-card">
            <div>
              <div className="algo-card-top">
                <div className="algo-icon-box" style={{ background: '#eff6ff', color: '#2563eb' }}>
                  <Scissors size={24} />
                </div>
                <div>
                  <div className="algo-card-title">Cây Đã Cắt Tỉa (Pruned)</div>
                  <div className="algo-card-badge">Cost-Complexity Pruning</div>
                </div>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: '1.5' }}>
                Áp dụng kỹ thuật cắt tỉa hậu kỳ với tham số phạt độ phức tạp α (Cost-Complexity Pruning path)
                kết hợp 5-Fold Cross-Validation. Cắt bỏ các nhánh lá nhỏ lẻ, giữ lại khung logic cốt lõi,
                giúp cây đơn giản và tổng quát hóa tốt hơn.
              </p>
            </div>
            <div className="algo-specs">
              <div className="algo-specs-row"><span>Độ sâu kiểm soát:</span><strong>4 tầng</strong></div>
              <div className="algo-specs-row"><span>Số nút lá:</span><strong>11 lá (giảm 70.3%)</strong></div>
              <div className="algo-specs-row"><span>Recall Malignant:</span><strong className="text-primary">96.15% (CV)</strong></div>
            </div>
          </div>

          {/* Rừng ngẫu nhiên */}
          <div className="algo-card" style={{ borderColor: '#86efac', background: 'linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%)' }}>
            <div>
              <div className="algo-card-top">
                <div className="algo-icon-box" style={{ background: '#dcfce7', color: '#16a34a' }}>
                  <Trees size={24} />
                </div>
                <div>
                  <div className="algo-card-title">Rừng Ngẫu Nhiên (Ensemble)</div>
                  <div className="algo-card-badge">Random Forest (Mô hình phục vụ)</div>
                </div>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#475569', lineHeight: '1.5' }}>
                Tập hợp <strong>100 cây quyết định độc lập</strong> kết hợp lấy mẫu có hoàn lại (Bootstrap) và
                chọn ngẫu nhiên không gian đặc trưng (max_features = 0.3, chọn 9/30 đặc trưng). Ra quyết định bằng cơ chế
                bầu chọn xác suất mềm (Soft-voting), giúp triệt tiêu phương sai và đạt độ chính xác tối ưu.
              </p>
            </div>
            <div className="algo-specs" style={{ background: '#ffffff', border: '1px solid #bbf7d0' }}>
              <div className="algo-specs-row"><span>Số lượng cây:</span><strong>100 cây (depth=8)</strong></div>
              <div className="algo-specs-row"><span>Accuracy trên Test:</span><strong className="text-success">98.84%</strong></div>
              <div className="algo-specs-row"><span>Recall Malignant:</span><strong className="text-success">96.88% (FN=1)</strong></div>
            </div>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          6. MINH HỌA LUỒNG KIẾN TRÚC: DATA -> ML MODEL -> API -> WEB
          ============================================================================== */}
      <section className="card">
        <div className="card-header">
          <span className="card-title">
            <Layers size={20} color="#2563eb" />
            Kiến Trúc Luồng Dữ Liệu Hoàn Chỉnh (Data &rarr; Model &rarr; API &rarr; Web)
          </span>
          <span className="badge badge-primary">End-to-End System Pipeline</span>
        </div>
        <div className="card-body">
          <p style={{ fontSize: '0.9rem', color: '#475569', marginBottom: '1.25rem' }}>
            Hệ thống được thiết kế theo kiến trúc phân tách độc lập (Decoupled Architecture), đảm bảo dữ liệu từ khi
            thu thập đến khi hiển thị trên giao diện đều được xác thực và bảo toàn tính toàn vẹn:
          </p>

          <div className="pipeline-flow-container">
            {/* Tầng 1 */}
            <div className="pipeline-step-card">
              <span className="step-badge">BƯỚC 1</span>
              <div className="step-card-title">
                <Database size={18} color="#2563eb" /> Tầng Dữ Liệu (Data)
              </div>
              <div className="step-card-desc">
                &bull; 569 bản ghi WDBC từ UCI.<br />
                &bull; Tiền xử lý, kiểm tra missing, loại bỏ ID.<br />
                &bull; Stratified Split chia 70% Train, 15% Val, 15% Test.<br />
                &bull; Lưu schema 30 đặc trưng.
              </div>
            </div>

            {/* Tầng 2 */}
            <div className="pipeline-step-card">
              <span className="step-badge">BƯỚC 2</span>
              <div className="step-card-title">
                <Cpu size={18} color="#16a34a" /> Tầng Mô Hình (ML)
              </div>
              <div className="step-card-desc">
                &bull; Huấn luyện Random Forest 100 cây trên Train+Val.<br />
                &bull; Đóng gói Scikit-Learn Pipeline vào file joblib.<br />
                &bull; Tạo mã băm an toàn <strong>SHA-256</strong>.<br />
                &bull; Xuất metadata và Model Card.
              </div>
            </div>

            {/* Tầng 3 */}
            <div className="pipeline-step-card">
              <span className="step-badge">BƯỚC 3</span>
              <div className="step-card-title">
                <Server size={18} color="#d97706" /> Tầng Backend (FastAPI)
              </div>
              <div className="step-card-desc">
                &bull; Nạp mô hình 1 lần bằng <strong>Lifespan Singleton</strong>.<br />
                &bull; Xác thực Pydantic (cấm thiếu, cấm thừa, cấm âm).<br />
                &bull; Kiểm tra Out-of-Distribution (OOD).<br />
                &bull; Phục vụ `POST /api/demo-classify`.
              </div>
            </div>

            {/* Tầng 4 */}
            <div className="pipeline-step-card">
              <span className="step-badge">BƯỚC 4</span>
              <div className="step-card-title">
                <Monitor size={18} color="#9333ea" /> Tầng Giao Diện (React)
              </div>
              <div className="step-card-desc">
                &bull; Single Page App xây dựng bằng Vite.<br />
                &bull; Nhập tay 30 đặc trưng hoặc chọn mẫu Demo.<br />
                &bull; Hiển thị xác suất và cờ cảnh báo nguy cơ.<br />
                &bull; Trực quan hóa phiếu bầu của 100 cây.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ==============================================================================
          7. CẢNH BÁO MIỄN TRỪ TRÁCH NHIỆM Y KHOA CHUYÊN BIỆT
          ============================================================================== */}
      <section className="advisory-card">
        <ShieldAlert size={28} color="#d97706" style={{ flexShrink: 0, marginTop: '2px' }} />
        <div>
          <h4>Tuyên Bố Miễn Trừ Trách Nhiệm Y Khoa (Clinical Non-Diagnostic Advisory)</h4>
          <p>
            Hệ thống phần mềm và mô hình học máy này là sản phẩm phục vụ mục đích <strong>nghiên cứu học thuật, giáo dục và
            minh họa thuật toán</strong> trong môn học <em>Học máy cơ bản</em> tại <strong>Đại Học Công Nghệ Kỹ Thuật Hưng Yên</strong>.
            Hệ thống <strong>TUYỆT ĐỐI KHÔNG PHẢI LÀ MỘT THIẾT BỊ Y TẾ</strong> và không có giá trị thay thế cho quy trình
            chẩn đoán lâm sàng, sinh thiết giải phẫu bệnh học hay chỉ định điều trị của các bác sĩ chuyên khoa ung bướu.
          </p>
        </div>
      </section>

      {/* ==============================================================================
          8. ĐIỀU HƯỚNG NHANH SANG CÁC MÀN HÌNH TIẾP THEO
          ============================================================================== */}
      <section className="quick-nav-box">
        <div>
          <h4 style={{ fontSize: '1.05rem', color: '#0f172a', marginBottom: '0.25rem' }}>
            Khám phá các màn hình chức năng tiếp theo của hệ thống:
          </h4>
          <p style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: 0 }}>
            Bạn có thể thử nghiệm suy luận phân loại trực tiếp hoặc xem báo cáo thực nghiệm chi tiết.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <Link to="/classification" className="btn btn-primary">
            <span>Màn hình 2: Không gian Chẩn đoán</span>
            <ArrowRight size={16} />
          </Link>
          <Link to="/dashboard" className="btn btn-secondary">
            <span>Màn hình 3: Dashboard Thực nghiệm</span>
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  );
}
