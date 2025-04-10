import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import magic
from app.main import app

client = TestClient(app)
TEST_FILES_DIR = Path("tests/test_files")


wav_short = TEST_FILES_DIR / "wav_short.wav"
mp3_short = TEST_FILES_DIR / "mp3_short.mp3"
aif_short = TEST_FILES_DIR / "aif_short.aif"
m4a_short = TEST_FILES_DIR / "m4a_short.m4a"

wav_long = TEST_FILES_DIR / "wav_long.wav"
mp3_long = TEST_FILES_DIR / "mp3_long.mp3"
aif_long = TEST_FILES_DIR / "aif_long.aif"
m4a_long = TEST_FILES_DIR / "m4a_long.m4a"


@pytest.mark.parametrize("test_short", [wav_short, mp3_short, aif_short, m4a_short])
def test_convert_to_mp3(test_short: Path) -> None:
    """Test converting WAV to MP3"""
    with open(test_short, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/convert/mp3", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mp3"
    assert response.headers["content-disposition"] == "attachment; filename=converted.mp3"
    assert magic.from_buffer(response.content, mime=True) == "audio/mpeg"


@pytest.mark.parametrize("test_short", [wav_short, mp3_short, aif_short, m4a_short])
def test_convert_to_wav(test_short: Path) -> None:
    """Test converting MP3 to WAV"""
    with open(test_short, "rb") as f:
        files = {"file": ("test.mp3", f, "audio/mpeg")}
        response = client.post("/convert/wav", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.headers["content-disposition"] == "attachment; filename=converted.wav"
    assert magic.from_buffer(response.content, mime=True) == "audio/x-wav"


def test_invalid_input_format() -> None:
    """Test uploading an unsupported file format"""
    # Create a dummy text file
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/convert/mp3", files=files)

    assert response.status_code == 400


@pytest.mark.parametrize("test_short", [wav_short, mp3_short, aif_short, m4a_short])
def test_invalid_output_format(test_short: Path) -> None:
    """Test requesting an unsupported output format"""
    with open(test_short, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/convert/flac", files=files)

    assert response.status_code == 422


@pytest.mark.parametrize("test_long", [wav_long, mp3_long, aif_long, m4a_long])
def test_audio_duration_exceeded(test_long: Path) -> None:
    """Test uploading an audio file that exceeds the allowed duration"""

    with open(test_long, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/convert/mp3", files=files)

    assert response.status_code == 400
    assert response.json() == {"message": "Audio duration exceeds 30 seconds limit"}
