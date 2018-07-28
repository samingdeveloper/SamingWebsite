import subprocess
process = subprocess.Popen(['pytest','{}'.format("pt.py"),'--tb=line','-s','--timeout=5'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
ret_code = process.wait()
print(stdout.decode("utf-8"))
x = (stderr.decode("utf-8"))
#x = eval(x)
print(x,type(x))
