#!/usr/bin/env python3
"""Generate a scientific figure through the optional Atlas Cloud provider."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.atlascloud.ai"
DEFAULT_MODEL = "google/nano-banana-2-lite/text-to-image-developer"
TERMINAL_SUCCESS = {"completed", "succeeded"}
TERMINAL_FAILURE = {"failed", "timeout", "canceled", "cancelled"}


def request_json(
    method: str,
    url: str,
    *,
    api_key: str | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 30,
) -> dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "User-Agent": "scientific-visual-skills/1.0",
    }
    data = None
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        decoded = json.loads(response.read().decode("utf-8"))
    if not isinstance(decoded, dict):
        raise RuntimeError(f"Expected a JSON object from {url}")
    return decoded


def iter_objects(value: Any):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from iter_objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_objects(item)


def validate_model(model: str) -> None:
    catalog = request_json("GET", f"{API_BASE}/api/v1/models")
    match = next(
        (
            item
            for item in iter_objects(catalog)
            if (item.get("model") or item.get("id")) == model
        ),
        None,
    )
    if match is None:
        raise RuntimeError(f"Model is not present in the live Atlas Cloud catalog: {model}")
    if match.get("display_console") is not True:
        raise RuntimeError(f"Model is not currently enabled in Atlas Cloud: {model}")


def poll_prediction(api_key: str, prediction_id: str, interval: float, timeout: float) -> str:
    deadline = time.monotonic() + timeout
    transient_errors = 0
    while time.monotonic() < deadline:
        try:
            response = request_json(
                "GET",
                f"{API_BASE}/api/v1/model/prediction/{prediction_id}",
                api_key=api_key,
            )
            transient_errors = 0
        except (urllib.error.URLError, TimeoutError):
            transient_errors += 1
            if transient_errors > 3:
                raise
            time.sleep(2 ** (transient_errors - 1))
            continue

        data = response.get("data") or {}
        status = str(data.get("status") or "").lower()
        if status in TERMINAL_SUCCESS:
            outputs = data.get("outputs") or []
            if not outputs or not isinstance(outputs[0], str):
                raise RuntimeError("Atlas Cloud completed without an output URL")
            return outputs[0]
        if status in TERMINAL_FAILURE:
            raise RuntimeError(str(data.get("error") or f"Generation ended with status {status}"))
        time.sleep(interval)

    raise TimeoutError(f"Prediction {prediction_id} did not finish within {timeout:g}s")


def download_output(url: str, output: Path) -> None:
    if not url.startswith(("https://", "http://")):
        raise RuntimeError("Atlas Cloud returned an unsupported output URL")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".part")
    with urllib.request.urlopen(url, timeout=60) as response:
        temporary.write_bytes(response.read())
    temporary.replace(output)


def generate(
    prompt: str,
    output: Path,
    *,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "16:9",
    interval: float = 3,
    timeout: float = 180,
) -> Path:
    api_key = os.environ.get("ATLASCLOUD_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ATLASCLOUD_API_KEY is required")
    if output.suffix.lower() != ".png":
        raise RuntimeError("--output must use a .png filename")
    if output.exists():
        raise RuntimeError(f"Output already exists; choose a new semantic filename: {output}")

    validate_model(model)
    # Submit exactly once. Retrying this POST can create duplicate billable jobs.
    response = request_json(
        "POST",
        f"{API_BASE}/api/v1/model/generateImage",
        api_key=api_key,
        payload={
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": "1k",
        },
    )
    prediction_id = str((response.get("data") or {}).get("id") or "")
    if not prediction_id:
        raise RuntimeError(str(response.get("message") or "Atlas Cloud did not return a prediction ID"))

    result_url = poll_prediction(api_key, prediction_id, interval, timeout)
    download_output(result_url, output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Complete scientific figure prompt")
    parser.add_argument("--output", type=Path, required=True, help="Semantic .png output path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Atlas Cloud image model ID")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--poll-interval", type=float, default=3)
    parser.add_argument("--timeout", type=float, default=180)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = generate(
            args.prompt,
            args.output,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            interval=args.poll_interval,
            timeout=args.timeout,
        )
    except (RuntimeError, TimeoutError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
