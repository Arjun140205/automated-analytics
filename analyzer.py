import re
import json
import boto3
from collections import defaultdict

S3_BUCKET = "ion-telemetry-bucket-arjunbir"
S3_KEY = "logs/server_logs.txt"
LOCAL_LOG_FILE = "server_logs.txt"
REPORT_FILE = "incident_report.json"

ERROR_PATTERN = re.compile(
    r'^(\d+\.\d+\.\d+\.\d+)\s.*"\w+\s\S+\sHTTP/\d\.\d"\s(500|503)\s'
)


def download_from_s3(bucket, key, filepath):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, filepath)
    print(f"[✓] Downloaded s3://{bucket}/{key} → {filepath}")


def parse_errors(filepath):
    error_counts = defaultdict(lambda: {"500": 0, "503": 0, "total": 0})

    with open(filepath, "r") as f:
        for line in f:
            match = ERROR_PATTERN.match(line)
            if match:
                ip = match.group(1)
                status = match.group(2)
                error_counts[ip][status] += 1
                error_counts[ip]["total"] += 1

    return error_counts


def build_report(error_counts):
    sorted_ips = sorted(error_counts.items(), key=lambda x: x[1]["total"], reverse=True)

    report = {
        "report_title": "Automated Incident Report — HTTP 500 & 503 Errors",
        "total_failing_ips": len(sorted_ips),
        "total_errors": sum(v["total"] for _, v in sorted_ips),
        "failing_nodes": [
            {
                "ip_address": ip,
                "http_500_count": counts["500"],
                "http_503_count": counts["503"],
                "total_errors": counts["total"],
            }
            for ip, counts in sorted_ips
        ],
    }
    return report


def save_report(report, filepath):
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[✓] Incident report saved → {filepath}")
    print(f"    Failing IPs : {report['total_failing_ips']}")
    print(f"    Total errors: {report['total_errors']}")


if __name__ == "__main__":
    download_from_s3(S3_BUCKET, S3_KEY, LOCAL_LOG_FILE)
    error_counts = parse_errors(LOCAL_LOG_FILE)
    report = build_report(error_counts)
    save_report(report, REPORT_FILE)
