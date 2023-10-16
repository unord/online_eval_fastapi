FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

WORKDIR /app
COPY . .
RUN pip install --upgrade cython && pip install --upgrade pip
RUN ln -sf /usr/share/zoneinfo/Europe/Copenhagen /etc/localtime
RUN pip install -r ./requirements.txt