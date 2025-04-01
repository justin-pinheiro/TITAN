FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt /app

RUN pip install -r requirements.txt

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libgbm1 \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Set Chromium as default browser
ENV BROWSER="/usr/bin/chromium --no-sandbox"

COPY . /app

EXPOSE 80

CMD ["python", "src/app.py"]
