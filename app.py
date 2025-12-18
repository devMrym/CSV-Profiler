import streamlit as st
import csv
from io import StringIO
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown, write_json, write_markdown
from pathlib import Path
import json

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Week 01 • Day 04 — Streamlit GUI")
with st.sidebar:
    st.sidebar.header("Inputs")
    show_preview = st.checkbox("Show preview", value=True)

csv_file = st.file_uploader("Upload CSV", type=["csv"])
rows = []
report = None
csv_valid = False

if csv_file:
    csv_name = csv_file.name
    text = csv_file.getvalue().decode("utf-8-sig")
    file_like = StringIO(text)
    reader = csv.DictReader(file_like)
    rows = list(reader)

    if not rows:
        st.error('Cannot create a report: CSV file has no data.', icon="🚨")
    elif all(k == "" for k in reader.fieldnames):
        st.warning("No headers detected in the CSV.", icon="⚠️")
    else:
        csv_valid = True
        if show_preview:
            st.write("### File Preview:")
            st.write(f"#### File Name: {csv_name}")
            st.write(rows[:5])

if rows and csv_valid:
    if st.button("Generate report"):
        report = profile_rows(rows)
        st.session_state["report"] = report
        st.markdown(render_markdown(report))
        write_json(report, "report.json")
        write_markdown(report, "report.md")
        json_text = Path("report.json").read_text(encoding="utf-8")
        md_text = Path("report.md").read_text(encoding="utf-8")
        st.download_button("Get JSON", data=json_text, file_name="report.json")
        st.download_button("Get Markdown", data=md_text, file_name="report.md")

report = st.session_state.get("report")
if report:
    summary = report.get("summary", {})

    report_name = st.sidebar.text_input("Report name", value="report")
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_text = render_markdown(report)
    d1, d2 = st.columns(2)

    if st.button("Save to outputs/"):
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{report_name}.json").write_text(json_text, encoding="utf-8")
        (out_dir / f"{report_name}.md").write_text(md_text, encoding="utf-8")
        st.success(f"Saved outputs/{report_name}.json and outputs/{report_name}.md", icon="✅")
