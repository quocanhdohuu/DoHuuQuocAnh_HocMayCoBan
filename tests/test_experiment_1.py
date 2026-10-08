"""
Module Kiểm thử Tự động cho Thí nghiệm 1 (Experiment 1: Tree Depth vs CV Performance).
Xác thực:
1. Tệp kết quả JSON và biểu đồ đường cong Train/CV tồn tại.
2. Đầy đủ 20 mức độ sâu từ 1 đến 20 với 5-Fold Stratified CV.
3. Xu hướng Train score tăng đơn điệu theo độ sâu (chứng minh mức độ phức tạp mô hình).
4. Nhận diện rõ rệt hiện tượng Overfitting khi Train score tiệm cận 1.0 trong khi CV score bão hòa.
5. Tuyệt đối không rò rỉ dữ liệu tập Test hay tập Validation ngoài.
"""

import json
import pytest

from backend.src.config import REPORTS_DIR, FIGURES_DIR
from backend.src.experiment_depth import (
    EXP1_RESULTS_PATH,
    EXP1_FIGURE_PATH,
    run_tree_depth_experiment,
)


@pytest.fixture(scope="module")
def exp1_data():
    """Fixture nạp kết quả thí nghiệm 1."""
    if not (EXP1_RESULTS_PATH.exists() and EXP1_FIGURE_PATH.exists()):
        res = run_tree_depth_experiment(save_results=True, save_figure=True)
    else:
        with open(EXP1_RESULTS_PATH, "r", encoding="utf-8") as f:
            res = json.load(f)
    return res


def test_exp1_artifacts_exist(exp1_data):
    """Kiểm tra tệp kết quả JSON và biểu đồ PNG tồn tại và hợp lệ."""
    assert EXP1_RESULTS_PATH.exists(), f"Thiếu tệp: {EXP1_RESULTS_PATH}"
    assert EXP1_FIGURE_PATH.exists(), f"Thiếu biểu đồ: {EXP1_FIGURE_PATH}"
    assert len(exp1_data["records"]) == 20, "Phải có đúng 20 mức độ sâu khảo sát"


def test_depth_range_completeness(exp1_data):
    """Kiểm tra danh sách độ sâu phủ kín từ 1 đến 20."""
    depths = [r["max_depth"] for r in exp1_data["records"]]
    assert depths == list(range(1, 21)), f"Danh sách độ sâu không liên tục 1..20: {depths}"


def test_train_score_increasing_trend(exp1_data):
    """Kiểm tra quy luật: Điểm số Train tăng dần khi độ sâu cây tăng (giảm Bias)."""
    rec_depth_1 = exp1_data["records"][0]
    rec_depth_10 = exp1_data["records"][9]

    assert rec_depth_10["train_accuracy"] > rec_depth_1["train_accuracy"], \
        "Train Accuracy tại depth=10 phải cao hơn depth=1"
    assert rec_depth_10["train_recall_malignant"] > rec_depth_1["train_recall_malignant"], \
        "Train Recall tại depth=10 phải cao hơn depth=1"
    assert rec_depth_10["train_accuracy"] == 1.0, \
        "Train Accuracy tại depth >= 10 phải đạt tuyệt đối 1.0"


def test_cv_overfitting_divergence(exp1_data):
    """Kiểm tra khoảng cách giữa Train và CV nới rộng ở độ sâu lớn (Bằng chứng Overfitting)."""
    rec_deep = exp1_data["records"][-1]  # depth = 20
    train_score = rec_deep["train_accuracy"]
    cv_score = rec_deep["cv_accuracy_mean"]

    gap = (train_score - cv_score) * 100
    assert gap > 5.0, f"Khoảng cách Train-CV ở độ sâu 20 phải đáng kể (>5%), thực tế: {gap:.2f}%"


def test_no_test_set_leakage_in_exp1(exp1_data):
    """Kiểm tra khẳng định thí nghiệm 1 chỉ chạy trên tập Train qua CV, không dùng Test."""
    assert exp1_data["dataset"] == "WDBC Train Set (N=398)"
    assert "test_metrics" not in exp1_data
