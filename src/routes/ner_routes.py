from typing import List
import fastapi

from core.core_ner import *

from models.ner_models import *

router = fastapi.APIRouter()


@router.post(
    path="/file_upload",
    response_class=fastapi.responses.JSONResponse,
    response_model=List[SingleWord],
)
async def file_ner(
    file: fastapi.UploadFile = fastapi.File(media_type="multipart", default="Any")
):

    if not hasattr(file, "file"):
        raise fastapi.HTTPException(status_code=400, detail="No file uploaded")
    return await ner_from_file(file.file)


@router.post(
    path="/text_upload",
    response_class=fastapi.responses.JSONResponse,
    response_model=List[SingleWord],
)
async def text_ner(content: TextUpload):
    return await ner_from_text(content.text)
