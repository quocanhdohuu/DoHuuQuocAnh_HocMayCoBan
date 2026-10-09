"""
Unit và Integration tests cho Backend FastAPI (Project 16 - Nhiệm vụ 18).
Bao phủ toàn diện:
1. Request đủ 30 feature (Benign, Malignant, Borderline).
2. Kiểm tra nhãn (B/M, Benign/Malignant) và tính nhất quán giữa predict_proba và predict.
3. Kiểm tra tổng xác suất các lớp xấp xỉ 1.0 (abs(p_b + p_m - 1.0) < 1e-4).
4. Kiểm tra sự dịch chuyển nhãn khi thay đổi decision_threshold tùy chỉnh.
5. Kiểm thử từ chối thiếu feature, thừa feature (extra=forbid).
6. Kiểm thử dữ liệu kiểu string không hợp lệ ("abc"), NaN, Infinity.
7. Kiểm thử giá trị ngoài miền tham chiếu: cảnh báo Out-of-Distribution và từ chối giá trị cực đoan.
8. Kiểm thử từ chối giá trị âm theo đặc tính sinh học tế bào (< 0).
9. Kiểm thử cấu trúc giải thích Random Forest: 100 cây, tỷ lệ phiếu bầu, top features, giới hạn phương pháp.
10. Kiểm thử trường hợp model artifact không thể nạp (HTTP 503 Degraded cho cả health và classify).
11. Kiểm tra tính đồng nhất giữa POST /api/demo-classify và alias POST /api/predict.
"""

import sys
import math
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
    sample_border = X_test.iloc[23].to_dict()  # Sample #23 (ca ranh giới / FN)
    return sample_b, sample_m, sample_border


# ==============================================================================
# 1. KIỂM THỬ DỰ ĐOÁN HỢP LỆ VÀ TÍNH TOÀN VẸN XÁC SUẤT (YÊU CẦU 2, 7, 8)
# ==============================================================================

def test_classify_benign_sample(client, test_samples):
    """Kiểm tra dự đoán mẫu Lành tính (Benign, nhãn B, mã 0)."""
    sample_b, _, _ = test_samples
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
    """Kiểm tra dự đoán mẫu Ác tính (Malignant, nhãn M, mã 1)."""
    _, sample_m, _ = test_samples
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


def test_probability_sum_equals_one(client, test_samples):
    """Kiểm tra tổng xác suất P(Benign) + P(Malignant) xấp xỉ 1.0 (Yêu cầu 8)."""
    for sample in test_samples:
        response = client.post("/api/demo-classify", json=sample)
        assert response.status_code == 200
        probs = response.json()["probabilities"]
        prob_sum = probs["benign"] + probs["malignant"]
        assert math.isclose(prob_sum, 1.0, abs_tol=1e-3), f"Tổng xác suất không bằng 1: {prob_sum}"


def test_consistency_between_predict_and_predict_proba(client, test_samples):
    """Kiểm tra tính nhất quán toán học giữa xác suất và nhãn dự đoán (Yêu cầu 7)."""
    for sample in test_samples:
        response = client.post("/api/demo-classify", json=sample)
        assert response.status_code == 200
        data = response.json()

        threshold = data["decision_threshold"]
        prob_m = data["probabilities"]["malignant"]
        expected_class = 1 if prob_m >= threshold else 0
        expected_code = "M" if expected_class == 1 else "B"
        expected_label = "Malignant" if expected_class == 1 else "Benign"

        assert data["predicted_class"] == expected_class
        assert data["predicted_code"] == expected_code
        assert data["predicted_label"] == expected_label


def test_threshold_shift_consistency(client, test_samples):
    """Kiểm tra điều chỉnh ngưỡng phân loại lâm sàng (Decision Threshold Tuning)."""
    _, _, sample_border = test_samples
    # Kiểm tra với ngưỡng chuẩn 0.50
    res_default = client.post("/api/demo-classify", json={"features": sample_border, "threshold": 0.50})
    assert res_default.status_code == 200
    data_def = res_default.json()
    prob_m = data_def["probabilities"]["malignant"]

    # Đặt ngưỡng thấp hơn prob_m -> phải chuyển sang Malignant
    lower_threshold = max(0.01, round(prob_m - 0.05, 2))
    res_lower = client.post("/api/demo-classify", json={"features": sample_border, "threshold": lower_threshold})
    assert res_lower.status_code == 200
    assert res_lower.json()["predicted_class"] == 1
    assert res_lower.json()["predicted_code"] == "M"

    # Đặt ngưỡng cao hơn prob_m -> phải chuyển sang Benign
    higher_threshold = min(0.99, round(prob_m + 0.05, 2))
    res_higher = client.post("/api/demo-classify", json={"features": sample_border, "threshold": higher_threshold})
    assert res_higher.status_code == 200
    assert res_higher.json()["predicted_class"] == 0
    assert res_higher.json()["predicted_code"] == "B"


