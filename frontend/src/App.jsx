import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import OverviewPage from './pages/OverviewPage';
import ClassificationPage from './pages/ClassificationPage';
import DashboardPage from './pages/DashboardPage';

import './styles/variables.css';
import './styles/global.css';
import './styles/components.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Mặc định chuyển hướng tới Màn hình 1: Tổng quan */}
          <Route index element={<Navigate to="/overview" replace />} />
          <Route path="overview" element={<OverviewPage />} />
          <Route path="classification" element={<ClassificationPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          {/* Bắt tất cả các đường dẫn không tồn tại và đưa về trang chủ */}
          <Route path="*" element={<Navigate to="/overview" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
