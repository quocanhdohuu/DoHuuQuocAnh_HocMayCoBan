"""
Module Xử lý Dữ liệu WDBC (Breast Cancer Wisconsin Diagnostic).
Chịu trách nhiệm:
1. Tải dữ liệu từ nguồn chính thức UCI Machine Learning Repository.
2. Xác thực cấu trúc schema, kiểu dữ liệu, tính toàn vẹn (không missing, đúng 569 mẫu, 30 đặc trưng số).
3. Tách biệt hoàn toàn Feature Matrix (X), Target Series (y), và Identifier Series (id).
4. Loại bỏ ID khỏi không gian đặc trưng học máy để chống Data Leakage / Overfitting giả tạo.
"""

import hashlib
import logging
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
import urllib.request
import pandas as pd
import numpy as np

# Đảm bảo đường dẫn gốc nằm trong sys.path khi chạy trực tiếp file
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Cấu hình encoding UTF-8 cho console stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from backend.src.config import (
    RAW_DATA_PATH,
    DATA_DIR,
    FEATURE_NAMES,
    TARGET_COLUMN,
    ID_COLUMN,
    POSITIVE_CLASS,
    NEGATIVE_CLASS,
)

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# URL chính thức của tập dữ liệu WDBC từ UCI Machine Learning Repository
UCI_WDBC_DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"

# Tên cột đầy đủ theo đặc tả UCI (ID + Diagnosis + 30 features)
ALL_COLUMNS = [ID_COLUMN, TARGET_COLUMN] + FEATURE_NAMES


def compute_sha256(file_path: Path) -> str:
    """Tính toán mã băm SHA256 của tệp tin để đảm bảo tính toàn vẹn."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_uci_wdbc_data(
    dest_path: Optional[Path] = None,
    force_download: bool = False
) -> Path:
    """
    Tải tập dữ liệu WDBC từ kho lưu trữ chính thức UCI.
    Nếu dest_path đã tồn tại và không force_download, bỏ qua việc tải lại.
    Nếu mạng gặp sự cố, tự động fallback sang tệp RAW_DATA_PATH có sẵn trong dự án.
    """
    if dest_path is None:
        dest_path = DATA_DIR / "wdbc.csv"

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if dest_path.exists() and not force_download:
        logger.info(f"Tệp dữ liệu đã tồn tại tại {dest_path}. Bỏ qua bước tải.")
        return dest_path

    try:
        logger.info(f"Đang tải dữ liệu từ nguồn chính thức UCI: {UCI_WDBC_DATA_URL}...")
        req = urllib.request.Request(
            UCI_WDBC_DATA_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode("utf-8").strip()

        # Dữ liệu wdbc.data của UCI không có dòng tiêu đề (header)
        rows = [line.split(",") for line in content.split("\n") if line.strip()]
        df = pd.DataFrame(rows, columns=ALL_COLUMNS)

        # Ép kiểu dữ liệu: ID thành int, 30 đặc trưng thành float
        df[ID_COLUMN] = df[ID_COLUMN].astype(np.int64)
        for col in FEATURE_NAMES:
            df[col] = df[col].astype(np.float64)

        df.to_csv(dest_path, index=False)
        checksum = compute_sha256(dest_path)
        logger.info(f"Tải thành công! Đã lưu tại {dest_path} (SHA256: {checksum})")
        return dest_path

    except Exception as e:
        logger.warning(f"Không thể kết nối đến UCI trực tiếp ({e}). Sử dụng tệp dự phòng nội bộ...")
        if RAW_DATA_PATH.exists():
            df_local = pd.read_csv(RAW_DATA_PATH)
            # Chuẩn hóa tên cột nếu có khoảng trắng
            df_local.columns = [c.strip() for c in df_local.columns]
            df_local.to_csv(dest_path, index=False)
            logger.info(f"Đã sao chép dữ liệu từ {RAW_DATA_PATH} sang {dest_path}")
            return dest_path
        raise FileNotFoundError(f"Không thể tải từ UCI và cũng không tìm thấy tệp {RAW_DATA_PATH}.")


def load_wdbc_dataframe(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Đọc tệp dữ liệu WDBC và trả về pandas DataFrame."""
    if file_path is None:
        file_path = DATA_DIR / "wdbc.csv"
        if not file_path.exists():
            file_path = download_uci_wdbc_data(file_path)

    df = pd.read_csv(file_path)
    # Loại bỏ các cột thừa vô danh nếu có (ví dụ 'Unnamed: 32')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


