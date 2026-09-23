from pathlib import Path
import pandas as pd

from evidently import Report
from evidently.presets import DataDriftPreset

BASE_DIR = Path(__file__).resolve().parent.parent

reference = pd.read_csv(BASE_DIR / "data" / "reference.csv")
current = pd.read_csv(BASE_DIR / "data" / "current.csv")

report = Report(metrics=[DataDriftPreset()])

report.run(
    reference_data=reference,
    current_data=current,
)

print(report)

print("=" * 50)
print("Drift analysis completed")
print("=" * 50)
