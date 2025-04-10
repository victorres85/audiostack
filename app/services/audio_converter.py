from pydub import AudioSegment
from io import BytesIO

from app.exceptions import AudioException

SUPPORTED_FORMATS = {"mp3", "wav"}
MAX_DURATION_SECONDS = 30


def audio_converter(file_content: BytesIO, output_format: str) -> bytes:
    audio = AudioSegment.from_file(file_content)

    # Check duration
    if len(audio) > MAX_DURATION_SECONDS * 1000:  # pydub works in milliseconds
        raise AudioException(status_code=400, detail=f"Audio duration exceeds {MAX_DURATION_SECONDS} seconds limit")

    # Export to desired format
    output = BytesIO()
    audio.export(output, format=output_format)
    return output.getvalue()
