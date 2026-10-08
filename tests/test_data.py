"""
Module Kiểm thử Tự động cho Pipeline Dữ liệu WDBC.
Kiểm tra tính toàn vẹn, kích thước, schema và đảm bảo loại trừ ID khỏi ma trận đặc trưng.
"""

import pytest
import pandas as pd
import numpy as np

from backend.src.config import (
    FEATURE_NAMES,
    TARGET_COLUMN,
    ID_COLUMN,
    DATA_DIR,
)
from backend.src.data import (
    download_uci_wdbc_data,
    load_wdbc_dataframe,
    validate_wdbc_schema,
    split_features_and_target,
)


@pytest.fixture(scope="module")
def wdbc_data():
    """Fixture tải hoặc đọc dữ liệu WDBC một lần duy nhất cho toàn bộ module test."""
    data_path = download_uci_wdbc_data()
    df = load_wdbc_dataframe(data_path)
    return df


def test_wdbc_total_samples_and_columns(wdbc_data):
    """Kiểm tra xác nhận dữ liệu có đúng 569 mẫu bệnh phẩm và chứa đủ 32 thuộc tính gốc."""
    assert len(wdbc_data) == 569, f"Số mẫu phải là 569, thực tế: {len(wdbc_data)}"
    assert ID_COLUMN in wdbc_data.columns, f"Thiếu cột ID '{ID_COLUMN}'"
    assert TARGET_COLUMN in wdbc_data.columns, f"Thiếu cột nhãn '{TARGET_COLUMN}'"


def test_wdbc_schema_integrity(wdbc_data):
    """Kiểm tra tính toàn vẹn của schema: không có NaN, không có dòng trùng lặp."""
    validation = validate_wdbc_schema(wdbc_data)
    assert validation["is_valid"] is True, f"Lỗi schema: {validation['errors']}"
    assert validation["missing_values_count"] == 0, "Dữ liệu không được chứa giá trị missing"
    assert validation["duplicate_rows_count"] == 0, "Dữ liệu không được có dòng trùng lặp"


def test_target_distribution(wdbc_data):
    """Kiểm tra phân bố nhãn mục tiêu: 357 Benign (B) và 212 Malignant (M)."""
    counts = wdbc_data[TARGET_COLUMN].value_counts().to_dict()
    assert counts.get("B") == 357, f"Số lượng Benign (B) phải là 357, thực tế: {counts.get('B')}"
    assert counts.get("M") == 212, f"Số lượng Malignant (M) phải là 212, thực tế: {counts.get('M')}"


def test_feature_matrix_separation(wdbc_data):
    """Kiểm tra ma trận X có đúng 30 đặc trưng số và TUYỆT ĐỐI không chứa ID hoặc diagnosis."""
    X, y, ids = split_features_and_target(wdbc_data, encode_target=True)

    # 1. Kiểm tra kích thước ma trận đặc trưng
    assert X.shape == (569, 30), f"Ma trận X phải có kích thước (569, 30), thực tế: {X.shape}"
    assert len(FEATURE_NAMES) == 30, "Danh sách FEATURE_NAMES phải có đủ 30 đặc trưng"

    # 2. Kiểm tra không bị nhiễm ID hoặc nhãn vào X
    assert ID_COLUMN not in X.columns, f"Cột '{ID_COLUMN}' không được xuất hiện trong X"
    assert TARGET_COLUMN not in X.columns, f"Cột '{TARGET_COLUMN}' không được xuất hiện trong X"

    # 3. Kiểm tra kiểu dữ liệu của 30 đặc trưng
    for col in X.columns:
        assert pd.api.types.is_numeric_dtype(X[col]), f"Đặc trưng {col} phải là kiểu số thực"
        assert not X[col].isnull().any(), f"Đặc trưng {col} có giá trị NaN"

    # 4. Kiểm tra vector nhãn y
    assert y.shape == (569,), f"Vector nhãn y phải có 569 phần tử, thực tế: {y.shape}"
    assert set(y.unique()) == {0, 1}, "Nhãn y phải được mã hóa thành nhị phân {0, 1}"
    assert int(y.sum()) == 212, f"Số ca ác tính (lớp 1) phải là 212, thực tế: {y.sum()}"

    # 5. Kiểm tra chuỗi định danh ID
    assert ids.shape == (569,), f"Chuỗi ID phải có 569 phần tử, thực tế: {ids.shape}"
    assert ids.nunique() == 569, "Mỗi mẫu bệnh phẩm phải có một ID duy nhất"
