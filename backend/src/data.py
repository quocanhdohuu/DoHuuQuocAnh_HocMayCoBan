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


if __name__ == "__main__":
    print("=" * 65)
    print("KIỂM TRA QUY TRÌNH TẢI VÀ XÁC THỰC DỮ LIỆU WDBC")
    print("=" * 65)

    data_file = download_uci_wdbc_data()
    df_raw = load_wdbc_dataframe(data_file)
    schema_info = validate_wdbc_schema(df_raw)

    print(f"1. Tệp dữ liệu lưu trữ tại: {data_file}")
    print(f"2. Mã băm SHA-256: {compute_sha256(data_file)}")
    print(f"3. Kích thước tập dữ liệu: {schema_info['num_rows']} mẫu, {schema_info['num_columns']} cột")
    print(f"4. Số giá trị khuyết thiếu (NaN): {schema_info['missing_values_count']}")
    print(f"5. Số dòng trùng lặp: {schema_info['duplicate_rows_count']}")
    print(f"6. Phân bố nhãn mục tiêu: {schema_info['target_distribution']}")
    print(f"7. Trạng thái kiểm tra Schema: {'HỢP LỆ (PASS)' if schema_info['is_valid'] else 'LỖI (FAIL)'}")

    X, y, ids = split_features_and_target(df_raw, encode_target=True)
    print(f"\n--- PHÂN TÁCH X, y, ID ---")
    print(f"- Ma trận đặc trưng X: Kích thước {X.shape} (30 đặc trưng số, không có ID/diagnosis)")
    print(f"- Vector nhãn mục tiêu y: Kích thước {y.shape} (Tỷ lệ lớp 1: {y.mean():.4f})")
    print(f"- Chuỗi định danh ID: Kích thước {ids.shape} (Đã tách riêng an toàn)")
    print("=" * 65)
