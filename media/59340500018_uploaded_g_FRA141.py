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

# Test case1
print(asd(2))
# Out 4
# Score 5.5
# Break
# Test case2
print(dsa(2))
# Out 8
# Score 3.8
# Break
# Test case3
print(sda(2))
# Out 16
# Score 4
# Stop
