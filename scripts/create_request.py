from datetime import datetime, timedelta
import json
import random
import time
import uuid

JSON_FILE = "requests.json"
PATH = "./statics"
LIMIT_ROW_IN_FILE = 10

class ValuesFixed:
    duration_time = [t / 1000 for t in range(10, 803)]  # seconds
    high_duration_time = [t / 1000 for t in range(900, 2000)]

def random_value(arr):
    val = random.choice(arr)
    return val

def write(row_data):
    """Write row data to json file"""
    path_to_write = f"{PATH}/{JSON_FILE}"
    print(f"Write: {row_data}")
    with open(path_to_write, "a") as f:
        json.dump(row_data, f)
        f.write("\n")

def generate(timestamp, index):
    if index % 3 == 0 and index != 0:
        duration_time = random_value(ValuesFixed.high_duration_time)
    else:
        duration_time = random_value(ValuesFixed.duration_time)
    row = {
        "timestamp": timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
        "request_id": str(uuid.uuid4()),
        "duration_time": duration_time
    }
    return row


def main():
    count = 0
    sleep_time = [x / 10 for x in range(1, 8)]
    timestamp = datetime(
        year=2024,
        month=2,
        day=22,
        hour=0,
        minute=0,
        second=0
    )
    while True:
        if count == LIMIT_ROW_IN_FILE:
            break
        row = generate(timestamp, count)
        timestamp = timestamp + timedelta(minutes=5)
        write(row_data=row)
        count += 1
        time.sleep(random_value(sleep_time))


if __name__ == "__main__":
    main()