import csv
import os
from datetime import datetime

LOG_FILE = "prediction_logs.csv"

def log_prediction(cylinders, horsepower, weight, acceleration, prediction):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "cylinders",
                "horsepower",
                "weight",
                "acceleration",
                "prediction"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cylinders,
            horsepower,
            weight,
            acceleration,
            prediction
        ])