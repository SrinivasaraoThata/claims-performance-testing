import os
from pathlib import Path

def test_adjudication_status_stress(scenario, jmeter_runner, parser, validator):
    jmx_path = Path("jmeter/test-plans/adjudication_status_stress.jmx")
    jtl_path = Path(f"target/results/adjudication_status_stress_{scenario}.jtl")
    
    # Run JMeter
    success = jmeter_runner.run_plan(jmx_path, scenario, jtl_path)
    assert success, "JMeter run failed"
    
    # Parse results
    metrics = parser.parse(jtl_path)
    
    # Validate against SLA
    validator.validate("adjudication_status", scenario, metrics)
