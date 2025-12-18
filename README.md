# CSV Profiler
Generate a profiling report for a CSV file.
# Features
- CLI: JSON + Markdown report
- Streamlit GUI: upload CSV + export reports

# Setup
- uv venv -p 3.11
- uv pip install -r requirements.txt

# Run CLI
## If you have a src/ folder, run this:
- for Mac/Linux:   
export PYTHONPATH=src
- for Windows:     
$env:PYTHONPATH="src"
#### then run this:
uv run python -m csv_profiler.cli profile data/sample.csv --out-dir outputs

 # Run GUI
 ## If you have a src/ folder, run this:
- for Mac/Linux:   
export PYTHONPATH=src
- for Windows:     
$env:PYTHONPATH="src"
#### then run this:
uv run python -m csv_profiler.cli profile data/sample.csv --out-dir outputs


# Smoke Test

1) Run the CLI:
# If you have a `src/` folder: set `PYTHONPATH=src` first
uv run python -m csv_profiler.cli profile data/sample.csv -out-dir outputs

2) Check the output files exist:

 # Mac/Linux
 ls outputs

 # Windows PowerShell
 dir outputs

 You should see `report.json` and `report.md`.
