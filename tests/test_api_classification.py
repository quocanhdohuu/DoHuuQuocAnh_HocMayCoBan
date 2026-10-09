"""
Unit tests cho Classification API (Nhiệm vụ 17).
Kiểm thử chi tiết:
1. Dự đoán thành công mẫu Lành tính (Benign, nhãn B, mã 0, xác suất hợp lệ).
2. Dự đoán thành công mẫu Ác tính (Malignant, nhãn M, mã 1, xác suất hợp lệ).
3. Hỗ trợ cấu trúc payload trực tiếp 30 đặc trưng và dạng gói (wrapped with custom threshold).
4. Kiểm tra endpoint alias POST /api/predict hoạt động đồng nhất với /api/demo-classify.
5. Từ chối yêu cầu thiếu đặc trưng (HTTP 422).
6. Từ chối yêu cầu thừa đặc trưng ngoài danh mục schema (HTTP 422 extra=forbid).
7. Từ chối giá trị âm (HTTP 422).
8. Từ chối giá trị NaN, Infinity hoặc sai kiểu dữ liệu (HTTP 422).
9. Từ chối giá trị cực đoan phi lý sinh học (HTTP 422).
10. Cảnh báo Out-of-Distribution (OOD) khi đặc trưng nằm ngoài dải huấn luyện nhưng vẫn trong giới hạn an toàn.
11. Kiểm tra cấu trúc giải thích Random Forest: 100 cây, tỷ lệ phiếu bầu, top đặc trưng và tuyên bố giới hạn phương pháp.
12. Xử lý khi mô hình chưa nạp: trả về HTTP 503 Service Unavailable.
"""

import sys
from pathlib import Path
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.main import app
from backend.src.data import load_split_data
from backend.src.config import FEATURE_NAMES


