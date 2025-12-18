from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json


def write_json(report: dict, path: str | Path) -> None:
    """
    Write the report as a JSON file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


def write_markdown(report: dict, path: str | Path) -> None:
    """
    Write the report as a Markdown file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows_count = report["n_rows"]
    columns_count = report["n_columns"]

    with open(path, "w", encoding="utf-8") as f:
        # Header
        f.write("# CSV Profiling Report\n\n")
        f.write(f"- Rows: {rows_count}\n")
        f.write(f"- Columns: {columns_count}\n\n")

        # Summary table
        f.write("| Column Name | Type | Missing % | Unique |\n")
        f.write("| ----------- | ---- | --------- | ------ |\n")
        for col_info in report["columns"]:
            f.write(
                f"| {col_info['name']} | {col_info['type']} | {col_info['missing_pct']:.2f} | {col_info['unique']} |\n"
            )
        f.write("\n")

        # Detailed column stats
        for col_info in report["columns"]:
            f.write(f"## Column: {col_info['name']}\n")
            f.write(f"- Type: {col_info['type']}\n")
            f.write(f"- Missing: {col_info['missing']} ({col_info['missing_pct']:.2f}%)\n")
            f.write(f"- Unique: {col_info['unique']}\n")

            stats = col_info.get("stats", {})
            if col_info["type"] == "number":
                f.write(f"- Min: {stats.get('min')}\n")
                f.write(f"- Max: {stats.get('max')}\n")
                f.write(f"- Mean: {stats.get('mean')}\n")
            else:
                f.write("- Top values:\n")
                for val, count in stats.get("top", []):
                    f.write(f"  - {val}: {count}\n")
            f.write("\n")


def render_markdown(report: dict) -> str:
    """
    Render the report as a Markdown string (for Streamlit display).
    """
    lines: list[str] = []

    rows = report["n_rows"]
    cols = report["n_columns"]

    lines.append(f"# CSV Profiling Report\n")

    # Summary
    lines.append("## Summary\n")
    lines.append(f"- Number Of Rows: **{rows}**")
    lines.append(f"- Number Of Columns: **{cols}**\n")

    # Columns table
    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")

    for col in report["columns"]:
        lines.append(
            f"| {col['name']} | {col['type']} | {col['missing']} | {col['missing_pct']:.2f} | {col['unique']} |"
        )

    lines.append("")

    # Notes
    lines.append("## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)
