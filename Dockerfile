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
        libfdk-aac-dev \  # Consider alternatives for licensing reasons
        libmp3lame-dev \
        libopus-dev \
        libtheora-dev \
        libvorbis-dev \
        libvpx-dev \
        libx264-dev \
        libx265-dev \
        libaom-dev \    # AV1 codec
        libdav1d-dev \  # AV1 decoder
        libbluray-dev \  # Bluray
        libnuma-dev   &&  #NUMA
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN wget https://ffmpeg.org/releases/ffmpeg-8.0.tar.gz && \
    tar -xzf ffmpeg-8.0.tar.gz

WORKDIR /app/ffmpeg-4.4

RUN ./configure \
    --prefix=/usr/local \
    --enable-gpl \
    --enable-nonfree \
    --enable-libfdk-aac \  # Be mindful of licensing
    --enable-libx264 \
    --enable-libx265 \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libvorbis \
    --enable-libass \
    --enable-libtheora \
    --enable-libvpx \
    --enable-libaom \  # AV1
    --enable-libdav1d \ # AV1 decoder
    --enable-libbluray \ #Bluray
    --enable-version3 \
    --enable-sdl2 \
    --extra-ldflags="-L/usr/local/lib" \
    --extra-cflags="-I/usr/local/include"
RUN make -j$(nproc)
RUN make install
RUN ldconfig

WORKDIR /app
COPY . .

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "run.sh"]
