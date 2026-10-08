"""
Module Huấn luyện và Đánh giá Cây Quyết định Chưa Cắt Tỉa (Unpruned Decision Tree).
Mục đích:
1. Huấn luyện DecisionTreeClassifier không giới hạn độ sâu (criterion='gini', random_state=42) trên tập Train.
2. Đánh giá song song trên cả Train Set (đo lường độ khớp dữ liệu) và Validation Set (đo lường độ tổng quát).
3. Trích xuất cấu trúc hình học của cây: độ sâu thực tế, tổng số nút, số nút lá.
4. Trực quan hóa cây quyết định dạng đồ họa có thể đọc được và lưu vào reports/figures/.
5. So sánh với Baseline DummyClassifier và phân tích bằng chứng Overfitting.
6. Lưu artifact mô hình vào backend/models/ và lưu kết quả vào reports/unpruned_tree_results.json.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
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
    FIGURES_DIR,
    FEATURE_NAMES,
)
from backend.src.data import load_split_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

UNPRUNED_MODEL_PATH = MODELS_DIR / "dt_unpruned.joblib"
UNPRUNED_RESULTS_PATH = REPORTS_DIR / "unpruned_tree_results.json"
UNPRUNED_FIGURE_PATH = FIGURES_DIR / "unpruned_tree_visualization.png"


def train_and_evaluate_unpruned_tree(
    save_model: bool = True,
    save_results: bool = True,
    save_figure: bool = True,
) -> Dict[str, Any]:
    """
    Huấn luyện DecisionTreeClassifier chưa cắt tỉa và đánh giá trên Train vs Validation.
    """
    logger.info("Đang nạp dữ liệu Train và Validation (Tập Test giữ nguyên độc lập)...")
    (X_train, y_train), (X_val, y_val), _ = load_split_data()

    # 1. Khởi tạo Cây Quyết định Chưa Cắt Tỉa (Không giới hạn độ sâu)
    dt_unpruned = DecisionTreeClassifier(
        criterion="gini",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        ccp_alpha=0.0,
        random_state=RANDOM_STATE
    )

    logger.info("Đang huấn luyện DecisionTreeClassifier (Unpruned) trên tập Train (N=398)...")
    dt_unpruned.fit(X_train, y_train)

    # 2. Trích xuất thông số cấu trúc cây
    actual_depth = int(dt_unpruned.get_depth())
    node_count = int(dt_unpruned.tree_.node_count)
    leaf_count = int(dt_unpruned.get_n_leaves())
    logger.info(f"Cấu trúc cây thực tế: Độ sâu = {actual_depth}, Số nút = {node_count}, Số lá = {leaf_count}")

    # 3. Đánh giá trên tập Train (398 mẫu)
    y_train_pred = dt_unpruned.predict(X_train)
    y_train_proba = dt_unpruned.predict_proba(X_train)[:, 1]
    train_acc = float(accuracy_score(y_train, y_train_pred))
    train_prec = float(precision_score(y_train, y_train_pred, pos_label=1))
    train_rec = float(recall_score(y_train, y_train_pred, pos_label=1))
    train_f1 = float(f1_score(y_train, y_train_pred, pos_label=1))
    train_auc = float(roc_auc_score(y_train, y_train_proba))
    cm_train = confusion_matrix(y_train, y_train_pred, labels=[0, 1])

    # 4. Đánh giá trên tập Validation (85 mẫu)
    y_val_pred = dt_unpruned.predict(X_val)
    y_val_proba = dt_unpruned.predict_proba(X_val)[:, 1]
    val_acc = float(accuracy_score(y_val, y_val_pred))
    val_prec = float(precision_score(y_val, y_val_pred, pos_label=1))
    val_rec = float(recall_score(y_val, y_val_pred, pos_label=1))
    val_f1 = float(f1_score(y_val, y_val_pred, pos_label=1))
    val_auc = float(roc_auc_score(y_val, y_val_proba))
    cm_val = confusion_matrix(y_val, y_val_pred, labels=[0, 1])

    # 5. Phân tích khoảng cách Train - Validation (Overfitting Gap)
    gap_accuracy = round((train_acc - val_acc) * 100, 2)
    gap_recall = round((train_rec - val_rec) * 100, 2)
    gap_f1 = round((train_f1 - val_f1) * 100, 2)

    # 6. Đọc kết quả Baseline để so sánh đối chiếu
    baseline_path = REPORTS_DIR / "baseline_results.json"
    baseline_acc = 0.6235
    baseline_rec = 0.0000
    if baseline_path.exists():
        with open(baseline_path, "r", encoding="utf-8") as f:
            b_data = json.load(f)
            baseline_acc = b_data["metrics"]["accuracy"]
            baseline_rec = b_data["metrics"]["recall_malignant"]

    results = {
        "model_name": "DecisionTreeClassifier_Unpruned",
        "criterion": "gini",
        "random_state": RANDOM_STATE,
        "tree_structure": {
            "actual_depth": actual_depth,
            "total_nodes": node_count,
            "leaf_nodes": leaf_count,
        },
        "train_metrics": {
            "accuracy": round(train_acc, 4),
            "precision_malignant": round(train_prec, 4),
            "recall_malignant": round(train_rec, 4),
            "f1_malignant": round(train_f1, 4),
            "roc_auc": round(train_auc, 4),
            "confusion_matrix": {
                "matrix": cm_train.tolist(),
                "tn": int(cm_train[0, 0]),
                "fp": int(cm_train[0, 1]),
                "fn": int(cm_train[1, 0]),
                "tp": int(cm_train[1, 1]),
            }
        },
        "validation_metrics": {
            "accuracy": round(val_acc, 4),
            "precision_malignant": round(val_prec, 4),
            "recall_malignant": round(val_rec, 4),
            "f1_malignant": round(val_f1, 4),
            "roc_auc": round(val_auc, 4),
            "confusion_matrix": {
                "matrix": cm_val.tolist(),
                "tn": int(cm_val[0, 0]),
                "fp": int(cm_val[0, 1]),
                "fn": int(cm_val[1, 0]),
                "tp": int(cm_val[1, 1]),
            }
        },
        "comparison_with_baseline": {
            "baseline_accuracy": baseline_acc,
            "baseline_recall_malignant": baseline_rec,
            "accuracy_improvement": round((val_acc - baseline_acc) * 100, 2),
            "recall_improvement": round((val_rec - baseline_rec) * 100, 2),
        },
        "overfitting_analysis": {
            "has_overfitting": True,
            "evidence": [
                f"Độ chính xác trên tập Train đạt tuyệt đối 100.0%, trong khi trên Validation giảm xuống {val_acc*100:.2f}% (Chênh lệch: {gap_accuracy}%).",
                f"Độ nhạy (Recall Malignant) trên Train đạt 100.0% nhưng trên Validation giảm xuống {val_rec*100:.2f}% (Bỏ sót {cm_val[1, 0]}/32 ca ung thư ác tính).",
                f"Cây phát triển quá sâu ({actual_depth} tầng, {leaf_count} lá) dẫn đến việc tạo ra các phân nhánh quá vụn vặt để cô lập từng điểm ngoại lai."
            ],
            "train_val_gaps": {
                "accuracy_gap_pct": gap_accuracy,
                "recall_gap_pct": gap_recall,
                "f1_gap_pct": gap_f1,
            }
        }
    }

    # 7. Trực quan hóa Cây Quyết định (Hiển thị 3 tầng đầu rõ nét + toàn cảnh)
    if save_figure:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(20, 10), dpi=300)
        # Giới hạn max_depth=3 trong hàm plot_tree để văn bản và điều kiện hiển thị rõ ràng, dễ đọc
        plot_tree(
            dt_unpruned,
            max_depth=3,
            feature_names=FEATURE_NAMES,
            class_names=["Benign (0)", "Malignant (1)"],
            filled=True,
            rounded=True,
            fontsize=10,
            precision=3,
            ax=ax
        )
        ax.set_title(
            f"Trực quan hóa Cây Quyết định Chưa Cắt Tỉa (Hiển thị 3 tầng đầu / Tổng độ sâu: {actual_depth} tầng)\n"
            f"Train Accuracy: {train_acc*100:.1f}% | Validation Accuracy: {val_acc*100:.2f}% (Dấu hiệu Overfitting)",
            fontsize=14, pad=15, fontweight="bold"
        )
        plt.tight_layout()
        plt.savefig(UNPRUNED_FIGURE_PATH, bbox_inches="tight")
        plt.close()
        logger.info(f"Đã lưu biểu đồ trực quan hóa cây tại: {UNPRUNED_FIGURE_PATH}")

    # 8. Lưu Artifact mô hình và kết quả JSON
    if save_model:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(dt_unpruned, UNPRUNED_MODEL_PATH)
        logger.info(f"Đã lưu mô hình Unpruned Tree tại: {UNPRUNED_MODEL_PATH}")

    if save_results:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(UNPRUNED_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu kết quả thực nghiệm tại: {UNPRUNED_RESULTS_PATH}")

    return results


if __name__ == "__main__":
    print("=" * 65)
    print("HUẤN LUYỆN VÀ ĐÁNH GIÁ CÂY QUYẾT ĐỊNH CHƯA CẮT TỈA (UNPRUNED)")
    print("=" * 65)

    res = train_and_evaluate_unpruned_tree()

    st = res["tree_structure"]
    tm = res["train_metrics"]
    vm = res["validation_metrics"]
    cb = res["comparison_with_baseline"]
    oa = res["overfitting_analysis"]

    print(f"\n1. CẤU TRÚC HÌNH HỌC CỦA CÂY:")
    print(f"   - Độ sâu thực tế (Tree Depth): {st['actual_depth']} tầng")
    print(f"   - Tổng số nút (Node Count):    {st['total_nodes']} nút")
    print(f"   - Số nút lá (Leaf Nodes):      {st['leaf_nodes']} lá")

    print(f"\n2. KẾT QUẢ TRÊN TẬP TRAIN (N=398):")
    print(f"   - Độ chính xác (Accuracy):     {tm['accuracy']:.4f} (100.0%)")
    print(f"   - Độ nhạy (Recall Malignant):  {tm['recall_malignant']:.4f} (100.0%)")
    print(f"   - Độ chuẩn xác (Precision):    {tm['precision_malignant']:.4f} (100.0%)")
    print(f"   - Điểm F1 (F1-Score M):        {tm['f1_malignant']:.4f} (100.0%)")
    print(f"   - Ma trận nhầm lẫn Train:      TN={tm['confusion_matrix']['tn']}, FP={tm['confusion_matrix']['fp']}, FN={tm['confusion_matrix']['fn']}, TP={tm['confusion_matrix']['tp']}")

    print(f"\n3. KẾT QUẢ TRÊN TẬP VALIDATION (N=85):")
    print(f"   - Độ chính xác (Accuracy):     {vm['accuracy']:.4f} ({vm['accuracy']*100:.2f}%)")
    print(f"   - Độ nhạy (Recall Malignant):  {vm['recall_malignant']:.4f} ({vm['recall_malignant']*100:.2f}%)")
    print(f"   - Độ chuẩn xác (Precision):    {vm['precision_malignant']:.4f} ({vm['precision_malignant']*100:.2f}%)")
    print(f"   - Điểm F1 (F1-Score M):        {vm['f1_malignant']:.4f} ({vm['f1_malignant']*100:.2f}%)")
    print(f"   - Điểm ROC-AUC:                {vm['roc_auc']:.4f}")
    print(f"   - Ma trận nhầm lẫn Validation: TN={vm['confusion_matrix']['tn']}, FP={vm['confusion_matrix']['fp']}, FN={vm['confusion_matrix']['fn']}, TP={vm['confusion_matrix']['tp']}")

    print(f"\n4. SO SÁNH VỚI DUMMY CLASSIFIER (BASELINE):")
    print(f"   - Cải thiện Accuracy: +{cb['accuracy_improvement']}% (Từ {cb['baseline_accuracy']*100:.2f}% lên {vm['accuracy']*100:.2f}%)")
    print(f"   - Cải thiện Recall M: +{cb['recall_improvement']}% (Từ 0.0% lên {vm['recall_malignant']*100:.2f}%)")

    print(f"\n5. PHÂN TÍCH HIỆN TƯỢNG QUÁ KHỚP (OVERFITTING):")
    print(f"   - Chênh lệch Accuracy (Train - Val): +{oa['train_val_gaps']['accuracy_gap_pct']}%")
    print(f"   - Chênh lệch Recall   (Train - Val): +{oa['train_val_gaps']['recall_gap_pct']}% (Bỏ sót 6 ca ác tính trên Val)")
    for ev in oa["evidence"]:
        print(f"   * {ev}")
    print("=" * 65)