def validate_wdbc_schema(df: pd.DataFrame) -> Dict[str, any]:
    """
    Kiểm tra tính hợp lệ của schema dữ liệu WDBC:
    - Đúng 569 dòng.
    - Chứa cột ID_COLUMN và TARGET_COLUMN.
    - Đủ 30 đặc trưng số trong FEATURE_NAMES.
    - Không có giá trị thiếu (missing values / NaN).
    - Không có dòng trùng lặp hoàn toàn.
    - Phân bố nhãn nhị phân: chỉ gồm 'B' và 'M'.
    """
    validation_results = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "missing_values_count": int(df.isnull().sum().sum()),
        "duplicate_rows_count": int(df.duplicated().sum()),
        "has_id_column": ID_COLUMN in df.columns,
        "has_target_column": TARGET_COLUMN in df.columns,
        "features_present_count": sum(1 for col in FEATURE_NAMES if col in df.columns),
        "target_distribution": df[TARGET_COLUMN].value_counts().to_dict() if TARGET_COLUMN in df.columns else {},
        "is_valid": True,
        "errors": []
    }

    if validation_results["num_rows"] != 569:
        validation_results["errors"].append(f"Số dòng không phải 569 (hiện tại: {validation_results['num_rows']})")
    if not validation_results["has_id_column"]:
        validation_results["errors"].append(f"Thiếu cột định danh '{ID_COLUMN}'")
    if not validation_results["has_target_column"]:
        validation_results["errors"].append(f"Thiếu cột nhãn '{TARGET_COLUMN}'")
    if validation_results["features_present_count"] != 30:
        validation_results["errors"].append(f"Số đặc trưng không đủ 30 (hiện tại: {validation_results['features_present_count']})")
    if validation_results["missing_values_count"] > 0:
        validation_results["errors"].append(f"Phát hiện {validation_results['missing_values_count']} giá trị NaN/Missing")
    
    # Kiểm tra kiểu dữ liệu của 30 features
    for feat in FEATURE_NAMES:
        if feat in df.columns and not pd.api.types.is_numeric_dtype(df[feat]):
            validation_results["errors"].append(f"Đặc trưng '{feat}' không phải kiểu số")

    if validation_results["errors"]:
        validation_results["is_valid"] = False

    return validation_results


