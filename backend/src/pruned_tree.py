"""
Module Huấn luyện, Cắt Tỉa và Đánh Giá Cây Quyết Định (Decision Tree Pruning).
Nhiệm vụ 10: Xây dựng Decision Tree có kiểm soát độ phức tạp (Pre-pruning & Post-pruning).

Các khía cạnh kỹ thuật cốt lõi:
1. Cơ chế Cost-Complexity Pruning (CCP - Minimal Cost-Complexity Pruning):
   Hàm mục tiêu tối thiểu hóa:
       R_alpha(T) = R(T) + alpha * |T|
   Trong đó:
   - R(T): Tổng độ vẩn đục (Impurity / Misclassification error) của toàn bộ cây T trên tập huấn luyện.
   - |T|: Số lượng nút lá (terminal leaves) đại diện cho độ phức tạp cấu trúc của cây.
   - alpha >= 0: Tham số phạt độ phức tạp (complexity parameter). Khi alpha = 0, cây phát triển tối đa (unpruned).
     Khi alpha tăng, hình phạt cho số lượng lá tăng lên, buộc các nhánh con ít cải thiện độ thuần phải bị tỉa bớt.

2. Vai trò của các siêu tham số:
   - max_depth (Pre-pruning): Giới hạn chiều sâu tối đa từ nút gốc tới nút lá xa nhất. Ngăn ngừa cây phát triển
     các tầng điều kiện quá sâu và chi tiết, kiểm soát thời gian suy luận và nguy cơ overfitting sớm.
   - min_samples_leaf (Pre-pruning): Quy định số lượng mẫu tối thiểu bắt buộc phải có trong mỗi nút lá.
     Ngăn cây tạo ra các nút lá đơn độc (1-2 mẫu) chỉ để cô lập các điểm ngoại lai cục bộ.
   - ccp_alpha (Post-pruning): Thuật toán tỉa sau thông minh. Cho phép cây mọc tự do để nắm bắt các tương tác phi tuyến,
     sau đó tính toán dãy alpha hiệu dụng (effective alphas) thông qua `cost_complexity_pruning_path`,
     rồi dùng Cross-Validation để cắt bỏ các nhánh yếu.

3. Nguyên tắc Đánh giá và Chọn mô hình:
   - Stratified 5-Fold Cross-Validation CHỈ TRÊN TẬP TRAIN (398 mẫu).
   - Tuyệt đối không chạm vào tập Test (86 mẫu đóng băng).
   - Tập Validation (85 mẫu) chỉ dùng để so sánh độc lập sau khi đã chọn xong best_params qua CV.
   - Ưu tiên hàng đầu: Recall Malignant (độ nhạy lâm sàng không bỏ sót bệnh), kết hợp cân đối Precision và F1-Score.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
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

PRUNED_MODEL_PATH = MODELS_DIR / "dt_pruned.joblib"
PRUNING_RESULTS_PATH = REPORTS_DIR / "pruning_search_results.json"
PRUNED_TREE_FIGURE_PATH = FIGURES_DIR / "pruned_tree_visualization.png"
CCP_PATH_FIGURE_PATH = FIGURES_DIR / "pruning_ccp_path.png"
UNPRUNED_RESULTS_PATH = REPORTS_DIR / "unpruned_tree_results.json"


def compute_pruning_path(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = RANDOM_STATE,
) -> Tuple[np.ndarray, np.ndarray, List[int], List[int]]:
    """
    Tính toán cost_complexity_pruning_path trên tập Train để sinh tập alpha ứng viên phù hợp.
    Đồng thời mô phỏng số nút và độ sâu tương ứng của cây theo từng mức alpha.
    """
    logger.info("Đang tính toán cost_complexity_pruning_path trên dữ liệu Train...")
    clf_base = DecisionTreeClassifier(random_state=random_state)
    path = clf_base.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities

    node_counts = []
    depths = []
    for alpha in ccp_alphas:
        tree = DecisionTreeClassifier(random_state=random_state, ccp_alpha=alpha)
        tree.fit(X_train, y_train)
        node_counts.append(int(tree.tree_.node_count))
        depths.append(int(tree.get_depth()))

    logger.info(f"Đã sinh {len(ccp_alphas)} giá trị alpha hiệu dụng từ {ccp_alphas[0]:.6f} đến {ccp_alphas[-1]:.6f}")
    return ccp_alphas, impurities, node_counts, depths


def plot_ccp_path(
    ccp_alphas: np.ndarray,
    impurities: np.ndarray,
    node_counts: List[int],
    depths: List[int],
    save_path: Path = CCP_PATH_FIGURE_PATH,
) -> None:
    """
    Trực quan hóa sự biến thiên của Impurity và độ phức tạp cấu trúc cây theo ccp_alpha.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

    # Đồ thị 1: Alpha vs Impurity (Độ vẩn đục)
    ax1.plot(ccp_alphas[:-1], impurities[:-1], marker="o", drawstyle="steps-post", color="#1f77b4", linewidth=2)
    ax1.set_xlabel("Effective ccp_alpha", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Total Leaf Impurity", fontsize=12, fontweight="bold")
    ax1.set_title("Alpha vs Total Impurity trên Tập Huấn Luyện", fontsize=13, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Đồ thị 2: Alpha vs Số nút và Chiều sâu
    ax2.plot(ccp_alphas[:-1], node_counts[:-1], marker="s", drawstyle="steps-post", color="#e6550d", label="Tổng số nút (Nodes)", linewidth=2)
    ax2.plot(ccp_alphas[:-1], depths[:-1], marker="^", drawstyle="steps-post", color="#31a354", label="Độ sâu cây (Max Depth)", linewidth=2)
    ax2.set_xlabel("Effective ccp_alpha", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Độ phức tạp hình học", fontsize=12, fontweight="bold")
    ax2.set_title("Alpha vs Cấu Trúc Cây (Số Nút & Chiều Sâu)", fontsize=13, fontweight="bold")
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.suptitle("Khảo Sát Cost-Complexity Pruning Path (Train Set N=398)", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ khảo sát CCP path vào: {save_path}")


def run_pruning_grid_search(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    ccp_alphas: np.ndarray,
    cv_splits: int = 5,
    random_state: int = RANDOM_STATE,
) -> Tuple[Dict[str, Any], DecisionTreeClassifier, pd.DataFrame]:
    """
    Sử dụng GridSearchCV với 5-Fold Stratified CV trên tập Train để dò tìm bộ siêu tham số tối ưu.
    Bộ tham số bao gồm ccp_alpha, max_depth, và min_samples_leaf.
    Tiêu chí lựa chọn: Ưu tiên Recall Malignant tối đa, kết hợp cân đối F1-score và độ tinh gọn mô hình.
    """
    logger.info("Đang khởi tạo lưới siêu tham số (GridSearchCV) có kiểm soát độ phức tạp...")
    
    # Lấy các alpha không tầm thường (loại bỏ alpha cuối cùng vì cắt tỉa toàn bộ cây thành 1 nút gốc duy nhất)
    valid_alphas = [float(a) for a in ccp_alphas[:-1]]

    param_grid = {
        "ccp_alpha": valid_alphas,
        "max_depth": [3, 4, 5, 6, 7, 8, None],
        "min_samples_leaf": [1, 2, 4, 6],
    }

    skf = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=random_state)
    scoring = {
        "recall": "recall",
        "precision": "precision",
        "f1": "f1",
        "accuracy": "accuracy",
    }

    grid_search = GridSearchCV(
        estimator=DecisionTreeClassifier(criterion="gini", random_state=random_state),
        param_grid=param_grid,
        scoring=scoring,
        refit="recall",
        cv=skf,
        n_jobs=-1,
        return_train_score=True,
    )

    logger.info(f"Bắt đầu huấn luyện Grid Search với {len(valid_alphas) * 7 * 4} = {len(valid_alphas)*28} tổ hợp tham số qua {cv_splits}-Fold CV...")
    grid_search.fit(X_train, y_train)

    cv_results_df = pd.DataFrame(grid_search.cv_results_)

    # Chiến lược lựa chọn mô hình tối ưu theo yêu cầu y học:
    # 1. Ưu tiên hàng đầu: Recall Malignant trung bình CV cao nhất (giảm tối đa False Negative).
    # 2. Tiêu chí phụ 1: F1-score trung bình CV cao nhất (cân bằng hài hòa).
    # 3. Tiêu chí phụ 2: Precision trung bình CV cao nhất.
    # 4. Tiêu chí phụ 3: ccp_alpha lớn hơn (Nguyên lý Occam's Razor - chọn cây được cắt tỉa gọn gàng hơn khi điểm tương đương).
    cv_sorted = cv_results_df.sort_values(
        by=["mean_test_recall", "mean_test_f1", "mean_test_precision", "param_ccp_alpha"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)

    best_row = cv_sorted.iloc[0]
    best_params = {
        "ccp_alpha": float(best_row["param_ccp_alpha"]),
        "max_depth": None if pd.isna(best_row["param_max_depth"]) else int(best_row["param_max_depth"]),
        "min_samples_leaf": int(best_row["param_min_samples_leaf"]),
    }

    logger.info(f"Bộ tham số tối ưu lựa chọn: {best_params}")
    logger.info(
        f"Điểm CV trung bình tại best_params: "
        f"Recall={best_row['mean_test_recall']:.4f} (±{best_row['std_test_recall']:.4f}), "
        f"F1={best_row['mean_test_f1']:.4f}, "
        f"Precision={best_row['mean_test_precision']:.4f}, "
        f"Accuracy={best_row['mean_test_accuracy']:.4f}"
    )

    # Huấn luyện mô hình tối ưu trên toàn bộ tập Train (N=398)
    best_pruned_tree = DecisionTreeClassifier(
        criterion="gini",
        max_depth=best_params["max_depth"],
        min_samples_leaf=best_params["min_samples_leaf"],
        ccp_alpha=best_params["ccp_alpha"],
        random_state=random_state,
    )
    best_pruned_tree.fit(X_train, y_train)

    return best_params, best_pruned_tree, cv_sorted


def evaluate_pruned_tree(
    model: DecisionTreeClassifier,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> Dict[str, Any]:
    """
    Đánh giá mô hình đã cắt tỉa trên tập Train và tập Validation.
    Lưu ý: Tập Test TUYỆT ĐỐI không được sử dụng ở bước này.
    """
    logger.info("Đang đánh giá Cây Quyết Định Đã Cắt Tỉa trên Train và Validation...")

    # Cấu trúc hình học cây
    actual_depth = int(model.get_depth())
    node_count = int(model.tree_.node_count)
    leaf_count = int(model.get_n_leaves())

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

    eval_results = {
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


def plot_pruned_tree(
    model: DecisionTreeClassifier,
    feature_names: List[str] = FEATURE_NAMES,
    save_path: Path = PRUNED_TREE_FIGURE_PATH,
) -> None:
    """
    Trực quan hóa cấu trúc Cây Quyết Định Đã Cắt Tỉa với độ phân giải cao và thẩm mỹ trực quan.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    depth = model.get_depth()
    n_leaves = model.get_n_leaves()

    fig, ax = plt.subplots(figsize=(24, 12), dpi=300)
    plot_tree(
        model,
        feature_names=feature_names,
        class_names=["Benign", "Malignant"],
        filled=True,
        rounded=True,
        proportion=False,
        fontsize=9,
        ax=ax,
    )

    plt.title(
        f"Trực quan hóa Cây Quyết Định Đã Cắt Tỉa (Pruned Decision Tree)\n"
        f"Tham số: ccp_alpha={model.ccp_alpha:.6f}, max_depth={depth}, min_samples_leaf={model.min_samples_leaf} "
        f"| Quy mô: {model.tree_.node_count} nút, {n_leaves} lá",
        fontsize=15,
        fontweight="bold",
        pad=15,
    )
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu hình ảnh trực quan hóa Cây Đã Cắt Tỉa vào: {save_path}")


def compare_with_unpruned(
    pruned_eval: Dict[str, Any],
    unpruned_path: Path = UNPRUNED_RESULTS_PATH,
) -> Dict[str, Any]:
    """
    So sánh toàn diện giữa Cây Chưa Cắt (Nhiệm vụ 08) và Cây Đã Cắt Tỉa (Nhiệm vụ 10).
    """
    comparison = {
        "unpruned_available": False,
        "structural_reduction": {},
        "metric_changes": {},
    }

    if not unpruned_path.exists():
        logger.warning(f"Không tìm thấy file kết quả cây chưa cắt tại: {unpruned_path}")
        return comparison

    with open(unpruned_path, "r", encoding="utf-8") as f:
        unpruned_data = json.load(f)

    comparison["unpruned_available"] = True
    u_struct = unpruned_data["tree_structure"]
    p_struct = pruned_eval["tree_structure"]

    nodes_diff = u_struct["total_nodes"] - p_struct["total_nodes"]
    nodes_reduction_pct = (nodes_diff / u_struct["total_nodes"]) * 100
    leaves_diff = u_struct["leaf_nodes"] - p_struct["leaf_nodes"]
    leaves_reduction_pct = (leaves_diff / u_struct["leaf_nodes"]) * 100
    depth_diff = u_struct["actual_depth"] - p_struct["actual_depth"]

    comparison["structural_reduction"] = {
        "unpruned_depth": u_struct["actual_depth"],
        "pruned_depth": p_struct["actual_depth"],
        "depth_reduction": depth_diff,
        "unpruned_nodes": u_struct["total_nodes"],
        "pruned_nodes": p_struct["total_nodes"],
        "nodes_reduced": nodes_diff,
        "nodes_reduction_pct": round(nodes_reduction_pct, 2),
        "unpruned_leaves": u_struct["leaf_nodes"],
        "pruned_leaves": p_struct["leaf_nodes"],
        "leaves_reduced": leaves_diff,
        "leaves_reduction_pct": round(leaves_reduction_pct, 2),
    }

    u_val = unpruned_data["validation_metrics"]
    p_val = pruned_eval["validation_metrics"]

    comparison["validation_comparison"] = {
        "accuracy": {
            "unpruned": u_val["accuracy"],
            "pruned": p_val["accuracy"],
            "delta": round(p_val["accuracy"] - u_val["accuracy"], 4),
        },
        "precision_malignant": {
            "unpruned": u_val["precision_malignant"],
            "pruned": p_val["precision_malignant"],
            "delta": round(p_val["precision_malignant"] - u_val["precision_malignant"], 4),
        },
        "recall_malignant": {
            "unpruned": u_val["recall_malignant"],
            "pruned": p_val["recall_malignant"],
            "delta": round(p_val["recall_malignant"] - u_val["recall_malignant"], 4),
        },
        "f1_malignant": {
            "unpruned": u_val["f1_malignant"],
            "pruned": p_val["f1_malignant"],
            "delta": round(p_val["f1_malignant"] - u_val["f1_malignant"], 4),
        },
        "confusion_matrix_change": {
            "unpruned_fn": u_val["confusion_matrix"]["fn"],
            "pruned_fn": p_val["confusion_matrix"]["fn"],
            "unpruned_fp": u_val["confusion_matrix"]["fp"],
            "pruned_fp": p_val["confusion_matrix"]["fp"],
        },
    }

    return comparison


def run_decision_tree_pruning_pipeline(
    save_model: bool = True,
    save_results: bool = True,
    save_figures: bool = True,
) -> Dict[str, Any]:
    """
    Thực thi toàn bộ quy trình cắt tỉa Decision Tree:
    1. Tải dữ liệu Train và Validation (Tập Test giữ nguyên).
    2. Sinh tập alpha ứng viên qua cost_complexity_pruning_path.
    3. Vẽ biểu đồ biến thiên CCP path.
    4. Chạy GridSearchCV qua 5-Fold Stratified CV trên Train.
    5. Đánh giá mô hình đã tỉa trên Train và Validation.
    6. Trực quan hóa cây đã tỉa.
    7. So sánh với Cây Chưa Tỉa.
    8. Lưu artifact mô hình và toàn bộ kết quả tìm kiếm ra JSON.
    """
    logger.info("=== BẮT ĐẦU NHIỆM VỤ 10: DECISION TREE PRUNING ===")

    # 1. Nạp dữ liệu
    (X_train, y_train), (X_val, y_val), _ = load_split_data()

    # 2. Sinh tập alpha ứng viên từ cost_complexity_pruning_path
    ccp_alphas, impurities, node_counts, depths = compute_pruning_path(X_train, y_train)

    # 3. Vẽ biểu đồ CCP Path
    if save_figures:
        plot_ccp_path(ccp_alphas, impurities, node_counts, depths)

    # 4. Tìm kiếm tham số qua GridSearchCV
    best_params, best_pruned_tree, cv_sorted = run_pruning_grid_search(
        X_train=X_train,
        y_train=y_train,
        ccp_alphas=ccp_alphas,
        cv_splits=5,
    )

    # 5. Đánh giá mô hình đã tỉa
    eval_results = evaluate_pruned_tree(
        model=best_pruned_tree,
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
    )

    # 6. Trực quan hóa cây đã tỉa
    if save_figures:
        plot_pruned_tree(best_pruned_tree)

    # 7. So sánh với Cây Chưa Tỉa
    comparison = compare_with_unpruned(eval_results)

    # 8. Chuẩn bị top 10 cấu hình trong Grid Search
    top_candidates = []
    top_rows = cv_sorted.head(10)
    for _, row in top_rows.iterrows():
        top_candidates.append({
            "ccp_alpha": float(row["param_ccp_alpha"]),
            "max_depth": None if pd.isna(row["param_max_depth"]) else int(row["param_max_depth"]),
            "min_samples_leaf": int(row["param_min_samples_leaf"]),
            "cv_mean_recall": round(float(row["mean_test_recall"]), 4),
            "cv_std_recall": round(float(row["std_test_recall"]), 4),
            "cv_mean_precision": round(float(row["mean_test_precision"]), 4),
            "cv_mean_f1": round(float(row["mean_test_f1"]), 4),
            "cv_mean_accuracy": round(float(row["mean_test_accuracy"]), 4),
        })

    # Đóng gói toàn bộ kết quả nghiên cứu
    final_output = {
        "pipeline_name": "DecisionTreeClassifier_Cost_Complexity_Pruning",
        "random_state": RANDOM_STATE,
        "candidate_alphas_count": len(ccp_alphas),
        "effective_alphas_list": [round(float(a), 6) for a in ccp_alphas.tolist()],
        "best_params": best_params,
        "cv_performance_at_best_params": {
            "mean_recall": float(cv_sorted.iloc[0]["mean_test_recall"]),
            "std_recall": float(cv_sorted.iloc[0]["std_test_recall"]),
            "mean_f1": float(cv_sorted.iloc[0]["mean_test_f1"]),
            "mean_precision": float(cv_sorted.iloc[0]["mean_test_precision"]),
            "mean_accuracy": float(cv_sorted.iloc[0]["mean_test_accuracy"]),
        },
        "top_10_parameter_combinations": top_candidates,
        "tree_structure": eval_results["tree_structure"],
        "train_metrics": eval_results["train_metrics"],
        "validation_metrics": eval_results["validation_metrics"],
        "generalization_gap": eval_results["generalization_gap"],
        "comparison_with_unpruned": comparison,
    }

    # 9. Lưu Model Artifacts và Kết Quả JSON
    if save_model:
        PRUNED_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_pruned_tree, PRUNED_MODEL_PATH)
        logger.info(f"Đã lưu mô hình đã cắt tỉa vào: {PRUNED_MODEL_PATH}")

    if save_results:
        PRUNING_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PRUNING_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        logger.info(f"Đã lưu toàn bộ kết quả tìm kiếm vào: {PRUNING_RESULTS_PATH}")

    return final_output


if __name__ == "__main__":
    results = run_decision_tree_pruning_pipeline()
    print("\n=== TỔNG HỢP KẾT QUẢ NHIỆM VỤ 10: DECISION TREE PRUNING ===")
    print(f"Best Params: {results['best_params']}")
    print(f"Cấu trúc cây đã tỉa: Độ sâu={results['tree_structure']['actual_depth']}, "
          f"Số nút={results['tree_structure']['total_nodes']}, "
          f"Số lá={results['tree_structure']['leaf_nodes']}")
    print(f"Điểm CV (Train): Recall={results['cv_performance_at_best_params']['mean_recall']:.4f}, "
          f"F1={results['cv_performance_at_best_params']['mean_f1']:.4f}")
    print(f"Điểm Validation: Recall={results['validation_metrics']['recall_malignant']:.4f}, "
          f"Precision={results['validation_metrics']['precision_malignant']:.4f}, "
          f"F1={results['validation_metrics']['f1_malignant']:.4f}, "
          f"Accuracy={results['validation_metrics']['accuracy']:.4f}")
    if results['comparison_with_unpruned']['unpruned_available']:
        red = results['comparison_with_unpruned']['structural_reduction']
        print(f"Mức độ giảm độ phức tạp so với cây chưa tỉa: "
              f"Nút: {red['unpruned_nodes']} -> {red['pruned_nodes']} (-{red['nodes_reduction_pct']}%), "
              f"Lá: {red['unpruned_leaves']} -> {red['pruned_leaves']} (-{red['leaves_reduction_pct']}%)")
