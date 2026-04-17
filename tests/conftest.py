import pytest
from utils.jmeter_runner import JMeterRunner
from utils.jtl_parser import JTLParser
from utils.threshold_validator import ThresholdValidator

def pytest_addoption(parser):
    parser.addoption("--scenario", action="store", default="smoke", help="Performance scenario to run: smoke, load, stress, spike")

@pytest.fixture(scope="session")
def scenario(request):
    return request.config.getoption("--scenario")

@pytest.fixture(scope="session")
def jmeter_runner():
    return JMeterRunner()

@pytest.fixture(scope="session")
def parser():
    return JTLParser()

@pytest.fixture(scope="session")
def validator():
    return ThresholdValidator()
