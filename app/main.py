from fastapi import FastAPI, Request
from app.api.routes import router
from fastapi.responses import JSONResponse
from app.exceptions import AudioException

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    title="AudioStacks Converter API",
    description="API for converting audio files between mp3 and wav formats",
    version="1.0.0",
)


@app.exception_handler(AudioException)
async def _audio_size_exception_handler(request: Request, exc: AudioException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


app.include_router(router)
