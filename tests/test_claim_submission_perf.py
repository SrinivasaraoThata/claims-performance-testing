import os
from pathlib import Path

import pytest

@pytest.mark.smoke
@pytest.mark.load
def test_claim_submission_load(scenario, jmeter_runner, parser, validator):
    jmx_path = Path("jmeter/test-plans/claim_submission_load.jmx")
    jtl_path = Path(f"target/results/claim_submission_load_{scenario}.jtl")
    
    # Run JMeter
    success = jmeter_runner.run_plan(jmx_path, scenario, jtl_path)
    assert success, "JMeter run failed"
    
    # Parse results
    metrics = parser.parse(jtl_path)
    
    # Validate against SLA
    validator.validate("claim_submission", scenario, metrics)
