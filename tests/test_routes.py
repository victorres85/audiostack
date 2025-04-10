import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import magic
from app.main import app

client = TestClient(app)
TEST_FILES_DIR = Path("tests/test_files")


@pytest.fixture
def test_wav_long() -> Path:
    return TEST_FILES_DIR / "wav_long.wav"


@pytest.fixture
def test_mp3_long() -> Path:
    return TEST_FILES_DIR / "mp3_long.mp3"


@pytest.fixture
def test_wav_short() -> Path:
    return TEST_FILES_DIR / "wav_short.wav"


@pytest.fixture
def test_mp3_short() -> Path:
    return TEST_FILES_DIR / "mp3_short.mp3"


def test_wav_to_mp3_conversion(test_wav_short: Path) -> None:
    """Test converting WAV to MP3"""
    with open(test_wav_short, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/convert/mp3", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mp3"
    assert response.headers["content-disposition"] == "attachment; filename=converted.mp3"
    # Best practice: Validate the output file format
    assert magic.from_buffer(response.content, mime=True) == "audio/mpeg"


def test_mp3_to_wav_conversion(test_mp3_short: Path) -> None:
    """Test converting MP3 to WAV"""
    with open(test_mp3_short, "rb") as f:
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


def test_invalid_output_format(test_wav_short: Path) -> None:
    """Test requesting an unsupported output format"""
    with open(test_wav_short, "rb") as f:
        files = {"file": ("test.wav", f, "audio/wav")}
        response = client.post("/convert/flac", files=files)

    assert response.status_code == 422
