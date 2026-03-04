# Product Requirements Document: Automated Log Analyzer

## Project Overview

- **Goal:** Reduce Mean Time to Resolution (MTTR) by automating log ingestion and root cause analysis.
- **Target Environment:** AWS S3 (Cloud-native).
- **Role Focus:** Technical Analyst / Production Support.

## Technical Requirements

- **Language:** Python 3.x.
- **Cloud Integration:** Use `boto3` for all AWS S3 interactions (Upload/Download).
- **Data Parsing:** Use the `re` (Regular Expressions) library to isolate HTTP `500` (Internal Server Error) and `503` (Service Unavailable) status codes.
- **Input Data:** 10,000 lines of simulated Apache-style server logs.
- **Output Format:** A structured `incident_report.json` file summarizing error counts per IP address.

## Success Metrics

- Successful ingestion of data from a local script to a remote AWS S3 bucket.
- Accurate identification of "failing nodes" (IP addresses) without manual log reading.
- Zero external database dependencies (keep it lightweight and script-based).

## Out of Scope (Do Not Build)

- No web frontend or UI.
- No SQL or NoSQL databases.
- No complex libraries like Pandas or Spark.