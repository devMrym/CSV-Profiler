from __future__ import annotations

def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Return a structured CSV profiling report."""
    if not rows:
        return {
            "source": None,
            "summary": {"rows": 0, "columns": 0},
            "columns": {}
        }

    row_count = len(rows)
    column_names = list(rows[0].keys())
    report_columns = {}

    for col_name in column_names:
        values = [row[col_name] for row in rows if row[col_name].strip() != ""]
        missing = row_count - len(values)
        col_type = infer_type(values)  
        stats = numeric_stats(values) if col_type == "number" else text_stats(values)
        report_columns[col_name] = {
            "type": col_type,
            "stats": stats,
            "missing": missing,
            "missing_pct": (missing / row_count) * 100 if row_count else 0.0,
            "unique": len(set(values))
        }

    return {
        "source": None,  
        "summary": {"rows": row_count, "columns": len(column_names)},
        "columns": report_columns
    }

#Day 2 task 1 add the functions is_missing, try_float, infer_type
def is_missing(value: str | None) -> bool:
    MISSING = {"", "na", "n/a", "null", "none", "nan"}
    if value is None:
        return True
    cleaned = value.strip().casefold()
    return cleaned in MISSING

def try_float(value: str) -> float | None:
    try:
        '''return float(value) or None is it fails'''
        turn_float = float(value)

        if isinstance(turn_float, float):
            return turn_float
        
    except ValueError:
        return None

def infer_type(value: list[str]) -> str:
    values = []
    for i in value:
        if is_missing(i) is False:
            values.append(i)

    for v in values:
        if try_float(v) is None:
            return "text"
        else:
            return "number"
            
# day2 task 2 extract column values(return one value per row, use row.get(col,""), keep as strings)
def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    value = []
    for row in rows:
        value.append(row.get(col, ""))
    return value

# day2 task 3 compute numeric stats
def numeric_stats(values: list[str]) -> dict:
    """compute stats for numeric column values (strings)"""
    Usable = [v for v in values if not is_missing(v)]
    nums = [try_float(v) for v in Usable]
    count = len(nums)

    return {
        "count":count,
        "unique": len(set(nums)),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums)/count,
        "missing": len(values) - len(Usable)
    }

# day2 task 4 compute text stats
def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    return {
        "count": len(usable),
        "unique": len(counts),
        "top": top,
        "missing": len(values) - len(usable)
    }
#day3 task 3 report keys n_rows and n_columns columns (list) checkpoint: profile_row(rows) return a json-serializable dict with keys n_rows, n_columns, columns (list of column names)
def profile_rows(rows:list[dict[str,str]]) -> dict:
    n_rows = len(rows)
    n_columns = list(rows[0].keys())
    #should have name, type, missing, missing pct, unique

    col_profiles = []
    for col in n_columns:
        values = [i.get(col,"") for i in rows]
        Usable = [v for v in values if not is_missing(v)]
        missing = len(values)-len(Usable)
        unique = len(set(Usable))

        profile = {
    
            "name": col,
            "type": infer_type(column_values(rows, col)),
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique
        }

        col_profiles.append(profile)
    
     
        
    return {"n_rows": n_rows, "n_columns": len(n_columns), "columns": col_profiles}


