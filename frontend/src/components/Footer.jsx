import React from 'react';

export default function Footer() {
  return (
    <footer className="app-footer">
      <div className="container footer-container">
        <div className="footer-left">
          <span>
            <strong>Project 16</strong> &bull; Học phần Học máy cơ bản &bull; Bộ môn Khoa học dữ liệu, Đại Học Công Nghệ Kỹ Thuật Hưng Yên
          </span>
        </div>
        <div className="footer-links">
          <span>Tác giả: <strong>Đỗ Hữu Quốc Anh</strong></span>
          <span>&bull;</span>
          <span>Phiên bản: <strong>1.0.0 (FastAPI + React)</strong></span>
        </div>
      </div>
    </footer>
  );
}