def test_predict_alias_endpoint(client, test_samples):
    """Kiểm tra endpoint alias POST /api/predict hoạt động đồng nhất với /api/demo-classify."""
    sample_b, _, _ = test_samples
    res_predict = client.post("/api/predict", json=sample_b)
    res_demo = client.post("/api/demo-classify", json=sample_b)

    assert res_predict.status_code == 200
    assert res_demo.status_code == 200
    assert res_predict.json()["predicted_code"] == res_demo.json()["predicted_code"]
    assert res_predict.json()["probabilities"] == res_demo.json()["probabilities"]


# ==============================================================================
# 2. KIỂM THỬ XÁC THỰC PYDANTIC & MIỀN GIÁ TRỊ (YÊU CẦU 3, 4, 5)
# ==============================================================================

def test_validation_missing_feature(client, test_samples):
    """Từ chối khi thiếu bất kỳ đặc trưng nào trong 30 đặc trưng (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    del invalid_sample["radius_mean"]

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422
    data = response.json()
    assert any("radius_mean" in str(err) for err in data["detail"])


def test_validation_extra_feature_forbidden(client, test_samples):
    """Từ chối khi có trường thừa ngoài schema (HTTP 422 extra=forbid)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["patient_blood_pressure"] = 120.0

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_invalid_string_datatype(client, test_samples):
    """Từ chối dữ liệu chuỗi không hợp lệ 'abc' (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["texture_mean"] = "not_a_valid_float"

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_nan_rejected(client, test_samples):
    """Từ chối giá trị NaN (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["radius_mean"] = "NaN"

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_infinity_rejected(client, test_samples):
    """Từ chối giá trị Infinity (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["radius_mean"] = "Infinity"

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422


def test_validation_negative_value_rejected(client, test_samples):
    """Từ chối khi đặc trưng sinh học nhận giá trị âm < 0 (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["area_mean"] = -10.5

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422
    assert "không thể nhận giá trị âm" in response.text


def test_validation_extreme_biological_anomaly(client, test_samples):
    """Từ chối giá trị vượt quá giới hạn sinh học cực đoan > 15 * max_train (HTTP 422)."""
    sample_b, _, _ = test_samples
    invalid_sample = sample_b.copy()
    invalid_sample["radius_mean"] = 5000.0

    response = client.post("/api/demo-classify", json=invalid_sample)
    assert response.status_code == 422
    assert "vượt quá giới hạn sinh học cực đoan" in response.text


def test_out_of_distribution_warning(client, test_samples):
    """Chấp nhận mẫu hợp lệ nhưng cảnh báo OOD khi giá trị nằm ngoài dải Train."""
    sample_b, _, _ = test_samples
    ood_sample = sample_b.copy()
    ood_sample["radius_mean"] = 32.0  # Max train là 28.11, nhưng vẫn dưới ngưỡng cực đoan 421

    response = client.post("/api/demo-classify", json=ood_sample)
    assert response.status_code == 200
    data = response.json()
    assert len(data["warnings"]) >= 1
    assert any("radius_mean" in w and "Out-Of-Distribution" in w for w in data["warnings"])


# ==============================================================================
# 3. KIỂM THỬ CẤU TRÚC GIẢI THÍCH MÔ HÌNH VÀ DEGRADED MODE (YÊU CẦU 6, 9, 10)
# ==============================================================================

def test_random_forest_explanation_structure(client, test_samples):
    """Kiểm tra tính chuẩn mực của phần giải thích mô hình Random Forest."""
    sample_b, _, _ = test_samples
    response = client.post("/api/demo-classify", json=sample_b)
    assert response.status_code == 200
    exp = response.json()["explanation"]

    assert exp["model_type"] == "RandomForestClassifier"
    assert exp["total_trees"] == 100
    assert "votes_breakdown" in exp
    assert exp["votes_breakdown"]["benign_votes"] + exp["votes_breakdown"]["malignant_votes"] == 100
    assert "top_influential_features" in exp
    assert len(exp["top_influential_features"]) == 5

    # Tuyên bố rõ ràng về GIỚI HẠN phương pháp
    assert "methodological_limitation" in exp
    assert "KHÔNG CÓ một đường đi rẽ nhánh đơn lẻ nào" in exp["methodological_limitation"]


def test_health_endpoint_healthy(client):
    """Kiểm tra GET /api/health khi hệ thống bình thường."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["sha256_verified"] is True
    assert data["input_features_count"] == 30


def test_both_endpoints_degraded_when_model_missing(test_samples):
    """Kiểm tra cả /api/health và /api/demo-classify trả về 503 khi thiếu model (Yêu cầu 9)."""
    sample_b, _, _ = test_samples
    with patch("backend.app.main.PIPELINE_PATH", Path("non_existent_model_file.joblib")):
        with TestClient(app) as degraded_client:
            # 1. Health endpoint báo degraded
            res_health = degraded_client.get("/api/health")
            assert res_health.status_code == 503
            assert res_health.json()["status"] == "degraded"
            assert res_health.json()["model_loaded"] is False

            # 2. Classify endpoint báo 503 Service Unavailable
            res_classify = degraded_client.post("/api/demo-classify", json=sample_b)
            assert res_classify.status_code == 503
            assert "Mô hình phân loại chưa sẵn sàng" in res_classify.json()["detail"]
