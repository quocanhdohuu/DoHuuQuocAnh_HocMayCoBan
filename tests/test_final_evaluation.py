"""
Unit tests cho Nhiệm vụ 14: Đánh giá mô hình cuối cùng trên tập Test.
Kiểm tra:
1. Tệp cấu hình final_model_config.json, artifact mô hình rf_final.joblib, tệp kết quả JSON và báo cáo Markdown tồn tại.
2. Cả 3 biểu đồ trực quan hóa (final_test_confusion_matrix.png, final_test_roc_pr_curves.png, exp2_model_comparison_test.png) tồn tại và không rỗng.
3. Kết quả đánh giá tập Test đạt tiêu chuẩn chất lượng cao (Recall >= 95%, Precision = 100%, ROC-AUC > 0.99).
4. Ma trận nhầm lẫn Test chính xác: TN=54, FP=0, FN=1, TP=31.
5. Tập Test giữ nguyên vẹn đúng 86 mẫu (54 Benign, 32 Malignant).
"""

import json
from pathlib import Path
import pytest
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from backend.src.config import ROOT_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR


def test_final_artifacts_exist():
    """Kiểm tra sự tồn tại của tất cả các artifacts cho lần đánh giá Test cuối cùng."""
    config_path = MODELS_DIR / "final_model_config.json"
    model_path = MODELS_DIR / "rf_final.joblib"
    results_path = REPORTS_DIR / "final_test_evaluation.json"
    report_path = REPORTS_DIR / "final_test_report.md"

    assert config_path.exists(), f"Thiếu file cấu hình tại {config_path}"
    assert model_path.exists(), f"Thiếu file mô hình sản xuất tại {model_path}"
    assert results_path.exists(), f"Thiếu file kết quả JSON tại {results_path}"
    assert report_path.exists(), f"Thiếu file báo cáo Markdown tại {report_path}"

    # Kiểm tra model joblib
    model = joblib.load(model_path)
    assert isinstance(model, RandomForestClassifier), "Mô hình phải là RandomForestClassifier"
    assert model.n_estimators == 100
    assert model.random_state == 42


def test_final_figures_exist():
    """Kiểm tra các biểu đồ trực quan hóa đánh giá Test và Thí nghiệm 2 tồn tại và hợp lệ."""
    figures = [
        FIGURES_DIR / "final_test_confusion_matrix.png",
        FIGURES_DIR / "final_test_roc_pr_curves.png",
        FIGURES_DIR / "exp2_model_comparison_test.png",
    ]
    for fig in figures:
        assert fig.exists(), f"Thiếu biểu đồ tại {fig}"
        assert fig.stat().st_size > 10000, f"File biểu đồ quá nhỏ hoặc rỗng: {fig}"


def test_final_test_metrics_values():
    """Kiểm tra tính chính xác của các chỉ số hiệu năng trên tập Test trong tệp JSON."""
    results_path = REPORTS_DIR / "final_test_evaluation.json"
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = data["test_metrics_summary"]
    assert metrics["accuracy"] >= 0.95, f"Accuracy thấp: {metrics['accuracy']}"
    assert metrics["recall_malignant"] >= 0.95, f"Recall thấp: {metrics['recall_malignant']}"
    assert metrics["precision_malignant"] == 1.0, f"Precision phải là 1.0, nhận được: {metrics['precision_malignant']}"
    assert metrics["roc_auc"] >= 0.99, f"ROC-AUC thấp: {metrics['roc_auc']}"

    # Kiểm tra ma trận nhầm lẫn
    cm = metrics["confusion_matrix"]
    assert cm["tn"] == 54, f"TN phải là 54, nhận được: {cm['tn']}"
    assert cm["fp"] == 0, f"FP phải là 0, nhận được: {cm['fp']}"
    assert cm["fn"] == 1, f"FN phải là 1, nhận được: {cm['fn']}"
    assert cm["tp"] == 31, f"TP phải là 31, nhận được: {cm['tp']}"


def test_test_set_integrity():
    """Đảm bảo tập Test độc lập tuyệt đối và giữ nguyên đúng 86 mẫu (54 Benign, 32 Malignant)."""
    test_csv = ROOT_DIR / "data" / "test.csv"
    assert test_csv.exists(), "Tập test.csv phải tồn tại"
    df_test = pd.read_csv(test_csv)
    assert len(df_test) == 86, f"Tập Test phải giữ nguyên đúng 86 mẫu, hiện có {len(df_test)}"
    assert df_test["diagnosis"].isin(["B", 0]).sum() == 54, "Số ca Benign trong Test phải là 54"
    assert df_test["diagnosis"].isin(["M", 1]).sum() == 32, "Số ca Malignant trong Test phải là 32"
