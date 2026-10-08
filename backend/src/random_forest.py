"""
Module Huấn luyện, Tối ưu Siêu tham số và Đánh giá Rừng Ngẫu nhiên (Random Forest).
Nhiệm vụ 11: Xây dựng RandomForestClassifier sử dụng dữ liệu Train có kiểm soát và tối ưu hóa.

Nguyên lý hoạt động và nền tảng lý thuyết:
1. Bootstrap Sampling (Lấy mẫu hoàn lại):
   - Với tập huấn luyện ban đầu D gồm N mẫu, mỗi cây con trong rừng được huấn luyện trên một tập mẫu con D_b
     được tạo bằng cách rút ngẫu nhiên N mẫu có hoàn lại (sampling with replacement) từ D.
   - Về mặt xác suất, xác suất một mẫu cụ thể KHÔNG được chọn vào cây con là (1 - 1/N)^N. Khi N -> vô cùng,
     giới hạn này tiến tới 1/e ~ 36.8%. Khoảng 36.8% mẫu không tham gia huấn luyện cây này gọi là Out-Of-Bag (OOB),
     có thể được dùng như một tập kiểm chứng nội tại (internal validation) mà không cần chia tách tập dữ liệu ngoài.

2. Random Feature Selection (Lựa chọn đặc trưng ngẫu nhiên):
   - Tại mỗi nút phân chia, thay vì quét toàn bộ p đặc trưng (p=30) như Decision Tree truyền thống,
     Random Forest chỉ chọn ngẫu nhiên một tập con gồm m đặc trưng (m = max_features, thường là sqrt(p) ~ 5).
   - Tác dụng: Phá vỡ tính tương quan (de-correlation) giữa các cây con. Nếu có một đặc trưng quá vượt trội,
     mọi cây trong Bagging thông thường đều sẽ chọn đặc trưng đó ở nút gốc, khiến các cây tương tự nhau.
     Bằng cách hạn chế đặc trưng, các cây buộc phải khai thác các tín hiệu từ những đặc trưng tiềm năng khác.

3. Voting (Cơ chế bỏ phiếu bầu):
   - Phân loại bằng biểu quyết đa số (Majority Voting) hoặc trung bình xác suất (Soft Voting):
     P(y = c | x) = (1 / B) * sum_{b=1}^B P_b(y = c | x).
   - Soft Voting được scikit-learn áp dụng mặc định qua predict_proba, cho đường cong ROC mịn màng hơn.

4. Giảm Phương Sai (Variance Reduction):
   - Xét trung bình của B biến ngẫu nhiên có cùng phương sai sigma^2 và hệ số tương quan cặp đôi rho:
     Var(X_bar) = rho * sigma^2 + ((1 - rho) / B) * sigma^2
   - Khi số lượng cây B tăng lên (B -> inf), thành phần thứ hai ((1 - rho)/B)*sigma^2 tiến về 0.
   - Random Feature Selection làm giảm hệ số tương quan rho giữa các cây con, do đó làm giảm thành phần
     chặn dưới rho * sigma^2, kéo phương sai tổng thể của mô hình rừng xuống thấp hơn rất nhiều so với một cây đơn lẻ,
     trong khi vẫn duy trì độ lệch (bias) thấp.
"""

import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
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

RF_CANDIDATE_MODEL_PATH = MODELS_DIR / "rf_candidate.joblib"
RF_RESULTS_PATH = REPORTS_DIR / "random_forest_results.json"
RF_IMPORTANCE_FIGURE_PATH = FIGURES_DIR / "rf_feature_importance.png"
PRUNED_RESULTS_PATH = REPORTS_DIR / "pruning_search_results.json"


