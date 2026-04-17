import os
from pathlib import Path

import pytest

@pytest.mark.smoke
@pytest.mark.spike
def test_historical_retrieval_spike(scenario, jmeter_runner, parser, validator):
    jmx_path = Path("jmeter/test-plans/historical_retrieval_spike.jmx")
    jtl_path = Path(f"target/results/historical_retrieval_spike_{scenario}.jtl")
    
    # Run JMeter
    success = jmeter_runner.run_plan(jmx_path, scenario, jtl_path)
    assert success, "JMeter run failed"
    
    # Parse results
    metrics = parser.parse(jtl_path)
    
    # Validate against SLA
    validator.validate("historical_retrieval", scenario, metrics)
