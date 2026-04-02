FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-devel-ubuntu22.04

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MODE_TO_RUN=serverless \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

COPY handler.py /app/handler.py
COPY local_test.py /app/local_test.py
COPY src /app/src

CMD ["python", "-u", "handler.py"]
