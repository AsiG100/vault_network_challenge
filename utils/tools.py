import os
import json
import csv
from datetime import datetime


def format_date(date: str) -> str:
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d")

def export_data(data: list[dict]):
    root_path = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(root_path, ".."))
    output_path = os.path.join(root_dir, "output.json")

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def read_csv(file_path: str) -> list[dict]:
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        return list[list[str]](reader)

def cleanup_csv(file_path: str):
    root_path = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(root_path, ".."))
    csv_path = os.path.join(root_dir, file_path)
    if os.path.exists(csv_path):
        os.remove(csv_path)