"""
Unit tests cho Nhiệm vụ 15: Error Analysis and Model Packaging.
Kiểm tra:
1. Các artifacts đóng gói mô hình (wdbc_pipeline.joblib, feature_schema.json, model_metadata.json, model_card.md, error_analysis.md) tồn tại đầy đủ.
2. Schema 30 đặc trưng có đúng thứ tự 100% so với FEATURE_NAMES.
3. Mã băm SHA-256 trong metadata khớp hoàn toàn với tệp nhị phân pipeline thực tế.
4. Hàm predict_sample hoạt động chuẩn xác, xuất đủ xác suất từng lớp và class mapping.
5. Cơ chế xác minh đầu vào (input alignment) phát hiện lỗi thiếu cột và tự động sắp xếp lại cột đúng vị trí.
"""

import json
import hashlib
from pathlib import Path
import pytest
import numpy as np
import pandas as pd

from backend.src.config import ROOT_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR, FEATURE_NAMES
from backend.src.predict import load_model_package, predict_sample, validate_and_align_input


def test_packaging_artifacts_exist():
    """Kiểm tra sự hiện diện của toàn bộ các file đóng gói và tài liệu bàn giao."""
    pipeline_path = MODELS_DIR / "wdbc_pipeline.joblib"
    schema_path = MODELS_DIR / "feature_schema.json"
    metadata_path = MODELS_DIR / "model_metadata.json"
    model_card_path = REPORTS_DIR / "model_card.md"
    error_report_path = REPORTS_DIR / "error_analysis.md"
    error_fig_path = FIGURES_DIR / "error_analysis_fn_comparison.png"

    assert pipeline_path.exists(), f"Thiếu file pipeline tại: {pipeline_path}"
    assert schema_path.exists(), f"Thiếu file schema tại: {schema_path}"
    assert metadata_path.exists(), f"Thiếu file metadata tại: {metadata_path}"
    assert model_card_path.exists(), f"Thiếu Model Card tại: {model_card_path}"
    assert error_report_path.exists(), f"Thiếu báo cáo phân tích lỗi tại: {error_report_path}"
    assert error_fig_path.exists(), f"Thiếu biểu đồ phân tích lỗi tại: {error_fig_path}"
    assert error_fig_path.stat().st_size > 10000, "Biểu đồ phân tích lỗi quá nhỏ hoặc rỗng"


def test_feature_schema_exact_ordering():
    """Kiểm tra schema 30 đặc trưng có độ dài chính xác và thứ tự khớp 100% với FEATURE_NAMES."""
    schema_path = MODELS_DIR / "feature_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    assert len(schema) == 30, f"Schema phải có đúng 30 đặc trưng, hiện có: {len(schema)}"
    extracted_names = [item["name"] for item in schema]
    assert extracted_names == FEATURE_NAMES, "Thứ tự tên đặc trưng trong schema không khớp với FEATURE_NAMES"


def test_sha256_checksum_matches_binary():
    """Kiểm tra mã băm SHA-256 lưu trong metadata khớp chính xác với file joblib thực tế."""
    pipeline_path = MODELS_DIR / "wdbc_pipeline.joblib"
    metadata_path = MODELS_DIR / "model_metadata.json"

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    hasher = hashlib.sha256()
    with open(pipeline_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    actual_hash = hasher.hexdigest()

    assert metadata["sha256_checksum"] == actual_hash, (
        f"Mã băm không khớp! Lưu: {metadata['sha256_checksum']}, Thực tế: {actual_hash}"
    )


def test_predict_sample_functionality_and_structure():
    """Kiểm tra hàm predict_sample dự đoán thành công và xuất cấu trúc dữ liệu chuẩn hóa."""
    from backend.src.data import load_split_data
    _, _, (X_test, y_test) = load_split_data()

    # Mẫu Benign
    sample_b = X_test.iloc[0].to_dict()
    res_b = predict_sample(sample_b)

    assert res_b["status"] == "success"
    assert res_b["predicted_class"] in [0, 1]
    assert res_b["predicted_label"] in ["Benign", "Malignant"]
    assert 0.0 <= res_b["probability"]["benign"] <= 1.0
    assert 0.0 <= res_b["probability"]["malignant"] <= 1.0
    assert pytest.approx(res_b["probability"]["benign"] + res_b["probability"]["malignant"], rel=1e-3) == 1.0
    assert "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA" in res_b["disclaimer"]


def test_input_alignment_and_validation():
    """Kiểm tra cơ chế phòng vệ tự động sắp xếp lại cột và bắt lỗi khi thiếu đặc trưng."""
    # 1. Bắt lỗi khi thiếu đặc trưng
    invalid_dict = {"radius_mean": 14.5, "texture_mean": 20.1}
    with pytest.raises(ValueError, match="thiếu"):
        validate_and_align_input(invalid_dict)

    # 2. Tự động sắp xếp lại các cột bị xáo trộn vị trí
    shuffled_features = FEATURE_NAMES[::-1]  # Đảo ngược thứ tự 30 cột
    sample_values = {feat: float(i + 1) for i, feat in enumerate(FEATURE_NAMES)}
    shuffled_dict = {feat: sample_values[feat] for feat in shuffled_features}

    df_aligned = validate_and_align_input(shuffled_dict)
    assert list(df_aligned.columns) == FEATURE_NAMES, "Thứ tự cột sau khi căn chỉnh phải khớp với FEATURE_NAMES"
    assert df_aligned["radius_mean"].iloc[0] == sample_values["radius_mean"]
