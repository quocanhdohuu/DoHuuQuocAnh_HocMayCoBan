"""
Ứng dụng Backend FastAPI - Project 16: Phân Loại Khối U Vú (WDBC).
Nhiệm vụ 16: Khởi tạo Backend FastAPI, nạp model một lần bằng Lifespan, kiểm tra health và cấu hình CORS.

Nguyên lý kiến trúc:
1. Lifespan Context Manager:
   - Mô hình Machine Learning được nạp đúng MỘT LẦN DUY NHẤT vào bộ nhớ RAM khi ứng dụng khởi động.
   - Tránh việc nạp lại mô hình trong từng request gây nghẽn I/O và tăng độ trễ (latency).
2. Kiểm tra tính tương thích và toàn vẹn:
   - Kiểm tra sự tồn tại của tệp pipeline joblib, schema 30 đặc trưng và metadata.
   - Xác thực mã băm SHA-256 để đảm bảo tệp mô hình không bị giả mạo hoặc hư hỏng.
3. Cơ chế phục hồi lỗi (Graceful Degradation):
   - Nếu tệp mô hình bị thiếu hoặc lỗi, server không bị crash đột ngột mà chuyển sang trạng thái
     "degraded" để endpoint /api/health báo lỗi rõ ràng cho quản trị viên.
4. Bảo vệ CORS (Cross-Origin Resource Sharing):
   - Cấu hình mở cho các cổng phát triển cục bộ của Frontend (ReactJS: 3000, Vite: 5173).
"""

import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Đảm bảo đường dẫn gốc nằm trong sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.src.config import MODELS_DIR, FEATURE_NAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("backend.app.main")

PIPELINE_PATH = MODELS_DIR / "wdbc_pipeline.joblib"
SCHEMA_PATH = MODELS_DIR / "feature_schema.json"
METADATA_PATH = MODELS_DIR / "model_metadata.json"

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan Context Manager:
    Nạp mô hình, schema và metadata MỘT LẦN DUY NHẤT khi server khởi động.
    Dọn dẹp tài nguyên khi server tắt.
    """
    logger.info("Đang khởi động FastAPI Backend (Project 16)...")
    app.state.model = None
    app.state.schema = None
    app.state.metadata = None
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

        # Lưu trữ trạng thái vào app.state (Singleton pattern)
        app.state.model = pipeline
        app.state.schema = schema
        app.state.metadata = metadata
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


if __name__ == "__main__":
    import uvicorn
    # Khởi chạy cục bộ khi chạy trực tiếp file
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
