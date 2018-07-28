import pytest
import importlib
import sys
from gr import _dat
#import 
############################################ Initialize Section ############################################
prob = importlib.import_module("import_lib")
#print(prob.a(2))
def write(status,e=None): #write(status,score=0,level=0,e=None)
	if status == "pass":
		if 0 <= _dat._dat['level']  <= 1:
			_dat._dat['case'].append(status)
			_dat._dat['score']+=5
	elif status == "fail":
		if _dat._dat['level'] == 0:
			_dat._dat['case'].append(str(e))
		elif _dat._dat['level'] == 1:
			_dat._dat['case'].append("fail")	
		pytest.fail(str(e))
	else:
		_dat._dat['case'].append("timeout")

@pytest.yield_fixture(scope='session', autouse=True)
def finalizer():
	# Will be executed before the first test
	yield
	# Will be executed after the last test
	sys.stderr.write(str(_dat._dat))
	#sys.stderr.write(str(pytest.score))

#def setup_function(function):
	#print ("setting up %s" % function)
	#prob = importlib.import_module(fileName[:-3])
############################################ TEST Section ############################################
def test_1():
	#while(1):pass
	try:
		assert prob.a(2) == 1 #assert prob.function(n) == expected
		write("pass") #write("pass",score,level)
	except Exception as e:
		write("fail",e) #write("pass",score,level,e)

def test_2():
	while(1):pass
	assert 1 == 1
	write("pass")
	#print(pytest.score)

def test_3():
	#while(1):pass
	assert 1 == 1
	write("pass")

def test_4():
	#while(1):pass
	try:
		assert 2 == 1 #assert prob.function(n) == expected
		write("pass") #write("pass",score,level)
	except Exception as e:
		write("fail",e) #write("pass",score,level,e)
#sys.stderr.write(str(case))