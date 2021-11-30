# typo error in import
import subprocess
import os
import os.path
import codecs


from datetime import datetime
import threading
from multiprocessing.dummy import Pool as ThreadPool
import time
from Useful_Fun import *  ### my Class of Functions
from Global_Variables import Global_Variables ## Call Class to set or Use global Variables

class Ping_Check :

	# ===============================================================
	# ===============================================================

	Class_of_Global_Variables=Global_Variables()

	Directory_Path = Class_of_Global_Variables.Directory_Path
	Source_IPs_File = Class_of_Global_Variables.Source_IP_File_for_Ping
	Worked_and_Old_IPs_File = Class_of_Global_Variables.Pinged_New_and_Old_IP_File
	Pass_IPs_to_File = Class_of_Global_Variables.Source_IP_File_for_Automation

	# ===============================================================
	# ===============================================================

	def __init__(self):

		self.active=[]
		self.inactive=[]
		self.Failed_IP=[]
		self.FailedExceptionIps=[]
		self.num_len=0
		self.num=[]

		print("\n==============================================")
		print ("Welcome to Init in Ping Script")
		print("==============================================\n")


#####################################################################################################
#####################################################################################################

	def Set_Num(self) :
		print("\n==============================================")
		print ("Welcome to Set Function")
		print("==============================================\n")
		global num

		Directory_Path=self.Directory_Path
		Source_IPs_File=self.Source_IPs_File

		fullpath_to_sourceIP=Directory_Path+'/'+Source_IPs_File
		print(fullpath_to_sourceIP)
		print(fullpath_to_sourceIP)
		with open(fullpath_to_sourceIP, 'r') as file:
				num =file.read().splitlines()
		file.close()

		num= list(dict.fromkeys(num))
		num_len=len(num)
		self.num=num
		self.num_len=num_len
		print ("num")
		print (num)
		print ("self.num")
		print (self.num)
		print(f"\n Num length {num_len} is not Validated yet")

#####################################################################################################
#####################################################################################################

	def Ping_Test(self,num) :
		print("\n==============================================")
		print ("Welcome to Ping_Test Function")
		print("==============================================\n")
		print ("num")
		print (num)
		print (self.num)
		ip= num

		try :
			if os.name=="nt" :
				result=subprocess.Popen(["ping", "-n", "3","-w", "20", ip]).wait()
				print("\nHey it's Win\n")
			else :
				print("\nHey it's NOT Win\n")
				result=subprocess.Popen(["ping", "-c", "3", "-n", "-W", "20", ip]).wait()
			print ("\nResult")
			print (result)
			if result:
				print (f"\n{ip} :( inactive :( \n")
				print("\n\nBefore inactive")
				print(self.inactive)
				self.inactive.append(ip)
				print("After inactive")
				print(self.inactive)
				print("\n\n")
			else:
				print (f"\n{ip}  ^_^ active ^_^\n")
				self.active.append(ip)
		except Exception as e :
			print (f"\nException {e} for IP {ip}\n")
			self.Failed_IP.append(ip)

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

#####################################################################################################
#####################################################################################################

	def Ping_Test_Thread(self) :
		print("\n==============================================")
		print ("Welcome to Ping_Test_Thread Function")
		print("==============================================\n")
		
		global num
		global num_len


		self.Set_Num()
		# Validate IP Schema
		print("\nValidate_List_ip for NUM")
		num=Validate_List_ip (self.num)
		print(f"\n Num IP length {len(num)} is  Validated ^_^ \n\n")

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
						my_thread = threading.Thread(target=self.Ping_Test, args=(x,))
						my_thread.start()
				except Exception:
						self.FailedExceptionIps.append(num[x])


		## Main Threading
		main_thread = threading.current_thread()
		for some_thread in threading.enumerate():
				if some_thread != main_thread:
						print(some_thread)
						some_thread.join()


		 # new file for only new IPs , aslo to update old active file in case or loop repeatation
		Append_to_Old_File(path=self.Directory_Path, file_name=self.Worked_and_Old_IPs_File ,Unknown_Lists=self.active)


		# Add active IPs to s File to use it in Automation Script
		Append_to_Old_File(path=self.Directory_Path, file_name=self.Pass_IPs_to_File ,Unknown_Lists=self.active)



		### overwrite on the old file and keep just inactive IPs to iterate it again
		Overwrite_Old_File(path=self.Directory_Path ,file_name=self.Source_IPs_File,Unknown_Lists=self.inactive )



		if len(self.Failed_IP) !=0 :
			print ("Failed_IP")
			for i in self.Failed_IP :
				print (f"Failed_IP {i}")

		if len(self.FailedExceptionIps) !=0 :
			print ("\n\nFailedExceptionIps")
			for i in self.FailedExceptionIps :
				print (f"FailedExceptionIps {i}")

		if self.num_len !=0 :
			print(f"\n\n length of num :{self.num_len}")
		if len(self.active) !=0 :
			print(f"\n length of active :{len(self.active)}")
		if len(self.inactive) !=0 :
			print(f"\n length of inactive :{len(self.inactive)}")
		if len(self.Failed_IP) !=0 :
			print(f"\n length of Failed_IP :{len(self.Failed_IP)}")
		if len(self.FailedExceptionIps) !=0 :
			print(f"\n length of FailedExceptionIps :{len(self.FailedExceptionIps)}")

		result_sum =len(self.active) +len(self.inactive) +len(self.Failed_IP) +len(self.FailedExceptionIps)
		print (f"\n result_sum is :{str(result_sum)}")



	# ================================================================================================ #
	# ===============================		It's the END	========================================== #
	# ================================================================================================ #
	def Main_Fun_Call_Ping(self):
		print("\n==============================================")
		print ("Welcome to Ping Script Main_Fun_Call Function")
		print("==============================================\n")
		
		start_time = datetime.now()
		self.Ping_Test_Thread()

		print("Hello, World!")
		if __name__== "__main__" :
			print("Main_of_Ping_Script")

		print("\n\tElapsed time for Ping_Test_Script : " + str(datetime.now() - start_time))

	# main()
		print ("\n\nHey We Have Finished Successfully From Ping . ^_^ \n")



if __name__== "__main__" :
	print("\nThis is Run Main of Ping_Test_Script")
	Ping_IPs_run=Ping_Check()
	Ping_IPs_run.Main_Fun_Call_Ping()

