import React, { useState, useMemo } from 'react';
import {
  Stethoscope,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  AlertOctagon,
  Info,
  RotateCcw,
  Send,
  Activity,
  Sliders,
  ShieldCheck,
  ShieldAlert,
  HelpCircle,
  Layers,
  TrendingUp,
  BarChart3,
  ListFilter,
  Check,
  ExternalLink,
} from 'lucide-react';
import {
  FEATURE_DEFINITIONS,
  DEMO_PRESETS,
  EMPTY_FEATURES,
} from '../data/featureMetadata';
import { classifySample } from '../services/api';

// Tạo bản đồ tra cứu đặc trưng theo key để tra cứu nhãn tiếng Việt & đơn vị
const FEATURE_MAP = FEATURE_DEFINITIONS.reduce((acc, feat) => {
  acc[feat.key] = feat;
  return acc;
}, {});

export default function ClassificationPage() {
  // Trạng thái chọn mẫu Preset (mặc định chọn mẫu lành tính benign để người dùng trải nghiệm ngay)
  const [selectedPresetKey, setSelectedPresetKey] = useState('benign');

  // Trạng thái lưu trữ 30 giá trị đặc trưng người dùng đang nhập / chỉnh sửa
  const [inputs, setInputs] = useState(() => ({ ...DEMO_PRESETS.benign.data }));

  // Ngưỡng quyết định lâm sàng (Decision Threshold, mặc định 0.50)
  const [threshold, setThreshold] = useState(0.50);

  // Tab lọc nhóm đặc trưng hiển thị: 'all' | 'mean' | 'se' | 'worst'
  const [activeGroupTab, setActiveGroupTab] = useState('all');

  // Trạng thái API: loading, success (result), error
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Khi người dùng chọn 1 Preset từ thanh mẫu
  const handleSelectPreset = (presetKey) => {
    setSelectedPresetKey(presetKey);
    if (DEMO_PRESETS[presetKey]) {
      setInputs({ ...DEMO_PRESETS[presetKey].data });
    } else {
      setInputs({ ...EMPTY_FEATURES });
    }
    setResult(null);
    setError(null);
  };

  // Khi người dùng thay đổi giá trị một ô input
  const handleInputChange = (key, value) => {
    setInputs((prev) => ({
      ...prev,
      [key]: value,
    }));
    // Đổi preset sang 'custom' nếu đang sửa tay
    if (selectedPresetKey !== 'custom') {
      setSelectedPresetKey('custom');
    }
  };

  // Đặt lại toàn bộ ô nhập về rỗng để nhập thủ công từ đầu
  const handleResetToEmpty = () => {
    setSelectedPresetKey('custom');
    setInputs({ ...EMPTY_FEATURES });
    setResult(null);
    setError(null);
  };

  // Kiểm tra danh sách đặc trưng hiển thị theo tab
  const displayedFeatures = useMemo(() => {
    if (activeGroupTab === 'all') return FEATURE_DEFINITIONS;
    return FEATURE_DEFINITIONS.filter((feat) => feat.group === activeGroupTab);
  }, [activeGroupTab]);

  // Kiểm tra xem một giá trị có nằm ngoài miền huấn luyện Train không
  const isOutOfRange = (feat, val) => {
    if (val === '' || val === null || val === undefined) return false;
    const num = parseFloat(val);
    if (isNaN(num)) return false;
    return num < feat.min || num > feat.max;
  };

  // Đếm số lượng đặc trưng ngoài miền đang nhập
  const oodCount = useMemo(() => {
    return FEATURE_DEFINITIONS.reduce((acc, feat) => {
      const val = inputs[feat.key];
      return isOutOfRange(feat, val) ? acc + 1 : acc;
    }, 0);
  }, [inputs]);

  // Xử lý gửi yêu cầu suy luận đến FastAPI
  const handleClassify = async (e) => {
    if (e) e.preventDefault();

    // 1. Kiểm tra tính đầy đủ và hợp lệ của 30 đặc trưng
    // Tuân thủ nguyên tắc: Không tự ý điền giá trị ngầm hay làm tròn
    const missing = [];
    const invalid = [];
    const parsedFeatures = {};

    FEATURE_DEFINITIONS.forEach((feat) => {
      const rawVal = inputs[feat.key];
      if (rawVal === '' || rawVal === null || rawVal === undefined) {
        missing.push({ key: feat.key, label: feat.label });
      } else {
        const num = parseFloat(rawVal);
        if (isNaN(num)) {
          invalid.push({ key: feat.key, label: feat.label, val: rawVal, reason: 'Không phải số hợp lệ' });
        } else if (num < 0) {
          invalid.push({ key: feat.key, label: feat.label, val: rawVal, reason: 'Giá trị âm không hợp lệ trong sinh học tế bào' });
        } else {
          parsedFeatures[feat.key] = num;
        }
      }
    });

    if (missing.length > 0 || invalid.length > 0) {
      setError({
        type: 'validation_error',
        title: 'Dữ liệu đầu vào chưa hoàn chỉnh hoặc có lỗi định dạng',
        message: 'Hệ thống tuân thủ nghiêm ngặt nguyên tắc KHÔNG tự ý bổ sung hoặc suy diễn ngầm giá trị thiếu/sai. Vui lòng kiểm tra và hoàn thiện tất cả 30 chỉ số.',
        missing,
        invalid,
      });
      setResult(null);
      return;
    }

    // 2. Bắt đầu gọi API
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      features: parsedFeatures,
      threshold: parseFloat(threshold),
    };

    try {
      const response = await classifySample(payload);
      setLoading(false);

      if (response.ok && response.data.status === 'success') {
        setResult(response.data);
      } else {
        // Lỗi từ FastAPI (ví dụ 422 Unprocessable Entity, 503 Model Not Loaded, v.v.)
        const detail = response.data?.detail || response.data?.message || 'Lỗi không xác định từ máy chủ API.';
        setError({
          type: 'api_error',
          title: `Lỗi từ Máy chủ API (Mã HTTP: ${response.status})`,
          detail,
        });
      }
    } catch (err) {
      setLoading(false);
      setError({
        type: 'network_error',
        title: 'Lỗi kết nối mạng',
        detail: `Không thể giao tiếp với FastAPI Backend tại endpoint /api/demo-classify: ${err.message}`,
      });
    }
  };

  return (
    <div className="classification-page animate-fade-in">
      {/* Tiêu đề & Giới thiệu Trang */}
      <div className="page-header">
        <div className="page-title-badge">
          <Stethoscope size={16} />
          <span>Màn hình 2 • Không gian Suy luận Học máy</span>
        </div>
        <h2 className="page-title">Chẩn Đoán & Phân Loại Khối U Trực Tuyến</h2>
        <p className="page-description">
          Thực hiện suy luận dự đoán khối u vú Lành tính (Benign) hay Ác tính (Malignant) từ 30 đặc trưng sinh thiết FNA
          bằng mô hình Random Forest (100 cây) đã huấn luyện và đóng gói trong Scikit-Learn Pipeline.
        </p>
      </div>

      {/* Cảnh báo phi lâm sàng bắt buộc */}
      <div className="advisory-card">
        <AlertTriangle size={24} className="flex-shrink-0" color="#d97706" />
        <div>
          <h4>CẢNH BÁO: CHỈ SỬ DỤNG CHO MỤC ĐÍCH NGHIÊN CỨU & HỌC TẬP</h4>
          <p>
            Hệ thống là sản phẩm mô phỏng thuộc đề tài Project 16 môn Học máy cơ bản tại{' '}
            <strong>Đại Học Công Nghệ Kỹ Thuật Hưng Yên</strong>. Mô hình <strong>TUYỆT ĐỐI KHÔNG ĐƯỢC DÙNG</strong>{' '}
            để thay thế chẩn đoán y khoa của bác sĩ chuyên khoa hoặc chỉ định can thiệp lâm sàng trên người bệnh.
            Hệ thống chỉ xử lý dữ liệu số vô danh, không lưu trữ dữ liệu cá nhân hay hồ sơ bệnh án thật.
          </p>
        </div>
      </div>

      {/* PHẦN 1: THANH CHỌN MẪU THỬ NGHIỆM ĐÃ CHUẨN BỊ (PRESETS) */}
      <div className="card mb-6">
        <div className="card-header">
          <div className="card-title-group">
            <span className="card-title">
              <Sparkles size={20} color="#0284c7" />
              1. Chọn Mẫu Thử Nghiệm Từ Tập Dữ Liệu Nghiên Cứu
            </span>
            <span className="card-subtitle">
              Chọn nhanh các mẫu đặc trưng điển hình trong tập Test đã được đánh giá ở Nhiệm vụ 14 & 15
            </span>
          </div>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleResetToEmpty}
            title="Xóa trắng tất cả các trường để nhập thủ công từ đầu"
          >
            <RotateCcw size={14} />
            <span>Xóa Trống / Nhập Thủ Công</span>
          </button>
        </div>

        <div className="card-body">
          <div className="presets-grid">
            {/* 1. Mẫu Lành Tính */}
            <div
              className={`preset-card ${selectedPresetKey === 'benign' ? 'active benign' : ''}`}
              onClick={() => handleSelectPreset('benign')}
            >
              <div className="preset-card-header">
                <span className="badge badge-benign">Benign (Lành tính)</span>
                <span className="preset-source">{DEMO_PRESETS.benign.source}</span>
              </div>
              <h4 className="preset-card-title">{DEMO_PRESETS.benign.name}</h4>
              <p className="preset-card-desc">{DEMO_PRESETS.benign.description}</p>
              <div className="preset-card-footer">
                <span className="preset-expected">Kỳ vọng: {DEMO_PRESETS.benign.expected}</span>
                {selectedPresetKey === 'benign' && <Check size={16} color="#059669" />}
              </div>
            </div>

            {/* 2. Mẫu Ác Tính */}
            <div
              className={`preset-card ${selectedPresetKey === 'malignant' ? 'active malignant' : ''}`}
              onClick={() => handleSelectPreset('malignant')}
            >
              <div className="preset-card-header">
                <span className="badge badge-malignant">Malignant (Ác tính)</span>
                <span className="preset-source">{DEMO_PRESETS.malignant.source}</span>
              </div>
              <h4 className="preset-card-title">{DEMO_PRESETS.malignant.name}</h4>
              <p className="preset-card-desc">{DEMO_PRESETS.malignant.description}</p>
              <div className="preset-card-footer">
                <span className="preset-expected">Kỳ vọng: {DEMO_PRESETS.malignant.expected}</span>
                {selectedPresetKey === 'malignant' && <Check size={16} color="#dc2626" />}
              </div>
            </div>

            {/* 3. Mẫu Ranh Giới (Borderline Case) */}
            <div
              className={`preset-card ${selectedPresetKey === 'borderline' ? 'active borderline' : ''}`}
              onClick={() => handleSelectPreset('borderline')}
            >
              <div className="preset-card-header">
                <span className="badge badge-warning">Ca Ranh Giới (FN #23)</span>
                <span className="preset-source">{DEMO_PRESETS.borderline.source}</span>
              </div>
              <h4 className="preset-card-title">{DEMO_PRESETS.borderline.name}</h4>
              <p className="preset-card-desc">{DEMO_PRESETS.borderline.description}</p>
              <div className="preset-card-footer">
                <span className="preset-expected">Kỳ vọng: {DEMO_PRESETS.borderline.expected}</span>
                {selectedPresetKey === 'borderline' && <Check size={16} color="#d97706" />}
              </div>
            </div>

            {/* 4. Mẫu Ngoài Miền (Out-of-Distribution) */}
            <div
              className={`preset-card ${selectedPresetKey === 'ood' ? 'active ood' : ''}`}
              onClick={() => handleSelectPreset('ood')}
            >
              <div className="preset-card-header">
                <span className="badge badge-warning">Cảnh báo OOD</span>
                <span className="preset-source">{DEMO_PRESETS.ood.source}</span>
              </div>
              <h4 className="preset-card-title">{DEMO_PRESETS.ood.name}</h4>
              <p className="preset-card-desc">{DEMO_PRESETS.ood.description}</p>
              <div className="preset-card-footer">
                <span className="preset-expected">Kỳ vọng: {DEMO_PRESETS.ood.expected}</span>
                {selectedPresetKey === 'ood' && <Check size={16} color="#d97706" />}
              </div>
            </div>
          </div>

          {selectedPresetKey === 'custom' && (
            <div className="custom-input-notice">
              <Info size={16} color="#0284c7" />
              <span>
                Chế độ nhập tùy chỉnh: Bạn đang tự điền hoặc chỉnh sửa các chỉ số tế bào. Bạn có thể thay đổi bất kỳ trường nào dưới đây.
              </span>
            </div>
          )}
        </div>
      </div>

      {/* PHẦN 2: BẢNG NHẬP & CHỈNH SỬA 30 ĐẶC TRƯNG SỐ FNA */}
      <form onSubmit={handleClassify}>
        <div className="card mb-6">
          <div className="card-header">
            <div className="card-title-group">
              <span className="card-title">
                <Layers size={20} color="#0d9488" />
                2. Thông Số 30 Đặc Trưng Tế Bào Nhân FNA
              </span>
              <span className="card-subtitle">
                Được sắp xếp thành 3 nhóm khoa học: Mean (Trung bình), SE (Sai số chuẩn), và Worst (Giá trị lớn nhất)
              </span>
            </div>

            {/* Tab điều hướng nhóm đặc trưng */}
            <div className="group-tabs">
              <button
                type="button"
                className={`group-tab-btn ${activeGroupTab === 'all' ? 'active' : ''}`}
                onClick={() => setActiveGroupTab('all')}
              >
                Tất cả (30)
              </button>
              <button
                type="button"
                className={`group-tab-btn ${activeGroupTab === 'mean' ? 'active' : ''}`}
                onClick={() => setActiveGroupTab('mean')}
              >
                1. Mean (10)
              </button>
              <button
                type="button"
                className={`group-tab-btn ${activeGroupTab === 'se' ? 'active' : ''}`}
                onClick={() => setActiveGroupTab('se')}
              >
                2. Standard Error (10)
              </button>
              <button
                type="button"
                className={`group-tab-btn ${activeGroupTab === 'worst' ? 'active' : ''}`}
                onClick={() => setActiveGroupTab('worst')}
              >
                3. Worst (10)
              </button>
            </div>
          </div>

          <div className="card-body">
            {/* Cảnh báo OOD đếm được trực tiếp */}
            {oodCount > 0 && (
              <div className="ood-alert-pill mb-4">
                <AlertTriangle size={16} />
                <span>
                  Phát hiện <strong>{oodCount} đặc trưng</strong> có giá trị nằm ngoài miền tham chiếu quan sát được của tập Train.
                  Mô hình vẫn sẽ thực hiện suy luận nhưng sẽ đính kèm cảnh báo ngoại miền (OOD).
                </span>
              </div>
            )}

            {/* Grid hiển thị các trường nhập */}
            <div className="features-input-grid">
              {displayedFeatures.map((feat) => {
                const currentVal = inputs[feat.key] ?? '';
                const ood = isOutOfRange(feat, currentVal);

                return (
                  <div
                    key={feat.key}
                    className={`feature-field-card ${ood ? 'is-ood' : ''}`}
                  >
                    <div className="feature-field-header">
                      <label htmlFor={`input-${feat.key}`} className="feature-field-label">
                        {feat.label}
                      </label>
                      <span className="feature-unit-badge">{feat.unit}</span>
                    </div>

                    <div className="feature-field-key">{feat.key}</div>

                    <div className="feature-input-wrapper">
                      <input
                        id={`input-${feat.key}`}
                        type="number"
                        step={feat.step || 'any'}
                        className={`form-input feature-input ${ood ? 'input-warning' : ''}`}
                        value={currentVal}
                        placeholder={`VD: ${feat.min}`}
                        onChange={(e) => handleInputChange(feat.key, e.target.value)}
                      />
                    </div>

                    <div className="feature-field-meta">
                      <div className="feature-range-tag">
                        Miền Train: [{feat.min} — {feat.max}]
                      </div>
                      {ood && (
                        <div className="feature-ood-tag">
                          Ngoài dải!
                        </div>
                      )}
                    </div>

                    <div className="feature-description-text" title={feat.description}>
                      {feat.description}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Thanh cài đặt ngưỡng & Nút Gửi suy luận */}
          <div className="card-footer classification-action-bar">
            <div className="threshold-control-box">
              <div className="threshold-label-group">
                <Sliders size={16} color="#0d9488" />
                <label htmlFor="decision-threshold" className="threshold-label">
                  Ngưỡng Quyết Định Phân Loại: <strong>{threshold.toFixed(2)}</strong>
                </label>
              </div>
              <input
                id="decision-threshold"
                type="range"
                min="0.10"
                max="0.90"
                step="0.05"
                value={threshold}
                onChange={(e) => setThreshold(parseFloat(e.target.value))}
                className="threshold-slider"
              />
              <span className="threshold-hint">
                Nếu P(Malignant) ≥ {threshold.toFixed(2)} → Dự đoán Ác tính (M). Mặc định chuẩn: 0.50.
              </span>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-lg btn-classify"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner-border spinner-sm" />
                  <span>Đang Suy Luận Qua 100 Cây...</span>
                </>
              ) : (
                <>
                  <Send size={18} />
                  <span>Thực Hiện Phân Loại Bệnh Phẩm</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* PHẦN 3: HIỂN THỊ TRẠNG THÁI LOADING / LỖI / KẾT QUẢ */}

      {/* A. Trạng thái Đang Tải (Loading State) */}
      {loading && (
        <div className="card loading-card animate-fade-in mb-6">
          <div className="card-body text-center py-8">
            <div className="spinner-border spinner-lg mb-4" />
            <h3 className="loading-title">Đang Gửi Dữ Liệu Tới Backend & Thực Hiện Suy Luận Học Máy</h3>
            <p className="loading-desc">
              FastAPI đang nạp vector 30 đặc trưng, chuẩn hóa theo thứ tự schema, tính toán xác suất qua 100 cây quyết định ngẫu nhiên và trích xuất độ quan trọng của đặc trưng...
            </p>
          </div>
        </div>
      )}

      {/* B. Trạng thái Báo Lỗi (Error State) */}
      {error && (
        <div className="error-alert-card animate-fade-in mb-6">
          <div className="error-alert-header">
            <AlertOctagon size={24} color="#dc2626" />
            <div>
              <h4 className="error-alert-title">{error.title}</h4>
              {error.message && <p className="error-alert-subtitle">{error.message}</p>}
            </div>
          </div>

          {/* Nếu có trường bị thiếu */}
          {error.missing && error.missing.length > 0 && (
            <div className="error-list-section">
              <h5>Các trường còn thiếu dữ liệu ({error.missing.length} trường):</h5>
              <div className="error-tags-wrap">
                {error.missing.map((item) => (
                  <span key={item.key} className="badge badge-malignant">
                    {item.label} ({item.key})
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Nếu có trường bị sai định dạng / âm */}
          {error.invalid && error.invalid.length > 0 && (
            <div className="error-list-section">
              <h5>Các trường có giá trị không hợp lệ ({error.invalid.length} trường):</h5>
              <ul className="error-details-list">
                {error.invalid.map((item) => (
                  <li key={item.key}>
                    <strong>{item.label} ({item.key})</strong>: Nhận giá trị "{item.val}" — <em>{item.reason}</em>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Nếu là lỗi API / Network */}
          {error.detail && (
            <div className="error-raw-box">
              <pre>{typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail, null, 2)}</pre>
            </div>
          )}
        </div>
      )}

      {/* C. Trạng thái Thành Công: HIỂN THỊ KẾT QUẢ DỰ ĐOÁN & GIẢI THÍCH MÔ HÌNH */}
      {result && (
        <div className="result-container animate-fade-in mb-6">
          {/* 1. Thẻ Kết Quả Dự Đoán Chính */}
          <div className={`card result-main-card ${result.predicted_code === 'M' ? 'result-malignant' : 'result-benign'}`}>
            <div className="result-header">
              <div className="result-badge-group">
                {result.predicted_code === 'M' ? (
                  <div className="result-main-badge malignant">
                    <ShieldAlert size={32} />
                    <div>
                      <div className="result-type-label">KẾT QUẢ DỰ ĐOÁN TỪ RANDOM FOREST</div>
                      <h3 className="result-class-name">KHỐI U ÁC TÍNH (MALIGNANT)</h3>
                      <span className="result-code-tag">Mã nhãn: M (Lớp 1) • Nguy cơ cao</span>
                    </div>
                  </div>
                ) : (
                  <div className="result-main-badge benign">
                    <ShieldCheck size={32} />
                    <div>
                      <div className="result-type-label">KẾT QUẢ DỰ ĐOÁN TỪ RANDOM FOREST</div>
                      <h3 className="result-class-name">KHỐI U LÀNH TÍNH (BENIGN)</h3>
                      <span className="result-code-tag">Mã nhãn: B (Lớp 0) • Nguy cơ thấp</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="result-meta-box">
                <div className="result-meta-item">
                  <span className="meta-label">Độ tin cậy mô hình</span>
                  <span className="meta-value font-bold">{result.confidence_score}%</span>
                </div>
                <div className="result-meta-item">
                  <span className="meta-label">Ngưỡng quyết định</span>
                  <span className="meta-value">τ = {result.decision_threshold}</span>
                </div>
                <div className="result-meta-item">
                  <span className="meta-label">Thời gian phản hồi</span>
                  <span className="meta-value text-xs">{new Date(result.timestamp).toLocaleTimeString('vi-VN')}</span>
                </div>
              </div>
            </div>

            {/* Phân bổ xác suất 2 lớp */}
            <div className="probabilities-section">
              <div className="prob-header-row">
                <span className="prob-title">Phân Bổ Xác Suất Dự Đoán (predict_proba):</span>
                <span className="prob-sum-check">Tổng xác suất = 100.0%</span>
              </div>

              {/* Thanh tiến trình tỉ lệ xác suất */}
              <div className="prob-bar-container">
                <div
                  className="prob-bar-segment benign-bar"
                  style={{ width: `${result.probabilities.benign * 100}%` }}
                >
                  {result.probabilities.benign >= 0.15 && (
                    <span className="prob-bar-text">
                      Lành tính: {(result.probabilities.benign * 100).toFixed(2)}%
                    </span>
                  )}
                </div>
                <div
                  className="prob-bar-segment malignant-bar"
                  style={{ width: `${result.probabilities.malignant * 100}%` }}
                >
                  {result.probabilities.malignant >= 0.15 && (
                    <span className="prob-bar-text">
                      Ác tính: {(result.probabilities.malignant * 100).toFixed(2)}%
                    </span>
                  )}
                </div>
              </div>

              <div className="prob-labels-row">
                <div className="prob-label-item benign">
                  <span className="prob-dot benign" />
                  <span>Xác suất Lành tính (Benign - B):</span>
                  <strong>{(result.probabilities.benign * 100).toFixed(2)}%</strong>
                </div>
                <div className="prob-label-item malignant">
                  <span className="prob-dot malignant" />
                  <span>Xác suất Ác tính (Malignant - M):</span>
                  <strong>{(result.probabilities.malignant * 100).toFixed(2)}%</strong>
                </div>
              </div>
            </div>

            {/* Hộp Cảnh báo Ngoại Miền (OOD) nếu Backend phát hiện */}
            {result.warnings && result.warnings.length > 0 && (
              <div className="ood-warning-panel">
                <div className="ood-panel-header">
                  <AlertTriangle size={18} color="#d97706" />
                  <strong>Cảnh Báo Đặc Trưng Nằm Ngoài Miền Dữ Liệu Huấn Luyện (OOD):</strong>
                </div>
                <ul className="ood-warnings-list">
                  {result.warnings.map((warn, idx) => (
                    <li key={idx}>{warn}</li>
                  ))}
                </ul>
                <div className="ood-panel-note">
                  Lưu ý: Mô hình học máy dựa trên phân phối thực nghiệm. Khi các chỉ số vượt ra ngoài phạm vi từng quan sát, mức độ tin cậy của xác suất có thể bị suy giảm.
                </div>
              </div>
            )}
          </div>

          {/* 2. Thẻ Giải Thích Mô Hình Học Máy (Model Explanation) */}
          <div className="card mt-6">
            <div className="card-header">
              <div className="card-title-group">
                <span className="card-title">
                  <BarChart3 size={20} color="#0284c7" />
                  3. Giải Thích Quyết Định Dự Đoán (Model Explanation)
                </span>
                <span className="card-subtitle">
                  Phương pháp giải thích phù hợp với kiến trúc Random Forest (Ensemble Voting & Feature Importance)
                </span>
              </div>
              <span className="badge badge-info">
                {result.explanation.explanation_method || 'Ensemble Voting'}
              </span>
            </div>

            <div className="card-body">
              {/* A. Thống kê Bầu Chọn Của 100 Cây Quyết Định (Voting Consensus) */}
              {result.explanation.votes_breakdown && (
                <div className="explanation-section mb-6">
                  <h4 className="explanation-section-title">
                    <Activity size={18} color="#0d9488" />
                    Cơ Chế Bầu Chọn Đồng Thuận Của Rừng Cây (Ensemble Voting Breakdown)
                  </h4>
                  <p className="explanation-section-desc">
                    Mô hình Random Forest bao gồm{' '}
                    <strong>{result.explanation.total_trees || 100} cây quyết định</strong> độc lập được huấn luyện với kĩ thuật Bootstrap Aggregation (Bagging).
                    Mỗi cây đưa ra một phiếu bầu nhãn riêng biệt:
                  </p>

                  <div className="voting-meters-grid">
                    <div className="voting-meter-card benign">
                      <div className="voting-meter-count">
                        {result.explanation.votes_breakdown.benign_votes} / {result.explanation.total_trees || 100}
                      </div>
                      <div className="voting-meter-label">Cây bầu Khối u Lành tính (Benign)</div>
                      <div className="voting-meter-pct">
                        Tỷ lệ: {result.explanation.vote_percentage?.Benign || ((result.explanation.votes_breakdown.benign_votes / 100) * 100)}%
                      </div>
                    </div>

                    <div className="voting-meter-card malignant">
                      <div className="voting-meter-count">
                        {result.explanation.votes_breakdown.malignant_votes} / {result.explanation.total_trees || 100}
                      </div>
                      <div className="voting-meter-label">Cây bầu Khối u Ác tính (Malignant)</div>
                      <div className="voting-meter-pct">
                        Tỷ lệ: {result.explanation.vote_percentage?.Malignant || ((result.explanation.votes_breakdown.malignant_votes / 100) * 100)}%
                      </div>
                    </div>
                  </div>

                  <div className="aggregation-tag">
                    <Info size={14} />
                    <span>Cơ chế tổng hợp: <strong>{result.explanation.aggregation_mechanism}</strong></span>
                  </div>
                </div>
              )}

              {/* B. Bảng Top 5 Đặc Trưng Quan Trọng Nhất */}
              {result.explanation.top_influential_features && (
                <div className="explanation-section mb-6">
                  <h4 className="explanation-section-title">
                    <TrendingUp size={18} color="#0284c7" />
                    Top 5 Đặc Trưng Quan Trọng Nhất Trong Quyết Định Của Rừng Cây
                  </h4>
                  <p className="explanation-section-desc">
                    Trích xuất từ thuộc tính <code>feature_importances_</code> (Gini Importance) của Random Forest,
                    kết hợp đối chiếu giá trị thực tế của bệnh phẩm đang thử nghiệm:
                  </p>

                  <div className="table-responsive">
                    <table className="table">
                      <thead>
                        <tr>
                          <th style={{ width: '8%' }}>Thứ hạng</th>
                          <th style={{ width: '32%' }}>Đặc trưng sinh học</th>
                          <th style={{ width: '18%' }}>Tên biến (Schema)</th>
                          <th style={{ width: '22%' }}>Độ quan trọng toàn cục</th>
                          <th style={{ width: '20%' }}>Giá trị mẫu hiện tại</th>
                        </tr>
                      </thead>
                      <tbody>
                        {result.explanation.top_influential_features.map((feat) => {
                          const meta = FEATURE_MAP[feat.feature];
                          return (
                            <tr key={feat.feature}>
                              <td>
                                <span className="rank-badge">#{feat.rank}</span>
                              </td>
                              <td>
                                <strong>{meta ? meta.label : feat.feature}</strong>
                              </td>
                              <td>
                                <code className="feature-code">{feat.feature}</code>
                              </td>
                              <td>
                                <div className="importance-bar-wrapper">
                                  <div
                                    className="importance-bar-fill"
                                    style={{ width: `${Math.min(feat.importance_score * 400, 100)}%` }}
                                  />
                                  <span className="importance-score-text">
                                    {(feat.importance_score * 100).toFixed(2)}% ({feat.importance_score})
                                  </span>
                                </div>
                              </td>
                              <td>
                                <span className="sample-val-badge">
                                  {feat.sample_value} {meta ? meta.unit : ''}
                                </span>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* C. Tuyên Bố Giới Hạn Phương Pháp Giải Thích (Methodological Limitation) */}
              {result.explanation.methodological_limitation && (
                <div className="methodological-box">
                  <div className="methodological-box-header">
                    <Info size={16} color="#0284c7" />
                    <strong>NGUYÊN TẮC KHOA HỌC & GIỚI HẠN GIẢI THÍCH ENSEMBLE:</strong>
                  </div>
                  <p className="methodological-box-text">
                    {result.explanation.methodological_limitation}
                  </p>
                </div>
              )}
            </div>

            <div className="card-footer bg-slate-50 flex items-center justify-between text-xs text-slate-500">
              <span>Mô hình: <strong>{result.model_info.model_name}</strong> (Phiên bản {result.model_info.version})</span>
              <span>Thuật toán: <strong>{result.model_info.algorithm}</strong></span>
              <span>Đặc trưng đầu vào: <strong>{result.model_info.input_features_count} chiều</strong></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
