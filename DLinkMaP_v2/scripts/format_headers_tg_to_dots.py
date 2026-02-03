import csv
import sys
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: python3 scripts/format_headers_tg_to_dots.py <input_csv> <output_csv>")
    sys.exit(2)

inp = Path(sys.argv[1])
out = Path(sys.argv[2])
out.parent.mkdir(parents=True, exist_ok=True)

rename = {
    "cross type": "cross.type",
    "female line": "female.line",
    "male line": "male.line",
    "food type": "food.type",
    "month crossed": "month.crossed",
    "cross number": "cross.number",
}

with inp.open(newline="") as f:
    reader = csv.DictReader(f)
    if reader.fieldnames is None:
        raise SystemExit("Input has no header row.")

    new_fieldnames = [rename.get(h, h) for h in reader.fieldnames]

    # Simple guardrails
    required = {"vial", "cross.type", "female.line", "male.line", "food.type",
                "month.crossed", "cross.number", "plate", "y"}
    if not required.issubset(set(new_fieldnames)):
        missing = sorted(required - set(new_fieldnames))
        raise SystemExit(f"Missing required columns after renaming: {missing}\n"
                         f"Got columns: {new_fieldnames}")

    with out.open("w", newline="") as g:
        writer = csv.DictWriter(g, fieldnames=new_fieldnames)
        writer.writeheader()
        for row in reader:
            # Rename keys in each row
            row2 = {}
            for k, v in row.items():
                row2[rename.get(k, k)] = v
            writer.writerow(row2)

print("Wrote:", out)
print("Header:", ",".join(new_fieldnames))
