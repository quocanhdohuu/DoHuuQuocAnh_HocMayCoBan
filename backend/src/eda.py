"""
Module Phân tích Khám phá Dữ liệu (Exploratory Data Analysis - EDA).
CHỈ SỬ DỤNG TẬP HUẤN LUYỆN (Train Set - data/train.csv) để đảm bảo không rò rỉ dữ liệu (Zero Data Leakage).
Xuất các bảng thống kê và biểu đồ trực quan hóa độ phân giải cao vào reports/figures/.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import (
    TRAIN_DATA_PATH,
    FIGURES_DIR,
    FEATURE_NAMES,
    TARGET_COLUMN,
    POSITIVE_CLASS,
    NEGATIVE_CLASS,
)

# Cấu hình phong cách biểu đồ học thuật
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8
sns.set_theme(style="whitegrid", palette="muted")

# Bảng màu chuẩn: Benign (Xanh lam / #2b5c8f), Malignant (Đỏ cam / #d95f02)
COLOR_PALETTE = {NEGATIVE_CLASS: "#2b5c8f", POSITIVE_CLASS: "#d95f02"}
LABEL_NAMES = {NEGATIVE_CLASS: "Lành tính (Benign - B)", POSITIVE_CLASS: "Ác tính (Malignant - M)"}


def load_train_data() -> pd.DataFrame:
    """Đọc dữ liệu tập Train độc lập."""
    if not TRAIN_DATA_PATH.exists():
        raise FileNotFoundError(f"Chưa tìm thấy tập Train tại {TRAIN_DATA_PATH}. Hãy chạy data.py trước!")
    df_train = pd.read_csv(TRAIN_DATA_PATH, index_col=0)
    return df_train


def generate_descriptive_stats(df_train: pd.DataFrame) -> pd.DataFrame:
    """Tính toán thống kê mô tả (min, max, mean, median, std, skewness) cho 30 đặc trưng."""
    stats_list = []
    for col in FEATURE_NAMES:
        series = df_train[col]
        stats_list.append({
            "Feature": col,
            "Mean": series.mean(),
            "Std": series.std(),
            "Min": series.min(),
            "Q1 (25%)": series.quantile(0.25),
            "Median (50%)": series.median(),
            "Q3 (75%)": series.quantile(0.75),
            "Max": series.max(),
            "Skewness": series.skew()
        })
    stats_df = pd.DataFrame(stats_list)
    return stats_df


def plot_target_distribution(df_train: pd.DataFrame, save_path: Path):
    """Vẽ biểu đồ phân bố nhãn mục tiêu (Bar chart + Pie chart)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    
    counts = df_train[TARGET_COLUMN].value_counts()
    percentages = df_train[TARGET_COLUMN].value_counts(normalize=True) * 100

    # 1. Bar Chart
    bars = ax1.bar(
        [LABEL_NAMES[c] for c in counts.index],
        counts.values,
        color=[COLOR_PALETTE[c] for c in counts.index],
        width=0.5,
        edgecolor="#222",
        linewidth=1.2
    )
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f"{int(yval)} ({yval/len(df_train)*100:.1f}%)",
                 ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax1.set_title("Phân bố số lượng mẫu theo Nhãn (Train Set, N=398)", fontsize=13, pad=12, fontweight="bold")
    ax1.set_ylabel("Số lượng mẫu bệnh phẩm", fontsize=11)
    ax1.set_ylim(0, max(counts.values) * 1.15)

    # 2. Donut Chart
    wedges, texts, autotexts = ax2.pie(
        counts.values,
        labels=[LABEL_NAMES[c] for c in counts.index],
        autopct="%1.1f%%",
        startangle=140,
        colors=[COLOR_PALETTE[c] for c in counts.index],
        wedgeprops=dict(width=0.45, edgecolor="#222", linewidth=1.2),
        pctdistance=0.75
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(11)
    ax2.set_title("Tỷ lệ phần trăm các lớp trong tập Train", fontsize=13, pad=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã lưu biểu đồ: {save_path.name}")


def plot_feature_histograms(df_train: pd.DataFrame, key_features: list, save_path: Path):
    """Vẽ Histogram phân bố tần suất kèm đường cong KDE cho các đặc trưng tiêu biểu."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 9), dpi=300)
    axes = axes.flatten()

    for idx, feature in enumerate(key_features):
        ax = axes[idx]
        for label, group in df_train.groupby(TARGET_COLUMN):
            sns.histplot(
                group[feature],
                kde=True,
                ax=ax,
                color=COLOR_PALETTE[label],
                label=LABEL_NAMES[label],
                stat="density",
                common_norm=False,
                bins=20,
                alpha=0.45,
                line_kws={"linewidth": 2}
            )
        ax.set_title(f"Phân bố: {feature}", fontsize=12, fontweight="bold")
        ax.set_xlabel(feature, fontsize=10)
        ax.set_ylabel("Mật độ xác suất (Density)", fontsize=10)
        ax.legend(loc="upper right", fontsize=8)

    plt.suptitle("Histogram và Đường cong Mật độ (KDE) của 6 Đặc trưng Tiêu biểu (Train Set)", fontsize=15, y=0.99, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã lưu biểu đồ: {save_path.name}")


def plot_feature_boxplots(df_train: pd.DataFrame, key_features: list, save_path: Path):
    """Vẽ Boxplot so sánh phân bố giữa lớp B và lớp M để quan sát ngoại lệ và độ phân tách."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 9), dpi=300)
    axes = axes.flatten()

    for idx, feature in enumerate(key_features):
        ax = axes[idx]
        sns.boxplot(
            data=df_train,
            x=TARGET_COLUMN,
            y=feature,
            hue=TARGET_COLUMN,
            palette=COLOR_PALETTE,
            legend=False,
            ax=ax,
            width=0.4,
            fliersize=4,
            linewidth=1.2
        )
        ax.set_title(f"Boxplot: {feature}", fontsize=12, fontweight="bold")
        ax.set_xticks([0, 1])
        ax.set_xticklabels([LABEL_NAMES["B"], LABEL_NAMES["M"]], fontsize=10)
        ax.set_xlabel("")
        ax.set_ylabel(feature, fontsize=10)

    plt.suptitle("Boxplot So sánh Phân bố Đặc trưng giữa Khối u Lành tính và Ác tính", fontsize=15, y=0.99, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã lưu biểu đồ: {save_path.name}")


def plot_correlation_heatmap(df_train: pd.DataFrame, save_path: Path):
    """Vẽ Ma trận Tương quan Heatmap cho 10 đặc trưng trung bình (_mean) và các đặc trưng _worst cốt lõi."""
    selected_cols = [
        "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
        "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
        "radius_worst", "perimeter_worst", "area_worst", "concave points_worst"
    ]
    corr_matrix = df_train[selected_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1.0,
        vmax=1.0,
        square=True,
        linewidths=0.6,
        cbar_kws={"shrink": 0.8, "label": "Hệ số tương quan Pearson (r)"},
        ax=ax,
        annot_kws={"size": 8}
    )
    ax.set_title("Ma trận Tương quan Pearson (Correlation Heatmap) trên Tập Train", fontsize=14, pad=15, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã lưu biểu đồ: {save_path.name}")


def plot_discriminative_features(df_train: pd.DataFrame, save_path: Path):
    """
    Vẽ Biểu đồ Tán xạ (Scatter plot) kết hợp Marginal KDE giữa hai đặc trưng phân biệt mạnh nhất:
    'concave points_worst' và 'perimeter_worst'.
    """
    feat_x = "concave points_worst"
    feat_y = "perimeter_worst"

    g = sns.JointGrid(data=df_train, x=feat_x, y=feat_y, hue=TARGET_COLUMN, palette=COLOR_PALETTE, height=8, ratio=4)
    g.plot_joint(sns.scatterplot, s=55, alpha=0.8, edgecolor="#222", linewidth=0.7)
    g.plot_marginals(sns.kdeplot, fill=True, common_norm=False, alpha=0.45)

    g.ax_joint.set_xlabel(f"{feat_x} (Số lượng điểm lõm cực đại)", fontsize=12, fontweight="bold")
    g.ax_joint.set_ylabel(f"{feat_y} (Chu vi cực đại nhân tế bào - μm)", fontsize=12, fontweight="bold")
    g.ax_joint.legend(title="Nhãn chẩn đoán", labels=[LABEL_NAMES["B"], LABEL_NAMES["M"]], loc="upper left", fontsize=10)

    # Thêm ngưỡng phân chia tiềm năng trực quan (minh họa cách Decision Tree cắt không gian)
    g.ax_joint.axvline(x=0.135, color="black", linestyle="--", linewidth=1.5, label="Ngưỡng phân chia gợi ý (x=0.135)")
    g.ax_joint.axhline(y=105.0, color="gray", linestyle=":", linewidth=1.5, label="Ngưỡng chu vi gợi ý (y=105.0)")

    plt.suptitle("Không gian Phân tách giữa 2 Đặc trưng Cốt lõi: concave points_worst vs perimeter_worst", fontsize=13, y=1.02, fontweight="bold")
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"-> Đã lưu biểu đồ: {save_path.name}")


def run_eda_pipeline():
    """Hàm điều phối toàn bộ quy trình EDA trên tập Train."""
    print("=" * 65)
    print("BẮT ĐẦU QUY TRÌNH EDA (CHỈ TRÊN TẬP TRAIN - ZERO LEAKAGE)")
    print("=" * 65)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df_train = load_train_data()
    print(f"1. Đã nạp tập Train: {len(df_train)} mẫu, {len(df_train.columns)} cột.")

    # 1. Thống kê mô tả
    stats_df = generate_descriptive_stats(df_train)
    print("\n2. Bảng Thống kê mô tả (Top 5 đặc trưng tiêu biểu):")
    print(stats_df.head(5)[["Feature", "Mean", "Std", "Min", "Median (50%)", "Max"]].to_string(index=False))

    # 2. Danh sách 6 đặc trưng tiêu biểu
    key_features = [
        "radius_mean", "texture_mean", "area_mean",
        "concave points_mean", "perimeter_worst", "concave points_worst"
    ]

    # 3. Sinh các biểu đồ chất lượng cao
    print("\n3. Đang tạo các biểu đồ trực quan hóa...")
    plot_target_distribution(df_train, FIGURES_DIR / "eda_target_distribution.png")
    plot_feature_histograms(df_train, key_features, FIGURES_DIR / "eda_feature_histograms.png")
    plot_feature_boxplots(df_train, key_features, FIGURES_DIR / "eda_feature_boxplots.png")
    plot_correlation_heatmap(df_train, FIGURES_DIR / "eda_correlation_heatmap.png")
    plot_discriminative_features(df_train, FIGURES_DIR / "eda_discriminative_features.png")

    print("\nHOÀN THÀNH TOÀN BỘ QUY TRÌNH EDA!")
    print(f"Tất cả biểu đồ đã được lưu trữ tại: {FIGURES_DIR}")
    print("=" * 65)


if __name__ == "__main__":
    run_eda_pipeline()
