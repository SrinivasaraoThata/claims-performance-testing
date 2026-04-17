import yaml
from pathlib import Path

class ThresholdValidator:
    def __init__(self):
        with open(Path("config/sla_thresholds.yml"), "r") as f:
            self.thresholds = yaml.safe_load(f)

    def validate(self, api_name, scenario_name, metrics):
        if api_name not in self.thresholds or scenario_name not in self.thresholds[api_name]:
            raise ValueError(f"No SLA thresholds defined for {api_name} in scenario {scenario_name}")

        sla = self.thresholds[api_name][scenario_name]
        
        # Validate p95
        if metrics["p95"] > sla["p95"]:
            raise AssertionError(f"[SLA BREACH] p95 = {metrics['p95']:.2f}ms > limit {sla['p95']}ms (label={api_name})")
            
        # Validate error rate
        if metrics["error_rate"] > sla["error_rate"]:
            raise AssertionError(f"[SLA BREACH] error_rate = {metrics['error_rate']*100:.2f}% > limit {sla['error_rate']*100:.2f}% (label={api_name})")
            
        return True
