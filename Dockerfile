# syntax=docker/dockerfile:1
FROM python:3.11.4-bookworm

LABEL name="outages-ge-bot" \
      version="0.1.0" \
      description="Stay tuned with nearest outages in Georgia with this Telegram bot" \
      authors="roaddust2 <roaddust2@yahoo.com>" \
      license="GPL-3.0-only"

WORKDIR /outages-ge-bot
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .