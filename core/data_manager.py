
import json, csv, os
from core.models import Crop

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(_file_)), "data")
EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(_file_)), "exports")

CROPS_FILE = os.path.join(DATA_DIR, "crops.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)

def load_crops():
    _ensure_dirs()
    if not os.path.exists(CROPS_FILE):
        return []
    with open(CROPS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Crop(**c) for c in data]

def save_crops(crops):
    _ensure_dirs()
    with open(CROPS_FILE, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in crops], f, indent=2)

def load_settings():
    _ensure_dirs()
    if not os.path.exists(SETTINGS_FILE):
        return {"weather_delay_days": 0}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    _ensure_dirs()
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def export_csv(crops):
    _ensure_dirs()
    file = os.path.join(EXPORT_DIR, "harvest_report.csv")
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "harvest_date", "sowing_date", "crop_type", "notes"]
        )
        writer.writeheader()
        for crop in crops:
            writer.writerow(crop.to_dict())
    return file