# typo error in import
import subprocess
import os
import codecs

import threading
from multiprocessing.dummy import Pool as ThreadPool
import time


with open('d.txt', 'r') as file:
		num =file.read().splitlines()

num= list(dict.fromkeys(num))
num_len=len(num)

active=[]
inactive=[]
Failed_IP =[]
FailedExceptionIps=[]
def Ping_Test(num) :
	# with open(os.devnull, "wb") as limbo:
		ip= num
		try :	
			result=subprocess.Popen(["ping", "-c", "10", "-n", "-W", "20", ip]).wait()
			print ("Result")
			print (result)
			if result:
				print (ip, "inactive")
				inactive.append(ip)
			else:
				print (ip, "active")
				active.append(ip)
		except Exception as e :
			print (f"Exception {e} for IP {ip}")
			Failed_IP.append(ip)

# def Ping_Test(num) :
# 	with open(os.devnull, "wb") as limbo:
# 		# for n in num:
# 		ip= num
# 		try :	
# 			result=subprocess.Popen(["ping", "-c", "20", "-n", "-W", "30", ip],
# 				stdout=limbo, stderr=limbo).wait()
# 			if result:
# 				print (ip, "inactive")
# 				inactive.append(ip)
# 			else:
# 				print (ip, "active")
# 				active.append(ip)
# 		except Exception as e :
# 			print (f"Exception {e} for IP {ip}")
# 			Failed_IP.append(ip)

# num=["172.22.22.22","172.100.130.58"]
counter=0
for x in num:
		if not x :
			print (f"Continue it's empty {x}")
			continue
		counter+=1
		if (counter % 100)==0 :
			print ("\n\n\n\nsleep\n\n\n\n")
			time.sleep(10)
		print (f"\t\tWe are Processing this IP  {x}")
		try:
				my_thread = threading.Thread(target=Ping_Test, args=(x,))
				my_thread.start()
		except Exception:
				FailedExceptionIps.append(num[x])

main_thread = threading.currentThread()
for some_thread in threading.enumerate():
		if some_thread != main_thread:
				print(some_thread)
				some_thread.join()


 # new file for only new IPs
with open('active.txt', 'a') as file1:
	for i in active:
		file1.write((str(i)+"\n"))
file1.close()

with open('inactive.txt', 'a') as file2:
	for i in inactive:
		file2.write((str(i)+"\n"))
file2.close()


print ("Failed_IP")
for i in Failed_IP :
	print (f"Failed_IP {i}")



print ("\n\nFailedExceptionIps")
for i in FailedExceptionIps :
	print (f"FailedExceptionIps {i}")

print(f"\n\n length of num {num_len}")
print(f"\n length of active {len(active)}")
print(f"\n length of inactive {len(inactive)}")
print(f"\n length of Failed_IP {len(Failed_IP)}")
print(f"\n length of FailedExceptionIps {len(FailedExceptionIps)}")

result_sum =len(active) +len(inactive) +len(Failed_IP) +len(FailedExceptionIps)
print (f"\n result_sum is {str(result_sum)}")
