from datetime import datetime
import json
import random
import time

# CONSTs
JSON_FILE = "request_data_with_anomaly_pod_instance.json"
PATH = "./statics"
LIMIT_ROW_IN_FILE = 14798 * 10


class ValuesFixed:
    controller_pods = ["pod-1", "pod-2"]
    paths = ["/home", "/users"]
    duration_time = [t / 1000 for t in range(10, 803)]  # seconds


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


def generate(anomaly_by_instance: bool):
    current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    row = {
        "timestamp": current_time,
        "path": random_value(ValuesFixed.paths),
        "method": "GET",
        "service_name": "process_log",
        "controller_pod": random_value(ValuesFixed.controller_pods),
        "duration_time": random_value(ValuesFixed.duration_time)
    }
    if anomaly_by_instance and row['controller_pod'] == 'pod-1' and row['path'] == '/users':
        row['duration_time'] = random_value([t / 1000 for t in range(1400, 1500)])
    return row


if __name__ == "__main__":
    count = 0
    sleep_time = [x / 10 for x in range(1, 8)]
    while True:
        if count == LIMIT_ROW_IN_FILE:
            break
        # generate anomaly data for pod-1 in path == '/users' with latency >= 900ms
        if count in range(10, 13) or count in range(10101, 10999) or count in range(14798, 14798 + 999):
            row = generate(anomaly_by_instance=True)
        else:
            row = generate(anomaly_by_instance=False)
        write(row_data=row)
        count += 1
        time.sleep(random_value(sleep_time))
    print("Done!")
