FROM debian:stable-slim
EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    python3-pip \
    tesseract-ocr-vie \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean && rm -rf /tmp/*

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src/ /app/src
COPY ./VnCoreNLP/ /app/VnCoreNLP
WORKDIR /app/src
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]