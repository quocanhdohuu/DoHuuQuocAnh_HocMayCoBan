"""
Module Kiểm thử Tự động cho Cây Quyết định Chưa Cắt Tỉa (Unpruned Decision Tree).
Xác thực:
1. Mô hình được lưu trữ đúng định dạng artifact .joblib và biểu đồ PNG tồn tại.
2. Cấu trúc hình học cây: Độ sâu = 8 tầng, 37 nút, 19 lá.
3. Độ khớp tuyệt đối trên tập Train: Accuracy = 1.0, Recall = 1.0.
4. Bằng chứng Overfitting: Độ chính xác và Recall trên Validation sụt giảm rõ rệt.
5. Tuyệt đối không sử dụng tập Test.
"""

import json
import pytest
import joblib

from backend.src.config import MODELS_DIR, REPORTS_DIR, FIGURES_DIR
from backend.src.unpruned_tree import (
    UNPRUNED_MODEL_PATH,
    UNPRUNED_RESULTS_PATH,
    UNPRUNED_FIGURE_PATH,
    train_and_evaluate_unpruned_tree,
)


@pytest.fixture(scope="module")
def unpruned_tree_evaluation():
    """Fixture chạy huấn luyện và đánh giá Unpruned Tree một lần cho module test."""
    res = train_and_evaluate_unpruned_tree(save_model=True, save_results=True, save_figure=True)
    return res


def test_unpruned_artifacts_exist(unpruned_tree_evaluation):
    """Kiểm tra các tệp artifact, kết quả JSON và biểu đồ cây tồn tại."""
    assert UNPRUNED_MODEL_PATH.exists(), f"Thiếu mô hình: {UNPRUNED_MODEL_PATH}"
    assert UNPRUNED_RESULTS_PATH.exists(), f"Thiếu kết quả: {UNPRUNED_RESULTS_PATH}"
    assert UNPRUNED_FIGURE_PATH.exists(), f"Thiếu biểu đồ cây: {UNPRUNED_FIGURE_PATH}"

    # Nạp lại mô hình và kiểm tra thuộc tính cây
    loaded_model = joblib.load(UNPRUNED_MODEL_PATH)
    assert hasattr(loaded_model, "tree_"), "Mô hình không phải DecisionTreeClassifier hợp lệ"


def test_tree_geometric_structure(unpruned_tree_evaluation):
    """Kiểm tra cấu trúc hình học của cây unpruned: độ sâu 8 tầng, 37 nút, 19 lá."""
    st = unpruned_tree_evaluation["tree_structure"]
    assert st["actual_depth"] == 8, f"Độ sâu cây phải là 8, thực tế: {st['actual_depth']}"
    assert st["total_nodes"] == 37, f"Tổng số nút phải là 37, thực tế: {st['total_nodes']}"
    assert st["leaf_nodes"] == 19, f"Số nút lá phải là 19, thực tế: {st['leaf_nodes']}"


def test_perfect_train_memorization(unpruned_tree_evaluation):
    """Kiểm tra cây chưa cắt tỉa đạt điểm tuyệt đối 100% trên tập Train (Memorization)."""
    tm = unpruned_tree_evaluation["train_metrics"]
    assert tm["accuracy"] == 1.0, "Train Accuracy của cây chưa cắt tỉa phải đạt 1.0"
    assert tm["recall_malignant"] == 1.0, "Train Recall phải đạt 1.0"
    assert tm["precision_malignant"] == 1.0, "Train Precision phải đạt 1.0"
    assert tm["f1_malignant"] == 1.0, "Train F1 phải đạt 1.0"
    assert tm["confusion_matrix"]["fn"] == 0, "Train không được có ca FN nào"
    assert tm["confusion_matrix"]["fp"] == 0, "Train không được có ca FP nào"


def test_overfitting_evidence_on_validation(unpruned_tree_evaluation):
    """Kiểm tra khoảng cách sụt giảm hiệu năng trên Validation chứng minh Overfitting."""
    tm = unpruned_tree_evaluation["train_metrics"]
    vm = unpruned_tree_evaluation["validation_metrics"]
    oa = unpruned_tree_evaluation["overfitting_analysis"]

    # Hiệu năng trên Validation phải thấp hơn Train
    assert vm["accuracy"] < tm["accuracy"], "Validation Accuracy phải thấp hơn Train"
    assert vm["recall_malignant"] < tm["recall_malignant"], "Validation Recall phải thấp hơn Train"

    # Khoảng cách sụt giảm phải đáng kể (> 10% Accuracy gap)
    assert oa["train_val_gaps"]["accuracy_gap_pct"] > 10.0, "Chênh lệch Accuracy phải > 10%"
    assert oa["train_val_gaps"]["recall_gap_pct"] > 15.0, "Chênh lệch Recall phải > 15%"
    assert vm["confusion_matrix"]["fn"] == 6, f"Validation bỏ sót đúng 6 ca ác tính (FN=6)"


def test_no_test_set_leakage(unpruned_tree_evaluation):
    """Kiểm tra khẳng định tập Test độc lập không bị xâm phạm."""
    with open(UNPRUNED_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Đảm bảo kết quả chỉ lưu trên Validation và Train
    assert "test_metrics" not in data, "LỖI LEAKAGE: Xuất hiện kết quả tập Test trong Unpruned Task!"
    assert data["validation_metrics"]["confusion_matrix"]["tn"] + \
           data["validation_metrics"]["confusion_matrix"]["fp"] + \
           data["validation_metrics"]["confusion_matrix"]["fn"] + \
           data["validation_metrics"]["confusion_matrix"]["tp"] == 85
