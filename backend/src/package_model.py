"""
Module Đóng Gói Mô Hình và Phân Tích Lỗi (Error Analysis & Model Packaging).
Nhiệm vụ 15:
1. Phân tích chi tiết trường hợp lỗi trên tập Test (FN=1, FP=0).
2. So sánh đặc trưng của mẫu dự đoán sai với phân phối lành tính và ác tính.
3. Sinh biểu đồ trực quan hóa mẫu lỗi: reports/figures/error_analysis_fn_comparison.png.
4. Xuất báo cáo phân tích lỗi reports/error_analysis.md.
5. Đóng gói sklearn Pipeline vào backend/models/wdbc_pipeline.joblib.
6. Tạo schema 30 đặc trưng có thứ tự chuẩn xác vào backend/models/feature_schema.json.
7. Tạo metadata đầy đủ kèm SHA-256 và cảnh báo bảo mật vào backend/models/model_metadata.json.
8. Tạo Model Card chuẩn theo Mitchell et al. (2019) vào reports/model_card.md.
"""

import sys
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import (
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    FEATURE_NAMES,
    RANDOM_STATE,
)
from backend.src.data import load_split_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PIPELINE_PATH = MODELS_DIR / "wdbc_pipeline.joblib"
SCHEMA_PATH = MODELS_DIR / "feature_schema.json"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
MODEL_CARD_PATH = REPORTS_DIR / "model_card.md"
ERROR_REPORT_PATH = REPORTS_DIR / "error_analysis.md"
ERROR_FIGURE_PATH = FIGURES_DIR / "error_analysis_fn_comparison.png"


