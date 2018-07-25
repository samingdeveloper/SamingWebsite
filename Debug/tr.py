import time
uin = input(">> ")
try:
	stop_time = abs(int(uin))
except KeyboardInterrupt:
	#break
	pass
except:
	print("NaN")

if stop_time:
	print("yes")
	stop_time = ''

if stop_time:
	print("yess")
else:
	print("its null")
'''while stop_time > 0:
	m, s = divmod(stop_time, 60)
	time.sleep(1)
	print(m)
	print(s)'''