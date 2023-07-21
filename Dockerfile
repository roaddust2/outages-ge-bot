# syntax=docker/dockerfile:1
FROM python:3.11.4-bookworm as builder
COPY requirements.txt requirements.txt
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11.4-slim-bookworm

LABEL name="outages-ge-bot" \
      version="0.1.0" \
      description="Stay tuned with nearest outages in Georgia with this Telegram bot" \
      authors="roaddust2 <roaddust2@yahoo.com>" \
      license="GPL-3.0-only"

ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .