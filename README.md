# Automated Log Analyzer & Root Cause Engine

A lightweight, cloud-native analytics pipeline that ingests server logs into AWS S3, isolates critical HTTP failures, and produces a structured incident report — reducing Mean Time to Resolution from hours to seconds.

**Author:** Arjunbir Singh

---

## The Business Problem

In production support, system outages are inevitable. When they hit, the clock starts.

The standard response involves an engineer manually SSH-ing into a server, tailing thousands of log lines, and visually scanning for failure patterns — a process that is slow, error-prone, and does not scale. During a real incident, every minute of downtime translates directly into lost revenue, breached SLAs, and degraded customer trust.

The core bottleneck is **Mean Time to Resolution (MTTR)**. It stays high not because the root cause is complex, but because *finding it* inside raw logs is a manual grind.

This tool eliminates that grind. It programmatically ingests 10,000 lines of server logs, uploads them to a centralized cloud store, pulls them back for analysis, and isolates every IP address responsible for HTTP `500` (Internal Server Error) and `503` (Service Unavailable) responses. The output is a clean, sorted JSON report that tells an on-call engineer exactly which nodes are failing and how badly — without reading a single log line.

---

## System Architecture

```
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│  data_generator   │  ───►  │     AWS S3        │  ───►  │    analyzer       │  ───►  │  incident_report  │
│  .py              │ Upload │  (boto3)          │Download│    .py            │ Output │  .json            │
│                   │        │                   │        │                   │        │                   │
│ 10,000 simulated  │        │ ion-telemetry-    │        │ Regex engine      │        │ Failing IPs       │
│ Apache log lines  │        │ bucket-arjunbir   │        │ isolates 500/503  │        │ sorted by severity│
└──────────────────┘        └──────────────────┘        └──────────────────┘        └──────────────────┘
```

**Data Flow:**

1. **Generate** — `data_generator.py` creates 10,000 realistic Apache-style log entries with randomized IPs, timestamps, endpoints, and a weighted mix of HTTP status codes. Saves to `server_logs.txt`.
2. **Upload** — The same script pushes the log file to an AWS S3 bucket via `boto3`, simulating a centralized log ingestion point.
3. **Download & Analyze** — `analyzer.py` pulls the log file back from S3, then runs a compiled regular expression against every line to extract entries with HTTP `500` or `503` status codes.
4. **Report** — Error counts are aggregated per IP address, sorted by severity (highest first), and written to `incident_report.json`.

---

## Tech Stack

| Layer             | Technology                  | Purpose                                      |
|-------------------|-----------------------------|----------------------------------------------|
| Language          | Python 3.x                  | Core scripting and orchestration              |
| Cloud Storage     | AWS S3 via `boto3`          | Centralized log ingestion and retrieval       |
| Pattern Matching  | `re` (Regular Expressions)  | Isolation of HTTP 500 and 503 error lines     |
| Data Output       | `json` (Standard Library)   | Structured incident report generation         |

No databases. No heavy frameworks. No external dependencies beyond `boto3`.

---

## Installation & Execution

**Prerequisites:** Python 3.x, an AWS account with S3 access, and configured AWS credentials (`aws configure`).

```bash
# Clone the repository
git clone https://github.com/Arjun140205/automated-analytics.git
cd automated-analytics

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Part 1 — Generate logs and upload to S3
python data_generator.py

# Part 2 — Download from S3, analyze, and generate the incident report
python analyzer.py
```

---

## Actionable Output

After execution, `incident_report.json` contains a structured breakdown of every failing node, sorted by error severity:

```json
{
  "report_title": "Automated Incident Report — HTTP 500 & 503 Errors",
  "total_failing_ips": 50,
  "total_errors": 1338,
  "failing_nodes": [
    {
      "ip_address": "128.149.253.20",
      "http_500_count": 20,
      "http_503_count": 15,
      "total_errors": 35
    },
    {
      "ip_address": "168.94.106.142",
      "http_500_count": 21,
      "http_503_count": 14,
      "total_errors": 35
    },
    {
      "ip_address": "72.128.255.74",
      "http_500_count": 17,
      "http_503_count": 17,
      "total_errors": 34
    }
  ]
}
```

An on-call engineer can immediately identify `128.149.253.20` and `168.94.106.142` as the highest-severity nodes — no log tailing, no guesswork.

---
