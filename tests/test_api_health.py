"""
Unit tests cho FastAPI Initialization và Health Endpoint (Nhiệm vụ 16).
Kiểm tra:
1. Khởi động ứng dụng FastAPI và chạy lifespan thành công.
2. Root endpoint GET / trả về 200 và trạng thái online.
3. Health endpoint GET /api/health trả về 200, status 'ok', model_loaded=True, sha256_verified=True.
4. Cấu hình CORS phản hồi đúng Access-Control-Allow-Origin cho Frontend local.
5. Xử lý lỗi khi model không thể nạp: trả về HTTP 503, status 'degraded' mà không làm crash ứng dụng.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Đảm bảo đường dẫn gốc
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app, PIPELINE_PATH, SCHEMA_PATH, METADATA_PATH


@pytest.fixture
def client():
    """Fixture cung cấp TestClient kích hoạt đầy đủ lifespan context manager."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Kiểm tra GET / trả về thông tin chào mừng và mã trạng thái 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "WDBC Breast Cancer Classification API" in data["app_name"]
    assert data["health_check"] == "/api/health"
    assert data["documentation"] == "/docs"


def test_health_endpoint_healthy(client):
    """Kiểm tra GET /api/health khi hệ thống bình thường và mô hình được nạp thành công."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()

    # Kiểm tra các trường dữ liệu bắt buộc
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["sha256_verified"] is True
    assert data["model_name"] == "WDBC_RandomForest_Classifier_Pipeline"
    assert data["input_features_count"] == 30
    assert data["decision_threshold"] == 0.50
    assert data["target_positive_class"] == "Malignant"
    assert data["error"] is None
    assert "timestamp" in data
    assert "startup_time" in data


def test_cors_headers(client):
    """Kiểm tra CORS headers cho các origin Frontend cục bộ (Vite 5173 và React 3000)."""
    # Kiểm tra Origin Vite 5173
    response_vite = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    assert response_vite.status_code == 200
    assert response_vite.headers.get("access-control-allow-origin") == "http://localhost:5173"

    # Kiểm tra Origin React 3000
    response_react = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
    assert response_react.status_code == 200
    assert response_react.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_health_endpoint_degraded_when_pipeline_missing():
    """Kiểm tra xử lý lỗi khi tệp pipeline bị thiếu: trả về HTTP 503 và trạng thái degraded."""
    with patch("backend.app.main.PIPELINE_PATH", Path("non_existent_model_file.joblib")):
        with TestClient(app) as degraded_client:
            response = degraded_client.get("/api/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "degraded"
            assert data["model_loaded"] is False
            assert "Không tìm thấy file pipeline" in data["error"]
