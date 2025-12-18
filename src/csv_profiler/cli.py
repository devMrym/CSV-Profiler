import json
import time
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

#added so it can work with command (uv run python -m csv_profiler.cli profile data/sample.csv --out-dir outputs) 
@app.callback()

def main():
    """CSV Profiler CLI"""
    pass

@app.command(help="Profile a CSV file and write JSON + Markdown")

def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
    fail_missing: bool = typer.Option(False, "--fail-on-missing-pct", help="Print a short summary"),
):
    read_csv = read_csv_rows(input_path)

    report = profile_rows(read_csv)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = Path(out_dir, f"{report_name}.json")
    
    json_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    md_path = Path(out_dir, f"{report_name}.md")
    md_path.write_text(
            render_markdown(report),
            encoding="utf-8",
        )
    print(f"Wrote {json_path} and {md_path}")

    if preview:
        typer.echo("## Preview of report:")
        typer.echo(render_markdown(report))


    

if __name__ == "__main__":
    app()

