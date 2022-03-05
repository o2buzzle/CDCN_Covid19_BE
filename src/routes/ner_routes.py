import fastapi
import io

from pydantic import BaseModel
from app import *

router = fastapi.APIRouter()

class TextUpload(BaseModel):
    text: str

@router.post(path="/file_upload", response_class=fastapi.responses.JSONResponse)
async def main(file: fastapi.UploadFile = fastapi.File(media_type='multipart', default='Any')):
    file_container = io.BytesIO()
    file_container.write(file.file.read())
    file_container.seek(0)
    return await ner_from_file(file_container)

@router.post(path="/text_upload", response_class=fastapi.responses.JSONResponse)
async def main(content: TextUpload):
    return await ner_from_text(content.text)