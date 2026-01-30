from pathlib import Path
import json
from typing import Dict, Any

DATA_FILE = Path(__file__).resolve().parent.parent / "patients.json"


def load_data() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data: Dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file)
