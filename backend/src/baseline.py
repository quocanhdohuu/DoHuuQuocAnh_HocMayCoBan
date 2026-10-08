"""
Module Xây dựng và Đánh giá Mô hình Cơ sở (Baseline - DummyClassifier).
Yêu cầu:
1. Sử dụng sklearn.dummy.DummyClassifier với chiến lược 'most_frequent'.
2. Huấn luyện CHỈ TRÊN TẬP HUẤN LUYỆN (Train Set - 398 mẫu).
3. Đánh giá TRÊN TẬP KIỂM ĐỊNH (Validation Set - 85 mẫu), TUYỆT ĐỐI KHÔNG ĐỤNG ĐẾN TẬP TEST.
4. Xuất Accuracy, Precision, Recall malignant, F1-score và Confusion Matrix.
5. Xử lý mẫu số bằng 0 một cách minh bạch (zero_division=0.0).
6. Lưu artifact mô hình vào backend/models/ và lưu kết quả vào reports/baseline_results.json.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    classification_report,
)
import joblib

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import (
    RANDOM_STATE,
    MODELS_DIR,
    REPORTS_DIR,
)
from backend.src.data import load_split_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASELINE_MODEL_PATH = MODELS_DIR / "baseline_dummy.joblib"
BASELINE_RESULTS_PATH = REPORTS_DIR / "baseline_results.json"


def train_and_evaluate_baseline(
    save_model: bool = True,
    save_results: bool = True
) -> Dict[str, Any]:
    """
    Huấn luyện DummyClassifier (most_frequent) trên Train và đánh giá trên Validation.
    """
    logger.info("Đang nạp dữ liệu Train và Validation (Test set được đóng băng)...")
    (X_train, y_train), (X_val, y_val), _ = load_split_data()

    logger.info(f"Kích thước X_train: {X_train.shape}, y_train: {y_train.shape}")
    logger.info(f"Kích thước X_val:   {X_val.shape}, y_val: {y_val.shape}")

    # 1. Khởi tạo và Huấn luyện DummyClassifier
    # Chiến lược most_frequent: Luôn dự đoán lớp xuất hiện nhiều nhất trong tập Train (Lớp 0 / Benign)
    dummy_model = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy_model.fit(X_train, y_train)
    logger.info("Huấn luyện thành công DummyClassifier(strategy='most_frequent') trên Train!")

    # 2. Suy luận trên tập Validation
    y_val_pred = dummy_model.predict(X_val)
    # Xác suất dự đoán: most_frequent sẽ dự đoán xác suất 1.0 cho lớp 0 và 0.0 cho lớp 1
    y_val_proba = dummy_model.predict_proba(X_val)[:, 1]

    # 3. Tính toán Ma trận nhầm lẫn (Confusion Matrix)
    # y nhãn: 0 = Benign, 1 = Malignant (pos_label = 1)
    cm = confusion_matrix(y_val, y_val_pred, labels=[0, 1])
    tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])

    # 4. Tính toán các độ đo định lượng
    acc = float(accuracy_score(y_val, y_val_pred))
    
    # Xử lý mẫu số bằng 0 (Zero Division Handling):
    # Do mô hình không bao giờ dự đoán lớp 1 (Predicted Positive = TP + FP = 0 + 0 = 0),
    # nên công thức Precision = TP / (TP + FP) = 0 / 0 không xác định về mặt toán học.
    # Ta thiết lập zero_division=0.0 để phản ánh minh bạch rằng mô hình không tìm được ca dương tính nào.
    prec_m = float(precision_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    rec_m = float(recall_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    f1_m = float(f1_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    
    # ROC-AUC: Đường cong ROC của mô hình hằng số trùng với đường chéo ngẫu nhiên (AUC = 0.5)
    roc_auc = float(roc_auc_score(y_val, y_val_proba))

    results = {
        "model_name": "DummyClassifier",
        "strategy": "most_frequent",
        "random_state": RANDOM_STATE,
        "evaluation_split": "Validation",
        "sample_counts": {
            "train_samples": len(X_train),
            "val_samples": len(X_val)
        },
        "target_definition": {
            "positive_class": "Malignant (1)",
            "negative_class": "Benign (0)"
        },
        "metrics": {
            "accuracy": round(acc, 4),
            "precision_malignant": round(prec_m, 4),
            "recall_malignant": round(rec_m, 4),
            "f1_malignant": round(f1_m, 4),
            "roc_auc": round(roc_auc, 4)
        },
        "confusion_matrix": {
            "matrix": [[tn, fp], [fn, tp]],
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp
        },
        "zero_division_explanation": (
            "Do DummyClassifier (most_frequent) luôn dự đoán nhãn là 0 (Benign), số lượng ca được dự đoán là "
            "Dương tính bằng 0 (TP + FP = 0). Mẫu số của Precision = TP / (TP + FP) bị triệt tiêu (0 / 0). "
            "Theo quy chuẩn scikit-learn, giá trị được gán minh bạch bằng 0.0 để phản ánh mô hình không có khả "
            "năng nhận diện ca bệnh ác tính."
        ),
        "clinical_significance": (
            f"Mặc dù đạt Accuracy = {acc*100:.2f}%, mô hình bỏ sót toàn bộ {fn}/{fn+tp} ca ung thư ác tính "
            f"(Recall Malignant = 0.0%). Đây là minh chứng điển hình vì sao Accuracy là độ đo đánh lừa trong y tế."
        )
    }

    # 5. Lưu Artifact Mô hình và Tệp Kết quả
    if save_model:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(dummy_model, BASELINE_MODEL_PATH)
        logger.info(f"Đã lưu mô hình Baseline tại: {BASELINE_MODEL_PATH}")

    if save_results:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(BASELINE_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu kết quả thực nghiệm tại: {BASELINE_RESULTS_PATH}")

    return results


if __name__ == "__main__":
    print("=" * 65)
    print("HUẤN LUYỆN VÀ ĐÁNH GIÁ BASELINE DUMMY CLASSIFIER")
    print("=" * 65)

    res = train_and_evaluate_baseline()

    m = res["metrics"]
    cm = res["confusion_matrix"]

    print("\n--- KẾT QUẢ ĐÁNH GIÁ TRÊN TẬP VALIDATION (N=85) ---")
    print(f"Chiến lược mô hình:       {res['model_name']} ({res['strategy']})")
    print(f"Độ chính xác (Accuracy):   {m['accuracy']:.4f} ({m['accuracy']*100:.2f}%)")
    print(f"Độ nhạy (Recall Malignant): {m['recall_malignant']:.4f} (0.0% - Bỏ sót 100% ca ác tính)")
    print(f"Độ chuẩn xác (Precision): {m['precision_malignant']:.4f} (Mẫu số 0/0 -> gán 0.0)")
    print(f"Điểm F1 (F1-Score M):      {m['f1_malignant']:.4f}")
    print(f"Điểm ROC-AUC:              {m['roc_auc']:.4f} (Tương đương đoán mò ngẫu nhiên)")

    print("\n--- MA TRẬN NHẦM LẪN (CONFUSION MATRIX) ---")
    print(f"                  Dự đoán Lành tính (0)   Dự đoán Ác tính (1)")
    print(f"Thực tế Lành (0):       TN = {cm['true_negative']:<2}                  FP = {cm['false_positive']}")
    print(f"Thực tế Ác   (1):       FN = {cm['false_negative']:<2}                  TP = {cm['true_positive']}")

    print("\n--- KẾT LUẬN Y SINH & MACHINE LEARNING ---")
    print(res["clinical_significance"])
    print("=" * 65)
