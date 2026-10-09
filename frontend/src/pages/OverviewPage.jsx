import React from 'react';
import { BookOpen, Database, ShieldAlert, Cpu } from 'lucide-react';

export default function OverviewPage() {
  return (
    <div className="overview-page animate-fade-in">
      <div className="page-header">
        <h2 className="page-title">Màn hình 1: Tổng quan & Phạm vi Đề tài</h2>
        <p className="page-description">
          Khảo sát bài toán phân loại khối u vú FNA từ bộ dữ liệu Wisconsin Diagnostic Breast Cancer (WDBC),
          đặc tả 30 đặc trưng tế bào và thẻ thông tin mô hình học máy (Model Card).
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">
            <BookOpen size={20} color="#2563eb" />
            Giới thiệu Dự án & Mục tiêu Nghiên cứu
          </span>
          <span className="badge badge-primary">Project 16</span>
        </div>
        <div className="card-body">
          <div className="placeholder-box">
            <div className="placeholder-icon">
              <Database size={28} />
            </div>
            <h3>Khung Bố Cục Trang Tổng Quan (Overview)</h3>
            <p>
              Khu vực hiển thị bối cảnh bài toán, mô tả 30 đặc trưng nhân tế bào FNA (nhóm Mean, SE, Worst),
              thông tin phân chia dữ liệu Train/Validation/Test, và nội dung Model Card chuẩn Mitchell et al. (2019).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
