"""
Ứng dụng Backend FastAPI - Project 16: Phân Loại Khối U Vú (WDBC).
Nhiệm vụ 16 & 17:
- Khởi tạo Backend FastAPI, nạp model một lần bằng Lifespan, kiểm tra health và CORS.
- Endpoint POST /api/demo-classify (và alias /api/predict) nhận chính xác 30 đặc trưng số.
- Pydantic schema validation: cấm thiếu/thừa feature, cấm NaN/Inf, cấm giá trị âm.
- Kiểm tra miền giá trị theo Train statistics, cảnh báo Out-Of-Distribution và từ chối giá trị cực đoan phi lý.
- Giải thích mô hình: đường dẫn phân nhánh cho Decision Tree, voting consensus + top features + giới hạn phương pháp cho Random Forest.
- Trả về nhãn B/M, tên lớp, xác suất đúng thứ tự và metadata.
"""

import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List, Union

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from fastapi import FastAPI, Response, status, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.src.config import MODELS_DIR, FEATURE_NAMES
from backend.app.schemas import (
    WDBCFeaturesInput,
    ClassifyWrappedRequest,
    ClassificationResponse,
    ProbabilitiesOutput,
    ModelInfoOutput,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("backend.app.main")

PIPELINE_PATH = MODELS_DIR / "wdbc_pipeline.joblib"
SCHEMA_PATH = MODELS_DIR / "feature_schema.json"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
REPORTS_DIR = ROOT_DIR / "reports"

# Cấu hình danh sách tên miền Frontend được phép gọi API (CORS)
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def verify_sha256(filepath: Path, expected_hash: str) -> bool:
    """Tính toán và so khớp mã băm SHA-256 của tệp."""
    if not filepath.exists() or not expected_hash:
        return False
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest().lower() == expected_hash.lower()


def check_feature_ranges(
    feature_dict: Dict[str, float],
    train_ranges: Dict[str, Dict[str, float]]
) -> List[str]:
    """
    Kiểm tra miền giá trị của mẫu so với phân phối tập huấn luyện (Train set).
    - Nếu giá trị vượt quá giới hạn vật lý tế bào khả dĩ (> 15 * max_train), ném ngoại lệ 422.
    - Nếu giá trị nằm ngoài dải quan sát [min_train, max_train], trả về danh sách cảnh báo OOD.
    - Không âm thầm thay thế giá trị (tuân thủ nghiêm ngặt yêu cầu thiết kế).
    """
    warnings = []
    for col, val in feature_dict.items():
        if col in train_ranges:
            t_min = train_ranges[col]["min"]
            t_max = train_ranges[col]["max"]

            # Ngưỡng vật lý cực đoan (Hard Limit)
            hard_max = max(t_max * 15.0, 100.0 if ("radius" in col or "perimeter" in col) else 10000.0)
            if val > hard_max:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        f"Đặc trưng '{col}' có giá trị {val} vượt quá giới hạn sinh học cực đoan "
                        f"(ngưỡng tối đa cho phép: {hard_max:.2f}). Vui lòng kiểm tra lại thiết bị đo."
                    )
                )

            if val < t_min:
                warnings.append(
                    f"Đặc trưng '{col}' = {val:.4f} < min_train ({t_min:.4f}). "
                    f"Mẫu nằm ngoài khoảng quan sát huấn luyện phía dưới (Out-Of-Distribution)."
                )
            elif val > t_max:
                warnings.append(
                    f"Đặc trưng '{col}' = {val:.4f} > max_train ({t_max:.4f}). "
                    f"Mẫu nằm ngoài khoảng quan sát huấn luyện phía trên (Out-Of-Distribution)."
                )
    return warnings