def split_features_and_target(
    df: pd.DataFrame,
    encode_target: bool = True
) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Phân tách rõ ràng:
    - X: Ma trận đặc trưng (30 đặc trưng số, TUYỆT ĐỐI KHÔNG CHỨA 'id' và 'diagnosis').
    - y: Vector nhãn mục tiêu (mã hóa M=1, B=0 nếu encode_target=True).
    - ids: Series định danh bệnh phẩm phục vụ kiểm toán đối chiếu, không dùng cho học máy.
    """
    # 1. Trích xuất ID để đối soát nhưng loại bỏ khỏi X
    ids = df[ID_COLUMN].copy()

    # 2. Trích xuất nhãn mục tiêu y
    if encode_target:
        # Ác tính M = 1, Lành tính B = 0
        y = (df[TARGET_COLUMN] == POSITIVE_CLASS).astype(int)
        y.name = TARGET_COLUMN
    else:
        y = df[TARGET_COLUMN].copy()

    # 3. Trích xuất ma trận đặc trưng X (chỉ gồm 30 đặc trưng số)
    X = df[FEATURE_NAMES].copy().astype(np.float64)

    return X, y, ids


from sklearn.model_selection import train_test_split
import json

from backend.src.config import (
    RAW_DATA_PATH,
    DATA_DIR,
    FEATURE_NAMES,
    TARGET_COLUMN,
    ID_COLUMN,
    POSITIVE_CLASS,
    NEGATIVE_CLASS,
    RANDOM_STATE,
    TRAIN_RATIO,
    VAL_RATIO,
    TEST_RATIO,
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    TEST_DATA_PATH,
    SPLIT_METADATA_PATH,
)


def stratified_split_data(
    df: Optional[pd.DataFrame] = None,
    save_files: bool = True
) -> Dict[str, any]:
    """
    Thực hiện phân chia dữ liệu WDBC theo phương pháp Phân tầng (Stratified Split):
    - Tỷ lệ đề xuất: 70% Train / 15% Validation / 15% Test (Lựa chọn triển khai).
    - Cố định random_state = RANDOM_STATE (42) để đảm bảo tính tái lập 100%.
    - Bảo toàn tỷ lệ nhãn Benign/Malignant trên cả 3 tập con.
    - Ghi nhận và kiểm tra tính rời rạc tuyệt đối (Disjoint) của index giữa các tập.
    - Lưu trữ train.csv, val.csv, test.csv và split_metadata.json.
    """
    if df is None:
        df = load_wdbc_dataframe()

    # Bước 1: Tách 70% Train và 30% Temp (giữ tỷ lệ phân tầng theo nhãn)
    temp_ratio = VAL_RATIO + TEST_RATIO  # 0.30
    df_train, df_temp = train_test_split(
        df,
        test_size=temp_ratio,
        stratify=df[TARGET_COLUMN],
        random_state=RANDOM_STATE
    )

    # Bước 2: Tách 30% Temp thành 15% Validation và 15% Test (tỷ lệ 50:50 của temp)
    val_in_temp_ratio = VAL_RATIO / temp_ratio  # 0.15 / 0.30 = 0.50
    df_val, df_test = train_test_split(
        df_temp,
        test_size=(1.0 - val_in_temp_ratio),
        stratify=df_temp[TARGET_COLUMN],
        random_state=RANDOM_STATE
    )

    # Trích xuất chỉ số index ban đầu
    train_indices = [int(i) for i in df_train.index]
    val_indices = [int(i) for i in df_val.index]
    test_indices = [int(i) for i in df_test.index]

    # Kiểm tra tính rời rạc (Zero Overlap / Disjoint Check)
    set_train, set_val, set_test = set(train_indices), set(val_indices), set(test_indices)
    assert len(set_train & set_val) == 0, "LỖI LEAKAGE: Trùng lặp giữa Train và Validation!"
    assert len(set_train & set_test) == 0, "LỖI LEAKAGE: Trùng lặp giữa Train và Test!"
    assert len(set_val & set_test) == 0, "LỖI LEAKAGE: Trùng lặp giữa Validation và Test!"
    assert len(set_train | set_val | set_test) == len(df), "LỖI: Hợp các tập không bằng dữ liệu gốc!"

    # Thống kê phân bố nhãn
    def get_distribution(d: pd.DataFrame) -> Dict[str, any]:
        counts = d[TARGET_COLUMN].value_counts().to_dict()
        b_cnt = int(counts.get("B", 0))
        m_cnt = int(counts.get("M", 0))
        total = len(d)
        return {
            "total_samples": total,
            "benign_count": b_cnt,
            "malignant_count": m_cnt,
            "malignant_ratio": round(m_cnt / total, 4) if total > 0 else 0.0
        }

    metadata = {
        "split_config": {
            "train_ratio": TRAIN_RATIO,
            "val_ratio": VAL_RATIO,
            "test_ratio": TEST_RATIO,
            "random_state": RANDOM_STATE,
            "split_type": "StratifiedTwoStageSplit",
            "implementation_note": "Tỷ lệ 70/15/15 là lựa chọn triển khai thực nghiệm chuẩn, không phải ràng buộc cố định của tài liệu."
        },
        "sample_counts": {
            "train": len(df_train),
            "val": len(df_val),
            "test": len(df_test),
            "total": len(df)
        },
        "distributions": {
            "original": get_distribution(df),
            "train": get_distribution(df_train),
            "val": get_distribution(df_val),
            "test": get_distribution(df_test)
        },
        "disjoint_check": {
            "train_intersect_val": len(set_train & set_val),
            "train_intersect_test": len(set_train & set_test),
            "val_intersect_test": len(set_val & set_test),
            "is_perfectly_disjoint": True
        },
        "indices": {
            "train": train_indices,
            "val": val_indices,
            "test": test_indices
        }
    }

    if save_files:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df_train.to_csv(TRAIN_DATA_PATH, index=True)
        df_val.to_csv(VAL_DATA_PATH, index=True)
        df_test.to_csv(TEST_DATA_PATH, index=True)

        with open(SPLIT_METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Đã lưu tập Train: {TRAIN_DATA_PATH} ({len(df_train)} mẫu)")
        logger.info(f"Đã lưu tập Validation: {VAL_DATA_PATH} ({len(df_val)} mẫu)")
        logger.info(f"Đã lưu tập Test: {TEST_DATA_PATH} ({len(df_test)} mẫu)")
        logger.info(f"Đã lưu metadata phân chia: {SPLIT_METADATA_PATH}")

    # Tách X, y cho từng tập
    X_train, y_train, ids_train = split_features_and_target(df_train)
    X_val, y_val, ids_val = split_features_and_target(df_val)
    X_test, y_test, ids_test = split_features_and_target(df_test)

    return {
        "df_train": df_train, "df_val": df_val, "df_test": df_test,
        "X_train": X_train, "y_train": y_train, "ids_train": ids_train,
        "X_val": X_val, "y_val": y_val, "ids_val": ids_val,
        "X_test": X_test, "y_test": y_test, "ids_test": ids_test,
        "metadata": metadata
    }


def load_split_data() -> Tuple[
    Tuple[pd.DataFrame, pd.Series],
    Tuple[pd.DataFrame, pd.Series],
    Tuple[pd.DataFrame, pd.Series]
]:
    """
    Nạp sẵn các tập (X_train, y_train), (X_val, y_val), (X_test, y_test).
    Nếu các tệp CSV chưa tồn tại, tự động thực hiện phân chia trước khi nạp.
    """
    if not (TRAIN_DATA_PATH.exists() and VAL_DATA_PATH.exists() and TEST_DATA_PATH.exists()):
        splits = stratified_split_data(save_files=True)
        return (
            (splits["X_train"], splits["y_train"]),
            (splits["X_val"], splits["y_val"]),
            (splits["X_test"], splits["y_test"])
        )

    df_train = pd.read_csv(TRAIN_DATA_PATH, index_col=0)
    df_val = pd.read_csv(VAL_DATA_PATH, index_col=0)
    df_test = pd.read_csv(TEST_DATA_PATH, index_col=0)

    X_train, y_train, _ = split_features_and_target(df_train)
    X_val, y_val, _ = split_features_and_target(df_val)
    X_test, y_test, _ = split_features_and_target(df_test)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


if __name__ == "__main__":
    print("=" * 65)
    print("KIỂM TRA QUY TRÌNH TẢI VÀ PHÂN CHIA DỮ LIỆU WDBC")
    print("=" * 65)

    data_file = download_uci_wdbc_data()
    df_raw = load_wdbc_dataframe(data_file)
    schema_info = validate_wdbc_schema(df_raw)

    print(f"1. Tệp dữ liệu lưu trữ tại: {data_file}")
    print(f"2. Mã băm SHA-256: {compute_sha256(data_file)}")
    print(f"3. Kích thước tập dữ liệu: {schema_info['num_rows']} mẫu, {schema_info['num_columns']} cột")
    print(f"4. Số giá trị khuyết thiếu: {schema_info['missing_values_count']}")
    print(f"5. Số dòng trùng lặp: {schema_info['duplicate_rows_count']}")
    print(f"6. Phân bố nhãn mục tiêu: {schema_info['target_distribution']}")
    print(f"7. Trạng thái kiểm tra Schema: {'HỢP LỆ (PASS)' if schema_info['is_valid'] else 'LỖI (FAIL)'}")

    print("\n--- THỰC HIỆN PHÂN CHIA DỮ LIỆU STRATIFIED SPLIT 70/15/15 ---")
    split_res = stratified_split_data(df_raw, save_files=True)
    meta = split_res["metadata"]

    print(f"Tập Train:      {split_res['X_train'].shape[0]} mẫu ({meta['distributions']['train']['malignant_ratio']*100:.2f}% Malignant)")
    print(f"Tập Validation: {split_res['X_val'].shape[0]} mẫu ({meta['distributions']['val']['malignant_ratio']*100:.2f}% Malignant)")
    print(f"Tập Test:       {split_res['X_test'].shape[0]} mẫu ({meta['distributions']['test']['malignant_ratio']*100:.2f}% Malignant)")
    print(f"Kiểm tra rời rạc (Zero Overlap): {'PASS' if meta['disjoint_check']['is_perfectly_disjoint'] else 'FAIL'}")
    print("=" * 65)

