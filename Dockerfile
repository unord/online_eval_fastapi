# install alpine linux
FROM alpine:latest



RUN apk --no-cache update

# install python and git
RUN apk add --no-cache git python3

# install google chrome
RUN apk update && apk add unzip xvfb libxi6 libgconf-2-4
RUN apk update && apk add wget \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apk add - \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk update \
    && apk add google-chrome-stable ttf-freefont

# set display port to avoid crash
ENV DISPLAY=:99


#
WORKDIR /code

#
COPY ./requirements.txt code/src/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r code/src/requirements.txt

#
COPY . /code/

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