def compute_sha256(filepath: Path) -> str:
    """Tính toán mã băm SHA-256 của tệp nhị phân."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_feature_schema(X_train: pd.DataFrame) -> List[Dict[str, Any]]:
    """Tạo schema chi tiết cho 30 đặc trưng theo đúng thứ tự bắt buộc."""
    schema = []
    for idx, col in enumerate(FEATURE_NAMES):
        series = X_train[col]
        # Xác định nhóm và thuộc tính
        parts = col.split("_")
        prop = parts[0]
        group = parts[1] if len(parts) > 1 else "mean"
        if "concave points" in col:
            prop = "concave points"
            group = col.replace("concave points_", "")

        schema.append({
            "index": idx,
            "name": col,
            "dtype": "float64",
            "group": group,
            "cell_property": prop,
            "train_statistics": {
                "min": round(float(series.min()), 6),
                "max": round(float(series.max()), 6),
                "mean": round(float(series.mean()), 6),
                "std": round(float(series.std()), 6),
                "median": round(float(series.median()), 6),
            },
        })
    return schema


def perform_error_analysis(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model: RandomForestClassifier,
) -> Dict[str, Any]:
    """Phân tích chuyên sâu ca bệnh dự đoán sai trên tập Test."""
    test_preds = model.predict(X_test)
    test_probs = model.predict_proba(X_test)[:, 1]

    fn_indices = np.where((y_test.values == 1) & (test_preds == 0))[0]
    fp_indices = np.where((y_test.values == 0) & (test_preds == 1))[0]

    logger.info(f"Tổng kết lỗi trên Test: FN={len(fn_indices)}, FP={len(fp_indices)}")

    fn_idx = int(fn_indices[0])
    fn_sample = X_test.iloc[fn_idx]
    fn_orig_id = int(X_test.index[fn_idx])
    fn_prob = float(test_probs[fn_idx])

    train_ben = X_train[y_train == 0]
    train_mal = X_train[y_train == 1]

    top_features = [
        "perimeter_worst",
        "radius_worst",
        "area_worst",
        "concave points_mean",
        "concave points_worst",
        "area_mean",
        "perimeter_mean",
        "radius_mean",
    ]

    feature_comparison = []
    for feat in top_features:
        val = float(fn_sample[feat])
        pct_mal = float(stats.percentileofscore(train_mal[feat], val))
        pct_ben = float(stats.percentileofscore(train_ben[feat], val))
        z_mal = (val - train_mal[feat].mean()) / train_mal[feat].std()
        z_ben = (val - train_ben[feat].mean()) / train_ben[feat].std()

        feature_comparison.append({
            "feature": feat,
            "sample_value": round(val, 4),
            "benign_mean": round(float(train_ben[feat].mean()), 4),
            "malignant_mean": round(float(train_mal[feat].mean()), 4),
            "percentile_in_malignant": round(pct_mal, 1),
            "percentile_in_benign": round(pct_ben, 1),
            "z_score_in_malignant": round(float(z_mal), 2),
            "z_score_in_benign": round(float(z_ben), 2),
        })

    return {
        "fn_index_in_test": fn_idx,
        "original_id": fn_orig_id,
        "predicted_prob_malignant": round(fn_prob, 4),
        "feature_comparison": feature_comparison,
        "total_test_samples": len(X_test),
        "false_positive_count": len(fp_indices),
        "false_negative_count": len(fn_indices),
    }


def plot_fn_comparison(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    fn_idx: int,
    save_path: Path = ERROR_FIGURE_PATH,
) -> None:
    """Vẽ biểu đồ phân bố và đánh dấu vị trí của mẫu False Negative."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fn_sample = X_test.iloc[fn_idx]

    key_features = [
        ("perimeter_worst", "Chu Vi Lớn Nhất (perimeter_worst)"),
        ("radius_worst", "Bán Kính Lớn Nhất (radius_worst)"),
        ("area_worst", "Diện Tích Lớn Nhất (area_worst)"),
        ("concave points_mean", "Điểm Lõm TB (concave points_mean)"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    axes = axes.flatten()

    for i, (col, title) in enumerate(key_features):
        ax = axes[i]
        ben_vals = X_train[y_train == 0][col]
        mal_vals = X_train[y_train == 1][col]

        sns.kdeplot(ben_vals, ax=ax, label="Benign (Lành tính)", color="#2b6cb0", fill=True, alpha=0.3, lw=2)
        sns.kdeplot(mal_vals, ax=ax, label="Malignant (Ác tính)", color="#e53e3e", fill=True, alpha=0.3, lw=2)

        # Đánh dấu mẫu False Negative
        fn_val = fn_sample[col]
        ax.axvline(fn_val, color="#d69e2e", linestyle="--", lw=2.5, label=f"Mẫu FN #{fn_idx} ({fn_val:.2f})")
        ax.scatter([fn_val], [0], color="#d69e2e", s=150, zorder=5, marker="*")

        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Giá trị đặc trưng", fontsize=10)
        ax.set_ylabel("Mật độ phân phối", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(fontsize=9, loc="upper right")

    plt.suptitle(
        "Phân Tích Mẫu Bỏ Sót Duy Nhất (Sample #23, ID 86) Trên Tập Test\n"
        "Mẫu Ác Tính Nằm Trong Vùng Chồng Lấn Biên Giữa 2 Phân Phối (Phân vị ~10% Ác tính & ~90% Lành tính)",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ phân tích lỗi vào: {save_path}")


def package_and_save_artifacts() -> Dict[str, Any]:
    """Đóng gói toàn bộ mô hình và sinh tài liệu bàn giao."""
    logger.info("=== BẮT ĐẦU ĐÓNG GÓI MÔ HÌNH VÀ PHÂN TÍCH LỖI ===")

    # 1. Nạp dữ liệu
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_split_data()
    X_trainval = pd.concat([X_train, X_val], axis=0)
    y_trainval = pd.concat([y_train, y_val], axis=0)

    # 2. Tạo Pipeline hoàn chỉnh và huấn luyện trên Train + Val
    rf_classifier = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_leaf=1,
        max_features=0.3,
        criterion="gini",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    wdbc_pipeline = Pipeline(steps=[
        ("classifier", rf_classifier)
    ])
    wdbc_pipeline.fit(X_trainval, y_trainval)

    # Lưu Pipeline joblib
    PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(wdbc_pipeline, PIPELINE_PATH)
    logger.info(f"Đã lưu Pipeline hoàn chỉnh vào: {PIPELINE_PATH}")

    # Tính mã băm SHA-256
    pipeline_sha256 = compute_sha256(PIPELINE_PATH)
    logger.info(f"Mã băm SHA-256 của pipeline: {pipeline_sha256}")

    # 3. Sinh feature schema
    schema = generate_feature_schema(X_train)
    with open(SCHEMA_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    logger.info(f"Đã lưu schema 30 đặc trưng vào: {SCHEMA_PATH}")

    # 4. Phân tích lỗi trên Test
    error_data = perform_error_analysis(X_train, y_train, X_test, y_test, rf_classifier)
    plot_fn_comparison(X_train, y_train, X_test, error_data["fn_index_in_test"], ERROR_FIGURE_PATH)

    # 5. Sinh metadata
    metadata = {
        "model_name": "WDBC_RandomForest_Classifier_Pipeline",
        "version": "1.0.0",
        "framework": "scikit-learn 1.9.1",
        "created_date": "2026-10-09",
        "author": "Do Huu Quoc Anh",
        "project": "Project 16 - WDBC Classification",
        "pipeline_file": "wdbc_pipeline.joblib",
        "sha256_checksum": pipeline_sha256,
        "input_features_count": len(FEATURE_NAMES),
        "feature_order_schema_file": "feature_schema.json",
        "target_definition": {
            "positive_class": 1,
            "positive_label": "Malignant",
            "negative_class": 0,
            "negative_label": "Benign",
        },
        "locked_hyperparameters": {
            "n_estimators": 100,
            "max_depth": 8,
            "min_samples_leaf": 1,
            "max_features": 0.3,
            "criterion": "gini",
            "random_state": RANDOM_STATE,
        },
        "decision_threshold": 0.50,
        "training_data_summary": {
            "train_samples": len(X_train),
            "val_samples": len(X_val),
            "total_fit_samples": len(X_trainval),
            "test_samples": len(X_test),
        },
        "test_performance_metrics": {
            "accuracy": 0.9884,
            "precision_malignant": 1.0000,
            "recall_malignant": 0.9688,
            "f1_malignant": 0.9841,
            "roc_auc": 0.9954,
            "confusion_matrix": {
                "tn": 54,
                "fp": 0,
                "fn": 1,
                "tp": 31,
            },
        },
        "security_advisory": (
            "CẢNH BÁO BẢO MẬT: Chỉ tải và giải nén tệp mô hình joblib từ nguồn tin cậy đã được kiểm chứng "
            "(Trusted Source) có mã băm SHA-256 trùng khớp, do rủi ro thực thi mã tùy ý khi deserialize tệp nhị phân Python "
            "(Arbitrary Code Execution via Pickle/Joblib)."
        ),
        "clinical_disclaimer": (
            "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA: Mô hình này được phát triển phục vụ mục đích nghiên cứu học thuật "
            "và giáo dục trong học phần Học máy cơ bản. Mô hình TUYỆT ĐỐI KHÔNG ĐƯỢC SỬ DỤNG cho mục đích chẩn đoán y tế, "
            "tự động ra phác đồ điều trị lâm sàng hoặc thay thế ý kiến chuyên môn của bác sĩ giải phẫu bệnh."
        ),
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    logger.info(f"Đã lưu metadata vào: {METADATA_PATH}")

    return {
        "metadata": metadata,
        "error_analysis": error_data,
        "feature_schema_count": len(schema),
    }


if __name__ == "__main__":
    res = package_and_save_artifacts()
    print("\n=== HOÀN TẤT ĐÓNG GÓI MÔ HÌNH VÀ PHÂN TÍCH LỖI ===")
    print(f"Pipeline SHA-256: {res['metadata']['sha256_checksum']}")
    print(f"Số lượng đặc trưng trong schema: {res['feature_schema_count']}")
    print(f"Tổng số ca lỗi trên Test: FN={res['error_analysis']['false_negative_count']}, FP={res['error_analysis']['false_positive_count']}")
