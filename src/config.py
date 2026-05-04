from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT_DIR / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"

PLATFORMS = ["Rappi", "Uber Eats", "DiDi Food"]

REFERENCE_PRODUCTS = [
    "Big Mac",
    "Combo mediano",
    "Nuggets 10 piezas",
    "Coca-Cola 500ml",
    "Agua 1L",
]

