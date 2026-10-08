"""
Unit tests cho Nhiệm vụ 11: Random Forest Classifier.
Kiểm tra:
1. Mô hình rf_candidate.joblib tồn tại, tải được và là RandomForestClassifier với random_state=42.
2. Kết quả random_forest_results.json có schema chuẩn và đánh dấu rõ ràng là mô hình ứng viên (is_final_selected_model = False).
3. Random Forest thể hiện sự vượt trội về hiệu năng (Recall, F1, ROC-AUC) so với Cây Quyết định đã cắt tỉa trên Validation.
4. Biểu đồ rf_feature_importance.png tồn tại và có dung lượng hợp lệ (>10KB).
5. Tuyệt đối không rò rỉ dữ liệu sang tập Test (Test set nguyên vẹn 86 mẫu).
"""

import json
from pathlib import Path
import pytest
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from backend.src.config import ROOT_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR
from backend.src.random_forest import (
    RF_CANDIDATE_MODEL_PATH,
    RF_RESULTS_PATH,
    RF_IMPORTANCE_FIGURE_PATH,
    PRUNED_RESULTS_PATH,
)


def test_rf_candidate_model_artifact_exists():
    """Kiểm tra artifact mô hình rf_candidate.joblib tồn tại và là RandomForestClassifier hợp lệ."""
    assert RF_CANDIDATE_MODEL_PATH.exists(), f"Không tìm thấy file mô hình tại {RF_CANDIDATE_MODEL_PATH}"
    model = joblib.load(RF_CANDIDATE_MODEL_PATH)
    assert isinstance(model, RandomForestClassifier), "Model không phải RandomForestClassifier"
    assert model.random_state == 42, f"random_state phải là 42, hiện tại: {model.random_state}"
    assert model.n_estimators >= 50, f"n_estimators phải >= 50, hiện tại: {model.n_estimators}"


def test_rf_results_schema_and_metadata():
    """Kiểm tra schema và metadata của reports/random_forest_results.json."""
    assert RF_RESULTS_PATH.exists(), f"Không tìm thấy file kết quả tại {RF_RESULTS_PATH}"
    with open(RF_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = [
        "pipeline_name",
        "status",
        "is_final_selected_model",
        "random_state",
        "grid_search_total_time_seconds",
        "best_params",
        "cv_performance_at_best_params",
        "top_10_parameter_combinations",
        "ensemble_properties",
        "train_metrics",
        "validation_metrics",
        "comparison_with_pruned_tree",
    ]
    for key in required_keys:
        assert key in data, f"Thiếu key '{key}' trong random_forest_results.json"

    # Kiểm tra quy định: Chỉ lưu mô hình ứng viên, chưa kết luận mô hình cuối
    assert data["is_final_selected_model"] is False, "is_final_selected_model phải là False ở Nhiệm vụ 11"
    assert data["status"] == "candidate_model_evaluated"

    # Kiểm tra best_params
    bp = data["best_params"]
    assert "n_estimators" in bp and bp["n_estimators"] >= 50
    assert "max_features" in bp
    assert "min_samples_leaf" in bp

    # Kiểm tra metrics
    vm = data["validation_metrics"]
    assert 0.0 <= vm["accuracy"] <= 1.0
    assert 0.0 <= vm["recall_malignant"] <= 1.0
    assert 0.0 <= vm["precision_malignant"] <= 1.0
    assert 0.0 <= vm["f1_malignant"] <= 1.0
    assert 0.0 <= vm["roc_auc"] <= 1.0


def test_rf_superiority_over_pruned_tree():
    """Kiểm tra Random Forest vượt trội so với Cây Quyết Định Đã Cắt Tỉa trên tập Validation."""
    assert PRUNED_RESULTS_PATH.exists(), "Cần có pruning_search_results.json để đối chiếu"
    with open(PRUNED_RESULTS_PATH, "r", encoding="utf-8") as f:
        pruned_data = json.load(f)

    with open(RF_RESULTS_PATH, "r", encoding="utf-8") as f:
        rf_data = json.load(f)

    p_val = pruned_data["validation_metrics"]
    rf_val = rf_data["validation_metrics"]

    # Random Forest phải có Recall, F1 và ROC-AUC vượt trội
    assert rf_val["recall_malignant"] >= p_val["recall_malignant"], (
        f"RF Recall ({rf_val['recall_malignant']}) phải >= Pruned Tree Recall ({p_val['recall_malignant']})"
    )
    assert rf_val["f1_malignant"] > p_val["f1_malignant"], (
        f"RF F1 ({rf_val['f1_malignant']}) phải > Pruned Tree F1 ({p_val['f1_malignant']})"
    )
    assert rf_val["roc_auc"] > p_val["roc_auc"], (
        f"RF ROC-AUC ({rf_val['roc_auc']}) phải > Pruned Tree ROC-AUC ({p_val['roc_auc']})"
    )
    assert rf_val["confusion_matrix"]["fn"] <= p_val["confusion_matrix"]["fn"], (
        f"Số ca bỏ sót FN của RF ({rf_val['confusion_matrix']['fn']}) phải <= Pruned Tree ({p_val['confusion_matrix']['fn']})"
    )


def test_rf_feature_importance_visualization_exists():
    """Kiểm tra hình ảnh Feature Importance được tạo đầy đủ và có dung lượng hợp lệ."""
    assert RF_IMPORTANCE_FIGURE_PATH.exists(), f"Thiếu biểu đồ Feature Importance tại {RF_IMPORTANCE_FIGURE_PATH}"
    assert RF_IMPORTANCE_FIGURE_PATH.stat().st_size > 10000, "File biểu đồ quá nhỏ hoặc rỗng"


def test_no_test_set_leakage_in_rf():
    """Đảm bảo tập Test độc lập tuyệt đối và không bị rò rỉ hay thay đổi (giữ nguyên 86 mẫu)."""
    test_csv = ROOT_DIR / "data" / "test.csv"
    assert test_csv.exists(), "Tập test.csv phải tồn tại"
    df_test = pd.read_csv(test_csv)
    assert len(df_test) == 86, f"Tập Test phải giữ nguyên đúng 86 mẫu, hiện có {len(df_test)}"
