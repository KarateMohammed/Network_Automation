import os
import time


for i in range (10) :
	print ("########################################################################")
	print(f"START  {i+1}\n")
	os.system('python3 /home/khayat/Automation/Ping_Test.py')
	print(f"END  {i+1}")
	print ("########################################################################")
	print (f"sleep {i+1} \n")
	time.sleep(2)

print ("\n\n\n Ping Test is finishined let's take a break and Continue to Automation Script ^_^ \n\n\n\n")
time.sleep(2)
for i in range (5) :
	print(f"START  {i+1}\n")
	print ("########################################################################")
	os.system('python3 /home/khayat/Automation/Automation_Script_Main.py')
	print(f"END  {i+1}")
	print ("########################################################################")
	print (f"sleep {i+1} \n")
	time.sleep(2)

