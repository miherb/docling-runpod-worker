from __future__ import annotations

import os
from dataclasses import dataclass


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class WorkerConfig:
    docling_num_threads: int = _int_env("DOCLING_NUM_THREADS", 8)
    omp_num_threads: int = _int_env("OMP_NUM_THREADS", 8)
    layout_batch_size: int = _int_env("DOCLING_LAYOUT_BATCH_SIZE", 512)
    table_batch_size: int = _int_env("DOCLING_TABLE_BATCH_SIZE", 64)
    queue_size: int = _int_env("DOCLING_QUEUE_SIZE", 256)
    pdf_download_timeout_seconds: int = _int_env("PDF_DOWNLOAD_TIMEOUT_SECONDS", 120)
    callback_timeout_seconds: int = _int_env("CALLBACK_TIMEOUT_SECONDS", 20)


CONFIG = WorkerConfig()
