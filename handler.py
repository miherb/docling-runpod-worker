import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from docling_runpod_worker.callbacks import post_callback
from docling_runpod_worker.schema import ErrorInfo, JobResponse, parse_request


MODE_TO_RUN = os.getenv("MODE_TO_RUN", "pod").strip().lower()


def handler(event: dict) -> dict:
    from docling_runpod_worker.extractor import extract_from_job

    try:
        request = parse_request(event)
    except Exception as exc:
        job_id = None
        raw_input = event.get("input", {}) if isinstance(event, dict) else {}
        if isinstance(raw_input, dict):
            job_id = raw_input.get("job_id")
        return JobResponse.failure(
            job_id=job_id,
            error=ErrorInfo(code="BAD_REQUEST", message=str(exc)),
        ).to_dict()

    try:
        result = extract_from_job(request)
        response = JobResponse.success(request.job_id, result)
    except Exception as exc:
        response = JobResponse.failure(
            job_id=request.job_id,
            error=ErrorInfo(code="EXTRACTION_FAILED", message=str(exc)),
        )

    if request.callback_url:
        try:
            post_callback(request, response)
        except Exception as exc:
            payload = response.to_dict()
            payload["callback_error"] = str(exc)
            return payload

    return response.to_dict()


def _run_local_test() -> None:
    if len(sys.argv) > 1 and sys.argv[1].startswith("{"):
        event = json.loads(sys.argv[1])
    else:
        event = {
            "input": {
                "job_id": "local-smoke-test",
                "pdf_url": os.getenv("LOCAL_TEST_PDF_URL", ""),
            }
        }
    print(json.dumps(handler(event), indent=2))


def _warmup() -> None:
    print(json.dumps({"event": "warmup_start"}), flush=True)
    try:
        from docling_runpod_worker.extractor import get_converter
        get_converter()
        print(json.dumps({"event": "warmup_done"}), flush=True)
    except Exception as exc:
        print(json.dumps({"event": "warmup_failed", "error": str(exc)}), flush=True)


if __name__ == "__main__":
    print(json.dumps({"event": "worker_starting", "mode": MODE_TO_RUN}), flush=True)
    if MODE_TO_RUN == "serverless":
        import runpod

        runpod.serverless.start({"handler": handler})
    else:
        _run_local_test()
