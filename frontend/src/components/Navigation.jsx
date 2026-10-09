import React from 'react';
import { NavLink } from 'react-router-dom';
import { BookOpen, Stethoscope, BarChart3 } from 'lucide-react';

export default function Navigation() {
  return (
    <nav className="app-navigation">
      <div className="container nav-container">
        <NavLink
          to="/overview"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <BookOpen size={18} />
          <span>Màn hình 1: Tổng quan & Phạm vi</span>
        </NavLink>

        <NavLink
          to="/classification"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <Stethoscope size={18} />
          <span>Màn hình 2: Không gian Chẩn đoán</span>
        </NavLink>

        <NavLink
          to="/dashboard"
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <BarChart3 size={18} />
          <span>Màn hình 3: Dashboard Thực nghiệm</span>
        </NavLink>
      </div>
    </nav>
  );
}
