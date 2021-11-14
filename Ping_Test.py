# typo error in import
import subprocess
import os
import os.path
import codecs

import threading
from multiprocessing.dummy import Pool as ThreadPool
import time
from Useful_Fun import *  ### my Class of Functions
from Global_Variables import Global_Variables ## Call Class to set or Use global Variables

# ===============================================================
# ===============================================================

Class_of_Global_Variables=Global_Variables()

Directory_Path = Class_of_Global_Variables.Directory_Path
Source_IPs_File = Class_of_Global_Variables.Source_IP_File_for_Ping
Worked_and_Old_IPs_File = Class_of_Global_Variables.Pinged_New_and_Old_IP_File
Pass_IPs_to_File = Class_of_Global_Variables.Source_IP_File_for_Automation

# ===============================================================
# ===============================================================
print("\n\n==============================================")
print ("Welcome to Ping_Test Script")
print("==============================================\n\n")

fullpath_to_sourceIP=Directory_Path+'/'+Source_IPs_File
with open(fullpath_to_sourceIP, 'r') as file:
		num =file.read().splitlines()
file.close()

num= list(dict.fromkeys(num))
num_len=len(num)
print(f"\n Num length {num_len} is no Validated yet")
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
				print (ip, "   :( inactive :( ")
				inactive.append(ip)
			else:
				print (ip, "  ^_^ active ^_^")
				active.append(ip)
		except Exception as e :
			print (f"Exception {e} for IP {ip}")
			Failed_IP.append(ip)

# def Ping_Test(num) :  ## ping without getting output on the Screen
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

# num=["172.0.0.22","172.0.0.10"]


# Validate IP Schema
print("\nValidate_List_ip for NUM")
num=Validate_List_ip (num)
print(f"\n Num length {len(num)} is  Validated ^_^ ")

counter=0
for x in num:
		# if not x :
		# 	print (f"Continue it's empty {x}")
		# 	continue
		counter+=1
		if (counter % 50)==0 :
			print (f"\n\n\n\nsleep {counter}\n\n\n\n")
			time.sleep(10)
		print (f"\t\tWe are Processing this IP  {x}")
		try:
				my_thread = threading.Thread(target=Ping_Test, args=(x,))
				my_thread.start()
		except Exception:
				FailedExceptionIps.append(num[x])


## Main Threading
main_thread = threading.currentThread()
for some_thread in threading.enumerate():
		if some_thread != main_thread:
				print(some_thread)
				some_thread.join()


 # new file for only new IPs , aslo to update old active file in case or loop repeatation
fullpath=Directory_Path+'/'+Worked_and_Old_IPs_File
Append_to_Old_File(fullpath=fullpath ,Unknown_Lists=active)


# Add active IPs to s File to use it in Automation Script
fullpath=Directory_Path+'/'+Pass_IPs_to_File
Append_to_Old_File(fullpath=fullpath ,Unknown_Lists=active)



### overwrite on the old file and keep just inactive IPs to iterate it again
Overwrite_Old_File(path=Directory_Path ,file_name=Source_IPs_File,Unknown_Lists=inactive )



print ("Failed_IP")
for i in Failed_IP :
	print (f"Failed_IP {i}")

print ("\n\nFailedExceptionIps")
for i in FailedExceptionIps :
	print (f"FailedExceptionIps {i}")

print(f"\n\n length of num :{num_len}")
print(f"\n length of active :{len(active)}")
print(f"\n length of inactive :{len(inactive)}")
print(f"\n length of Failed_IP :{len(Failed_IP)}")
print(f"\n length of FailedExceptionIps :{len(FailedExceptionIps)}")

result_sum =len(active) +len(inactive) +len(Failed_IP) +len(FailedExceptionIps)
print (f"\n result_sum is :{str(result_sum)}")

# Mohammed