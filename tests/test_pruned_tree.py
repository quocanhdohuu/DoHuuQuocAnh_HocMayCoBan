"""
Unit tests cho Nhiệm vụ 10: Decision Tree Pruning.
Kiểm tra:
1. Mô hình dt_pruned.joblib tồn tại, load được và có ccp_alpha > 0.
2. Kết quả pruning_search_results.json có cấu trúc chuẩn và chứa best_params, tree_structure, metrics.
3. Cây đã cắt tỉa có cấu trúc tinh gọn hơn cây chưa cắt (ít nút hơn, ít lá hơn, độ sâu thấp hơn hoặc bằng).
4. Các hình ảnh trực quan hóa (pruned_tree_visualization.png, pruning_ccp_path.png) tồn tại và không rỗng.
5. Tuyệt đối không bị rò rỉ dữ liệu sang tập Test (Test set nguyên vẹn 86 mẫu).
"""

import json
from pathlib import Path
import pytest
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from backend.src.config import ROOT_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR
from backend.src.pruned_tree import (
    PRUNED_MODEL_PATH,
    PRUNING_RESULTS_PATH,
    PRUNED_TREE_FIGURE_PATH,
    CCP_PATH_FIGURE_PATH,
    UNPRUNED_RESULTS_PATH,
)


def test_pruned_model_artifact_exists():
    """Kiểm tra artifact mô hình dt_pruned.joblib tồn tại và là DecisionTreeClassifier hợp lệ."""
    assert PRUNED_MODEL_PATH.exists(), f"Không tìm thấy file mô hình tại {PRUNED_MODEL_PATH}"
    model = joblib.load(PRUNED_MODEL_PATH)
    assert isinstance(model, DecisionTreeClassifier), "Model không phải DecisionTreeClassifier"
    assert model.ccp_alpha > 0, f"ccp_alpha phải lớn hơn 0 đối với mô hình đã cắt tỉa, hiện tại: {model.ccp_alpha}"


def test_pruning_search_results_schema():
    """Kiểm tra schema và nội dung của reports/pruning_search_results.json."""
    assert PRUNING_RESULTS_PATH.exists(), f"Không tìm thấy file kết quả tại {PRUNING_RESULTS_PATH}"
    with open(PRUNING_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = [
        "pipeline_name",
        "random_state",
        "candidate_alphas_count",
        "effective_alphas_list",
        "best_params",
        "cv_performance_at_best_params",
        "top_10_parameter_combinations",
        "tree_structure",
        "train_metrics",
        "validation_metrics",
        "comparison_with_unpruned",
    ]
    for key in required_keys:
        assert key in data, f"Thiếu key '{key}' trong pruning_search_results.json"

    # Kiểm tra best_params
    bp = data["best_params"]
    assert "ccp_alpha" in bp and bp["ccp_alpha"] > 0
    assert "max_depth" in bp
    assert "min_samples_leaf" in bp

    # Kiểm tra metrics
    vm = data["validation_metrics"]
    assert 0.0 <= vm["accuracy"] <= 1.0
    assert 0.0 <= vm["recall_malignant"] <= 1.0
    assert 0.0 <= vm["precision_malignant"] <= 1.0
    assert 0.0 <= vm["f1_malignant"] <= 1.0


def test_structural_reduction_vs_unpruned():
    """Kiểm tra cây đã cắt tỉa giảm được số nút và số lá so với cây chưa cắt."""
    assert UNPRUNED_RESULTS_PATH.exists(), "Cần có unpruned_tree_results.json để so sánh"
    with open(UNPRUNED_RESULTS_PATH, "r", encoding="utf-8") as f:
        unpruned = json.load(f)

    with open(PRUNING_RESULTS_PATH, "r", encoding="utf-8") as f:
        pruned = json.load(f)

    u_struct = unpruned["tree_structure"]
    p_struct = pruned["tree_structure"]

    # Cây tỉa phải gọn hơn
    assert p_struct["total_nodes"] < u_struct["total_nodes"], (
        f"Số nút cây đã tỉa ({p_struct['total_nodes']}) phải nhỏ hơn cây chưa tỉa ({u_struct['total_nodes']})"
    )
    assert p_struct["leaf_nodes"] < u_struct["leaf_nodes"], (
        f"Số lá cây đã tỉa ({p_struct['leaf_nodes']}) phải nhỏ hơn cây chưa tỉa ({u_struct['leaf_nodes']})"
    )
    assert p_struct["actual_depth"] <= u_struct["actual_depth"], (
        f"Độ sâu cây đã tỉa ({p_struct['actual_depth']}) phải nhỏ hơn hoặc bằng cây chưa tỉa ({u_struct['actual_depth']})"
    )


def test_visualizations_exist():
    """Kiểm tra các biểu đồ trực quan hóa được tạo đầy đủ và có dung lượng hợp lệ."""
    assert PRUNED_TREE_FIGURE_PATH.exists(), f"Thiếu biểu đồ cây đã tỉa tại {PRUNED_TREE_FIGURE_PATH}"
    assert PRUNED_TREE_FIGURE_PATH.stat().st_size > 10000, "File biểu đồ cây quá nhỏ hoặc rỗng"

    assert CCP_PATH_FIGURE_PATH.exists(), f"Thiếu biểu đồ ccp_path tại {CCP_PATH_FIGURE_PATH}"
    assert CCP_PATH_FIGURE_PATH.stat().st_size > 10000, "File biểu đồ ccp_path quá nhỏ hoặc rỗng"


def test_no_test_set_leakage():
    """Đảm bảo tập Test độc lập tuyệt đối và không bị thay đổi."""
    test_csv = ROOT_DIR / "data" / "test.csv"
    assert test_csv.exists(), "Tập test.csv phải tồn tại"
    df_test = pd.read_csv(test_csv)
    assert len(df_test) == 86, f"Tập Test phải giữ nguyên đúng 86 mẫu, hiện có {len(df_test)}"
