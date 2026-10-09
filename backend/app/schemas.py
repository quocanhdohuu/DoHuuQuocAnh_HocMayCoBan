"""
Pydantic Schemas cho API Phân Loại Khối U Vú WDBC (Project 16).
Nhiệm vụ 17: Classification API.

Đặc tả:
- Nhận diện chính xác 30 đặc trưng số FNA theo schema đã lưu.
- Cấm tuyệt đối trường thừa (extra='forbid').
- Kiểm tra tính đầy đủ, ngăn chặn thiếu trường, sai kiểu dữ liệu.
- Ngăn chặn triệt để giá trị NaN, Infinity và giá trị âm vật lý (< 0).
- Hỗ trợ cả tên đặc trưng chuẩn có dấu cách và dạng snake_case.
- Cấu trúc Response tường minh, đầy đủ nhãn B/M, xác suất, metadata và phần giải thích phù hợp.
"""

import math
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class WDBCFeaturesInput(BaseModel):
    """
    Schema nhận diện chính xác 30 đặc trưng số tế bào WDBC.
    Cấm các trường ngoài danh mục (extra='forbid') và kiểm tra tính hợp lệ.
    """
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "radius_mean": 17.99,
                "texture_mean": 10.38,
                "perimeter_mean": 122.8,
                "area_mean": 1001.0,
                "smoothness_mean": 0.1184,
                "compactness_mean": 0.2776,
                "concavity_mean": 0.3001,
                "concave points_mean": 0.1471,
                "symmetry_mean": 0.2419,
                "fractal_dimension_mean": 0.07871,
                "radius_se": 1.095,
                "texture_se": 0.9053,
                "perimeter_se": 8.589,
                "area_se": 153.4,
                "smoothness_se": 0.006399,
                "compactness_se": 0.04904,
                "concavity_se": 0.05373,
                "concave points_se": 0.01587,
                "symmetry_se": 0.03003,
                "fractal_dimension_se": 0.006193,
                "radius_worst": 25.38,
                "texture_worst": 17.33,
                "perimeter_worst": 184.6,
                "area_worst": 2019.0,
                "smoothness_worst": 0.1622,
                "compactness_worst": 0.6656,
                "concavity_worst": 0.7119,
                "concave points_worst": 0.2654,
                "symmetry_worst": 0.4601,
                "fractal_dimension_worst": 0.1189
            }
        }
    )

    # 1. Nhóm Mean (10 đặc trưng trung bình)
    radius_mean: float = Field(..., description="Bán kính trung bình của nhân tế bào (micromet)")
    texture_mean: float = Field(..., description="Độ lệch chuẩn mức xám bề mặt")
    perimeter_mean: float = Field(..., description="Chu vi trung bình của nhân tế bào")
    area_mean: float = Field(..., description="Diện tích trung bình của nhân tế bào")
    smoothness_mean: float = Field(..., description="Độ nhẵn cục bộ (biến thiên chiều dài bán kính)")
    compactness_mean: float = Field(..., description="Độ co cụm: perimeter^2 / area - 1.0")
    concavity_mean: float = Field(..., description="Mức độ nghiêm trọng của phần lõm trên đường viền")
    concave_points_mean: float = Field(..., alias="concave points_mean", description="Số lượng điểm lõm trên đường viền")
    symmetry_mean: float = Field(..., description="Độ đối xứng của nhân tế bào")
    fractal_dimension_mean: float = Field(..., description="Số chiều fractal (xấp xỉ bờ tế bào)")

    # 2. Nhóm SE (10 đặc trưng sai số chuẩn)
    radius_se: float = Field(..., description="Sai số chuẩn của bán kính")
    texture_se: float = Field(..., description="Sai số chuẩn của độ nhám")
    perimeter_se: float = Field(..., description="Sai số chuẩn của chu vi")
    area_se: float = Field(..., description="Sai số chuẩn của diện tích")
    smoothness_se: float = Field(..., description="Sai số chuẩn của độ nhẵn")
    compactness_se: float = Field(..., description="Sai số chuẩn của độ co cụm")
    concavity_se: float = Field(..., description="Sai số chuẩn của độ lõm")
    concave_points_se: float = Field(..., alias="concave points_se", description="Sai số chuẩn của số điểm lõm")
    symmetry_se: float = Field(..., description="Sai số chuẩn của độ đối xứng")
    fractal_dimension_se: float = Field(..., description="Sai số chuẩn của số chiều fractal")

    # 3. Nhóm Worst (10 đặc trưng giá trị tệ nhất / lớn nhất)
    radius_worst: float = Field(..., description="Bán kính lớn nhất đo được")
    texture_worst: float = Field(..., description="Độ nhám lớn nhất đo được")
    perimeter_worst: float = Field(..., description="Chu vi lớn nhất đo được")
    area_worst: float = Field(..., description="Diện tích lớn nhất đo được")
    smoothness_worst: float = Field(..., description="Độ nhẵn lớn nhất đo được")
    compactness_worst: float = Field(..., description="Độ co cụm lớn nhất đo được")
    concavity_worst: float = Field(..., description="Độ lõm lớn nhất đo được")
    concave_points_worst: float = Field(..., alias="concave points_worst", description="Số điểm lõm lớn nhất đo được")
    symmetry_worst: float = Field(..., description="Độ đối xứng lớn nhất đo được")
    fractal_dimension_worst: float = Field(..., description="Số chiều fractal lớn nhất đo được")

    @field_validator("*")
    @classmethod
    def validate_numeric_boundaries(cls, value: float, info) -> float:
        """Kiểm tra số thực hữu hạn và giá trị không âm."""
        field_name = info.field_name
        if not math.isfinite(value):
            raise ValueError(f"Đặc trưng '{field_name}' phải là số thực hữu hạn, không được nhận NaN hoặc Infinity.")
        if value < 0:
            raise ValueError(f"Đặc trưng '{field_name}' không thể nhận giá trị âm ({value} < 0) theo đặc tính sinh học tế bào.")
        return value

    def to_feature_dict(self) -> Dict[str, float]:
        """Xuất từ điển với đúng key chuẩn hóa trong FEATURE_NAMES (kể cả key có dấu cách)."""
        return {
            "radius_mean": float(self.radius_mean),
            "texture_mean": float(self.texture_mean),
            "perimeter_mean": float(self.perimeter_mean),
            "area_mean": float(self.area_mean),
            "smoothness_mean": float(self.smoothness_mean),
            "compactness_mean": float(self.compactness_mean),
            "concavity_mean": float(self.concavity_mean),
            "concave points_mean": float(self.concave_points_mean),
            "symmetry_mean": float(self.symmetry_mean),
            "fractal_dimension_mean": float(self.fractal_dimension_mean),
            "radius_se": float(self.radius_se),
            "texture_se": float(self.texture_se),
            "perimeter_se": float(self.perimeter_se),
            "area_se": float(self.area_se),
            "smoothness_se": float(self.smoothness_se),
            "compactness_se": float(self.compactness_se),
            "concavity_se": float(self.concavity_se),
            "concave points_se": float(self.concave_points_se),
            "symmetry_se": float(self.symmetry_se),
            "fractal_dimension_se": float(self.fractal_dimension_se),
            "radius_worst": float(self.radius_worst),
            "texture_worst": float(self.texture_worst),
            "perimeter_worst": float(self.perimeter_worst),
            "area_worst": float(self.area_worst),
            "smoothness_worst": float(self.smoothness_worst),
            "compactness_worst": float(self.compactness_worst),
            "concavity_worst": float(self.concavity_worst),
            "concave points_worst": float(self.concave_points_worst),
            "symmetry_worst": float(self.symmetry_worst),
            "fractal_dimension_worst": float(self.fractal_dimension_worst),
        }


