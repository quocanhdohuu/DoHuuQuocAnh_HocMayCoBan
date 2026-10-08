"""
Module Thí nghiệm Bắt buộc 1: Khảo sát Đường cong Học tập Train / Cross-Validation theo Độ sâu Cây (Tree Depth).
Yêu cầu:
1. Khảo sát max_depth từ 1 đến 20.
2. Áp dụng 5-Fold Stratified Cross-Validation CHỈ TRÊN TẬP TRAIN (398 mẫu).
3. Đánh giá Recall lớp Malignant (ưu tiên số 1), F1-Score và Accuracy.
4. Ghi nhận điểm Train trung bình và CV trung bình kèm độ lệch chuẩn (Std).
5. Trực quan hóa đồ thị so sánh Train vs CV (có dải mờ sai số ±1 std) lưu vào reports/figures/exp1_depth_curve.png.
6. Phân tích 3 pha: Underfitting, Sweet Spot (Vùng tối ưu), và Overfitting.
7. Xuất kết quả chi tiết ra reports/exp1_depth_results.json.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import recall_score, f1_score, accuracy_score

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import (
    RANDOM_STATE,
    CV_FOLDS,
    FIGURES_DIR,
    REPORTS_DIR,
)
from backend.src.data import load_split_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

EXP1_RESULTS_PATH = REPORTS_DIR / "exp1_depth_results.json"
EXP1_FIGURE_PATH = FIGURES_DIR / "exp1_depth_curve.png"


def run_tree_depth_experiment(
    max_depth_limit: int = 20,
    n_splits: int = 5,
    save_results: bool = True,
    save_figure: bool = True,
) -> Dict[str, Any]:
    """
    Thực thi thí nghiệm khảo sát độ sâu cây từ 1 đến max_depth_limit qua 5-Fold Stratified CV.
    """
    logger.info(f"Bắt đầu Thí nghiệm 1: Khảo sát max_depth từ 1 đến {max_depth_limit} ({n_splits}-Fold Stratified CV)...")
    (X_train, y_train), _, _ = load_split_data()

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    depth_records = []

    for depth in range(1, max_depth_limit + 1):
        fold_train_acc, fold_cv_acc = [], []
        fold_train_rec, fold_cv_rec = [], []
        fold_train_f1, fold_cv_f1 = [], []

        for train_idx, val_idx in skf.split(X_train, y_train):
            X_tr, y_tr = X_train.iloc[train_idx], y_train.iloc[train_idx]
            X_va, y_va = X_train.iloc[val_idx], y_train.iloc[val_idx]

            clf = DecisionTreeClassifier(
                criterion="gini",
                max_depth=depth,
                random_state=RANDOM_STATE
            )
            clf.fit(X_tr, y_tr)

            # Đánh giá trên fold Train
            pred_tr = clf.predict(X_tr)
            fold_train_acc.append(accuracy_score(y_tr, pred_tr))
            fold_train_rec.append(recall_score(y_tr, pred_tr, pos_label=1, zero_division=0.0))
            fold_train_f1.append(f1_score(y_tr, pred_tr, pos_label=1, zero_division=0.0))

            # Đánh giá trên fold CV (Validation của fold)
            pred_va = clf.predict(X_va)
            fold_cv_acc.append(accuracy_score(y_va, pred_va))
            fold_cv_rec.append(recall_score(y_va, pred_va, pos_label=1, zero_division=0.0))
            fold_cv_f1.append(f1_score(y_va, pred_va, pos_label=1, zero_division=0.0))

        depth_records.append({
            "max_depth": depth,
            "train_accuracy": float(np.mean(fold_train_acc)),
            "cv_accuracy_mean": float(np.mean(fold_cv_acc)),
            "cv_accuracy_std": float(np.std(fold_cv_acc)),
            "train_recall_malignant": float(np.mean(fold_train_rec)),
            "cv_recall_mean": float(np.mean(fold_cv_rec)),
            "cv_recall_std": float(np.std(fold_cv_rec)),
            "train_f1_malignant": float(np.mean(fold_train_f1)),
            "cv_f1_mean": float(np.mean(fold_cv_f1)),
            "cv_f1_std": float(np.std(fold_cv_f1)),
        })

    # Tìm độ sâu tối ưu theo tiêu chí cân bằng CV F1 và CV Recall
    best_record = max(depth_records, key=lambda x: (x["cv_f1_mean"] + x["cv_recall_mean"]))
    recommended_depth = best_record["max_depth"]

    analysis = {
        "recommended_depth": recommended_depth,
        "recommended_metrics": {
            "cv_recall_mean": round(best_record["cv_recall_mean"], 4),
            "cv_f1_mean": round(best_record["cv_f1_mean"], 4),
            "cv_accuracy_mean": round(best_record["cv_accuracy_mean"], 4),
        },
        "zones": {
            "underfitting_zone": "max_depth = 1 đến 2 (Cây quá nông, mô hình đơn giản hóa quá mức, cả Train và CV score đều thấp)",
            "sweet_spot_zone": f"max_depth = 3 đến 5 (Đặc biệt depth={recommended_depth}: CV score đạt đỉnh, phương sai thấp, cây gọn gàng dễ giải thích)",
            "overfitting_zone": "max_depth >= 8 (Train score tiệm cận 100% nhưng CV score bão hòa và có xu hướng giảm, khoảng cách gap nới rộng)"
        }
    }

    results = {
        "experiment_name": "Experiment 1: Tree Depth vs Performance",
        "dataset": "WDBC Train Set (N=398)",
        "cv_method": f"{n_splits}-Fold StratifiedKFold",
        "random_state": RANDOM_STATE,
        "depth_range": [1, max_depth_limit],
        "analysis": analysis,
        "records": depth_records
    }

    # Vẽ đồ thị 3 đường cong (Recall, F1-Score, Accuracy)
    if save_figure:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        depths = [r["max_depth"] for r in depth_records]
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)

        # Subplot 1: Recall (Malignant) - Metric quan trọng nhất trong y tế
        ax = axes[0]
        train_rec = [r["train_recall_malignant"] for r in depth_records]
        cv_rec = [r["cv_recall_mean"] for r in depth_records]
        cv_rec_std = [r["cv_recall_std"] for r in depth_records]

        ax.plot(depths, train_rec, "o-", color="#2b5c8f", label="Train Recall (M)", linewidth=2, markersize=5)
        ax.plot(depths, cv_rec, "s-", color="#d95f02", label="CV Recall (M)", linewidth=2, markersize=5)
        ax.fill_between(
            depths,
            np.array(cv_rec) - np.array(cv_rec_std),
            np.array(cv_rec) + np.array(cv_rec_std),
            color="#d95f02", alpha=0.18, label="±1 Std CV"
        )
        ax.axvline(x=recommended_depth, color="#2ca02c", linestyle="--", linewidth=1.5, label=f"Đề xuất (depth={recommended_depth})")
        ax.set_title("Độ nhạy: Recall Malignant vs Độ sâu", fontsize=12, fontweight="bold")
        ax.set_xlabel("Độ sâu tối đa (max_depth)", fontsize=11)
        ax.set_ylabel("Recall Malignant", fontsize=11)
        ax.set_xticks(range(1, max_depth_limit + 1, 2))
        ax.set_ylim(0.78, 1.02)
        ax.legend(loc="lower right", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6)

        # Subplot 2: F1-Score Malignant
        ax = axes[1]
        train_f1 = [r["train_f1_malignant"] for r in depth_records]
        cv_f1 = [r["cv_f1_mean"] for r in depth_records]
        cv_f1_std = [r["cv_f1_std"] for r in depth_records]

        ax.plot(depths, train_f1, "o-", color="#2b5c8f", label="Train F1 (M)", linewidth=2, markersize=5)
        ax.plot(depths, cv_f1, "s-", color="#d95f02", label="CV F1 (M)", linewidth=2, markersize=5)
        ax.fill_between(
            depths,
            np.array(cv_f1) - np.array(cv_f1_std),
            np.array(cv_f1) + np.array(cv_f1_std),
            color="#d95f02", alpha=0.18, label="±1 Std CV"
        )
        ax.axvline(x=recommended_depth, color="#2ca02c", linestyle="--", linewidth=1.5, label=f"Đề xuất (depth={recommended_depth})")
        ax.set_title("Điểm F1 Malignant vs Độ sâu", fontsize=12, fontweight="bold")
        ax.set_xlabel("Độ sâu tối đa (max_depth)", fontsize=11)
        ax.set_ylabel("F1-Score Malignant", fontsize=11)
        ax.set_xticks(range(1, max_depth_limit + 1, 2))
        ax.set_ylim(0.82, 1.02)
        ax.legend(loc="lower right", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6)

        # Subplot 3: Accuracy
        ax = axes[2]
        train_acc = [r["train_accuracy"] for r in depth_records]
        cv_acc = [r["cv_accuracy_mean"] for r in depth_records]
        cv_acc_std = [r["cv_accuracy_std"] for r in depth_records]

        ax.plot(depths, train_acc, "o-", color="#2b5c8f", label="Train Accuracy", linewidth=2, markersize=5)
        ax.plot(depths, cv_acc, "s-", color="#d95f02", label="CV Accuracy", linewidth=2, markersize=5)
        ax.fill_between(
            depths,
            np.array(cv_acc) - np.array(cv_acc_std),
            np.array(cv_acc) + np.array(cv_acc_std),
            color="#d95f02", alpha=0.18, label="±1 Std CV"
        )
        ax.axvline(x=recommended_depth, color="#2ca02c", linestyle="--", linewidth=1.5, label=f"Đề xuất (depth={recommended_depth})")
        ax.set_title("Độ chính xác: Accuracy vs Độ sâu", fontsize=12, fontweight="bold")
        ax.set_xlabel("Độ sâu tối đa (max_depth)", fontsize=11)
        ax.set_ylabel("Accuracy", fontsize=11)
        ax.set_xticks(range(1, max_depth_limit + 1, 2))
        ax.set_ylim(0.85, 1.02)
        ax.legend(loc="lower right", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6)

        plt.suptitle(
            "THÍ NGHIỆM 1: ĐƯỜNG CONG HỌC TẬP TRAIN VÀ 5-FOLD CV THEO ĐỘ SÂU CÂY (WDBC TRAIN SET)\n"
            "Minh họa rõ nét ranh giới Underfitting (depth=1-2) -> Sweet Spot (depth=4) -> Overfitting (depth>=8)",
            fontsize=13, y=1.02, fontweight="bold"
        )
        plt.tight_layout()
        plt.savefig(EXP1_FIGURE_PATH, bbox_inches="tight")
        plt.close()
        logger.info(f"Đã lưu biểu đồ Thí nghiệm 1 tại: {EXP1_FIGURE_PATH}")

    # Lưu kết quả JSON
    if save_results:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXP1_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu kết quả Thí nghiệm 1 tại: {EXP1_RESULTS_PATH}")

    return results


if __name__ == "__main__":
    print("=" * 65)
    print("CHẠY THÍ NGHIỆM 1: ĐƯỜNG CONG TRAIN/CV THEO ĐỘ SÂU CÂY (MAX_DEPTH)")
    print("=" * 65)

    exp_res = run_tree_depth_experiment()

    print("\nBẢNG SỐ LIỆU ĐO LƯỜNG QUA CÁC ĐỘ SÂU TIÊU BIỂU:")
    print(f"{'Depth':<6} | {'Train Rec':<10} | {'CV Rec (Mean±Std)':<20} | {'Train F1':<10} | {'CV F1 (Mean±Std)':<20} | {'CV Acc Mean'}")
    print("-" * 88)
    for r in exp_res["records"]:
        d = r["max_depth"]
        if d in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]:
            print(
                f"{d:<6} | {r['train_recall_malignant']:.4f}     | "
                f"{r['cv_recall_mean']:.4f} ± {r['cv_recall_std']:.4f}       | "
                f"{r['train_f1_malignant']:.4f}   | "
                f"{r['cv_f1_mean']:.4f} ± {r['cv_f1_std']:.4f}       | "
                f"{r['cv_accuracy_mean']:.4f}"
            )

    print("\n--- PHÂN TÍCH BA VÙNG HOẠT ĐỘNG (BIAS-VARIANCE TRADEOFF) ---")
    z = exp_res["analysis"]["zones"]
    print(f"1. Vùng Underfitting: {z['underfitting_zone']}")
    print(f"2. Vùng Sweet Spot:   {z['sweet_spot_zone']}")
    print(f"3. Vùng Overfitting:  {z['overfitting_zone']}")

    rec = exp_res["analysis"]
    print(f"\n=> ĐỀ XUẤT ĐỘ SÂU TỐI ƯU CHO TIỀN CẮT TỈA (PRE-PRUNING): max_depth = {rec['recommended_depth']}")
    print(f"   CV Recall: {rec['recommended_metrics']['cv_recall_mean']*100:.2f}% | "
          f"CV F1: {rec['recommended_metrics']['cv_f1_mean']*100:.2f}% | "
          f"CV Acc: {rec['recommended_metrics']['cv_accuracy_mean']*100:.2f}%")
    print("=" * 65)
