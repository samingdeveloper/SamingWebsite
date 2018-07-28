import pytest
import signal
from gr import _dat
#def pytest_collection_modifyitems(items):
#    for item in items:
#        if item.get_marker('timeout') is None:
#            item.add_marker(pytest.mark.timeout(3))

#@pytest.fixture(scope = 'session')
#def _dat(): #global_data
#	return {	
#				"case":[],
#				"score":0,
#				"max":0,
#				"level":0,
#			}

class Termination(SystemExit):
	pass


class TimeoutExit(BaseException):
	pass


def _terminate(signum, frame):
	raise Termination("Runner is terminated from outside.")


def _timeout(signum, frame):
	_dat._dat['case'].append("timeout")
	raise TimeoutExit("Runner timeout is reached, runner is terminating.")


@pytest.hookimpl
def pytest_addoption(parser):
	parser.addoption(
		'--timeout', action='store', dest='timeout', type=int, default=None,
		help="number of seconds before each test failure")


@pytest.hookimpl
def pytest_configure(config):
	# Install the signal handlers that we want to process.
	signal.signal(signal.SIGTERM, _terminate)
	signal.signal(signal.SIGALRM, _timeout)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):

	# Set the per-test timeout (an alarm signal).
	if item.config.option.timeout is not None:
		signal.alarm(item.config.option.timeout)

	try:
		# Run the setup, test body, and teardown stages.
		yield
	finally:
		# Disable the alarm when the test passes or fails.
		# I.e. when we get into the framework's body.
		signal.alarm(0)