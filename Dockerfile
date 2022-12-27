FROM python:3.11-alpine
RUN apk add --no-cache git

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . ./app
RUN pip install -r /app/requirements.txt


CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "80"]
