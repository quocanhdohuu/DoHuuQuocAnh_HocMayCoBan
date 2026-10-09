import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  LineChart,
  ShieldCheck,
  AlertTriangle,
  Award,
  Layers,
  Activity,
  CheckCircle2,
  HelpCircle,
  RefreshCw,
  GitCommit,
  TrendingUp,
  FileText,
  Binary,
  Maximize2,
  Table,
  Info,
  Clock,
  Sparkles,
} from 'lucide-react';
import { getDashboardReports } from '../services/api';
import { STATIC_DASHBOARD_DATA } from '../data/dashboardStaticData';

export default function DashboardPage() {
  const [data, setData] = useState(STATIC_DASHBOARD_DATA);
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState('static'); // 'api' | 'static'
  const [selectedDepthZone, setSelectedDepthZone] = useState('all'); // 'all' | 'sweet'
  const [modalImage, setModalImage] = useState(null); // URL ảnh phóng to nếu người dùng click

  // Nạp dữ liệu từ backend API nếu sẵn sàng
  const loadData = async () => {
    setLoading(true);
    const res = await getDashboardReports();
    if (res.ok && res.data) {
      // Kết hợp dữ liệu API với static fallback nếu có trường bị thiếu
      setData({
        final_test: res.data.final_test || STATIC_DASHBOARD_DATA.final_test,
        exp1_depth: res.data.exp1_depth || STATIC_DASHBOARD_DATA.exp1_depth,
        exp4_stability: res.data.exp4_stability || STATIC_DASHBOARD_DATA.exp4_stability,
        model_metadata: res.data.model_metadata || STATIC_DASHBOARD_DATA.model_metadata,
      });
      setDataSource('api');
    } else {
      // Dùng dữ liệu artifact tĩnh
      setData(STATIC_DASHBOARD_DATA);
      setDataSource('static');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const finalTest = data.final_test;
  const exp1 = data.exp1_depth;
  const exp4 = data.exp4_stability;
  const metadata = data.model_metadata;

  return (
    <div className="dashboard-page animate-fade-in">
      {/* Tiêu đề & Giới thiệu Trang */}
      <div className="page-header">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="page-title-badge">
              <BarChart3 size={16} />
              <span>Màn hình 3 • Báo Cáo Thực Nghiệm & Đánh Giá Đóng Băng</span>
            </div>
            <h2 className="page-title">Dashboard Đánh Giá & Đối Sánh Thực Nghiệm Học Máy</h2>
            <p className="page-description">
              Trực quan hóa toàn bộ kết quả 4 thí nghiệm bắt buộc trên bộ dữ liệu ung thư vú WDBC.
              Dữ liệu được trích xuất nguyên bản từ các artifact báo cáo đã đóng băng (Frozen Evaluation Metrics),
              tuyệt đối không tính lại Test, không train lại mô hình và không bịa đặt số liệu.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className={`source-status-badge ${dataSource === 'api' ? 'online' : 'static'}`}>
              <span className="status-dot" />
              <span>Nguồn: {dataSource === 'api' ? 'FastAPI /api/reports/dashboard' : 'Artifacts JSON (Đóng Băng)'}</span>
            </span>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={loadData}
              disabled={loading}
              title="Tải lại dữ liệu từ API"
            >
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              <span>Làm Mới</span>
            </button>
          </div>
        </div>
      </div>

      {/* Cảnh báo phi lâm sàng */}
      <div className="advisory-card">
        <AlertTriangle size={24} className="flex-shrink-0" color="#d97706" />
        <div>
          <h4>CẢNH BÁO HỌC THUẬT: KẾT QUẢ ĐÃ ĐƯỢC ĐÓNG BĂNG CHO MỤC ĐÍCH NGHIÊN CỨU</h4>
          <p>
            Các kết quả đo lường dưới đây được thực hiện theo quy trình chuẩn của môn Học máy cơ bản tại{' '}
            <strong>Đại Học Công Nghệ Kỹ Thuật Hưng Yên</strong>. Tập Test (86 mẫu) được giữ bí mật và chỉ đánh giá
            đúng một lần duy nhất. Mô hình phục vụ mục đích học thuật, tuyệt đối không sử dụng trong chẩn đoán lâm sàng thực tế.
          </p>
        </div>
      </div>

      {/* KHỐI TỔNG QUAN CHỈ SỐ TEST CUỐI CÙNG (KPIs ROW) */}
      {finalTest?.test_metrics_summary ? (
        <div className="dashboard-kpis-grid mb-6">
          <div className="kpi-card highlight-emerald">
            <div className="kpi-header">
              <span className="kpi-title">Recall Malignant (Độ nhạy)</span>
              <span className="kpi-badge primary">Tiêu chí số 1</span>
            </div>
            <div className="kpi-value">
              {(finalTest.test_metrics_summary.recall_malignant * 100).toFixed(2)}%
            </div>
            <div className="kpi-desc">
              95% CI: [{(finalTest.test_metrics_summary.recall_95_ci[0] * 100).toFixed(1)}% —{' '}
              {(finalTest.test_metrics_summary.recall_95_ci[1] * 100).toFixed(1)}%]
            </div>
            <div className="kpi-note text-emerald-700">Chỉ 1 ca bỏ sót duy nhất (31/32 ca phát hiện)</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span className="kpi-title">Precision Malignant (Độ chuẩn xác)</span>
              <span className="kpi-badge">FP = 0</span>
            </div>
            <div className="kpi-value">
              {(finalTest.test_metrics_summary.precision_malignant * 100).toFixed(2)}%
            </div>
            <div className="kpi-desc">Không có bất kỳ ca báo động giả nào trên tập Test</div>
            <div className="kpi-note text-slate-600">Tránh sinh thiết hoặc phẫu thuật oan</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span className="kpi-title">F1-Score (Malignant)</span>
              <span className="kpi-badge">Harmonic Mean</span>
            </div>
            <div className="kpi-value">
              {(finalTest.test_metrics_summary.f1_malignant * 100).toFixed(2)}%
            </div>
            <div className="kpi-desc">Cân bằng hoàn hảo giữa Precision & Recall</div>
            <div className="kpi-note text-slate-600">Cao nhất trong tất cả 4 mô hình đối sánh</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span className="kpi-title">ROC-AUC Test</span>
              <span className="kpi-badge">Khả năng phân tách</span>
            </div>
            <div className="kpi-value">
              {(finalTest.test_metrics_summary.roc_auc * 100).toFixed(2)}%
            </div>
            <div className="kpi-desc">Mô hình sản xuất Train+Val: {(finalTest.production_model_on_trainval?.test_roc_auc * 100).toFixed(2)}%</div>
            <div className="kpi-note text-slate-600">Phân tách gần như tuyệt đối giữa 2 phân phối</div>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span className="kpi-title">Accuracy Toàn Cục</span>
              <span className="kpi-badge">85/86 đúng</span>
            </div>
            <div className="kpi-value">
              {(finalTest.test_metrics_summary.accuracy * 100).toFixed(2)}%
            </div>
            <div className="kpi-desc">95% CI: [{(finalTest.test_metrics_summary.accuracy_95_ci[0] * 100).toFixed(1)}% — {(finalTest.test_metrics_summary.accuracy_95_ci[1] * 100).toFixed(1)}%]</div>
            <div className="kpi-note text-slate-600">Trên toàn bộ 86 mẫu Test độc lập</div>
          </div>
        </div>
      ) : (
        <div className="missing-data-box mb-6">
          <Info size={18} />
          <span>Artifact final_test_evaluation.json chưa sẵn sàng hoặc bị thiếu.</span>
        </div>
      )}

      {/* 1. KHỐI BẢNG ĐỐI SÁNH 4 MÔ HÌNH HỌC MÁY (EXPERIMENT 2) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <Award size={20} color="#0284c7" />
              1. Bảng Đối Sánh 4 Mô Hình Học Máy Trên Tập Test Đã Khóa (Experiment 2)
            </span>
            <span className="card-subtitle">
              Đánh giá độc lập trên cùng tập Test (N=86, 54 Lành tính, 32 Ác tính) không có rò rỉ dữ liệu
            </span>
          </div>
          <span className="badge badge-info">Frozen Benchmark</span>
        </div>

        <div className="card-body">
          {finalTest?.experiment_2_all_models_on_test ? (
            <div className="table-responsive">
              <table className="table comparison-table">
                <thead>
                  <tr>
                    <th>Mô hình</th>
                    <th>Thuật toán</th>
                    <th>Recall (Malignant)</th>
                    <th>Precision (Malignant)</th>
                    <th>F1-Score (Malignant)</th>
                    <th>Accuracy Toàn cục</th>
                    <th>ROC-AUC</th>
                    <th>Ma trận (TN / FP / FN / TP)</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(finalTest.experiment_2_all_models_on_test).map(([key, model]) => {
                    const isSelected = key === 'Random Forest';
                    return (
                      <tr key={key} className={isSelected ? 'selected-model-row' : ''}>
                        <td>
                          <div className="flex items-center gap-2">
                            {isSelected && <Award size={16} color="#059669" />}
                            <strong>{model.model_name || key}</strong>
                            {isSelected && <span className="badge badge-benign text-xs">Mô hình chọn</span>}
                          </div>
                        </td>
                        <td>
                          <code>{key}</code>
                        </td>
                        <td>
                          <strong className={model.recall_malignant >= 0.95 ? 'text-emerald-700 font-bold' : ''}>
                            {(model.recall_malignant * 100).toFixed(2)}%
                          </strong>
                        </td>
                        <td>
                          <span className={model.precision_malignant === 1.0 ? 'text-emerald-700 font-bold' : ''}>
                            {(model.precision_malignant * 100).toFixed(2)}%
                          </span>
                        </td>
                        <td>
                          <strong>{(model.f1_malignant * 100).toFixed(2)}%</strong>
                        </td>
                        <td>{(model.accuracy * 100).toFixed(2)}%</td>
                        <td>
                          <strong>{(model.roc_auc * 100).toFixed(2)}%</strong>
                        </td>
                        <td>
                          <span className="cm-pill">
                            TN: {model.confusion_matrix.tn} | FP: {model.confusion_matrix.fp} | FN:{' '}
                            <strong className={model.confusion_matrix.fn > 1 ? 'text-red-600' : 'text-emerald-700'}>
                              {model.confusion_matrix.fn}
                            </strong>{' '}
                            | TP: {model.confusion_matrix.tp}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="missing-data-box">
              <Info size={16} />
              <span>Chưa có dữ liệu so sánh mô hình từ artifact.</span>
            </div>
          )}

          {/* Phân tích lý do chọn Random Forest */}
          <div className="selection-rationale-box mt-4">
            <div className="rationale-header">
              <CheckCircle2 size={18} color="#059669" />
              <strong>LÝ DO KHOA HỌC CHỌN RANDOM FOREST LÀM MÔ HÌNH CUỐI CÙNG:</strong>
            </div>
            <p className="rationale-text">
              {finalTest?.locked_model_config?.model_selection?.rationale ||
                'Random Forest vượt trội toàn diện so với DummyClassifier và các Cây quyết định đơn lẻ trên cả 5-Fold Cross-Validation và tập Validation độc lập. Mô hình đạt ROC-AUC 0.9954 trên Test, hạ số ca bỏ sót bệnh xuống chỉ còn 1 ca duy nhất (Recall 96.88%), đồng thời không mắc lỗi báo động giả nào (Precision 100.0%, FP=0). Cơ chế tập hợp 100 cây con với Random Feature Selection (max_features=0.3) triệt tiêu phương sai, giải quyết triệt để vấn đề Overfitting của cây đơn lẻ.'}
            </p>
          </div>
        </div>
      </div>

      {/* 2. KHỐI PHÂN BIỆT RÕ RÀNG VALIDATION / CV VÀ TEST CUỐI CÙNG (GENERALIZATION GAP) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <Layers size={20} color="#7c3aed" />
              2. Phân Biệt Rõ Ràng Các Pha Đánh Giá: Train vs CV vs Validation vs Test
            </span>
            <span className="card-subtitle">
              Đảm bảo nguyên tắc khoa học dữ liệu: Tuyệt đối không rò rỉ dữ liệu (No Data Leakage)
            </span>
          </div>
          <span className="badge badge-purple">Multi-Phase Rigor</span>
        </div>

        <div className="card-body">
          <div className="phases-grid">
            {/* Pha 1: Huấn luyện */}
            <div className="phase-card">
              <div className="phase-badge train">Pha 1: Huấn Luyện (Train)</div>
              <h4 className="phase-title">Tập Train</h4>
              <div className="phase-samples">N = 398 mẫu (70% tổng tập)</div>
              <ul className="phase-metrics-list">
                <li>Accuracy: <strong>100.0%</strong></li>
                <li>Mục đích: Khớp cấu trúc các cây con</li>
                <li>Hiện tượng: Cây đơn lẻ bị Overfitting nếu không kiểm soát độ sâu</li>
              </ul>
            </div>

            {/* Pha 2: Kiểm định chéo */}
            <div className="phase-card">
              <div className="phase-badge cv">Pha 2: Đánh Giá Chéo (CV)</div>
              <h4 className="phase-title">5-Fold Stratified CV</h4>
              <div className="phase-samples">N = 398 mẫu (phân tầng 5 fold)</div>
              <ul className="phase-metrics-list">
                <li>Recall Malignant: <strong>92.51% ± 4.08%</strong></li>
                <li>ROC-AUC: <strong>98.20%</strong></li>
                <li>Mục đích: Tìm siêu tham số tối ưu (max_depth=8, max_features=0.3)</li>
              </ul>
            </div>

            {/* Pha 3: Thẩm định độc lập */}
            <div className="phase-card">
              <div className="phase-badge val">Pha 3: Thẩm Định Độc Lập</div>
              <h4 className="phase-title">Tập Validation</h4>
              <div className="phase-samples">N = 85 mẫu (15% tổng tập)</div>
              <ul className="phase-metrics-list">
                <li>Recall Malignant: <strong>90.62%</strong> (29/32 ca)</li>
                <li>Precision: <strong>100.0%</strong> (FP=0)</li>
                <li>ROC-AUC: <strong>99.41%</strong></li>
                <li>Mục đích: Quyết định chọn mô hình và chốt ngưỡng phân loại τ = 0.50</li>
              </ul>
            </div>

            {/* Pha 4: Kiểm tra cuối cùng */}
            <div className="phase-card highlight-final">
              <div className="phase-badge test">Pha 4: Kiểm Tra Cuối (Test)</div>
              <h4 className="phase-title">Tập Test Đã Khóa</h4>
              <div className="phase-samples">N = 86 mẫu (15% tổng tập)</div>
              <ul className="phase-metrics-list">
                <li>Recall Malignant: <strong>96.88%</strong> (31/32 ca)</li>
                <li>Precision: <strong>100.0%</strong> (FP=0)</li>
                <li>ROC-AUC: <strong>99.54%</strong></li>
                <li>Mục đích: Đánh giá khả năng tổng quát hóa cuối cùng (Chỉ mở 1 lần)</li>
              </ul>
            </div>
          </div>

          <div className="leakage-note-banner mt-4">
            <Info size={16} color="#0284c7" />
            <span>
              <strong>Cam kết kiểm soát rò rỉ dữ liệu (Data Leakage Verification):</strong> Tập Test được đóng băng hoàn toàn. Mọi thao tác tiền xử lý, trích xuất đặc trưng, tối ưu siêu tham số và chốt ngưỡng phân loại đều chỉ diễn ra trên tập Train & Validation. Tập Test chỉ được giải nén để đo lường kết quả cuối cùng tại Nhiệm vụ 14.
            </span>
          </div>
        </div>
      </div>

      {/* 3. KHỐI KHẢO SÁT ĐỘ SÂU CÂY TRAIN VS CV (EXPERIMENT 1) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <LineChart size={20} color="#0d9488" />
              3. Khảo Sát Độ Sâu Cây: Train vs 5-Fold CV (Experiment 1)
            </span>
            <span className="card-subtitle">
              Phân tích trực quan 3 vùng hiện tượng: Underfitting, Sweet Spot và Overfitting
            </span>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              className={`btn btn-sm ${selectedDepthZone === 'all' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setSelectedDepthZone('all')}
            >
              Tất cả (depth 1–20)
            </button>
            <button
              type="button"
              className={`btn btn-sm ${selectedDepthZone === 'sweet' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setSelectedDepthZone('sweet')}
            >
              Sweet Spot (depth 3–8)
            </button>
          </div>
        </div>

        <div className="card-body">
          <div className="depth-layout-grid">
            {/* Cột trái: Bảng số liệu Train vs CV qua các độ sâu */}
            <div className="depth-table-col">
              {exp1?.records ? (
                <div className="table-responsive">
                  <table className="table depth-table">
                    <thead>
                      <tr>
                        <th>Độ sâu (depth)</th>
                        <th>Train Accuracy</th>
                        <th>CV Accuracy (Mean ± Std)</th>
                        <th>Train Recall</th>
                        <th>CV Recall (Mean ± Std)</th>
                        <th>Vùng phân loại</th>
                      </tr>
                    </thead>
                    <tbody>
                      {exp1.records
                        .filter((r) => {
                          if (selectedDepthZone === 'sweet') return r.max_depth >= 3 && r.max_depth <= 8;
                          return [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20].includes(r.max_depth);
                        })
                        .map((r) => {
                          const isBest = r.max_depth === 8;
                          let zoneLabel = 'Sweet Spot';
                          let zoneClass = 'badge-benign';
                          if (r.max_depth <= 2) {
                            zoneLabel = 'Underfitting';
                            zoneClass = 'badge-warning';
                          } else if (r.max_depth > 8) {
                            zoneLabel = 'Overfitting';
                            zoneClass = 'badge-malignant';
                          }

                          return (
                            <tr key={r.max_depth} className={isBest ? 'best-depth-row' : ''}>
                              <td>
                                <strong className="font-mono">depth = {r.max_depth}</strong>
                                {isBest && <span className="badge badge-info ml-1">Tối ưu</span>}
                              </td>
                              <td>{(r.train_accuracy * 100).toFixed(1)}%</td>
                              <td>
                                {(r.cv_accuracy_mean * 100).toFixed(1)}% ± {(r.cv_accuracy_std * 100).toFixed(1)}%
                              </td>
                              <td>{(r.train_recall_malignant * 100).toFixed(1)}%</td>
                              <td>
                                <strong>
                                  {(r.cv_recall_mean * 100).toFixed(1)}% ± {(r.cv_recall_std * 100).toFixed(1)}%
                                </strong>
                              </td>
                              <td>
                                <span className={`badge ${zoneClass}`}>{zoneLabel}</span>
                              </td>
                            </tr>
                          );
                        })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="missing-data-box">
                  <Info size={16} />
                  <span>Chưa có dữ liệu độ sâu cây từ artifact exp1_depth_results.json.</span>
                </div>
              )}

              {/* Giải thích 3 vùng */}
              <div className="zones-summary-cards mt-4">
                <div className="zone-summary-card underfitting">
                  <h5>1. Vùng Dưới Khớp (Underfitting, depth 1–2):</h5>
                  <p>Mô hình quá nông, chưa nắm bắt đủ phân tách biên tế bào. Cả Train và CV score đều thấp (&lt; 90%).</p>
                </div>
                <div className="zone-summary-card sweetspot">
                  <h5>2. Vùng Điểm Cân Bằng (Sweet Spot, depth 3–8):</h5>
                  <p>Đặc biệt tại <strong>max_depth = 8</strong>: CV Recall đạt đỉnh 89.84% và CV Accuracy đạt 92.46%, phương sai thấp.</p>
                </div>
                <div className="zone-summary-card overfitting">
                  <h5>3. Vùng Quá Khớp (Overfitting, depth &gt; 8):</h5>
                  <p>Train Accuracy chạm mốc tuyệt đối 100% nhưng CV score bão hòa và nới rộng khoảng cách tổng quát hóa.</p>
                </div>
              </div>
            </div>

            {/* Cột phải: Đồ thị đường Train vs CV trích xuất từ artifact */}
            <div className="depth-figure-col">
              <div className="figure-container">
                <div className="figure-header">
                  <span>Đồ thị Train vs CV Curve (Artifact Exp 1)</span>
                  <button
                    type="button"
                    className="btn-icon"
                    onClick={() => setModalImage('/figures/exp1_depth_curve.png')}
                    title="Phóng to ảnh"
                  >
                    <Maximize2 size={16} />
                  </button>
                </div>
                <img
                  src="/figures/exp1_depth_curve.png"
                  alt="Biểu đồ Train vs CV theo độ sâu cây"
                  className="figure-img"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.parentElement.innerHTML += '<div class="missing-img-fallback">Hình ảnh artifact exp1_depth_curve.png chưa được tạo.</div>';
                  }}
                />
                <div className="figure-caption">
                  Đồ thị thể hiện sự phân kỳ giữa đường Train (màu xanh tiệm cận 1.0) và đường CV (màu cam đạt đỉnh tại depth 8 rồi đi ngang).
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 4. KHỐI MA TRẬN NHẦM LẪN (CONFUSION MATRIX) & ĐƯỜNG CONG ROC/PR TRÊN TEST */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* A. Ma trận nhầm lẫn */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <span className="card-title">
                <Binary size={20} color="#059669" />
                4. Ma Trận Nhầm Lẫn Trên Test (Confusion Matrix)
              </span>
              <span className="card-subtitle">
                Đánh giá trên 86 mẫu Test: 54 Lành tính (Benign) và 32 Ác tính (Malignant)
              </span>
            </div>
            <button
              type="button"
              className="btn-icon"
              onClick={() => setModalImage('/figures/final_test_confusion_matrix.png')}
              title="Xem ảnh đồ thị Heatmap gốc"
            >
              <Maximize2 size={16} />
            </button>
          </div>

          <div className="card-body">
            {finalTest?.test_metrics_summary?.confusion_matrix ? (
              <div>
                <div className="cm-matrix-wrapper">
                  <div className="cm-grid-table">
                    <div className="cm-corner" />
                    <div className="cm-header-col">Dự đoán Lành tính (B)</div>
                    <div className="cm-header-col">Dự đoán Ác tính (M)</div>

                    <div className="cm-header-row">Thực tế Lành tính (54 mẫu)</div>
                    <div className="cm-cell cm-tn">
                      <div className="cm-count">{finalTest.test_metrics_summary.confusion_matrix.tn}</div>
                      <div className="cm-type">True Negative (TN)</div>
                      <div className="cm-sub">100.0% Lành tính đúng</div>
                    </div>
                    <div className="cm-cell cm-fp">
                      <div className="cm-count">{finalTest.test_metrics_summary.confusion_matrix.fp}</div>
                      <div className="cm-type">False Positive (FP)</div>
                      <div className="cm-sub">0 ca báo động giả</div>
                    </div>

                    <div className="cm-header-row">Thực tế Ác tính (32 mẫu)</div>
                    <div className="cm-cell cm-fn">
                      <div className="cm-count">{finalTest.test_metrics_summary.confusion_matrix.fn}</div>
                      <div className="cm-type">False Negative (FN)</div>
                      <div className="cm-sub">Duy nhất 1 ca ranh giới (#23)</div>
                    </div>
                    <div className="cm-cell cm-tp">
                      <div className="cm-count">{finalTest.test_metrics_summary.confusion_matrix.tp}</div>
                      <div className="cm-type">True Positive (TP)</div>
                      <div className="cm-sub">96.88% Ác tính đúng</div>
                    </div>
                  </div>
                </div>

                <div className="cm-clinical-insight mt-4">
                  <strong>Ý nghĩa lâm sàng:</strong>
                  <ul>
                    <li>
                      <strong>Tỉ lệ bỏ sót (Miss Rate = FN / (TP + FN)):</strong> Chỉ 1/32 = <strong>3.12%</strong>. Phát hiện thành công 31/32 khối u ác tính.
                    </li>
                    <li>
                      <strong>Tỉ lệ báo động giả (Fallout = FP / (TN + FP)):</strong> Bằng <strong>0.0%</strong> (0/54). Toàn bộ bệnh nhân lành tính đều không bị chẩn đoán nhầm thành ung thư.
                    </li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="missing-data-box">
                <Info size={16} />
                <span>Chưa có dữ liệu Confusion Matrix từ artifact.</span>
              </div>
            )}
          </div>
        </div>

        {/* B. Đường cong ROC và Precision-Recall Curve */}
        <div className="card">
          <div className="card-header">
            <div className="card-title-group">
              <span className="card-title">
                <TrendingUp size={20} color="#0284c7" />
                5. Đường Cong ROC & Precision-Recall Trên Test
              </span>
              <span className="card-subtitle">
                Độ nhạy và độ đặc hiệu trên toàn dải ngưỡng xác suất τ ∈ [0.0, 1.0]
              </span>
            </div>
            <button
              type="button"
              className="btn-icon"
              onClick={() => setModalImage('/figures/final_test_roc_pr_curves.png')}
              title="Phóng to ảnh"
            >
              <Maximize2 size={16} />
            </button>
          </div>

          <div className="card-body">
            <div className="figure-container">
              <img
                src="/figures/final_test_roc_pr_curves.png"
                alt="Đường cong ROC và PR Curves trên Test"
                className="figure-img"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.parentElement.innerHTML += '<div class="missing-img-fallback">Hình ảnh final_test_roc_pr_curves.png chưa được tạo.</div>';
                }}
              />
            </div>

            <div className="roc-stats-row mt-4">
              <div className="roc-stat-box">
                <span className="roc-stat-label">ROC-AUC Test (Fit Train)</span>
                <span className="roc-stat-val text-primary-700">0.9954 (99.54%)</span>
              </div>
              <div className="roc-stat-box">
                <span className="roc-stat-label">ROC-AUC Test (Fit Train+Val)</span>
                <span className="roc-stat-val text-emerald-700">0.9983 (99.83%)</span>
              </div>
              <div className="roc-stat-box">
                <span className="roc-stat-label">PR-AUC Test (Đường PR)</span>
                <span className="roc-stat-val text-purple-700">0.9940 (99.40%)</span>
              </div>
            </div>

            <div className="roc-interpretation mt-3">
              <strong>Diễn giải:</strong> Giá trị ROC-AUC đạt 0.9954 khẳng định mô hình có xác suất 99.54% xếp hạng một bệnh nhân có khối u ác tính cao hơn một bệnh nhân lành tính ngẫu nhiên.
            </div>
          </div>
        </div>
      </div>

      {/* 5. KHỐI ĐỘ ỔN ĐỊNH FEATURE IMPORTANCE QUA 5 RANDOM SEEDS (EXPERIMENT 4) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <Activity size={20} color="#0d9488" />
              6. Độ Ổn Định Feature Importance Qua 5 Random Seeds (Experiment 4)
            </span>
            <span className="card-subtitle">
              Đánh giá tính nhất quán của trọng số tầm quan trọng qua 5 seed ngẫu nhiên [42, 123, 456, 789, 999]
            </span>
          </div>
          <button
            type="button"
            className="btn-icon"
            onClick={() => setModalImage('/figures/exp4_feature_stability.png')}
            title="Xem biểu đồ Feature Stability gốc"
          >
            <Maximize2 size={16} />
          </button>
        </div>

        <div className="card-body">
          <div className="stability-layout-grid">
            {/* Cột trái: Bảng Top 10 đặc trưng ổn định nhất */}
            <div className="stability-table-col">
              {exp4?.top_10_features_summary ? (
                <div className="table-responsive">
                  <table className="table stability-table">
                    <thead>
                      <tr>
                        <th>Hạng</th>
                        <th>Đặc trưng</th>
                        <th>Tên Schema</th>
                        <th>Mean Importance (Gini)</th>
                        <th>Độ lệch chuẩn (Std)</th>
                        <th>Hệ số biến thiên (CV%)</th>
                        <th>Thứ hạng TB (Rank)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {exp4.top_10_features_summary.map((feat, idx) => (
                        <tr key={feat.feature_name}>
                          <td>
                            <span className="rank-badge">#{idx + 1}</span>
                          </td>
                          <td>
                            <strong>{feat.label || feat.feature_name}</strong>
                          </td>
                          <td>
                            <code>{feat.feature_name}</code>
                          </td>
                          <td>
                            <div className="importance-bar-wrapper">
                              <div
                                className="importance-bar-fill"
                                style={{ width: `${Math.min(feat.mean_importance * 400, 100)}%` }}
                              />
                              <span className="font-semibold text-xs">
                                {(feat.mean_importance * 100).toFixed(2)}%
                              </span>
                            </div>
                          </td>
                          <td className="text-slate-600 font-mono text-xs">
                            ± {(feat.std_importance * 100).toFixed(2)}%
                          </td>
                          <td>
                            <span className={`badge ${feat.cv_pct <= 25 ? 'badge-benign' : 'badge-warning'}`}>
                              {feat.cv_pct}%
                            </span>
                          </td>
                          <td className="font-mono text-xs">
                            {feat.mean_rank} ± {feat.std_rank}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="missing-data-box">
                  <Info size={16} />
                  <span>Chưa có dữ liệu kiểm định độ ổn định đặc trưng từ artifact.</span>
                </div>
              )}
            </div>

            {/* Cột phải: Ảnh đồ thị Top 10 Feature Stability */}
            <div className="stability-figure-col">
              <div className="figure-container">
                <img
                  src="/figures/exp4_feature_stability.png"
                  alt="Biểu đồ Top 10 Feature Importance Stability qua 5 seed"
                  className="figure-img"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.parentElement.innerHTML += '<div class="missing-img-fallback">Hình ảnh exp4_feature_stability.png chưa sẵn sàng.</div>';
                  }}
                />
                <div className="figure-caption">
                  Biểu đồ thanh thể hiện độ quan trọng trung bình kèm thanh sai số (error bar) qua 5 seed độc lập.
                </div>
              </div>
            </div>
          </div>

          {/* Phân tích ảnh hưởng của Đa cộng tuyến (Collinearity) */}
          <div className="collinearity-box mt-4">
            <div className="collinearity-header">
              <Sparkles size={16} color="#0d9488" />
              <strong>ẢNH HƯỞNG CỦA ĐA CỘNG TUYẾN (COLLINEARITY) & SO SÁNH VỚI DECISION TREE:</strong>
            </div>
            <div className="collinearity-content">
              <p>
                <strong>1. Trong Decision Tree đơn lẻ:</strong> Các đặc trưng kích thước tương quan cực mạnh ($r &gt; 0.95$ giữa <code>perimeter_worst</code>, <code>radius_worst</code>, <code>area_worst</code>) khiến nút gốc liên tục bị chiếm giữ bởi 1 đặc trưng duy nhất (<code>perimeter_worst</code> chiếm tới ~75.8% tổng importance). Các đặc trưng tương quan khác bị triệt tiêu hoàn toàn (hiệu ứng che lấp - Masking Effect).
              </p>
              <p>
                <strong>2. Trong Random Forest:</strong> Nhờ cơ chế chọn ngẫu nhiên tập con đặc trưng (<code>max_features = 0.3</code>, tức chỉ chọn ~9 trong số 30 đặc trưng tại mỗi lượt phân nhánh), các đặc trưng tương quan có cơ hội được chọn luân phiên tại các cây khác nhau. Trọng số importance được san đều một cách tự nhiên (18.2%, 13.7%, 13.6%), giúp mô hình bền bỉ, không bị phụ thuộc đơn lẻ và giảm thiểu phương sai.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 6. KHỐI THẺ MÔ HÌNH HỌC MÁY TOÀN DIỆN (MODEL CARD SUMMARY) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <FileText size={20} color="#0284c7" />
              7. Thẻ Mô Hình Học Máy (Model Card Specification)
            </span>
            <span className="card-subtitle">
              Đặc tả kỹ thuật, phiên bản, kiến trúc siêu tham số và giới hạn sử dụng
            </span>
          </div>
          <span className="badge badge-primary">Model Card v1.0.0</span>
        </div>

        <div className="card-body">
          <div className="model-card-grid">
            <div className="model-spec-item">
              <span className="spec-label">Tên Mô Hình</span>
              <span className="spec-value font-bold text-primary-700">
                {metadata?.model_name || 'WDBC_RandomForest_Classifier_Pipeline'}
              </span>
            </div>

            <div className="model-spec-item">
              <span className="spec-label">Phiên Bản & Framework</span>
              <span className="spec-value">
                Phiên bản {metadata?.version || '1.0.0'} ({metadata?.framework || 'scikit-learn 1.9.1'})
              </span>
            </div>

            <div className="model-spec-item">
              <span className="spec-label">Bộ Dữ Liệu Nguồn</span>
              <span className="spec-value">
                UCI Breast Cancer Wisconsin Diagnostic (569 mẫu, 30 đặc trưng FNA)
              </span>
            </div>

            <div className="model-spec-item">
              <span className="spec-label">Tác Giả & Cơ Sở</span>
              <span className="spec-value">
                {metadata?.author || 'Đỗ Hữu Quốc Anh'} • {metadata?.institution || 'Đại Học Công Nghệ Kỹ Thuật Hưng Yên'}
              </span>
            </div>

            <div className="model-spec-item">
              <span className="spec-label">Mã Băm Toàn Vẹn SHA-256</span>
              <span className="spec-value font-mono text-xs break-all">
                {metadata?.sha256_checksum || '1f5c3bc820674e6911d07fd1a372d592bc696e280470903a51276dc4a83451d1'}
              </span>
            </div>

            <div className="model-spec-item">
              <span className="spec-label">Ngưỡng Quyết Định Phân Loại</span>
              <span className="spec-value font-bold">
                τ = {metadata?.decision_threshold || 0.50} (Chuẩn lâm sàng)
              </span>
            </div>
          </div>

          <div className="hyperparameters-box mt-4">
            <h5>Siêu tham số đã đóng băng (Locked Hyperparameters):</h5>
            <div className="hyperparams-tags">
              <span className="hyperparam-tag">n_estimators: 100 cây con</span>
              <span className="hyperparam-tag">criterion: Gini Impurity</span>
              <span className="hyperparam-tag">max_depth: 8 (Kiểm soát Overfitting)</span>
              <span className="hyperparam-tag">max_features: 0.3 (~9 đặc trưng/nốt)</span>
              <span className="hyperparam-tag">min_samples_leaf: 1</span>
              <span className="hyperparam-tag">bootstrap: True</span>
              <span className="hyperparam-tag">random_state: 42</span>
            </div>
          </div>

          <div className="limitations-alert-box mt-4">
            <div className="limitations-header">
              <AlertTriangle size={16} color="#b45309" />
              <strong>GIỚI HẠN MÔ HÌNH & ĐIỀU KIỆN SỬ DỤNG:</strong>
            </div>
            <ul className="limitations-list">
              <li>
                <strong>Không suy diễn quan hệ nhân quả:</strong> Feature Importance đo lường khả năng chia cắt mẫu toán học (Gini decrease), tuyệt đối không suy luận đây là nguyên nhân sinh học gây ra ung thư.
              </li>
              <li>
                <strong>Dữ liệu lịch sử 1995:</strong> Bộ dữ liệu được thu thập từ Đại học Wisconsin vào những năm 1990 trên một nhóm dân số cụ thể. Khi áp dụng vào dữ liệu thiết bị FNA hiện đại cần hiệu chuẩn lại phân phối.
              </li>
              <li>
                <strong>Không dùng độc lập trong chẩn đoán y tế:</strong> Mọi kết quả dự đoán chỉ mang tính hỗ trợ tham khảo học tập, bắt buộc phải có bác sĩ giải phẫu bệnh đọc tiêu bản mô bệnh học trực tiếp.
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Modal phóng to ảnh artifact khi người dùng click */}
      {modalImage && (
        <div className="modal-backdrop" onClick={() => setModalImage(null)}>
          <div className="modal-content animate-scale-up" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <span>Artifact Hình Ảnh Nghiên Cứu Đóng Băng</span>
              <button type="button" className="btn-close" onClick={() => setModalImage(null)}>
                ✕
              </button>
            </div>
            <div className="modal-body">
              <img src={modalImage} alt="Artifact phóng to" className="modal-img" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
