import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from handler import handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Docling worker locally.")
    parser.add_argument("--pdf-url", required=True, help="Publicly reachable PDF URL")
    parser.add_argument("--job-id", default="local-test", help="Job identifier")
    parser.add_argument("--callback-url", help="Optional callback URL")
    parser.add_argument("--callback-secret", help="Optional callback bearer secret")
    parser.add_argument("--source-url", help="Alternate alias for --pdf-url")
    args = parser.parse_args()

    event = {
        "input": {
            "job_id": args.job_id,
            "pdf_url": args.pdf_url,
            "source_url": args.source_url,
            "callback_url": args.callback_url,
            "callback_secret": args.callback_secret,
        }
    }

    print(json.dumps(handler(event), indent=2))


if __name__ == "__main__":
    main()
