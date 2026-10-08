"""
Module Cấu hình chung cho Dự án Project 16.
Quản lý các hằng số toàn cục, đường dẫn hệ thống và tham số tái lập (Reproducibility).
"""

from pathlib import Path

# Cố định Seed ngẫu nhiên cho toàn bộ quy trình tái lập (Reproducibility)
RANDOM_STATE: int = 42

# Thiết lập đường dẫn gốc dự án (Project Root Directory)
SRC_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SRC_DIR.parent
ROOT_DIR = BACKEND_DIR.parent

# Các đường dẫn phân tầng
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = BACKEND_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCS_DIR = ROOT_DIR / "docs"

# Cấu hình dữ liệu WDBC
RAW_DATA_PATH = ROOT_DIR / "data.csv"
TRAIN_DATA_PATH = DATA_DIR / "train.csv"
TEST_DATA_PATH = DATA_DIR / "test.csv"

ID_COLUMN = "id"
TARGET_COLUMN = "diagnosis"
POSITIVE_CLASS = "M"  # Malignant - Ác tính (1)
NEGATIVE_CLASS = "B"  # Benign - Lành tính (0)

# Danh sách 30 đặc trưng tế bào FNA WDBC
FEATURE_NAMES = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"
]

# Tỷ lệ phân chia tập dữ liệu
TEST_SIZE = 0.2  # 80% Train, 20% Test
CV_FOLDS = 5     # 5-Fold Stratified Cross-Validation