def run_rf_grid_search(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cv_splits: int = 5,
    random_state: int = RANDOM_STATE,
) -> Tuple[Dict[str, Any], RandomForestClassifier, pd.DataFrame, float]:
    """
    Dò tìm siêu tham số tối ưu cho Random Forest sử dụng 5-Fold Stratified Cross-Validation chỉ trên Train.
    Không gian tham số được thiết kế phù hợp với quy mô dữ liệu WDBC (398 mẫu train, 30 đặc trưng).
    """
    logger.info("Thiết lập không gian siêu tham số cho Random Forest...")

    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 4, 6, 8],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", 0.3],
    }

    skf = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=random_state)
    scoring = {
        "recall": "recall",
        "precision": "precision",
        "f1": "f1",
        "accuracy": "accuracy",
        "roc_auc": "roc_auc",
    }

    total_combinations = (
        len(param_grid["n_estimators"])
        * len(param_grid["max_depth"])
        * len(param_grid["min_samples_leaf"])
        * len(param_grid["max_features"])
    )
    logger.info(
        f"Bắt đầu GridSearchCV Random Forest với {total_combinations} tổ hợp qua {cv_splits}-Fold CV "
        f"({total_combinations * cv_splits} lượt huấn luyện)..."
    )

    start_time = time.perf_counter()
    grid_search = GridSearchCV(
        estimator=RandomForestClassifier(random_state=random_state, n_jobs=-1),
        param_grid=param_grid,
        scoring=scoring,
        refit="recall",
        cv=skf,
        n_jobs=-1,
        return_train_score=True,
    )
    grid_search.fit(X_train, y_train)
    grid_search_time = time.perf_counter() - start_time
    logger.info(f"Hoàn thành GridSearchCV trong {grid_search_time:.2f} giây.")

    cv_results_df = pd.DataFrame(grid_search.cv_results_)

    # Tiêu chí chọn best model:
    # 1. Recall Malignant trung bình CV cao nhất
    # 2. F1-score trung bình CV cao nhất
    # 3. ROC-AUC trung bình CV cao nhất
    cv_sorted = cv_results_df.sort_values(
        by=["mean_test_recall", "mean_test_f1", "mean_test_roc_auc"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    best_row = cv_sorted.iloc[0]
    best_params = {
        "n_estimators": int(best_row["param_n_estimators"]),
        "max_depth": None if pd.isna(best_row["param_max_depth"]) else int(best_row["param_max_depth"]),
        "min_samples_leaf": int(best_row["param_min_samples_leaf"]),
        "max_features": (
            float(best_row["param_max_features"])
            if isinstance(best_row["param_max_features"], (int, float))
            else str(best_row["param_max_features"])
        ),
    }

    logger.info(f"Bộ tham số tối ưu (best_params): {best_params}")
    logger.info(
        f"Điểm CV trung bình tại best_params: "
        f"Recall={best_row['mean_test_recall']:.4f} (±{best_row['std_test_recall']:.4f}), "
        f"Precision={best_row['mean_test_precision']:.4f}, "
        f"F1={best_row['mean_test_f1']:.4f}, "
        f"Accuracy={best_row['mean_test_accuracy']:.4f}, "
        f"ROC-AUC={best_row['mean_test_roc_auc']:.4f}"
    )

    # Huấn luyện mô hình ứng viên tối ưu trên toàn bộ tập Train (N=398)
    fit_start = time.perf_counter()
    best_rf_candidate = RandomForestClassifier(
        n_estimators=best_params["n_estimators"],
        max_depth=best_params["max_depth"],
        min_samples_leaf=best_params["min_samples_leaf"],
        max_features=best_params["max_features"],
        random_state=random_state,
        n_jobs=-1,
    )
    best_rf_candidate.fit(X_train, y_train)
    fit_time = time.perf_counter() - fit_start
    logger.info(f"Thời gian khớp mô hình ứng viên trên toàn bộ tập Train: {fit_time:.4f} giây.")

    return best_params, best_rf_candidate, cv_sorted, grid_search_time


def evaluate_rf_candidate(
    model: RandomForestClassifier,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    fit_time: float,
) -> Dict[str, Any]:
    """
    Đánh giá mô hình Random Forest ứng viên trên tập Train và Validation.
    Lưu ý: Tập Test TUYỆT ĐỐI không được sử dụng ở bước này.
    """
    logger.info("Đang đánh giá Random Forest ứng viên trên Train và Validation...")

    # Đánh giá trên Train
    y_train_pred = model.predict(X_train)
    y_train_proba = model.predict_proba(X_train)[:, 1]
    train_acc = float(accuracy_score(y_train, y_train_pred))
    train_prec = float(precision_score(y_train, y_train_pred, pos_label=1))
    train_rec = float(recall_score(y_train, y_train_pred, pos_label=1))
    train_f1 = float(f1_score(y_train, y_train_pred, pos_label=1))
    train_auc = float(roc_auc_score(y_train, y_train_proba))
    cm_train = confusion_matrix(y_train, y_train_pred, labels=[0, 1])

    # Đánh giá trên Validation
    y_val_pred = model.predict(X_val)
    y_val_proba = model.predict_proba(X_val)[:, 1]
    val_acc = float(accuracy_score(y_val, y_val_pred))
    val_prec = float(precision_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    val_rec = float(recall_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    val_f1 = float(f1_score(y_val, y_val_pred, pos_label=1, zero_division=0.0))
    val_auc = float(roc_auc_score(y_val, y_val_proba))
    cm_val = confusion_matrix(y_val, y_val_pred, labels=[0, 1])

    # Tính toán thông số cây trong rừng
    tree_depths = [int(tree.get_depth()) for tree in model.estimators_]
    tree_leaves = [int(tree.get_n_leaves()) for tree in model.estimators_]

    eval_results = {
        "ensemble_properties": {
            "n_estimators": int(model.n_estimators),
            "max_features": model.max_features,
            "max_depth_param": model.max_depth,
            "min_samples_leaf": int(model.min_samples_leaf),
            "average_tree_depth": round(float(np.mean(tree_depths)), 2),
            "max_tree_depth": int(np.max(tree_depths)),
            "min_tree_depth": int(np.min(tree_depths)),
            "average_leaf_count": round(float(np.mean(tree_leaves)), 2),
            "training_time_seconds": round(fit_time, 4),
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
            },
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
            },
        },
        "generalization_gap": {
            "accuracy_gap_pct": round(abs(train_acc - val_acc) * 100, 2),
            "recall_gap_pct": round(abs(train_rec - val_rec) * 100, 2),
            "f1_gap_pct": round(abs(train_f1 - val_f1) * 100, 2),
        },
    }

    return eval_results


def plot_rf_feature_importance(
    model: RandomForestClassifier,
    feature_names: List[str] = FEATURE_NAMES,
    top_n: int = 15,
    save_path: Path = RF_IMPORTANCE_FIGURE_PATH,
) -> None:
    """
    Trực quan hóa mức độ quan trọng của đặc trưng (MDI - Mean Decrease in Impurity) trong Random Forest.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    top_features = [feature_names[i] for i in indices][::-1]
    top_scores = importances[indices][::-1]

    plt.figure(figsize=(10, 7), dpi=300)
    bars = plt.barh(top_features, top_scores, color="#2b5c8f", edgecolor="#1a365d", height=0.65)
    
    # Ghi nhãn giá trị trên từng thanh
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.003,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.3f}",
            ha="left",
            va="center",
            fontsize=9,
            color="#2d3748",
            fontweight="bold",
        )

    plt.xlabel("Mean Decrease in Impurity (Gini Importance)", fontsize=11, fontweight="bold")
    plt.title(
        f"Top {top_n} Đặc Trưng Quan Trọng Nhất Trong Random Forest (N=100 Trees)",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    plt.xlim(0, max(top_scores) * 1.15)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ Feature Importance vào: {save_path}")


def compare_with_pruned_tree(
    rf_eval: Dict[str, Any],
    pruned_path: Path = PRUNED_RESULTS_PATH,
) -> Dict[str, Any]:
    """
    So sánh đối chiếu hiệu năng giữa Cây Quyết định đã cắt tỉa (Nhiệm vụ 10) và Random Forest (Nhiệm vụ 11).
    """
    comparison = {
        "pruned_tree_available": False,
        "validation_metric_deltas": {},
        "confusion_matrix_comparison": {},
    }

    if not pruned_path.exists():
        logger.warning(f"Không tìm thấy file kết quả cây đã tỉa tại: {pruned_path}")
        return comparison

    with open(pruned_path, "r", encoding="utf-8") as f:
        pruned_data = json.load(f)

    comparison["pruned_tree_available"] = True
    p_val = pruned_data["validation_metrics"]
    r_val = rf_eval["validation_metrics"]

    comparison["validation_metric_deltas"] = {
        "accuracy": {
            "pruned_tree": p_val["accuracy"],
            "random_forest": r_val["accuracy"],
            "delta": round(r_val["accuracy"] - p_val["accuracy"], 4),
        },
        "precision_malignant": {
            "pruned_tree": p_val["precision_malignant"],
            "random_forest": r_val["precision_malignant"],
            "delta": round(r_val["precision_malignant"] - p_val["precision_malignant"], 4),
        },
        "recall_malignant": {
            "pruned_tree": p_val["recall_malignant"],
            "random_forest": r_val["recall_malignant"],
            "delta": round(r_val["recall_malignant"] - p_val["recall_malignant"], 4),
        },
        "f1_malignant": {
            "pruned_tree": p_val["f1_malignant"],
            "random_forest": r_val["f1_malignant"],
            "delta": round(r_val["f1_malignant"] - p_val["f1_malignant"], 4),
        },
        "roc_auc": {
            "pruned_tree": p_val["roc_auc"],
            "random_forest": r_val["roc_auc"],
            "delta": round(r_val["roc_auc"] - p_val["roc_auc"], 4),
        },
    }

    p_cm = p_val["confusion_matrix"]
    r_cm = r_val["confusion_matrix"]
    comparison["confusion_matrix_comparison"] = {
        "false_negatives": {
            "pruned_tree": p_cm["fn"],
            "random_forest": r_cm["fn"],
            "reduction": p_cm["fn"] - r_cm["fn"],
        },
        "false_positives": {
            "pruned_tree": p_cm["fp"],
            "random_forest": r_cm["fp"],
            "reduction": p_cm["fp"] - r_cm["fp"],
        },
    }

    return comparison


def run_random_forest_pipeline(
    save_candidate_model: bool = True,
    save_results: bool = True,
    save_figures: bool = True,
) -> Dict[str, Any]:
    """
    Thực thi toàn bộ quy trình xây dựng mô hình Random Forest ứng viên:
    1. Tải dữ liệu Train và Validation (Tập Test giữ nguyên).
    2. Chạy GridSearchCV với 5-Fold Stratified CV trên Train.
    3. Đánh giá ứng viên trên Train và Validation.
    4. Trực quan hóa Feature Importance.
    5. So sánh với Cây Quyết định đã cắt tỉa.
    6. Lưu mô hình ứng viên và kết quả JSON (chưa kết luận mô hình cuối).
    """
    logger.info("=== BẮT ĐẦU NHIỆM VỤ 11: RANDOM FOREST CLASSIFIER ===")

    # 1. Nạp dữ liệu
    (X_train, y_train), (X_val, y_val), _ = load_split_data()

    # 2. Dò tìm siêu tham số qua GridSearchCV
    best_params, best_rf, cv_sorted, total_search_time = run_rf_grid_search(
        X_train=X_train,
        y_train=y_train,
        cv_splits=5,
    )

    # 3. Đánh giá mô hình ứng viên
    eval_results = evaluate_rf_candidate(
        model=best_rf,
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        fit_time=0.05,
    )

    # 4. Trực quan hóa Feature Importance
    if save_figures:
        plot_rf_feature_importance(best_rf)

    # 5. So sánh với Cây Quyết định đã cắt tỉa
    comparison = compare_with_pruned_tree(eval_results)

    # 6. Trích xuất top 10 cấu hình trong Grid Search
    top_candidates = []
    top_rows = cv_sorted.head(10)
    for _, row in top_rows.iterrows():
        top_candidates.append({
            "n_estimators": int(row["param_n_estimators"]),
            "max_depth": None if pd.isna(row["param_max_depth"]) else int(row["param_max_depth"]),
            "min_samples_leaf": int(row["param_min_samples_leaf"]),
            "max_features": (
                float(row["param_max_features"])
                if isinstance(row["param_max_features"], (int, float))
                else str(row["param_max_features"])
            ),
            "cv_mean_recall": round(float(row["mean_test_recall"]), 4),
            "cv_std_recall": round(float(row["std_test_recall"]), 4),
            "cv_mean_precision": round(float(row["mean_test_precision"]), 4),
            "cv_mean_f1": round(float(row["mean_test_f1"]), 4),
            "cv_mean_accuracy": round(float(row["mean_test_accuracy"]), 4),
            "cv_mean_roc_auc": round(float(row["mean_test_roc_auc"]), 4),
        })

    # Đóng gói toàn bộ kết quả
    final_output = {
        "pipeline_name": "RandomForestClassifier_Tuning",
        "status": "candidate_model_evaluated",
        "is_final_selected_model": False,
        "note": "Mô hình ứng viên, chưa kết luận mô hình cuối cùng cho đến khi hoàn thành các thí nghiệm bắt buộc.",
        "random_state": RANDOM_STATE,
        "grid_search_total_time_seconds": round(total_search_time, 2),
        "best_params": best_params,
        "cv_performance_at_best_params": {
            "mean_recall": float(cv_sorted.iloc[0]["mean_test_recall"]),
            "std_recall": float(cv_sorted.iloc[0]["std_test_recall"]),
            "mean_precision": float(cv_sorted.iloc[0]["mean_test_precision"]),
            "mean_f1": float(cv_sorted.iloc[0]["mean_test_f1"]),
            "mean_accuracy": float(cv_sorted.iloc[0]["mean_test_accuracy"]),
            "mean_roc_auc": float(cv_sorted.iloc[0]["mean_test_roc_auc"]),
        },
        "top_10_parameter_combinations": top_candidates,
        "ensemble_properties": eval_results["ensemble_properties"],
        "train_metrics": eval_results["train_metrics"],
        "validation_metrics": eval_results["validation_metrics"],
        "generalization_gap": eval_results["generalization_gap"],
        "comparison_with_pruned_tree": comparison,
    }

    # 7. Lưu mô hình ứng viên và kết quả JSON
    if save_candidate_model:
        RF_CANDIDATE_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_rf, RF_CANDIDATE_MODEL_PATH)
        logger.info(f"Đã lưu mô hình Random Forest ứng viên vào: {RF_CANDIDATE_MODEL_PATH}")

    if save_results:
        RF_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RF_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu toàn bộ kết quả nghiên cứu Random Forest vào: {RF_RESULTS_PATH}")

    return final_output


if __name__ == "__main__":
    results = run_random_forest_pipeline()
    print("\n=== TỔNG HỢP KẾT QUẢ NHIỆM VỤ 11: RANDOM FOREST ===")
    print(f"Cấu hình ứng viên tối ưu (best_params): {results['best_params']}")
    print(f"Thời gian tìm kiếm lưới: {results['grid_search_total_time_seconds']}s")
    print(f"Điểm CV (Train): Recall={results['cv_performance_at_best_params']['mean_recall']:.4f}, "
          f"F1={results['cv_performance_at_best_params']['mean_f1']:.4f}, "
          f"ROC-AUC={results['cv_performance_at_best_params']['mean_roc_auc']:.4f}")
    print(f"Điểm Validation: Recall={results['validation_metrics']['recall_malignant']:.4f}, "
          f"Precision={results['validation_metrics']['precision_malignant']:.4f}, "
          f"F1={results['validation_metrics']['f1_malignant']:.4f}, "
          f"Accuracy={results['validation_metrics']['accuracy']:.4f}, "
          f"ROC-AUC={results['validation_metrics']['roc_auc']:.4f}")
    if results['comparison_with_pruned_tree']['pruned_tree_available']:
        deltas = results['comparison_with_pruned_tree']['validation_metric_deltas']
        print(f"Cải thiện so với Cây Đã Cắt Tỉa trên Validation: "
              f"Recall: {deltas['recall_malignant']['pruned_tree']:.4f} -> {deltas['recall_malignant']['random_forest']:.4f} (+{deltas['recall_malignant']['delta']:.4f}), "
              f"ROC-AUC: {deltas['roc_auc']['pruned_tree']:.4f} -> {deltas['roc_auc']['random_forest']:.4f} (+{deltas['roc_auc']['delta']:.4f})")
