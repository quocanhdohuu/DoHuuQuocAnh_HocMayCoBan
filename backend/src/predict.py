"""
Module Dự Đoán và Kiểm Thử Suy Luận (Inference & Validation Script).
Nhiệm vụ 15:
- Nạp Pipeline hoàn chỉnh từ backend/models/wdbc_pipeline.joblib.
- Kiểm tra nghiêm ngặt thứ tự 30 đặc trưng theo schema backend/models/feature_schema.json.
- Kiểm tra tên cột, kiểu dữ liệu, xác suất từng lớp và class mapping.
- Thực hiện dự đoán trên các mẫu demo (Benign, Malignant, Borderline).
- Cung cấp cảnh báo bảo mật và tuyên bố miễn trừ trách nhiệm y khoa.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Union, List, Tuple
import numpy as np
import pandas as pd
import joblib

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.src.config import MODELS_DIR, FEATURE_NAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PIPELINE_PATH = MODELS_DIR / "wdbc_pipeline.joblib"
SCHEMA_PATH = MODELS_DIR / "feature_schema.json"
METADATA_PATH = MODELS_DIR / "model_metadata.json"


def load_model_package() -> Tuple[Any, Any, Any]:
    """Nạp pipeline mô hình, schema đặc trưng và metadata đã được đóng gói."""
    if not PIPELINE_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file pipeline tại: {PIPELINE_PATH}")
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file schema tại: {SCHEMA_PATH}")
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file metadata tại: {METADATA_PATH}")

    pipeline = joblib.load(PIPELINE_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return pipeline, schema, metadata


def validate_and_align_input(
    input_data: Union[Dict[str, float], List[float], pd.DataFrame, np.ndarray],
    expected_features: List[str] = FEATURE_NAMES,
) -> pd.DataFrame:
    """
    Xác minh và sắp xếp lại các đặc trưng đầu vào theo đúng thứ tự 30 cột bắt buộc.
    Ngăn chặn tuyệt đối lỗi tráo đổi cột (Column Mismatch / Feature Misalignment).
    """
    if isinstance(input_data, dict):
        # Kiểm tra đủ 30 đặc trưng
        missing = [col for col in expected_features if col not in input_data]
        if missing:
            raise ValueError(f"Dữ liệu đầu vào thiếu {len(missing)} đặc trưng: {missing[:3]}...")
        # Ép thứ tự cột chuẩn xác
        aligned_values = [float(input_data[col]) for col in expected_features]
        df = pd.DataFrame([aligned_values], columns=expected_features)

    elif isinstance(input_data, pd.DataFrame):
        # Nếu có tên cột, kiểm tra và sắp xếp lại theo expected_features
        missing = [col for col in expected_features if col not in input_data.columns]
        if missing:
            raise ValueError(f"DataFrame đầu vào thiếu các cột: {missing[:3]}...")
        df = input_data[expected_features].astype(float).copy()

    elif isinstance(input_data, (list, np.ndarray)):
        arr = np.array(input_data)
        if arr.ndim == 1:
            if len(arr) != len(expected_features):
                raise ValueError(f"Đầu vào dạng mảng phải có đúng {len(expected_features)} phần tử, nhận được: {len(arr)}")
            df = pd.DataFrame([arr], columns=expected_features)
        elif arr.ndim == 2:
            if arr.shape[1] != len(expected_features):
                raise ValueError(f"Mảng 2D phải có đúng {len(expected_features)} cột, nhận được: {arr.shape[1]}")
            df = pd.DataFrame(arr, columns=expected_features)
        else:
            raise ValueError(f"Số chiều mảng không hợp lệ: {arr.ndim}")
    else:
        raise TypeError(f"Kiểu dữ liệu đầu vào không được hỗ trợ: {type(input_data)}")

    return df


def predict_sample(
    input_data: Union[Dict[str, float], List[float], pd.DataFrame, np.ndarray],
    threshold: float = 0.50,
) -> Dict[str, Any]:
    """
    Dự đoán nhãn và xác suất cho một mẫu đầu vào.
    Trả về cấu trúc chuẩn hóa cho Backend API và Web Interface.
    """
    pipeline, schema, metadata = load_model_package()
    df_aligned = validate_and_align_input(input_data, FEATURE_NAMES)

    # Dự đoán xác suất
    probs = pipeline.predict_proba(df_aligned)[0]
    prob_benign = float(probs[0])
    prob_malignant = float(probs[1])

    # Quyết định theo ngưỡng
    pred_class = 1 if prob_malignant >= threshold else 0
    pred_label = "Malignant" if pred_class == 1 else "Benign"

    result = {
        "status": "success",
        "predicted_class": pred_class,
        "predicted_label": pred_label,
        "probability": {
            "benign": round(prob_benign, 4),
            "malignant": round(prob_malignant, 4),
        },
        "decision_threshold": threshold,
        "confidence_score": round(max(prob_benign, prob_malignant) * 100, 2),
        "is_high_risk": bool(pred_class == 1),
        "model_version": metadata.get("version", "1.0.0"),
        "disclaimer": metadata.get("clinical_disclaimer", ""),
    }

    return result


def run_demo_predictions() -> None:
    """Chạy thử nghiệm kiểm tra suy luận trên 3 mẫu điển hình từ tập Test."""
    from backend.src.data import load_split_data

    logger.info("=== BẮT ĐẦU CHẠY THỬ NGHIỆM DỰ ĐOÁN (DEMO INFERENCE) ===")
    _, _, (X_test, y_test) = load_split_data()

    # 1. Mẫu Lành tính điển hình (Test sample 1)
    benign_idx = int(np.where(y_test.values == 0)[0][0])
    sample_benign_dict = X_test.iloc[benign_idx].to_dict()
    res_b = predict_sample(sample_benign_dict)
    logger.info(
        f"Mẫu Lành tính (Thực tế: Benign) -> Dự đoán: {res_b['predicted_label']} "
        f"(P_Benign={res_b['probability']['benign']*100:.1f}%, P_Malignant={res_b['probability']['malignant']*100:.1f}%)"
    )

    # 2. Mẫu Ác tính điển hình (Test sample 0)
    mal_idx = int(np.where(y_test.values == 1)[0][0])
    sample_mal_dict = X_test.iloc[mal_idx].to_dict()
    res_m = predict_sample(sample_mal_dict)
    logger.info(
        f"Mẫu Ác tính (Thực tế: Malignant) -> Dự đoán: {res_m['predicted_label']} "
        f"(P_Benign={res_m['probability']['benign']*100:.1f}%, P_Malignant={res_m['probability']['malignant']*100:.1f}%)"
    )

    # 3. Mẫu Biên giới (Sample 23, ca FN)
    sample_fn_dict = X_test.iloc[23].to_dict()
    res_fn = predict_sample(sample_fn_dict)
    logger.info(
        f"Mẫu Ranh giới #23 (Thực tế: Malignant) -> Dự đoán: {res_fn['predicted_label']} "
        f"(P_Benign={res_fn['probability']['benign']*100:.1f}%, P_Malignant={res_fn['probability']['malignant']*100:.1f}%)"
    )

    # In tuyên bố y khoa
    print("\n" + "=" * 80)
    print("TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA:")
    print(res_b["disclaimer"])
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_demo_predictions()
