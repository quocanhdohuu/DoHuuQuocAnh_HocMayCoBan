"""
Unit tests cho Nhiệm vụ 12: Model Comparison.
Kiểm tra:
1. Báo cáo reports/model_comparison.md tồn tại, có cấu trúc đầy đủ bảng biểu so sánh 4 mô hình.
2. Các biểu đồ so sánh mô hình (model_comparison_metrics.png, model_confusion_matrices.png, model_tradeoff_pr.png) tồn tại và không rỗng.
3. Cả 4 artifact mô hình đều tồn tại sẵn sàng trong backend/models/.
4. Tuyệt đối không rò rỉ dữ liệu sang tập Test (Test set nguyên vẹn 86 mẫu).
"""

from pathlib import Path
import pytest
import pandas as pd

from backend.src.config import ROOT_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR


def test_comparison_report_exists_and_complete():
    """Kiểm tra báo cáo so sánh model_comparison.md tồn tại và chứa đủ nội dung 4 mô hình."""
    report_path = REPORTS_DIR / "model_comparison.md"
    assert report_path.exists(), f"Không tìm thấy file báo cáo tại {report_path}"
    content = report_path.read_text(encoding="utf-8")

    # Kiểm tra sự hiện diện của 4 mô hình
    assert "DummyClassifier" in content
    assert "Unpruned" in content or "Chưa Cắt Tỉa" in content
    assert "Pruned" in content or "Đã Cắt Tỉa" in content
    assert "Random Forest" in content

    # Kiểm tra các metric bắt buộc
    assert "Accuracy" in content
    assert "Precision" in content
    assert "Recall" in content
    assert "F1" in content
    assert "ROC-AUC" in content

    # Kiểm tra phân tích trade-off và overfitting
    assert "Confusion Matrix" in content or "Ma Trận Nhầm Lẫn" in content
    assert "Trade-off" in content or "Đánh Đổi" in content
    assert "Overfitting" in content


def test_comparison_figures_exist():
    """Kiểm tra 3 biểu đồ so sánh được tạo đầy đủ và có kích thước hợp lệ."""
    figures = [
        FIGURES_DIR / "model_comparison_metrics.png",
        FIGURES_DIR / "model_confusion_matrices.png",
        FIGURES_DIR / "model_tradeoff_pr.png",
    ]
    for fig in figures:
        assert fig.exists(), f"Thiếu biểu đồ tại {fig}"
        assert fig.stat().st_size > 10000, f"File biểu đồ quá nhỏ hoặc rỗng: {fig}"


def test_all_four_model_artifacts_exist():
    """Kiểm tra đầy đủ 4 artifact mô hình đã được huấn luyện và lưu trữ."""
    models = [
        MODELS_DIR / "baseline_dummy.joblib",
        MODELS_DIR / "dt_unpruned.joblib",
        MODELS_DIR / "dt_pruned.joblib",
        MODELS_DIR / "rf_candidate.joblib",
    ]
    for model_path in models:
        assert model_path.exists(), f"Thiếu file mô hình artifact: {model_path}"


def test_no_test_set_leakage():
    """Đảm bảo tập Test độc lập tuyệt đối và không bị rò rỉ hay thay đổi (giữ nguyên 86 mẫu)."""
    test_csv = ROOT_DIR / "data" / "test.csv"
    assert test_csv.exists(), "Tập test.csv phải tồn tại"
    df_test = pd.read_csv(test_csv)
    assert len(df_test) == 86, f"Tập Test phải giữ nguyên đúng 86 mẫu, hiện có {len(df_test)}"
