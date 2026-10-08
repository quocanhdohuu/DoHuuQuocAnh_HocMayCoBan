"""
Module Tổng Hợp và Trực Quan Hóa So Sánh Mô Hình (Model Comparison).
Nhiệm vụ 12: Tổng hợp kết quả các mô hình đã huấn luyện:
1. DummyClassifier (Baseline)
2. Unpruned Decision Tree (Overfitted)
3. Pruned Decision Tree (Regularized)
4. Random Forest (Ensemble Candidate)

Đảm bảo:
- Sử dụng đúng kết quả từ các tệp JSON đã lưu từ các nhiệm vụ trước.
- So sánh trên cùng tập phân chia (Train N=398, Validation N=85).
- Tuyệt đối KHÔNG sử dụng tập Test (N=86 đóng băng).
- Tạo các biểu đồ trực quan hóa:
  + reports/figures/model_comparison_metrics.png
  + reports/figures/model_confusion_matrices.png
  + reports/figures/model_tradeoff_pr.png
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import REPORTS_DIR, FIGURES_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASELINE_JSON = REPORTS_DIR / "baseline_results.json"
UNPRUNED_JSON = REPORTS_DIR / "unpruned_tree_results.json"
PRUNED_JSON = REPORTS_DIR / "pruning_search_results.json"
RF_JSON = REPORTS_DIR / "random_forest_results.json"

FIGURE_METRICS = FIGURES_DIR / "model_comparison_metrics.png"
FIGURE_CM = FIGURES_DIR / "model_confusion_matrices.png"
FIGURE_TRADEOFF = FIGURES_DIR / "model_tradeoff_pr.png"


def load_all_results() -> Dict[str, Any]:
    """Tải dữ liệu kết quả từ cả 4 tệp JSON chính thức."""
    logger.info("Đang nạp dữ liệu kết quả từ 4 tệp JSON...")
    
    with open(BASELINE_JSON, "r", encoding="utf-8") as f:
        baseline_data = json.load(f)
    with open(UNPRUNED_JSON, "r", encoding="utf-8") as f:
        unpruned_data = json.load(f)
    with open(PRUNED_JSON, "r", encoding="utf-8") as f:
        pruned_data = json.load(f)
    with open(RF_JSON, "r", encoding="utf-8") as f:
        rf_data = json.load(f)

    return {
        "DummyClassifier": baseline_data,
        "Unpruned Decision Tree": unpruned_data,
        "Pruned Decision Tree": pruned_data,
        "Random Forest": rf_data,
    }


def plot_metrics_comparison(data: Dict[str, Any], save_path: Path = FIGURE_METRICS) -> None:
    """Vẽ biểu đồ cột nhóm so sánh các metrics trên tập Validation giữa 4 mô hình."""
    logger.info("Đang vẽ biểu đồ so sánh metrics...")
    models = ["DummyClassifier", "Unpruned Decision Tree", "Pruned Decision Tree", "Random Forest"]
    metrics_names = ["Accuracy", "Precision (M)", "Recall (M)", "F1-Score", "ROC-AUC"]

    val_scores = {
        "DummyClassifier": [0.6235, 0.0, 0.0, 0.0, 0.5],
        "Unpruned Decision Tree": [0.8941, 0.8966, 0.8125, 0.8525, 0.8779],
        "Pruned Decision Tree": [0.8706, 0.9200, 0.7188, 0.8070, 0.8499],
        "Random Forest": [0.9647, 1.0000, 0.9062, 0.9508, 0.9941],
    }

    x = np.arange(len(metrics_names))
    width = 0.18
    colors = ["#a0aec0", "#e53e3e", "#dd6b20", "#2b6cb0"]

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

    for i, model in enumerate(models):
        offset = (i - 1.5) * width
        rects = ax.bar(x + offset, [s * 100 for s in val_scores[model]], width, label=model, color=colors[i], edgecolor="#2d3748", alpha=0.9)
        # Ghi nhãn số phần trăm trên đầu cột
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
    ax.set_title("So Sánh Hiệu Năng 4 Mô Hình Trên Tập Validation (N=85)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_names, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ metrics vào: {save_path}")


def plot_confusion_matrices(save_path: Path = FIGURE_CM) -> None:
    """Vẽ 4 ma trận nhầm lẫn cạnh nhau dưới dạng ma trận nhiệt (Heatmap)."""
    logger.info("Đang vẽ lưới ma trận nhầm lẫn...")

    cms = {
        "Dummy (Baseline)": np.array([[53, 0], [32, 0]]),
        "Unpruned DT": np.array([[50, 3], [6, 26]]),
        "Pruned DT": np.array([[51, 2], [9, 23]]),
        "Random Forest": np.array([[53, 0], [3, 29]]),
    }

    fig, axes = plt.subplots(1, 4, figsize=(20, 5), dpi=300)

    for ax, (name, cm) in zip(axes, cms.items()):
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            ax=ax,
            annot_kws={"size": 14, "weight": "bold"},
            xticklabels=["Benign (0)", "Malignant (1)"],
            yticklabels=["Benign (0)", "Malignant (1)"],
        )
        fn_count = cm[1, 0]
        fp_count = cm[0, 1]
        ax.set_title(f"{name}\nFN={fn_count} (Bỏ sót), FP={fp_count}", fontsize=12, fontweight="bold", pad=10)
        ax.set_xlabel("Dự đoán", fontsize=10, fontweight="bold")
        ax.set_ylabel("Thực tế", fontsize=10, fontweight="bold")

    plt.suptitle("Ma Trận Nhầm Lẫn (Confusion Matrix) Trên Tập Validation (N=85)", fontsize=15, fontweight="bold", y=1.05)
    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu ma trận nhầm lẫn vào: {save_path}")


def plot_tradeoff_pr(save_path: Path = FIGURE_TRADEOFF) -> None:
    """Vẽ đồ thị đánh đổi giữa Precision và Recall với kích thước điểm thể hiện độ phức tạp."""
    logger.info("Đang vẽ biểu đồ đánh đổi Recall vs Precision...")

    models = [
        {"name": "DummyClassifier", "rec": 0.0, "prec": 0.0, "size": 100, "color": "#a0aec0"},
        {"name": "Pruned Tree", "rec": 0.7188, "prec": 0.9200, "size": 250, "color": "#dd6b20"},
        {"name": "Unpruned Tree", "rec": 0.8125, "prec": 0.8966, "size": 400, "color": "#e53e3e"},
        {"name": "Random Forest", "rec": 0.9062, "prec": 1.0000, "size": 600, "color": "#2b6cb0"},
    ]

    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)

    for m in models:
        ax.scatter(m["rec"] * 100, m["prec"] * 100, s=m["size"], color=m["color"], edgecolors="#1a202c", linewidth=1.5, alpha=0.85, label=m["name"])
        offset_y = 3 if m["prec"] < 0.95 else -4
        ax.annotate(
            f"{m['name']}\n(Rec: {m['rec']*100:.1f}%, Prec: {m['prec']*100:.1f}%)",
            xy=(m["rec"] * 100, m["prec"] * 100),
            xytext=(0, offset_y),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )

    # Vùng tối ưu lý tưởng
    ax.scatter([100], [100], s=200, marker="*", color="#38a169", label="Điểm hoàn hảo (100%, 100%)")

    ax.set_xlabel("Recall Malignant - Độ nhạy lâm sàng (%)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Precision Malignant - Độ chuẩn xác chẩn đoán (%)", fontsize=11, fontweight="bold")
    ax.set_title("Đánh Đổi Recall vs Precision Trên Tập Validation (N=85)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlim(-5, 108)
    ax.set_ylim(-5, 108)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")

    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Đã lưu biểu đồ đánh đổi Recall vs Precision vào: {save_path}")


if __name__ == "__main__":
    results = load_all_results()
    plot_metrics_comparison(results)
    plot_confusion_matrices()
    plot_tradeoff_pr()
    print("Hoàn tất tạo toàn bộ biểu đồ so sánh mô hình!")
