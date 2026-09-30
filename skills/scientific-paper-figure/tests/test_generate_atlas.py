from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "generate_atlas.py"
SPEC = importlib.util.spec_from_file_location("generate_atlas", SCRIPT)
assert SPEC and SPEC.loader
generate_atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_atlas)


class GenerateAtlasTests(unittest.TestCase):
    def test_generate_submits_once_and_downloads_result(self) -> None:
        calls: list[tuple[str, str]] = []

        def fake_request(method: str, url: str, **kwargs):
            calls.append((method, url))
            if url.endswith("/models"):
                return {
                    "data": [
                        {
                            "model": generate_atlas.DEFAULT_MODEL,
                            "display_console": True,
                        }
                    ]
                }
            if method == "POST":
                self.assertEqual(kwargs["payload"]["aspect_ratio"], "4:3")
                self.assertEqual(kwargs["api_key"], "secret")
                return {"data": {"id": "prediction-1"}}
            return {"data": {"status": "completed", "outputs": ["https://example.com/result.png"]}}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mechanism.png"
            with (
                mock.patch.dict(os.environ, {"ATLASCLOUD_API_KEY": "secret"}),
                mock.patch.object(generate_atlas, "request_json", side_effect=fake_request),
                mock.patch.object(generate_atlas, "download_output", side_effect=lambda _url, path: path.write_bytes(b"png")),
            ):
                result = generate_atlas.generate("mechanism diagram", output, aspect_ratio="4:3", interval=0)

            self.assertEqual(result, output)
            self.assertEqual(output.read_bytes(), b"png")
            self.assertEqual(sum(method == "POST" for method, _url in calls), 1)
            self.assertEqual([method for method, _url in calls], ["GET", "POST", "GET"])

    def test_poll_retries_transient_get_errors(self) -> None:
        responses = [
            urllib.error.URLError("temporary"),
            {"data": {"status": "processing"}},
            {"data": {"status": "completed", "outputs": ["https://example.com/result.png"]}},
        ]
        with (
            mock.patch.object(generate_atlas, "request_json", side_effect=responses),
            mock.patch.object(generate_atlas.time, "sleep"),
        ):
            url = generate_atlas.poll_prediction("secret", "prediction-1", 0, 30)
        self.assertEqual(url, "https://example.com/result.png")

    def test_missing_api_key_fails_before_network_access(self) -> None:
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(generate_atlas, "request_json") as request,
        ):
            with self.assertRaisesRegex(RuntimeError, "ATLASCLOUD_API_KEY"):
                generate_atlas.generate("prompt", Path("result.png"))
        request.assert_not_called()

    def test_existing_output_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mechanism.png"
            output.write_bytes(b"existing")
            with (
                mock.patch.dict(os.environ, {"ATLASCLOUD_API_KEY": "secret"}),
                mock.patch.object(generate_atlas, "request_json") as request,
            ):
                with self.assertRaisesRegex(RuntimeError, "already exists"):
                    generate_atlas.generate("prompt", output)
            self.assertEqual(output.read_bytes(), b"existing")
        request.assert_not_called()

    def test_failed_prediction_surfaces_provider_error(self) -> None:
        with mock.patch.object(
            generate_atlas,
            "request_json",
            return_value={"data": {"status": "failed", "error": "rejected"}},
        ):
            with self.assertRaisesRegex(RuntimeError, "rejected"):
                generate_atlas.poll_prediction("secret", "prediction-1", 0, 30)


if __name__ == "__main__":
    unittest.main()
