# Docling RunPod Worker

Standalone GPU-backed PDF extraction worker for RunPod Serverless.

This project is intentionally separate from `intel-weave-scan`. It owns one thing:

- accept one PDF extraction job
- run Docling on GPU
- return normalized markdown/text + metadata
- optionally POST the result to a callback URL

It does not know about Supabase, Lovable, `analysis_runs`, or any app-specific tables.

## Contract

Input payload:

```json
{
  "input": {
    "job_id": "job-123",
    "pdf_url": "https://example.com/report.pdf",
    "callback_url": "https://example.com/api/callback",
    "callback_secret": "shared-secret",
    "metadata": {
      "source": "intel-weave-scan"
    }
  }
}
```

Worker result:

```json
{
  "ok": true,
  "job_id": "job-123",
  "status": "completed",
  "result": {
    "text": "...",
    "title": "Report title",
    "word_count": 1234,
    "page_count": 42,
    "table_count": 3,
    "duration_seconds": 18.4
  }
}
```

On failure:

```json
{
  "ok": false,
  "job_id": "job-123",
  "status": "failed",
  "error": {
    "code": "EXTRACTION_FAILED",
    "message": "..."
  }
}
```

If `callback_url` is provided, the worker POSTs the same payload there after completion.

## Layout

- `handler.py`: RunPod entrypoint
- `src/docling_runpod_worker/schema.py`: request/response schema
- `src/docling_runpod_worker/extractor.py`: Docling GPU extraction core
- `src/docling_runpod_worker/staging.py`: markdown staging adapted from the original parser
- `src/docling_runpod_worker/callbacks.py`: callback POST helper
- `local_test.py`: direct local invocation without RunPod

## Environment

See `.env.example`.

Important knobs:

- `DOCLING_NUM_THREADS`
- `OMP_NUM_THREADS`
- `DOCLING_LAYOUT_BATCH_SIZE`
- `DOCLING_TABLE_BATCH_SIZE`
- `DOCLING_QUEUE_SIZE`
- `PDF_DOWNLOAD_TIMEOUT_SECONDS`
- `CALLBACK_TIMEOUT_SECONDS`
- `MODE_TO_RUN`

`MODE_TO_RUN=serverless` starts the RunPod worker.
`MODE_TO_RUN=pod` or unset lets you run local tests.

## Local development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python local_test.py --pdf-url "https://example.com/report.pdf" --job-id test-1
```

You can also use the RunPod SDK local server:

```bash
MODE_TO_RUN=serverless python handler.py --rp_serve_api
```

## Deployment

Build and push the Docker image, then deploy it to RunPod Serverless.

The container entrypoint is `python -u handler.py`.

## GHCR

Recommended registry target:

```text
ghcr.io/miherb/docling-runpod-worker:latest
```

Once the repo is on GitHub, the included workflow publishes to GHCR automatically on pushes to `main`.

RunPod can then pull the image directly from GHCR.
