import fastapi

router = fastapi.APIRouter()

from core.core_ocr import *
from models.ocr_models import *
from typing import List


@router.post("/file_upload", response_model=List[OCRResponse])
async def file_ocr(
    file: fastapi.UploadFile = fastapi.File(media_type="multipart", default="Any")
):
    if not hasattr(file, "file"):
        raise fastapi.HTTPException(status_code=400, detail="No file uploaded")
    return await ocr_from_file(file.file)
