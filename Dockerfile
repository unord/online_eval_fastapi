# install alpine linux
FROM alpine:latest

# Install Git, Python 3.11, and Google Chrome
RUN apk add --update git python3 google-chrome



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