@pytest.fixture(scope="module")
def client():
    """Fixture cung cấp TestClient kích hoạt lifespan context manager."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_samples():
    """Fixture nạp dữ liệu mẫu từ tập Test thực tế."""
    _, _, (X_test, y_test) = load_split_data()
    benign_idx = int((y_test.values == 0).argmax())
    mal_idx = int((y_test.values == 1).argmax())
    sample_b = X_test.iloc[benign_idx].to_dict()
    sample_m = X_test.iloc[mal_idx].to_dict()
    return sample_b, sample_m


def test_classify_benign_sample(client, test_samples):
    """Kiểm tra dự đoán mẫu Lành tính (Benign)."""
    sample_b, _ = test_samples
    response = client.post("/api/demo-classify", json=sample_b)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["predicted_class"] == 0
    assert data["predicted_code"] == "B"
    assert data["predicted_label"] == "Benign"
    assert data["is_high_risk"] is False
    assert data["probabilities"]["benign"] > 0.50
    assert data["probabilities"]["malignant"] < 0.50
    assert data["probabilities"]["B"] == data["probabilities"]["benign"]
    assert data["probabilities"]["M"] == data["probabilities"]["malignant"]
    assert data["model_info"]["model_name"] == "WDBC_RandomForest_Classifier_Pipeline"
    assert data["model_info"]["input_features_count"] == 30
    assert "clinical_disclaimer" in data


def test_classify_malignant_sample(client, test_samples):
    """Kiểm tra dự đoán mẫu Ác tính (Malignant)."""
    _, sample_m = test_samples
    response = client.post("/api/demo-classify", json=sample_m)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["predicted_class"] == 1
    assert data["predicted_code"] == "M"
    assert data["predicted_label"] == "Malignant"
    assert data["is_high_risk"] is True
    assert data["probabilities"]["malignant"] > 0.50
    assert data["probabilities"]["benign"] < 0.50


def test_wrapped_payload_with_custom_threshold(client, test_samples):
    """Kiểm tra payload dạng gói {"features": {...}, "threshold": 0.9}."""
    sample_b, _ = test_samples
    payload = {
        "features": sample_b,
        "threshold": 0.85
    }
    response = client.post("/api/demo-classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision_threshold"] == 0.85
    assert data["model_info"]["decision_threshold"] == 0.85


def test_predict_alias_endpoint(client, test_samples):
    """Kiểm tra endpoint alias POST /api/predict trả về kết quả tương đương /api/demo-classify."""
    sample_b, _ = test_samples
    res_predict = client.post("/api/predict", json=sample_b)
    res_demo = client.post("/api/demo-classify", json=sample_b)

    assert res_predict.status_code == 200
    assert res_demo.status_code == 200
    assert res_predict.json()["predicted_code"] == res_demo.json()["predicted_code"]
    assert res_predict.json()["probabilities"] == res_demo.json()["probabilities"]


def test_random_forest_explanation_structure(client, test_samples):
    """Kiểm tra tính chuẩn mực của phần giải thích mô hình Random Forest (Yêu cầu 10)."""
    sample_b, _ = test_samples
    response = client.post("/api/demo-classify", json=sample_b)
    assert response.status_code == 200
    exp = response.json()["explanation"]

    assert exp["model_type"] == "RandomForestClassifier"
    assert exp["total_trees"] == 100
    assert "votes_breakdown" in exp
    assert exp["votes_breakdown"]["benign_votes"] + exp["votes_breakdown"]["malignant_votes"] == 100
    assert "top_influential_features" in exp
    assert len(exp["top_influential_features"]) == 5

    # Phải có tuyên bố rõ ràng về GIỚI HẠN phương pháp
    assert "methodological_limitation" in exp
    assert "KHÔNG CÓ một đường đi rẽ nhánh đơn lẻ nào" in exp["methodological_limitation"]


def test_validation_missing_feature(client, test_samples):
    """Từ chối khi thiếu đặc trưng (HTTP 422)."""
    sample_b, _ = test_samples
    invalid_sample = sample_b.copy()
    del invalid_sample["radius_mean"]

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_extra_feature_forbidden(client, test_samples):
    """Từ chối khi có trường thừa ngoài schema (HTTP 422 extra=forbid)."""
    sample_b, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["unauthorized_patient_id"] = 12345

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_negative_value_rejected(client, test_samples):
    """Từ chối khi đặc trưng sinh học nhận giá trị âm (HTTP 422)."""
    sample_b, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["area_mean"] = -10.5

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422
    assert "không thể nhận giá trị âm" in response.text


def test_validation_nan_or_inf_rejected(client, test_samples):
    """Từ chối giá trị chuỗi không phải số hoặc NaN/Inf (HTTP 422)."""
    sample_b, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["radius_mean"] = "NaN"

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_extreme_biological_anomaly(client, test_samples):
    """Từ chối giá trị vượt quá giới hạn sinh học cực đoan (HTTP 422)."""
    sample_b, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["radius_mean"] = 5000.0  # Tế bào nhân không thể có bán kính 5000 micromet

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422
    assert "vượt quá giới hạn sinh học cực đoan" in response.text


def test_out_of_distribution_warning(client, test_samples):
    """Chấp nhận mẫu hợp lệ nhưng cảnh báo OOD khi giá trị ngoài dải Train."""
    sample_b, _ = test_samples
    ood_sample = sample_b.copy()
    ood_sample["radius_mean"] = 32.0  # Max train là 28.11, nhưng vẫn dưới ngưỡng cực đoan

    response = client.post("/api/demo-classify", json=ood_sample)
    assert response.status_code == 200
    data = response.json()
    assert len(data["warnings"]) >= 1
    assert any("radius_mean" in w and "Out-Of-Distribution" in w for w in data["warnings"])


def test_degraded_service_when_model_unloaded(test_samples):
    """Trả về HTTP 503 khi server ở trạng thái degraded / chưa nạp mô hình."""
    sample_b, _ = test_samples
    with patch("backend.app.main.PIPELINE_PATH", Path("non_existent_path.joblib")):
        with TestClient(app) as degraded_client:
            response = degraded_client.post("/api/demo-classify", json=sample_b)
            assert response.status_code == 503
            assert "Mô hình phân loại chưa sẵn sàng" in response.json()["detail"]
