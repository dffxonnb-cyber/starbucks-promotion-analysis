from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ANALYSIS_DIR = ROOT / "analysis"
NOTEBOOKS_DIR = ROOT / "analysis" / "notebooks"
ARTIFACTS_DIR = ROOT / "artifacts"
EXECUTED_DIR = ARTIFACTS_DIR / "executed_notebooks"
LOGS_DIR = ARTIFACTS_DIR / "logs"
DATA_DIR = ROOT / "data"
NOTEBOOK_DATA_DIR = ANALYSIS_DIR / "data"
JUPYTER_RUNTIME_DIR = ARTIFACTS_DIR / "jupyter_runtime"
JUPYTER_CONFIG_DIR = ARTIFACTS_DIR / "jupyter_config"
JUPYTER_DATA_DIR = ARTIFACTS_DIR / "jupyter_data"

DEFAULT_NOTEBOOKS = [
    "00_데이터_확인.ipynb",
    "01_데이터_전처리.ipynb",
    "02_데이터_조인.ipynb",
    "03_EDA_이상치_분석.ipynb",
    "04_오퍼_추천_ML.ipynb",
]
SCRAPING_NOTEBOOK = "98.스타벅스크롤링_260112.ipynb"
REQUIRED_INPUTS = ["portfolio.csv", "profile.csv", "transcript.csv"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the Starbucks notebook pipeline without modifying the source notebooks."
    )
    parser.add_argument(
        "--include-scraping",
        action="store_true",
        help="Run the optional scraping notebook before the main pipeline.",
    )
    parser.add_argument(
        "--clear-artifacts",
        action="store_true",
        help="Delete previous executed notebooks and logs before running.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop immediately when a notebook execution fails.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=-1,
        help="Per-notebook execution timeout in seconds. Default is -1 (no timeout).",
    )
    parser.add_argument(
        "--notebook",
        action="append",
        dest="selected_notebooks",
        default=[],
        help="Run only the specified notebook filename. Repeat to select multiple notebooks.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Directory containing the required Starbucks CSV files.",
    )
    parser.add_argument(
        "--skip-data-sync",
        action="store_true",
        help="Do not copy discovered input CSV files into this repository's data directory.",
    )
    return parser.parse_args()


def ensure_jupyter_available() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "nbconvert", "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "nbconvert is not available in the current Python environment. "
            "Install the notebook execution dependencies first."
        )


def resolve_notebooks(args: argparse.Namespace) -> list[Path]:
    notebook_names: list[str] = []
    if args.include_scraping:
        notebook_names.append(SCRAPING_NOTEBOOK)

    if args.selected_notebooks:
        notebook_names.extend(args.selected_notebooks)
    else:
        notebook_names.extend(DEFAULT_NOTEBOOKS)

    notebooks: list[Path] = []
    for name in notebook_names:
        notebook_path = NOTEBOOKS_DIR / name
        if not notebook_path.exists():
            raise SystemExit(f"Notebook not found: {notebook_path}")
        notebooks.append(notebook_path)
    return notebooks


def prepare_directories(clear_artifacts: bool) -> None:
    if clear_artifacts and ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR)

    EXECUTED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    JUPYTER_DATA_DIR.mkdir(parents=True, exist_ok=True)


def has_required_inputs(data_dir: Path) -> bool:
    return all((data_dir / filename).exists() for filename in REQUIRED_INPUTS)


def discover_input_directory() -> Path | None:
    workspace_root = ROOT.parents[1]
    search_roots = [
        ROOT,
        ROOT.parent,
        workspace_root,
        workspace_root / "01_projects",
    ]
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for filename in REQUIRED_INPUTS:
            for match in search_root.rglob(filename):
                parent = match.parent
                if has_required_inputs(parent):
                    return parent
    return None


