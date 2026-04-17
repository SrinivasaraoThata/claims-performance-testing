import os
import subprocess
import yaml
from pathlib import Path

class JMeterRunner:
    def __init__(self, jmeter_home=None):
        self.jmeter_home = jmeter_home or os.environ.get('JMETER_HOME')
        
        # Check for JMETER_HOME early, unless we are doing a dry run
        if not self.jmeter_home and os.environ.get("PERF_DRY_RUN") != "true":
            raise RuntimeError("JMETER_HOME environment variable is not set. Please install JMeter and set JMETER_HOME (or set PERF_DRY_RUN=true).")
        
    def _read_scenario(self, scenario_name):
        scenario_path = Path("config/scenarios.yml")
        with open(scenario_path, "r") as f:
            scenarios = yaml.safe_load(f)
        return scenarios.get(scenario_name, scenarios["smoke"])

    def _read_base_config(self):
        base_path = Path("config/base.yml")
        with open(base_path, "r") as f:
            return yaml.safe_load(f)

    def run_plan(self, jmx_file_path, scenario_name, output_jtl_path):
        scenario = self._read_scenario(scenario_name)
        base_cfg = self._read_base_config()
        
        Path(output_jtl_path).parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(output_jtl_path):
            os.remove(output_jtl_path)

        cmd = [
            f"-Jhost={base_cfg['host']}",
            f"-Jport={base_cfg['port']}",
            f"-Jprotocol={base_cfg['protocol']}",
            f"-Jthreads={scenario['threads']}",
            f"-Jrampup={scenario['rampup']}",
            f"-Jduration={scenario['duration']}"
        ]

        if os.environ.get("PERF_DRY_RUN") == "true":
            print(f"[DRY RUN] Would execute jmeter: {' '.join(cmd)}")
            import shutil
            fixture_path = Path("jmeter/results/sample.jtl")
            if not fixture_path.exists():
                raise FileNotFoundError(f"Dry run fixture not found: {fixture_path}")
            shutil.copy(fixture_path, output_jtl_path)
            return True

        jmeter_bin = Path(self.jmeter_home) / "bin" / "jmeter"
        if os.name == 'nt':
            jmeter_bin = jmeter_bin.with_suffix('.bat')
            
        if not jmeter_bin.exists():
            raise RuntimeError(f"JMeter binary not found at {jmeter_bin}. Please verify your JMETER_HOME path.")

        cmd = [str(jmeter_bin), "-n", "-t", str(jmx_file_path), "-l", str(output_jtl_path)] + cmd

        try:
            print(f"Running JMeter with command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            print(f"JMeter test failed: {e.stderr.decode()}")
            return False
