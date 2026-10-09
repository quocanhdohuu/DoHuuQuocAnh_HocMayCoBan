import React from 'react';
import { BarChart3, LineChart } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="dashboard-page animate-fade-in">
      <div className="page-header">
        <h2 className="page-title">Màn hình 3: Dashboard Thực nghiệm & So sánh</h2>
        <p className="page-description">
          Tổng hợp kết quả 4 thí nghiệm bắt buộc: Khảo sát độ sâu cây, Cắt tỉa cây,
          Đối sánh 4 mô hình học máy và Đánh giá độ ổn định Feature Importance qua nhiều seed.
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">
            <BarChart3 size={20} color="#7c3aed" />
            Bảng Điều Khiển Thực Nghiệm Lâm Sàng & Đánh Giá Mô Hình
          </span>
          <span className="badge" style={{ background: '#f5f3ff', color: '#7c3aed', border: '1px solid #ddd6fe' }}>
            Experimental Results
          </span>
        </div>
        <div className="card-body">
          <div className="placeholder-box">
            <div className="placeholder-icon" style={{ background: '#f5f3ff', color: '#7c3aed' }}>
              <LineChart size={28} />
            </div>
            <h3>Khung Bố Cục Trang Bảng Điều Khiển (Dashboard)</h3>
            <p>
              Khu vực hiển thị biểu đồ đường Train/CV theo độ sâu (Thí nghiệm 1), kết quả cắt tỉa CCP-Alpha,
              bảng đối sánh 4 mô hình (Dummy, Cây chưa tỉa, Cây đã tỉa, Random Forest), ma trận nhầm lẫn
              và đồ thị thanh độ ổn định Top 10 đặc trưng qua 5 random seeds (Thí nghiệm 4).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
