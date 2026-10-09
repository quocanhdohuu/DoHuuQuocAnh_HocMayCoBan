/**
 * Module Dịch vụ API Kết nối Backend FastAPI (Project 16).
 * Quản lý các yêu cầu HTTP thông qua fetch API và biến môi trường VITE_API_BASE_URL.
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Kiểm tra sức khỏe hệ thống và trạng thái mô hình học máy.
 * @returns {Promise<Object>} Dữ liệu trạng thái từ GET /api/health
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    const data = await response.json();
    return {
      ok: response.ok,
      status: response.status,
      data,
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: {
        status: 'offline',
        message: `Không thể kết nối đến máy chủ API: ${error.message}`,
        model_loaded: false,
      },
    };
  }
}

/**
 * Lấy thông tin metadata và định danh hệ thống từ Endpoint gốc.
 * @returns {Promise<Object>}
 */
export async function getRootInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    return await response.json();
  } catch (error) {
    console.error('Lỗi khi lấy thông tin root API:', error);
    return null;
  }
}

/**
 * Gửi yêu cầu phân loại khối u vú từ 30 đặc trưng số FNA.
 * @param {Object} payload Dữ liệu 30 đặc trưng (hoặc dạng gói có threshold)
 * @returns {Promise<Object>}
 */
export async function classifySample(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/demo-classify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    return {
      ok: response.ok,
      status: response.status,
      data,
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: {
        status: 'error',
        message: `Lỗi kết nối mạng khi gửi yêu cầu phân loại: ${error.message}`,
      },
    };
  }
}
