FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MODE_TO_RUN=serverless \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY handler.py /app/handler.py
COPY local_test.py /app/local_test.py
COPY src /app/src

CMD ["python", "-u", "handler.py"]
