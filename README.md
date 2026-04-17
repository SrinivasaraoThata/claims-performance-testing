# Claims Performance Suite

The Performance testing pillar of the Claims application.
Built using JMeter to generate load and Python (pytest) to orchestrate runs, parse results, and assert SLA thresholds.

## Quick Start (Local Run Modes)

There are two ways to invoke the local performance tests:

### 1. With JMeter Installed (Full Execution)
Requires [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi) downloaded and extracted locally.
```powershell
$env:JMETER_HOME="C:\apache-jmeter-5.6.3"
pytest tests/ -m smoke -v --scenario smoke
```

### 2. Without JMeter (Validates framework wiring only)
This performs a dry-run bypassing JMeter execution. It copies a fixture JTL file to simulate scenario output, allowing the `jtl_parser` and `threshold_validator` logic to execute end-to-end without needing a local JMeter installation.
```powershell
$env:PERF_DRY_RUN="true"
pytest tests/ -m smoke -v --scenario smoke
```
