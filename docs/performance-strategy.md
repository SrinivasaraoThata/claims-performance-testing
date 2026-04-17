# Claims Performance Testing Strategy

## Overview
This pillar validates the performance, scalability, and reliability of the Claims ecosystem using a hybrid Python + JMeter approach. JMeter acts as the load-generation engine, while Python (via `pytest`) orchestrates execution, parametrizes the environments, and validates the SLAs.

## Test Types & Scenarios
1. **Smoke (5 VUs)**: Run on every PR to validate that performance test scripts are functional and components respond well under minimal load.
2. **Load (50 VUs)**: Run nightly. Mimics anticipated peak concurrency to ensure the system handles normal operations efficiently.
3. **Stress (150 VUs)**: Run on-demand. Designed to push the system beyond normal bounds and find the breaking points.
4. **Spike (200 VUs burst)**: Run on-demand. Verifies the system's ability to maintain operations during sudden traffic bursts.

## Components & RTM Traceability
- **REQ-CLM-01**: Claim Submission Load (JMeter script: `claim_submission_load.jmx` + Python test: `test_claim_submission_perf.py`)
- **REQ-CLM-02**: Adjudication Status Stress (JMeter script: `adjudication_status_stress.jmx` + Python test: `test_adjudication_perf.py`)
- **REQ-HIS-01**: Historical Retrieval Spike (JMeter script: `historical_retrieval_spike.jmx` + Python test: `test_historical_retrieval_perf.py`)

## SLA Thresholds
Service Level Agreements (SLAs) are environment and scenario aware (configured in `config/sla_thresholds.yml`):
- **Submission**: p95 ≤ 2000ms
- **Historical Retrieval**: p95 ≤ 3000ms

## CI/CD Pipeline
GitHub Actions automatically pulls the required tools (Java 17 for JMeter, Python 3.11 for orchestration). JTL outputs are parsed by Pandas during execution, and detailed logs emphasize SLA breaches rather than raw tracebacks.
