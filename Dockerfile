FROM python:3.11-alpine
RUN apk add --no-cache git

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . ./
RUN ls
RUN python pip install -r /requirements.txt

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "80"]
