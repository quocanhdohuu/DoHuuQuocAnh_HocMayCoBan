import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, ShieldCheck, Wifi, WifiOff } from 'lucide-react';
import { checkHealth, API_BASE_URL } from '../services/api';

export default function Header() {
  const [healthStatus, setHealthStatus] = useState({
    status: 'checking',
    modelLoaded: false,
    modelName: '',
  });

  useEffect(() => {
    let isMounted = true;

    async function fetchHealth() {
      const res = await checkHealth();
      if (!isMounted) return;

      if (res.ok && res.data.status === 'ok') {
        setHealthStatus({
          status: 'online',
          modelLoaded: res.data.model_loaded,
          modelName: res.data.model_name || 'Random Forest',
        });
      } else if (res.data.status === 'degraded') {
        setHealthStatus({
          status: 'degraded',
          modelLoaded: false,
          modelName: 'Mô hình chưa sẵn sàng',
        });
      } else {
        setHealthStatus({
          status: 'offline',
          modelLoaded: false,
          modelName: 'Mất kết nối API',
        });
      }
    }

    fetchHealth();
    const interval = setInterval(fetchHealth, 15000); // Thăm dò liveness mỗi 15 giây
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      {/* 1. CLINICAL ALERT BANNER CỐ ĐỊNH BẮT BUỘC THEO ĐẶC TẢ PROJECT 16 */}
      <div className="clinical-alert-banner">
        <AlertTriangle size={16} color="#be123c" />
        <span>
          <strong>TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA:</strong> Mô hình AI được xây dựng phục vụ nghiên cứu học thuật
          trong học phần Học máy cơ bản (Đại Học Công Nghệ Kỹ Thuật Hưng Yên). <em>Tuyệt đối không sử dụng thay thế chẩn đoán y khoa lâm sàng của bác sĩ chuyên khoa.</em>
        </span>
      </div>

      {/* 2. HEADER CHÍNH */}
      <header className="app-header">
        <div className="container header-container">
          <div className="brand-section">
            <div className="brand-icon">
              <Activity size={24} />
            </div>
            <div className="brand-text">
              <h1>WDBC Breast Cancer Classification</h1>
              <p className="brand-subtitle">Project 16: Phân Loại Khối U Vú Bằng Cây & Rừng Ngẫu Nhiên</p>
            </div>
          </div>

          <div className="header-actions">
            {healthStatus.status === 'online' && (
              <span className="status-badge online" title={`API sẵn sàng tại ${API_BASE_URL}`}>
                <span className="status-dot pulsing"></span>
                <span>API Online: {healthStatus.modelName}</span>
              </span>
            )}
            {healthStatus.status === 'degraded' && (
              <span className="status-badge degraded" title="API hoạt động nhưng mô hình chưa nạp">
                <span className="status-dot"></span>
                <span>Cảnh báo: Mô hình degraded</span>
              </span>
            )}
            {healthStatus.status === 'offline' && (
              <span className="status-badge offline" title={`Không thể kết nối Backend tại ${API_BASE_URL}`}>
                <span className="status-dot"></span>
                <span>API Offline</span>
              </span>
            )}
            {healthStatus.status === 'checking' && (
              <span className="status-badge" style={{ backgroundColor: '#f1f5f9', color: '#64748b' }}>
                <span className="status-dot"></span>
                <span>Đang kết nối...</span>
              </span>
            )}
          </div>
        </div>
      </header>
    </>
  );
}
