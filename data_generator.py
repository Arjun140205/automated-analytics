import random
import datetime
import boto3

LOG_FILE = "server_logs.txt"
S3_BUCKET = "ion-telemetry-bucket-arjunbir"
S3_KEY = "logs/server_logs.txt"
NUM_LINES = 10_000

IP_POOL = [
    f"{random.randint(10, 220)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    for _ in range(50)
]

ENDPOINTS = [
    "/api/login",
    "/api/logout",
    "/api/signup",
    "/api/user/profile",
    "/api/user/settings",
    "/checkout",
    "/checkout/confirm",
    "/checkout/payment",
    "/api/products",
    "/api/products/search",
    "/api/cart",
    "/api/cart/add",
    "/api/orders",
    "/api/orders/history",
    "/api/inventory",
    "/api/notifications",
    "/healthcheck",
    "/dashboard",
    "/reports/daily",
    "/reports/monthly",
]

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]

STATUS_CODES = [200, 200, 200, 200, 200, 200, 301, 304, 400, 401, 403, 404, 404, 500, 503]

RESPONSE_SIZES = range(128, 65536)


def random_timestamp(start_year=2026, days_span=30):
    base = datetime.datetime(start_year, 1, 1)
    offset = datetime.timedelta(
        days=random.randint(0, days_span),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    dt = base + offset
    return dt.strftime("%d/%b/%Y:%H:%M:%S +0000")


def generate_log_line():
    ip = random.choice(IP_POOL)
    timestamp = random_timestamp()
    method = random.choice(HTTP_METHODS)
    endpoint = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    size = random.choice(RESPONSE_SIZES)
    return f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status} {size}'


def generate_logs(filepath, count):
    with open(filepath, "w") as f:
        for _ in range(count):
            f.write(generate_log_line() + "\n")
    print(f"[✓] Generated {count} log lines → {filepath}")


def upload_to_s3(filepath, bucket, key):
    s3 = boto3.client("s3")
    s3.upload_file(filepath, bucket, key)
    print(f"[✓] Uploaded {filepath} → s3://{bucket}/{key}")


if __name__ == "__main__":
    generate_logs(LOG_FILE, NUM_LINES)
    upload_to_s3(LOG_FILE, S3_BUCKET, S3_KEY)