class ClassifyWrappedRequest(BaseModel):
    """Hỗ trợ cấu trúc request dạng gói {"features": {...}, "threshold": 0.5}."""
    model_config = ConfigDict(extra="forbid")
    features: WDBCFeaturesInput
    threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Ngưỡng phân loại tùy chọn (0.0 đến 1.0). Mặc định theo metadata mô hình (0.50)."
    )


class ProbabilitiesOutput(BaseModel):
    """Cấu trúc xác suất dự đoán rõ ràng cho từng lớp và từng mã nhãn."""
    benign: float = Field(..., description="Xác suất mẫu là Khối u Lành tính (P >= 0.0)")
    malignant: float = Field(..., description="Xác suất mẫu là Khối u Ác tính (P >= 0.0)")
    B: float = Field(..., description="Mã viết tắt xác suất Lành tính (Benign)")
    M: float = Field(..., description="Mã viết tắt xác suất Ác tính (Malignant)")


class ModelInfoOutput(BaseModel):
    """Thông tin mô hình phục vụ suy luận."""
    model_name: str
    version: str
    algorithm: str
    decision_threshold: float
    input_features_count: int


class ClassificationResponse(BaseModel):
    """
    Schema phản hồi chuẩn hóa cho POST /api/demo-classify.
    """
    status: str = Field(default="success", description="Trạng thái thực thi")
    predicted_class: int = Field(..., description="Lớp phân loại dạng số: 0 (Benign) hoặc 1 (Malignant)")
    predicted_code: str = Field(..., description="Mã nhãn: 'B' (Benign) hoặc 'M' (Malignant)")
    predicted_label: str = Field(..., description="Tên nhãn lâm sàng: 'Benign' hoặc 'Malignant'")
    probabilities: ProbabilitiesOutput
    decision_threshold: float = Field(..., description="Ngưỡng xác suất áp dụng cho lớp Ác tính")
    confidence_score: float = Field(..., description="Độ tin cậy của mô hình (%)")
    is_high_risk: bool = Field(..., description="Cờ cảnh báo nguy cơ ác tính cao")
    model_info: ModelInfoOutput
    explanation: Dict[str, Any] = Field(..., description="Giải thích dự đoán phù hợp cấu trúc mô hình")
    warnings: List[str] = Field(default_factory=list, description="Cảnh báo đặc trưng nằm ngoài dải huấn luyện (Out-Of-Distribution)")
    clinical_disclaimer: str = Field(..., description="Tuyên bố miễn trừ trách nhiệm y tế bắt buộc")
    timestamp: str = Field(..., description="Thời gian thực thi chuẩn ISO UTC")
