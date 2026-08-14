from pathlib import Path

from analysis import build_executive_report_markdown, build_executive_summary
from data_loader import load_and_clean
import config


def main() -> None:
    df = load_and_clean(config.DEFAULT_DATA_FILE)
    summary = build_executive_summary(df)
    report_path = Path(config.REPORTS_DIR) / "executive_summary.md"
    report_path.write_text(build_executive_report_markdown(summary), encoding="utf-8")
    print(f"Executive report written to {report_path}")


if __name__ == "__main__":
    main()
