# install alpine linux
FROM alpine:latest

# install python and git
RUN apk add --no-cache git python3

# install chrome dependencies
RUN apk add --no-cache \
    bash \
    libX11 \
    libX11-xcb \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXext \
    libXfixes \
    libXi \
    libXrender \
    libXtst \
    libXrandr \
    libXv \
    libXxf86vm \
    libstdc++ \
    mesa-gl \
    mesa-dri-swrast \
    atk \
    pango \
    gtk+3.0 \
    cairo \
    gdk-pixbuf \
    mpc \
    mpfr \
    gmp \
    libgomp \
    freetype \
    fontconfig \
    ttf-freefont \
    ttf-opensans \
    harfbuzz \
    fribidi \
    icu-libs \
    unzip \
    wget

# install google chrome
RUN wget -O /tmp/google-chrome.zip https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    unzip /tmp/google-chrome.zip -d /opt && \
    rm /tmp/google-chrome.zip

COPY start-chrome /usr/bin/start-chrome
RUN chmod +x /usr/bin/start-chrome
CMD ["/usr/bin/start-chrome"]

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