def sync_input_data(args: argparse.Namespace) -> Path:
    source_dir = args.data_dir.resolve() if args.data_dir else None
    if source_dir and not source_dir.exists():
        raise SystemExit(f"Input data directory does not exist: {source_dir}")

    if not source_dir and has_required_inputs(NOTEBOOK_DATA_DIR):
        return NOTEBOOK_DATA_DIR

    if not source_dir and has_required_inputs(DATA_DIR):
        source_dir = DATA_DIR

    if not source_dir:
        source_dir = discover_input_directory()

    if source_dir is None:
        expected = ", ".join(REQUIRED_INPUTS)
        raise SystemExit(
            "Required input CSV files were not found. "
            f"Place {expected} in {DATA_DIR} or pass --data-dir."
        )

    if args.skip_data_sync:
        if source_dir == DATA_DIR or has_required_inputs(source_dir):
            return source_dir
        raise SystemExit(f"Input data directory does not contain all required files: {source_dir}")

    copied_files: list[str] = []
    for filename in REQUIRED_INPUTS:
        src = source_dir / filename
        root_dst = DATA_DIR / filename
        notebook_dst = NOTEBOOK_DATA_DIR / filename
        if not src.exists():
            raise SystemExit(f"Missing required file in input data directory: {src}")
        if not root_dst.exists() or src.resolve() != root_dst.resolve():
            shutil.copy2(src, root_dst)
        if not notebook_dst.exists() or src.resolve() != notebook_dst.resolve():
            shutil.copy2(src, notebook_dst)
            copied_files.append(filename)

    if copied_files:
        print(f"Copied input data into notebook data directory: {', '.join(copied_files)}")

    return NOTEBOOK_DATA_DIR


def print_preflight_summary(data_dir: Path, notebooks: list[Path], log_path: Path) -> None:
    print(f"Analysis working directory: {ANALYSIS_DIR}")
    print(f"Notebook source directory: {NOTEBOOKS_DIR}")
    print(f"Input data directory: {data_dir}")
    print(f"Executed notebook output: {EXECUTED_DIR}")
    print(f"Log file: {log_path}")
    print("Notebook order:")
    for notebook in notebooks:
        print(f"- {notebook.name}")


def build_nbconvert_command(notebook: Path, timeout: int) -> list[str]:
    return [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        str(Path("notebooks") / notebook.name),
        "--output",
        notebook.name,
        "--output-dir",
        str(EXECUTED_DIR),
        f"--ExecutePreprocessor.timeout={timeout}",
    ]


def run_notebook(notebook: Path, timeout: int, log_handle) -> int:
    command = build_nbconvert_command(notebook, timeout)
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[RUN] {notebook.name} ({started_at})")
    log_handle.write(f"\n=== {notebook.name} | START {started_at} ===\n")
    log_handle.write("COMMAND: " + " ".join(command) + "\n")
    log_handle.flush()
    env = dict(os.environ)
    env["JUPYTER_RUNTIME_DIR"] = str(JUPYTER_RUNTIME_DIR)
    env["JUPYTER_CONFIG_DIR"] = str(JUPYTER_CONFIG_DIR)
    env["JUPYTER_DATA_DIR"] = str(JUPYTER_DATA_DIR)

    result = subprocess.run(
        command,
        cwd=ANALYSIS_DIR,
        env=env,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )

    finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "OK" if result.returncode == 0 else f"FAILED ({result.returncode})"
    print(f"[{status}] {notebook.name} ({finished_at})")
    log_handle.write(f"=== {notebook.name} | END {finished_at} | {status} ===\n")
    log_handle.flush()
    return result.returncode


def main() -> int:
    args = parse_args()
    ensure_jupyter_available()
    notebooks = resolve_notebooks(args)
    prepare_directories(clear_artifacts=args.clear_artifacts)
    data_dir = sync_input_data(args)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"run_pipeline_{timestamp}.log"
    failures: list[tuple[str, int]] = []

    print_preflight_summary(data_dir=data_dir, notebooks=notebooks, log_path=log_path)

    with log_path.open("w", encoding="utf-8") as log_handle:
        for notebook in notebooks:
            return_code = run_notebook(notebook, timeout=args.timeout, log_handle=log_handle)
            if return_code != 0:
                failures.append((notebook.name, return_code))
                if args.stop_on_error:
                    break

    if failures:
        print("\nPipeline finished with errors:")
        for notebook_name, return_code in failures:
            print(f"- {notebook_name}: exit code {return_code}")
        print(f"See log: {log_path}")
        return 1

    print("\nPipeline completed successfully.")
    print(f"Executed notebooks saved to: {EXECUTED_DIR}")
    print(f"Log saved to: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
