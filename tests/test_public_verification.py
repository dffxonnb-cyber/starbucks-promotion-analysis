from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = load_module("check_public_artifacts", ROOT / "scripts" / "check_public_artifacts.py")
        cls.pipeline = load_module("run_pipeline", ROOT / "run_pipeline.py")

    def test_public_artifact_checker_passes(self) -> None:
        self.assertEqual(self.artifacts.main(), 0)

    def test_pipeline_notebook_sequence_is_declared_and_present(self) -> None:
        notebooks = [self.pipeline.NOTEBOOKS_DIR / name for name in self.pipeline.DEFAULT_NOTEBOOKS]
        self.assertGreaterEqual(len(notebooks), 5)
        missing = [path for path in notebooks if not path.exists()]
        self.assertEqual(missing, [])

    def test_required_inputs_are_documented_but_not_tracked(self) -> None:
        self.assertEqual(self.pipeline.REQUIRED_INPUTS, ["portfolio.csv", "profile.csv", "transcript.csv"])
        self.assertTrue((ROOT / "VERIFY.md").exists())
        self.assertTrue((ROOT / "AUTOMATION_GUIDE.md").exists())


if __name__ == "__main__":
    unittest.main()
