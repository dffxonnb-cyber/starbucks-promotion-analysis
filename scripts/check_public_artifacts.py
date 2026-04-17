from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "한페이지_요약.md",
    ROOT / "docs" / "reproducibility_and_validation.md",
    ROOT / "docs" / "images" / "dashboard-overview.png",
    ROOT / "docs" / "images" / "menu-recommendation-dashboard.png",
    ROOT / "docs" / "images" / "event-distribution.png",
    ROOT / "docs" / "images" / "offer-channel-coverage.png",
    ROOT / "docs" / "images" / "offer-type-volume.png",
    ROOT / "스벅_최종_통합본.twb",
    ROOT / "run_pipeline.py",
]


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        print("Missing required public review artifacts:")
        for path in missing:
            print(f"- {path.relative_to(ROOT)}")
        return 1

    print("Public review artifacts verified:")
    for path in REQUIRED_PATHS:
        print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
