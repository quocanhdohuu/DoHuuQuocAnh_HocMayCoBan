"""
Module Kiểm thử Data Leakage và Tính Đúng đắn ở cấp độ Chia tập (Data Splitting).
Xác thực:
1. Tính rời rạc tuyệt đối giữa các tập Train, Validation, Test (Zero Index/ID Overlap).
2. Bảo toàn tỷ lệ phân tầng (Stratified Distribution).
3. Độc lập tuyệt đối của tập Test và Validation trước mọi tham số huấn luyện.
"""

import json
import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from backend.src.config import (
    FEATURE_NAMES,
    TARGET_COLUMN,
    ID_COLUMN,
    SPLIT_METADATA_PATH,
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    TEST_DATA_PATH,
)
from backend.src.data import (
    load_wdbc_dataframe,
    stratified_split_data,
    load_split_data,
)


@pytest.fixture(scope="module")
def split_datasets():
    """Fixture nạp các tập dữ liệu đã chia và metadata kiểm toán."""
    splits = stratified_split_data(save_files=True)
    return splits


def test_split_sample_sizes(split_datasets):
    """Kiểm tra tỷ lệ 70/15/15: Train 398 mẫu, Val 85 mẫu, Test 86 mẫu (Tổng: 569)."""
    X_train = split_datasets["X_train"]
    X_val = split_datasets["X_val"]
    X_test = split_datasets["X_test"]

    assert len(X_train) == 398, f"Train phải có 398 mẫu, thực tế: {len(X_train)}"
    assert len(X_val) == 85, f"Validation phải có 85 mẫu, thực tế: {len(X_val)}"
    assert len(X_test) == 86, f"Test phải có 86 mẫu, thực tế: {len(X_test)}"
    assert len(X_train) + len(X_val) + len(X_test) == 569, "Tổng số mẫu phải là 569"

    # Đảm bảo mỗi tập đều có đúng 30 đặc trưng số
    assert X_train.shape[1] == 30
    assert X_val.shape[1] == 30
    assert X_test.shape[1] == 30


def test_zero_index_overlap_leakage(split_datasets):
    """Kiểm tra Data Leakage thông qua trùng lặp Index (Disjoint Index Sets)."""
    df_train = split_datasets["df_train"]
    df_val = split_datasets["df_val"]
    df_test = split_datasets["df_test"]

    train_idx = set(df_train.index)
    val_idx = set(df_val.index)
    test_idx = set(df_test.index)

    # 1. Giao giữa các cặp tập con bắt buộc phải rỗng
    assert len(train_idx & val_idx) == 0, "RÒ RỈ: Có mẫu trùng lặp giữa Train và Validation!"
    assert len(train_idx & test_idx) == 0, "RÒ RỈ: Có mẫu trùng lặp giữa Train và Test!"
    assert len(val_idx & test_idx) == 0, "RÒ RỈ: Có mẫu trùng lặp giữa Validation và Test!"

    # 2. Hợp của 3 tập phải phủ kín 569 mẫu
    assert len(train_idx | val_idx | test_idx) == 569, "Mất mát mẫu trong quá trình chia tập!"


def test_zero_id_overlap_leakage(split_datasets):
    """Kiểm tra Data Leakage thông qua trùng lặp mã định danh bệnh phẩm (ID)."""
    ids_train = set(split_datasets["ids_train"])
    ids_val = set(split_datasets["ids_val"])
    ids_test = set(split_datasets["ids_test"])

    assert len(ids_train & ids_val) == 0, "RÒ RỈ ID: Bệnh nhân trong Train xuất hiện ở Validation!"
    assert len(ids_train & ids_test) == 0, "RÒ RỈ ID: Bệnh nhân trong Train xuất hiện ở Test!"
    assert len(ids_val & ids_test) == 0, "RÒ RỈ ID: Bệnh nhân trong Validation xuất hiện ở Test!"


def test_stratification_preservation(split_datasets):
    """Kiểm tra tính bảo toàn phân bố nhãn (Stratified Preservation)."""
    y_train = split_datasets["y_train"]
    y_val = split_datasets["y_val"]
    y_test = split_datasets["y_test"]

    # Tỷ lệ Malignant (1) của tập tổng thể là 212 / 569 ≈ 37.26%
    original_m_ratio = 212 / 569

    train_m_ratio = y_train.mean()
    val_m_ratio = y_val.mean()
    test_m_ratio = y_test.mean()

    # Độ lệch tỷ lệ nhãn không được vượt quá 1% (0.01) so với tổng thể
    assert abs(train_m_ratio - original_m_ratio) < 0.01, f"Train lệch tỷ lệ: {train_m_ratio:.4f}"
    assert abs(val_m_ratio - original_m_ratio) < 0.01, f"Validation lệch tỷ lệ: {val_m_ratio:.4f}"
    assert abs(test_m_ratio - original_m_ratio) < 0.01, f"Test lệch tỷ lệ: {test_m_ratio:.4f}"


def test_independent_preprocessing_simulation_no_leakage(split_datasets):
    """
    Kiểm thử mô phỏng nguyên tắc chống Data Leakage trong tiền xử lý:
    Scaler/Transformer BẮT BUỘC chỉ được fit trên X_train, không được fit trên X_val hay X_test.
    """
    X_train = split_datasets["X_train"]
    X_val = split_datasets["X_val"]
    X_test = split_datasets["X_test"]

    # Giả lập: Fit scaler chỉ trên Train
    scaler_train = StandardScaler()
    scaler_train.fit(X_train)

    # Giả lập vi phạm: Fit scaler trên toàn bộ dữ liệu (Leakage)
    X_all = pd.concat([X_train, X_val, X_test])
    scaler_leaked = StandardScaler()
    scaler_leaked.fit(X_all)

    # Khẳng định: Mean của Train khác với Mean của toàn bộ tập dữ liệu
    # (chứng minh rằng nếu lấy mean toàn bộ sẽ làm rò rỉ thông tin tập Test vào Train)
    assert not np.allclose(scaler_train.mean_, scaler_leaked.mean_), \
        "Cảnh báo: Mean của Train và All trùng nhau hoàn toàn (không hợp lý)!"

    # Áp dụng chuẩn: transform trên Val và Test chỉ dùng tham số của Train
    X_val_scaled = scaler_train.transform(X_val)
    X_test_scaled = scaler_train.transform(X_test)

    assert X_val_scaled.shape == X_val.shape
    assert X_test_scaled.shape == X_test.shape
    assert not np.isnan(X_val_scaled).any()
    assert not np.isnan(X_test_scaled).any()


def test_metadata_file_validity():
    """Kiểm tra tệp split_metadata.json tồn tại và có đủ thông tin kiểm toán."""
    assert SPLIT_METADATA_PATH.exists(), f"Thiếu tệp metadata: {SPLIT_METADATA_PATH}"

    with open(SPLIT_METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["split_config"]["random_state"] == 42
    assert meta["split_config"]["train_ratio"] == 0.70
    assert meta["disjoint_check"]["is_perfectly_disjoint"] is True
    assert meta["sample_counts"]["train"] == 398
    assert meta["sample_counts"]["val"] == 85
    assert meta["sample_counts"]["test"] == 86
