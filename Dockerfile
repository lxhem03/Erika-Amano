FROM python:3.9-slim-buster

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Kolkata"

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        mediainfo \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["bash", "run.sh"]
