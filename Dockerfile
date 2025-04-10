FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg libmagic-dev

COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
