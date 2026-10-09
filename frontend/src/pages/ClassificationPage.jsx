import React from 'react';
import { Stethoscope, Sparkles } from 'lucide-react';

export default function ClassificationPage() {
  return (
    <div className="classification-page animate-fade-in">
      <div className="page-header">
        <h2 className="page-title">Màn hình 2: Không gian Chẩn đoán Trực tiếp</h2>
        <p className="page-description">
          Thực hiện suy luận phân loại khối u vú Lành tính (Benign) hoặc Ác tính (Malignant)
          từ 30 đặc trưng số FNA thông qua mô hình Scikit-Learn Pipeline đã đóng gói.
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">
            <Stethoscope size={20} color="#059669" />
            Không gian Thao tác Chẩn đoán & Suy luận AI
          </span>
          <span className="badge badge-benign">Inference Workspace</span>
        </div>
        <div className="card-body">
          <div className="placeholder-box">
            <div className="placeholder-icon" style={{ background: '#ecfdf5', color: '#059669' }}>
              <Sparkles size={28} />
            </div>
            <h3>Khung Bố Cục Trang Phân Loại (Classification)</h3>
            <p>
              Khu vực thiết kế các nút chọn mẫu thử nghiệm có sẵn (Preset Benign, Preset Malignant, ca Ranh giới),
              biểu mẫu nhập tay 30 đặc trưng tế bào, nút gửi API POST /api/demo-classify, bảng kết quả xác suất,
              và sơ đồ giải thích mô hình ensemble / đường rẽ nhánh cây quyết định.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