def extract_model_explanation(
    pipeline: Any,
    df_input: pd.DataFrame,
    feature_names: List[str]
) -> Dict[str, Any]:
    """
    Trích xuất giải thích dự đoán phù hợp với kiến trúc mô hình học máy:
    1. Nếu là Decision Tree: Trích xuất chính xác chuỗi điều kiện rẽ nhánh từng nút từ gốc tới lá.
    2. Nếu là Random Forest:
       - Thống kê chi tiết số phiếu bầu (Tree Voting Consensus) của 100 cây.
       - Trích xuất Top 5 đặc trưng quan trọng toàn cục (Global Feature Importance).
       - Tuyên bố rõ ràng GIỚI HẠN PHƯƠNG PHÁP: Quyết định là của toàn bộ ensemble 100 cây,
         tuyệt đối không mô tả một đường đi của cây đơn lẻ là quyết định của cả rừng.
    """
    classifier = pipeline
    if hasattr(pipeline, "named_steps"):
        classifier = pipeline.named_steps.get("classifier", pipeline.steps[-1][1])

    # 1. Trường hợp: DecisionTreeClassifier
    if isinstance(classifier, DecisionTreeClassifier):
        tree_ = classifier.tree_
        node_indicator = classifier.decision_path(df_input)
        leaf_id = classifier.apply(df_input)[0]
        node_indices = node_indicator.indices[node_indicator.indptr[0]:node_indicator.indptr[1]]

        path_steps = []
        for node_id in node_indices:
            if node_id == leaf_id:
                val_counts = tree_.value[node_id][0].tolist()
                path_steps.append({
                    "step": len(path_steps) + 1,
                    "node_id": int(node_id),
                    "is_leaf": True,
                    "condition": f"Kết thúc tại Nút lá #{node_id}",
                    "leaf_samples": int(tree_.n_node_samples[node_id]),
                    "leaf_class_distribution": {
                        "Benign": int(val_counts[0]) if len(val_counts) > 0 else 0,
                        "Malignant": int(val_counts[1]) if len(val_counts) > 1 else 0,
                    },
                    "decision": "Malignant (Ác tính)" if val_counts[1] > val_counts[0] else "Benign (Lành tính)"
                })
            else:
                f_idx = tree_.feature[node_id]
                f_name = feature_names[f_idx]
                thresh = float(tree_.threshold[node_id])
                val = float(df_input.iloc[0, f_idx])
                went_left = val <= thresh
                path_steps.append({
                    "step": len(path_steps) + 1,
                    "node_id": int(node_id),
                    "is_leaf": False,
                    "feature": f_name,
                    "threshold": round(thresh, 4),
                    "sample_value": round(val, 4),
                    "condition": f"{f_name} <= {thresh:.4f}" if went_left else f"{f_name} > {thresh:.4f}",
                    "branch_direction": "left (nhỏ hơn hoặc bằng)" if went_left else "right (lớn hơn)"
                })

        return {
            "model_type": "DecisionTreeClassifier",
            "explanation_method": "Decision Path (Chuỗi vết rẽ nhánh từ gốc đến lá)",
            "tree_depth": int(classifier.get_depth()),
            "path_length": len(path_steps),
            "decision_path": path_steps,
            "interpretation_note": "Mô hình Cây Quyết Định đơn lẻ cho phép suy luận nguyên nhân trực tiếp qua chuỗi điều kiện rẽ nhánh."
        }

    # 2. Trường hợp: RandomForestClassifier
    elif isinstance(classifier, RandomForestClassifier):
        total_trees = len(classifier.estimators_)
        tree_preds = [int(tree.predict(df_input.values)[0]) for tree in classifier.estimators_]
        votes_b = sum(1 for p in tree_preds if p == 0)
        votes_m = sum(1 for p in tree_preds if p == 1)

        importances = classifier.feature_importances_
        top_indices = np.argsort(importances)[::-1][:5]
        top_features = [
            {
                "rank": i + 1,
                "feature": feature_names[idx],
                "importance_score": round(float(importances[idx]), 4),
                "sample_value": round(float(df_input.iloc[0, idx]), 4),
            }
            for i, idx in enumerate(top_indices)
        ]

        return {
            "model_type": "RandomForestClassifier",
            "explanation_method": "Ensemble Voting & Global Feature Importance",
            "total_trees": total_trees,
            "votes_breakdown": {
                "benign_votes": votes_b,
                "malignant_votes": votes_m,
                "B": votes_b,
                "M": votes_m
            },
            "vote_percentage": {
                "Benign": round(votes_b / total_trees * 100, 2),
                "Malignant": round(votes_m / total_trees * 100, 2),
                "B": round(votes_b / total_trees * 100, 2),
                "M": round(votes_m / total_trees * 100, 2)
            },
            "top_influential_features": top_features,
            "aggregation_mechanism": "Soft-Voting (Trung bình cộng xác suất dự đoán qua 100 cây quyết định ngẫu nhiên)",
            "methodological_limitation": (
                "GIẢI THÍCH VÀ GIỚI HẠN PHƯƠNG PHÁP: Mô hình hiện tại là Random Forest gồm 100 cây quyết định độc lập. "
                "Quyết định phân loại là kết quả tổng hợp của TOÀN BỘ 100 CÂY thông qua cơ chế soft-voting. "
                "KHÔNG CÓ một đường đi rẽ nhánh đơn lẻ nào đại diện cho toàn bộ mô hình rừng. Mọi nỗ lực lấy đường "
                "đi của 1 cây đơn lẻ trong rừng để giải thích là SAI BẢN CHẤT thuật toán ensemble và gây hiểu nhầm lâm sàng."
            )
        }

    # 3. Mặc định
    else:
        return {
            "model_type": type(classifier).__name__,
            "explanation_method": "General Estimator",
            "note": "Mô hình không hỗ trợ trích xuất đường dẫn phân nhánh."
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan Context Manager:
    Nạp mô hình, schema, metadata và thống kê train MỘT LẦN DUY NHẤT khi server khởi động.
    Dọn dẹp tài nguyên khi server tắt.
    """
    logger.info("Đang khởi động FastAPI Backend (Project 16)...")
    app.state.model = None
    app.state.schema = None
    app.state.metadata = None
    app.state.train_ranges = {}
    app.state.model_loaded = False
    app.state.sha256_verified = False
    app.state.load_error = None
    app.state.startup_time = datetime.now(timezone.utc).isoformat()

    try:
        # 1. Kiểm tra sự tồn tại của tệp
        if not PIPELINE_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy file pipeline tại: {PIPELINE_PATH}")
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy file schema tại: {SCHEMA_PATH}")
        if not METADATA_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy file metadata tại: {METADATA_PATH}")

        # 2. Đọc metadata và schema
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)

        # 3. Kiểm tra mã băm SHA-256
        expected_hash = metadata.get("sha256_checksum", "")
        sha_ok = verify_sha256(PIPELINE_PATH, expected_hash)
        if not sha_ok:
            logger.warning("CẢNH BÁO BẢO MẬT: Mã băm SHA-256 của pipeline không trùng khớp với metadata!")

        # 4. Nạp Pipeline vào bộ nhớ
        logger.info(f"Đang nạp mô hình từ: {PIPELINE_PATH}...")
        pipeline = joblib.load(PIPELINE_PATH)

        # 5. Kiểm tra tính tương thích số lượng đặc trưng
        if len(schema) != len(FEATURE_NAMES):
            raise ValueError(f"Số lượng đặc trưng trong schema ({len(schema)}) không khớp FEATURE_NAMES ({len(FEATURE_NAMES)})")

        # 6. Trích xuất thống kê miền giá trị để kiểm tra OOD
        train_ranges = {}
        for item in schema:
            if "name" in item and "train_statistics" in item:
                train_ranges[item["name"]] = {
                    "min": float(item["train_statistics"]["min"]),
                    "max": float(item["train_statistics"]["max"]),
                }

        # Lưu trữ trạng thái vào app.state (Singleton pattern)
        app.state.model = pipeline
        app.state.schema = schema
        app.state.metadata = metadata
        app.state.train_ranges = train_ranges
        app.state.model_loaded = True
        app.state.sha256_verified = sha_ok
        logger.info(f"Nạp mô hình '{metadata.get('model_name')}' phiên bản {metadata.get('version')} thành công.")

    except Exception as e:
        logger.error(f"LỖI KHỞI ĐỘNG: Không thể nạp mô hình: {str(e)}", exc_info=True)
        app.state.model_loaded = False
        app.state.load_error = str(e)

    yield  # Ứng dụng chạy và lắng nghe requests

    # Khi server dừng
    logger.info("Đang tắt ứng dụng FastAPI Backend...")
    app.state.model = None


# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="WDBC Breast Cancer Classification API",
    description=(
        "Backend API phục vụ phân loại khối u vú Wisconsin Diagnostic Breast Cancer (WDBC) "
        "sử dụng Cây Quyết Định và Rừng Ngẫu Nhiên (Project 16 - Học máy cơ bản)."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Cấu hình CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Root Endpoint", tags=["General"])
async def root_endpoint() -> Dict[str, Any]:
    """Endpoint gốc chào mừng và cung cấp thông tin tổng quan về API."""
    return {
        "app_name": "WDBC Breast Cancer Classification API",
        "project": "Project 16 - Học máy cơ bản",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
        "health_check": "/api/health",
        "classification_endpoint": "/api/demo-classify",
        "author": "Do Huu Quoc Anh",
    }


@app.get(
    "/api/health",
    summary="Kiểm tra trạng thái hệ thống và mô hình",
    tags=["Health"],
    response_model=Dict[str, Any],
)
async def health_check_endpoint(response: Response) -> Dict[str, Any]:
    """
    Endpoint kiểm tra sức khỏe của dịch vụ và trạng thái sẵn sàng của mô hình:
    - Báo cáo trạng thái 'ok' nếu mô hình đã sẵn sàng.
    - Báo cáo trạng thái 'degraded' (HTTP 503) nếu mô hình bị thiếu hoặc không thể nạp.
    """
    model_loaded = getattr(app.state, "model_loaded", False)
    metadata = getattr(app.state, "metadata", None) or {}
    sha_verified = getattr(app.state, "sha256_verified", False)
    load_error = getattr(app.state, "load_error", None)
    startup_time = getattr(app.state, "startup_time", None)

    if model_loaded:
        response.status_code = status.HTTP_200_OK
        current_status = "ok"
        message = "Dịch vụ hoạt động bình thường, mô hình sẵn sàng phục vụ suy luận."
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        current_status = "degraded"
        message = f"Dịch vụ hoạt động nhưng mô hình chưa sẵn sàng: {load_error}"

    return {
        "status": current_status,
        "message": message,
        "app_name": "WDBC Breast Cancer Classification API",
        "version": metadata.get("version", "1.0.0"),
        "model_loaded": model_loaded,
        "model_name": metadata.get("model_name", "Unknown"),
        "sha256_verified": sha_verified,
        "input_features_count": metadata.get("input_features_count", len(FEATURE_NAMES)),
        "decision_threshold": metadata.get("decision_threshold", 0.50),
        "target_positive_class": metadata.get("target_definition", {}).get("positive_label", "Malignant"),
        "startup_time": startup_time,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": load_error,
    }


@app.get(
    "/api/reports/dashboard",
    summary="Đọc dữ liệu tổng hợp các báo cáo thực nghiệm và đánh giá mô hình",
    tags=["Reports"],
    response_model=Dict[str, Any],
)
async def get_dashboard_reports_endpoint() -> Dict[str, Any]:
    """
    Endpoint chỉ đọc cung cấp dữ liệu báo cáo thực nghiệm đã được đóng băng:
    - final_test: kết quả đánh giá trên tập Test và đối sánh 4 mô hình
    - exp1_depth: kết quả khảo sát độ sâu cây Train vs CV
    - exp4_stability: kết quả kiểm tra độ ổn định Feature Importance qua 5 seeds
    - model_metadata: thẻ mô hình và siêu tham số đóng băng
    Nếu tệp artifact bị thiếu, trả về None cho trường tương ứng thay vì bịa số liệu.
    """
    data = {}

    # 1. Đọc final_test_evaluation.json
    final_test_file = REPORTS_DIR / "final_test_evaluation.json"
    if final_test_file.exists():
        try:
            with open(final_test_file, "r", encoding="utf-8") as f:
                data["final_test"] = json.load(f)
        except Exception as e:
            logger.warning(f"Không thể đọc {final_test_file}: {e}")
            data["final_test"] = None
    else:
        data["final_test"] = None

    # 2. Đọc exp1_depth_results.json
    exp1_file = REPORTS_DIR / "exp1_depth_results.json"
    if exp1_file.exists():
        try:
            with open(exp1_file, "r", encoding="utf-8") as f:
                data["exp1_depth"] = json.load(f)
        except Exception as e:
            logger.warning(f"Không thể đọc {exp1_file}: {e}")
            data["exp1_depth"] = None
    else:
        data["exp1_depth"] = None

    # 3. Đọc exp4_feature_stability_results.json
    exp4_file = REPORTS_DIR / "exp4_feature_stability_results.json"
    if exp4_file.exists():
        try:
            with open(exp4_file, "r", encoding="utf-8") as f:
                data["exp4_stability"] = json.load(f)
        except Exception as e:
            logger.warning(f"Không thể đọc {exp4_file}: {e}")
            data["exp4_stability"] = None
    else:
        data["exp4_stability"] = None

    # 4. Đọc model_metadata
    metadata_file = METADATA_PATH
    if metadata_file.exists():
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                data["model_metadata"] = json.load(f)
        except Exception as e:
            logger.warning(f"Không thể đọc {metadata_file}: {e}")
            data["model_metadata"] = None
    else:
        data["model_metadata"] = None

    return {
        "status": "success",
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/api/demo-classify",
    summary="Phân loại khối u vú từ 30 đặc trưng FNA",
    tags=["Classification"],
    response_model=ClassificationResponse,
)
async def demo_classify_endpoint(
    payload: Union[ClassifyWrappedRequest, WDBCFeaturesInput] = Body(
        ...,
        description="30 đặc trưng số FNA của tế bào (trực tiếp hoặc lồng trong object features)"
    )
) -> ClassificationResponse:
    """
    Endpoint phân loại bệnh phẩm chẩn đoán ung thư vú WDBC:
    1. Nhận chính xác 30 đặc trưng số, kiểm tra chặt chẽ tính toàn vẹn (không thiếu/thừa, không NaN/Inf, không âm).
    2. Kiểm tra miền giá trị theo dữ liệu Train, cảnh báo Out-Of-Distribution và từ chối các giá trị cực đoan phi lý.
    3. Không âm thầm thay thế giá trị sai hoặc thiếu.
    4. Sắp xếp đúng thứ tự 30 đặc trưng và đưa vào Scikit-Learn Pipeline.
    5. Gọi predict và predict_proba, trả về xác suất từng lớp và nhãn B/M.
    6. Cung cấp phần giải thích mô hình chuẩn xác kèm giới hạn phương pháp.
    """
    # 1. Kiểm tra trạng thái mô hình
    if not getattr(app.state, "model_loaded", False) or app.state.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Mô hình phân loại chưa sẵn sàng phục vụ suy luận "
                f"(Lỗi nạp mô hình: {getattr(app.state, 'load_error', 'Chưa nạp')}). Vui lòng kiểm tra GET /api/health."
            )
        )

    # 2. Phân giải payload
    if isinstance(payload, ClassifyWrappedRequest):
        features_input = payload.features
        custom_threshold = payload.threshold
    else:
        features_input = payload
        custom_threshold = None

    feature_dict = features_input.to_feature_dict()

    # 3. Kiểm tra miền giá trị theo Train statistics
    train_ranges = getattr(app.state, "train_ranges", {})
    warnings = check_feature_ranges(feature_dict, train_ranges)

    # 4. Đảm bảo đúng thứ tự 30 đặc trưng đưa vào Pipeline
    df_input = pd.DataFrame([[feature_dict[col] for col in FEATURE_NAMES]], columns=FEATURE_NAMES)

    # 5. Thực hiện suy luận (Inference)
    pipeline = app.state.model
    metadata = getattr(app.state, "metadata", None) or {}

    try:
        probs = pipeline.predict_proba(df_input)[0]
    except Exception as e:
        logger.error(f"Lỗi tính toán suy luận mô hình: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi nội bộ khi thực hiện suy luận mô hình: {str(e)}"
        )

    prob_benign = float(probs[0])
    prob_malignant = float(probs[1])

    # 6. Xác định ngưỡng quyết định và phân loại
    base_threshold = float(metadata.get("decision_threshold", 0.50))
    applied_threshold = custom_threshold if custom_threshold is not None else base_threshold

    pred_class = 1 if prob_malignant >= applied_threshold else 0
    pred_code = "M" if pred_class == 1 else "B"
    pred_label = "Malignant" if pred_class == 1 else "Benign"
    confidence_score = round(max(prob_benign, prob_malignant) * 100.0, 2)

    # 7. Trích xuất phần giải thích mô hình
    explanation = extract_model_explanation(pipeline, df_input, FEATURE_NAMES)

    # 8. Đóng gói response
    model_name = metadata.get("model_name", "WDBC_RandomForest_Classifier_Pipeline")
    version = metadata.get("version", "1.0.0")
    disclaimer = metadata.get(
        "clinical_disclaimer",
        "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA: Kết quả này chỉ phục vụ mục đích nghiên cứu học thuật trong môn học Học máy cơ bản, không có giá trị chẩn đoán y khoa lâm sàng."
    )

    return ClassificationResponse(
        status="success",
        predicted_class=pred_class,
        predicted_code=pred_code,
        predicted_label=pred_label,
        probabilities=ProbabilitiesOutput(
            benign=round(prob_benign, 4),
            malignant=round(prob_malignant, 4),
            B=round(prob_benign, 4),
            M=round(prob_malignant, 4),
        ),
        decision_threshold=applied_threshold,
        confidence_score=confidence_score,
        is_high_risk=bool(pred_class == 1),
        model_info=ModelInfoOutput(
            model_name=model_name,
            version=version,
            algorithm=explanation.get("model_type", "RandomForestClassifier"),
            decision_threshold=applied_threshold,
            input_features_count=len(FEATURE_NAMES),
        ),
        explanation=explanation,
        warnings=warnings,
        clinical_disclaimer=disclaimer,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Đăng ký thêm alias POST /api/predict theo tài liệu Project 16
@app.post(
    "/api/predict",
    summary="Alias cho /api/demo-classify",
    tags=["Classification"],
    response_model=ClassificationResponse,
    include_in_schema=True,
)
async def predict_alias_endpoint(
    payload: Union[ClassifyWrappedRequest, WDBCFeaturesInput] = Body(...)
) -> ClassificationResponse:
    """Endpoint tương đương với /api/demo-classify nhằm tương thích với các tài liệu Project 16."""
    return await demo_classify_endpoint(payload)


if __name__ == "__main__":
    import uvicorn
    # Khởi chạy cục bộ khi chạy trực tiếp file
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
