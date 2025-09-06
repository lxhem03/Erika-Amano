FROM python:3.9-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Kolkata"

RUN echo "deb http://archive.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        mediainfo \
        build-essential \
        git \
        yasm \
        libtool \
        pkg-config \
        autoconf \
        automake \
        nasm \
        wget \
        ca-certificates \
        libsdl2-dev \
        libass-dev \
        libfdk-aac-dev \
        libmp3lame-dev \
        libopus-dev \
        libtheora-dev \
        libvorbis-dev \
        libvpx-dev \
        libx264-dev \
        libx265-dev \
        libaom-dev \
        libdav1d-dev \
        libbluray-dev \
        libnuma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN wget https://ffmpeg.org/releases/ffmpeg-7.0.2.tar.gz && \
    tar -xzf ffmpeg-7.0.2.tar.gz && \
    cd ffmpeg-7.0.2 && \
    ./configure \
        --prefix=/usr/local \
        --enable-gpl \
        --enable-nonfree \
        --enable-libfdk-aac \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libmp3lame \
        --enable-libopus \
        --enable-libvorbis \
        --enable-libass \
        --enable-libtheora \
        --enable-libvpx \
        --enable-libaom \
        --enable-libdav1d \
        --enable-libbluray \
        --enable-version3 \
        --enable-sdl2 \
        --extra-ldflags="-L/usr/local/lib" \
        --extra-cflags="-I/usr/local/include" && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf ffmpeg-7.0.2 ffmpeg-7.0.2.tar.gz

COPY . /app
WORKDIR /app

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/run.sh

CMD ["bash", "run.sh"]
