FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

LABEL maintainer="Nguyen Hoang <htnguyen98.act@gmail.com>"

# Install Python packages
RUN python3 -m pip install --upgrade pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install \
    Pillow \
    python-telegram-bot==13.15 \
    requests \
    flask \
    celery \
    redis \
    onnxruntime \
    ultralytics \
    playwright && \
    playwright install --with-deps chromium

COPY . /opt/In0ri
EXPOSE 8080
WORKDIR /opt/In0ri/FlaskApp
CMD ["python3", "app.py"]
