"""
Module Kiểm thử Tự động cho Mô hình Cơ sở (Baseline - DummyClassifier).
Xác thực:
1. Mô hình DummyClassifier được lưu trữ đúng định dạng artifact .joblib.
2. Các chỉ số hiệu năng trên tập Validation khớp chính xác với phân tích lý thuyết.
3. Nhãn Malignant được xác định nhất quán là lớp dương (1).
4. Xử lý mẫu số bằng 0 (Zero Division) minh bạch.
5. Tuyệt đối không sử dụng tập Test cho việc đánh giá baseline.
"""

import json
import pytest
import numpy as np
import joblib
from sklearn.metrics import precision_score, recall_score

from backend.src.config import (
    MODELS_DIR,
    REPORTS_DIR,
)
from backend.src.baseline import (
    BASELINE_MODEL_PATH,
    BASELINE_RESULTS_PATH,
    train_and_evaluate_baseline,
)
from backend.src.data import load_split_data


@pytest.fixture(scope="module")
def baseline_evaluation():
    """Fixture chạy huấn luyện và đánh giá baseline một lần cho module test."""
    res = train_and_evaluate_baseline(save_model=True, save_results=True)
    return res


def test_baseline_artifacts_exist(baseline_evaluation):
    """Kiểm tra các tệp artifact và báo cáo kết quả tồn tại trên đĩa."""
    assert BASELINE_MODEL_PATH.exists(), f"Thiếu tệp mô hình: {BASELINE_MODEL_PATH}"
    assert BASELINE_RESULTS_PATH.exists(), f"Thiếu tệp kết quả: {BASELINE_RESULTS_PATH}"

    # Kiểm tra nạp lại mô hình từ artifact
    loaded_model = joblib.load(BASELINE_MODEL_PATH)
    assert hasattr(loaded_model, "predict"), "Mô hình nạp lại không có phương thức predict"


def test_baseline_validation_metrics(baseline_evaluation):
    """Kiểm tra các số đo định lượng của Baseline trên Validation (N=85: 53 B, 32 M)."""
    m = baseline_evaluation["metrics"]
    cm = baseline_evaluation["confusion_matrix"]

    # 1. Accuracy phải bằng tỷ lệ lớp đa số trên Val: 53 / 85 ≈ 0.6235
    expected_acc = round(53 / 85, 4)
    assert abs(m["accuracy"] - expected_acc) < 1e-4, f"Accuracy lệch: {m['accuracy']} vs {expected_acc}"

    # 2. Recall lớp Malignant (1) bắt buộc bằng 0.0 (Bỏ sót toàn bộ ca ác tính)
    assert m["recall_malignant"] == 0.0, "Recall Malignant phải bằng 0.0"

    # 3. Precision lớp Malignant bắt buộc bằng 0.0 (Xử lý 0/0 minh bạch)
    assert m["precision_malignant"] == 0.0, "Precision Malignant phải bằng 0.0"

    # 4. F1-score bắt buộc bằng 0.0
    assert m["f1_malignant"] == 0.0, "F1-Score Malignant phải bằng 0.0"

    # 5. ROC-AUC phải bằng 0.5 (Đoán mò ngẫu nhiên)
    assert m["roc_auc"] == 0.5, "ROC-AUC phải bằng 0.5"

    # 6. Kiểm tra cấu trúc Confusion Matrix
    assert cm["true_negative"] == 53, "TN phải là 53"
    assert cm["false_positive"] == 0, "FP phải là 0"
    assert cm["false_negative"] == 32, "FN phải là 32 (toàn bộ ca ác tính bị bỏ sót)"
    assert cm["true_positive"] == 0, "TP phải là 0"


def test_zero_division_behavior():
    """Kiểm tra hành vi toán học khi mẫu số của Precision bằng 0."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 0, 0, 0])  # Không dự đoán mẫu nào là 1

    # Kiểm tra Scikit-learn cảnh báo hoặc gán 0.0 với zero_division=0.0
    prec = precision_score(y_true, y_pred, pos_label=1, zero_division=0.0)
    assert prec == 0.0, "Precision khi 0/0 phải được gán là 0.0"

    rec = recall_score(y_true, y_pred, pos_label=1, zero_division=0.0)
    assert rec == 0.0, "Recall khi không đoán trúng ca nào phải là 0.0"


def test_no_test_set_leakage_in_baseline():
    """Đảm bảo tập Test độc lập không bị sử dụng trong báo cáo baseline."""
    with open(BASELINE_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["evaluation_split"] == "Validation"
    assert data["sample_counts"]["val_samples"] == 85
    assert data["sample_counts"]["val_samples"] != 86, "Cảnh báo: Có dấu hiệu nhầm lẫn với kích thước Test (86 mẫu)!"
