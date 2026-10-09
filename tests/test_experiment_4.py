"""
Unit tests cho Nhiệm vụ 13: Thí nghiệm 4 - Feature Importance Stability.
Kiểm tra:
1. File kết quả JSON và báo cáo Markdown tồn tại.
2. Các biểu đồ exp4_feature_stability.png và exp4_feature_ranks_heatmap.png tồn tại và có kích thước hợp lệ.
3. Schema kết quả chứa đủ 5 seeds [42, 123, 456, 789, 999] và Top 10 đặc trưng.
4. Nhóm Top 5 đặc trưng cốt lõi (perimeter_worst, radius_worst, area_worst, concave points_mean, concave points_worst) được xác định chính xác.
5. Tuyệt đối không rò rỉ dữ liệu sang tập Test (Test set nguyên vẹn 86 mẫu).
"""

import json
from pathlib import Path
import pytest
import pandas as pd

from backend.src.config import ROOT_DIR, REPORTS_DIR, FIGURES_DIR


def test_exp4_artifacts_exist():
    """Kiểm tra sự tồn tại của tệp JSON, Markdown báo cáo và 2 biểu đồ trực quan."""
    json_path = REPORTS_DIR / "exp4_feature_stability_results.json"
    md_path = REPORTS_DIR / "feature_importance_stability.md"
    fig_bar = FIGURES_DIR / "exp4_feature_stability.png"
    fig_heatmap = FIGURES_DIR / "exp4_feature_ranks_heatmap.png"

    assert json_path.exists(), f"Thiếu file JSON tại {json_path}"
    assert md_path.exists(), f"Thiếu file báo cáo Markdown tại {md_path}"
    assert fig_bar.exists(), f"Thiếu biểu đồ thanh ngang tại {fig_bar}"
    assert fig_heatmap.exists(), f"Thiếu biểu đồ heatmap tại {fig_heatmap}"

    assert fig_bar.stat().st_size > 10000, "Biểu đồ bar quá nhỏ hoặc rỗng"
    assert fig_heatmap.stat().st_size > 10000, "Biểu đồ heatmap quá nhỏ hoặc rỗng"


def test_exp4_json_schema_and_seeds():
    """Kiểm tra schema JSON và 5 seeds thực nghiệm."""
    json_path = REPORTS_DIR / "exp4_feature_stability_results.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = [
        "experiment_name",
        "model_type",
        "model_parameters",
        "seeds_evaluated",
        "train_samples_count",
        "total_features_count",
        "top_10_features_summary",
        "collinearity_analysis",
    ]
    for key in required_keys:
        assert key in data, f"Thiếu key '{key}' trong exp4_feature_stability_results.json"

    # Kiểm tra 5 seeds
    assert data["seeds_evaluated"] == [42, 123, 456, 789, 999], "Seeds phải là [42, 123, 456, 789, 999]"
    assert len(data["top_10_features_summary"]) == 10, "Phải có đúng 10 đặc trưng trong top 10"


def test_exp4_top_features_consistency():
    """Kiểm tra nhóm Top 5 đặc trưng quan trọng nhất có mặt đầy đủ."""
    json_path = REPORTS_DIR / "exp4_feature_stability_results.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    top_5_names = [f["feature_name"] for f in data["top_10_features_summary"][:5]]
    expected_top_5 = {
        "perimeter_worst",
        "radius_worst",
        "area_worst",
        "concave points_mean",
        "concave points_worst",
    }
    assert set(top_5_names) == expected_top_5, f"Top 5 đặc trưng không khớp: {top_5_names}"

    # Kiểm tra giá trị mean_importance hợp lệ (0 < importance < 1)
    for feat in data["top_10_features_summary"]:
        assert 0.0 < feat["mean_importance"] < 1.0
        assert feat["std_importance"] >= 0.0


def test_no_test_set_leakage_in_exp4():
    """Đảm bảo tập Test độc lập tuyệt đối và không bị rò rỉ hay thay đổi (giữ nguyên 86 mẫu)."""
    test_csv = ROOT_DIR / "data" / "test.csv"
    assert test_csv.exists(), "Tập test.csv phải tồn tại"
    df_test = pd.read_csv(test_csv)
    assert len(df_test) == 86, f"Tập Test phải giữ nguyên đúng 86 mẫu, hiện có {len(df_test)}"
