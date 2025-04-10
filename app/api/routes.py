from fastapi import APIRouter, UploadFile
from app.exceptions import AudioException
from app.services.audio_converter import audio_converter
from fastapi.responses import Response
from typing import Literal
import logging
import io

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/convert/{output_format}")
def convert_audio(output_format: Literal["wav", "mp3"], file: UploadFile) -> Response:
    # Read file content
    file_content = io.BytesIO(file.file.read())
    content_type = file.content_type or ""
    if not content_type.startswith("audio/"):
        raise AudioException(status_code=400, detail="File must be an audio file")

    converted_audio = audio_converter(file_content, output_format.lower())

    return Response(
        content=converted_audio,
        media_type=f"audio/{output_format.lower()}",
        headers={"Content-Disposition": f"attachment; filename=converted.{output_format.lower()}"},
    )
