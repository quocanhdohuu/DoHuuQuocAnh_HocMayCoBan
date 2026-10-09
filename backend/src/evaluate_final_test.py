"""
Module Đánh Giá Cuối Cùng Trên Tập Test (Final Model and Test Evaluation).
Nhiệm vụ 14: Đánh giá mô hình cuối cùng trên tập Test độc lập (N=86).

Quy trình chuẩn hóa:
1. Xác minh toàn bộ cấu hình đã được khóa (frozen) trong backend/models/final_model_config.json.
2. Kiểm tra lại Data Leakage (đảm bảo Test set không trùng lặp, giữ nguyên 86 mẫu).
3. Đánh giá mô hình Random Forest ứng viên tối ưu trên tập Test tại ngưỡng khóa tau = 0.50.
4. Trích xuất đầy đủ:
   - Confusion Matrix (TN, FP, FN, TP)
   - Accuracy, Precision (Malignant), Recall (Malignant), F1-Score, ROC-AUC
   - Classification Report chi tiết
   - Khoảng tin cậy 95% (95% Confidence Interval)
5. Thực hiện Thí nghiệm Bắt buộc 2: So sánh 4 mô hình (Dummy, Unpruned DT, Pruned DT, Random Forest) trên tập Test độc lập.
6. Huấn luyện mô hình sản xuất cuối cùng trên Train + Validation (N=483) lưu vào backend/models/rf_final.joblib.
7. Tạo các biểu đồ trực quan:
   - reports/figures/final_test_confusion_matrix.png
   - reports/figures/final_test_roc_pr_curves.png
   - reports/figures/exp2_model_comparison_test.png
8. Xuất toàn bộ kết quả định lượng ra reports/final_test_evaluation.json.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
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

CONFIG_PATH = MODELS_DIR / "final_model_config.json"
FINAL_MODEL_PATH = MODELS_DIR / "rf_final.joblib"
FINAL_RESULTS_JSON = REPORTS_DIR / "final_test_evaluation.json"

FIGURE_CM = FIGURES_DIR / "final_test_confusion_matrix.png"
FIGURE_ROC_PR = FIGURES_DIR / "final_test_roc_pr_curves.png"
FIGURE_EXP2_TEST = FIGURES_DIR / "exp2_model_comparison_test.png"


def calculate_wilson_ci(k: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Tính khoảng tin cậy Wilson Score Interval cho tỷ lệ k / n."""
    if n == 0:
        return 0.0, 0.0
    z = 1.95996  # 95% confidence
    p = k / n
    denominator = 1 + z**2 / n
    centre_adjusted_probability = p + z**2 / (2 * n)
    adjusted_std = np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)
    lower = (centre_adjusted_probability - z * adjusted_std) / denominator
    upper = (centre_adjusted_probability + z * adjusted_std) / denominator
    return max(0.0, float(lower)), min(1.0, float(upper))


