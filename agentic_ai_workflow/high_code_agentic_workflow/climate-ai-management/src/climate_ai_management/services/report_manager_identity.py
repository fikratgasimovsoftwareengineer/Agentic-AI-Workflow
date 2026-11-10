import hashlib
import json


def generate_report_id(report: dict) -> str:
    """Generate a deterministic SHA-256 identifier for a report."""

    serialized_report = json.dumps(
        report,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )

    return hashlib.sha256(
        serialized_report.encode("utf-8")
    ).hexdigest()