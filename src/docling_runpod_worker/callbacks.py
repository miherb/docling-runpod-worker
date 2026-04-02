from __future__ import annotations

import requests

from docling_runpod_worker.config import CONFIG
from docling_runpod_worker.schema import JobRequest, JobResponse


def post_callback(request: JobRequest, response: JobResponse) -> None:
    if not request.callback_url:
        return

    headers = {"Content-Type": "application/json"}
    if request.callback_secret:
        headers["Authorization"] = f"Bearer {request.callback_secret}"

    callback_response = requests.post(
        request.callback_url,
        json=response.to_dict(),
        headers=headers,
        timeout=CONFIG.callback_timeout_seconds,
    )
    callback_response.raise_for_status()