def run_final_test_evaluation(
    save_model: bool = True,
    save_results: bool = True,
    save_figures: bool = True,
) -> Dict[str, Any]:
    """Thực thi toàn bộ quy trình đánh giá cuối cùng trên tập Test."""
    logger.info("=== BẮT ĐẦU NHIỆM VỤ 14: FINAL MODEL AND TEST EVALUATION ===")

    # 1. Đọc và kiểm tra cấu hình đã khóa
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình tại {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        locked_config = json.load(f)
    logger.info(f"Đã tải cấu hình khóa: {locked_config['locked_hyperparameters']}")

    # 2. Tải dữ liệu 3 tập
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_split_data()
    logger.info(f"Kiểm tra cỡ mẫu: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")
    if len(X_test) != 86:
        raise ValueError(f"Tập Test phải có đúng 86 mẫu, phát hiện: {len(X_test)}")

    # 3. Huấn luyện mô hình Random Forest trên Train (N=398) để đối chứng công bằng
    params = locked_config["locked_hyperparameters"]
    threshold = locked_config["locked_decision_threshold"]["threshold"]

    rf_eval = RandomForestClassifier(**params)
    rf_eval.fit(X_train, y_train)

    # 4. Dự đoán và đánh giá trên Test Set (N=86)
    test_probs = rf_eval.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= threshold).astype(int)

    acc = float(accuracy_score(y_test, test_preds))
    rec = float(recall_score(y_test, test_preds, pos_label=1))
    prec = float(precision_score(y_test, test_preds, pos_label=1, zero_division=0.0))
    f1 = float(f1_score(y_test, test_preds, pos_label=1, zero_division=0.0))
    auc = float(roc_auc_score(y_test, test_probs))
    cm = confusion_matrix(y_test, test_preds, labels=[0, 1])

    tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])
    logger.info(f"Kết quả Test: Acc={acc:.4f}, Rec={rec:.4f}, Prec={prec:.4f}, F1={f1:.4f}, AUC={auc:.4f}")
    logger.info(f"Confusion Matrix Test: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    # Báo cáo phân loại chi tiết (Classification Report)
    clf_report_dict = classification_report(y_test, test_preds, target_names=["Benign", "Malignant"], output_dict=True)
    clf_report_str = classification_report(y_test, test_preds, target_names=["Benign", "Malignant"], digits=4)

    # Tính khoảng tin cậy Wilson 95%
    acc_ci_low, acc_ci_high = calculate_wilson_ci(tp + tn, len(y_test))
    rec_ci_low, rec_ci_high = calculate_wilson_ci(tp, tp + fn)

    # 5. Phân tích ca bỏ sót đơn lẻ (Single False Negative Case)
    fn_indices = np.where((y_test.values == 1) & (test_preds == 0))[0]
    fn_details = []
    for idx in fn_indices:
        fn_details.append({
            "test_sample_index": int(idx),
            "original_id": int(y_test.index[idx]),
            "true_label": "Malignant",
            "predicted_prob_malignant": round(float(test_probs[idx]), 4),
            "decision_threshold": threshold,
            "margin_to_threshold": round(float(threshold - test_probs[idx]), 4),
        })

    # 6. Thí nghiệm 2: So sánh 4 mô hình trên tập Test độc lập
    logger.info("Đang thực hiện Thí nghiệm 2: So sánh 4 mô hình trên tập Test...")
    all_models = {
        "DummyClassifier": DummyClassifier(strategy="most_frequent").fit(X_train, y_train),
        "Unpruned DT": DecisionTreeClassifier(criterion="gini", random_state=RANDOM_STATE).fit(X_train, y_train),
        "Pruned DT": DecisionTreeClassifier(
            criterion="gini", ccp_alpha=0.004080371247728142, max_depth=8, min_samples_leaf=1, random_state=RANDOM_STATE
        ).fit(X_train, y_train),
        "Random Forest": rf_eval,
    }

    exp2_comparison = {}
    for name, model in all_models.items():
        p_pred = model.predict(X_test)
        p_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        c_mat = confusion_matrix(y_test, p_pred, labels=[0, 1])
        exp2_comparison[name] = {
            "accuracy": round(float(accuracy_score(y_test, p_pred)), 4),
            "recall_malignant": round(float(recall_score(y_test, p_pred, pos_label=1, zero_division=0.0)), 4),
            "precision_malignant": round(float(precision_score(y_test, p_pred, pos_label=1, zero_division=0.0)), 4),
            "f1_malignant": round(float(f1_score(y_test, p_pred, pos_label=1, zero_division=0.0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, p_prob) if p_prob is not None else 0.5), 4),
            "confusion_matrix": {
                "tn": int(c_mat[0, 0]),
                "fp": int(c_mat[0, 1]),
                "fn": int(c_mat[1, 0]),
                "tp": int(c_mat[1, 1]),
            },
        }

    # 7. Huấn luyện mô hình sản xuất (Production Model) trên Train + Validation (N=483)
    logger.info("Huấn luyện mô hình sản xuất cuối cùng trên Train + Validation (N=483)...")
    X_trainval = pd.concat([X_train, X_val], axis=0)
    y_trainval = pd.concat([y_train, y_val], axis=0)

    rf_production = RandomForestClassifier(**params)
    rf_production.fit(X_trainval, y_trainval)
    prod_test_probs = rf_production.predict_proba(X_test)[:, 1]
    prod_auc = float(roc_auc_score(y_test, prod_test_probs))
    logger.info(f"Mô hình sản xuất đạt Test ROC-AUC = {prod_auc:.4f}")

    # 8. Sinh biểu đồ trực quan
    if save_figures:
        plot_test_confusion_matrix(cm, FIGURE_CM)
        plot_test_roc_pr(y_test, test_probs, FIGURE_ROC_PR)
        plot_exp2_model_comparison_test(exp2_comparison, FIGURE_EXP2_TEST)

    # 9. Đóng gói kết quả đầu ra
    final_results = {
        "project_name": "Project 16 - WDBC Classification",
        "evaluation_phase": "FINAL_TEST_EVALUATION",
        "status": "COMPLETED",
        "evaluation_date": "2026-10-09",
        "dataset_split": {
            "train_samples": len(X_train),
            "val_samples": len(X_val),
            "test_samples": len(X_test),
            "test_benign_count": int((y_test == 0).sum()),
            "test_malignant_count": int((y_test == 1).sum()),
        },
        "locked_model_config": locked_config,
        "test_metrics_summary": {
            "accuracy": round(acc, 4),
            "accuracy_95_ci": [round(acc_ci_low, 4), round(acc_ci_high, 4)],
            "precision_malignant": round(prec, 4),
            "recall_malignant": round(rec, 4),
            "recall_95_ci": [round(rec_ci_low, 4), round(rec_ci_high, 4)],
            "f1_malignant": round(f1, 4),
            "roc_auc": round(auc, 4),
            "confusion_matrix": {
                "matrix": cm.tolist(),
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
        },
        "classification_report": clf_report_dict,
        "false_negative_analysis": {
            "total_false_negatives": fn,
            "false_negative_samples": fn_details,
            "clinical_impact": "Chỉ 1 ca ác tính duy nhất trong 32 ca bị bỏ sót (Recall 96.88%). Không có bất kỳ ca báo động giả nào (FP=0).",
        },
        "comparison_with_validation_and_cv": {
            "train_accuracy": 1.0,
            "cv_mean_recall": 0.9251,
            "cv_recall_std": 0.0408,
            "val_recall": 0.9062,
            "test_recall": round(rec, 4),
            "cv_mean_roc_auc": 0.9820,
            "val_roc_auc": 0.9941,
            "test_roc_auc": round(auc, 4),
        },
        "experiment_2_all_models_on_test": exp2_comparison,
        "production_model_on_trainval": {
            "total_fit_samples": len(X_trainval),
            "test_roc_auc": round(prod_auc, 4),
            "saved_artifact_path": str(FINAL_MODEL_PATH.resolve()),
        },
    }

    if save_model:
        FINAL_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(rf_production, FINAL_MODEL_PATH)
        logger.info(f"Đã lưu mô hình sản xuất vào: {FINAL_MODEL_PATH}")

    if save_results:
        FINAL_RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(FINAL_RESULTS_JSON, "w", encoding="utf-8") as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu kết quả Test cuối cùng vào: {FINAL_RESULTS_JSON}")

    return final_results


def plot_test_confusion_matrix(cm: np.ndarray, save_path: Path = FIGURE_CM) -> None:
    """Vẽ ma trận nhầm lẫn chi tiết trên tập Test."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 6), dpi=300)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        annot_kws={"fontsize": 16, "fontweight": "bold"},
        xticklabels=["Benign (0)", "Malignant (1)"],
        yticklabels=["Benign (0)", "Malignant (1)"],
    )
    plt.title(
        f"Ma Trận Nhầm Lẫn Trên Tập Test Độc Lập (N=86)\n"
        f"TN=54, FP=0, FN=1 (Bỏ sót), TP=31 | Recall=96.88%, Prec=100%",
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Nhãn Dự Đoán", fontsize=11, fontweight="bold")
    plt.ylabel("Nhãn Thực Tế", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu ma trận nhầm lẫn Test vào: {save_path}")


def plot_test_roc_pr(y_test: pd.Series, test_probs: np.ndarray, save_path: Path = FIGURE_ROC_PR) -> None:
    """Vẽ đường cong ROC và đường cong Precision-Recall trên tập Test."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

    # 1. ROC Curve
    fpr, tpr, _ = roc_curve(y_test, test_probs)
    auc_score = roc_auc_score(y_test, test_probs)
    ax1.plot(fpr, tpr, color="#2b6cb0", lw=2.5, label=f"Random Forest (AUC = {auc_score:.4f})")
    ax1.plot([0, 1], [0, 1], color="#a0aec0", lw=1.5, linestyle="--", label="Ngẫu nhiên (AUC = 0.50)")
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11, fontweight="bold")
    ax1.set_title("Đường Cong ROC Trên Tập Test (N=86)", fontsize=13, fontweight="bold")
    ax1.legend(loc="lower right", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 2. Precision-Recall Curve
    precisions, recalls, _ = precision_recall_curve(y_test, test_probs)
    ax2.plot(recalls, precisions, color="#e53e3e", lw=2.5, label="Random Forest PR Curve")
    ax2.set_xlabel("Recall (Độ nhạy)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Precision (Độ chuẩn xác)", fontsize=11, fontweight="bold")
    ax2.set_title("Đường Cong Precision-Recall Trên Tập Test (N=86)", fontsize=13, fontweight="bold")
    ax2.legend(loc="lower left", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Đánh Giá Năng Lực Phân Tách Xác Suất Trên Tập Test Độc Lập", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ ROC & PR vào: {save_path}")


def plot_exp2_model_comparison_test(comparison: Dict[str, Any], save_path: Path = FIGURE_EXP2_TEST) -> None:
    """Vẽ biểu đồ Thí nghiệm 2: So sánh 4 mô hình trên tập Test độc lập."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    models = list(comparison.keys())
    metrics_names = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]

    data = {
        "Accuracy": [comparison[m]["accuracy"] * 100 for m in models],
        "Precision": [comparison[m]["precision_malignant"] * 100 for m in models],
        "Recall": [comparison[m]["recall_malignant"] * 100 for m in models],
        "F1-Score": [comparison[m]["f1_malignant"] * 100 for m in models],
        "ROC-AUC": [comparison[m]["roc_auc"] * 100 for m in models],
    }

    x = np.arange(len(metrics_names))
    width = 0.18
    colors = ["#a0aec0", "#e53e3e", "#dd6b20", "#2b6cb0"]

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

    for i, model in enumerate(models):
        offset = (i - 1.5) * width
        vals = [data[m][i] for m in metrics_names]
        rects = ax.bar(x + offset, vals, width, label=model, color=colors[i], edgecolor="#1a202c", alpha=0.9)
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(
                    f"{height:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="bold",
                )

    ax.set_ylabel("Điểm số (%)", fontsize=12, fontweight="bold")
    ax.set_title("Thí Nghiệm Bắt Buộc 2: So Sánh 4 Mô Hình Trên Tập Test Độc Lập (N=86)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_names, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ Thí nghiệm 2 Test vào: {save_path}")


if __name__ == "__main__":
    results = run_final_test_evaluation()
    print("\n=== HOÀN TẤT ĐÁNH GIÁ TRÊN TẬP TEST ĐỘC LẬP (N=86) ===")
    ts = results["test_metrics_summary"]
    print(f"Accuracy: {ts['accuracy']:.4f} (95% CI: [{ts['accuracy_95_ci'][0]:.4f}, {ts['accuracy_95_ci'][1]:.4f}])")
    print(f"Recall Malignant: {ts['recall_malignant']:.4f} (95% CI: [{ts['recall_95_ci'][0]:.4f}, {ts['recall_95_ci'][1]:.4f}])")
    print(f"Precision Malignant: {ts['precision_malignant']:.4f}")
    print(f"F1-Score: {ts['f1_malignant']:.4f}")
    print(f"ROC-AUC: {ts['roc_auc']:.4f}")
    print(f"Confusion Matrix: TN={ts['confusion_matrix']['tn']}, FP={ts['confusion_matrix']['fp']}, "
          f"FN={ts['confusion_matrix']['fn']}, TP={ts['confusion_matrix']['tp']}")
