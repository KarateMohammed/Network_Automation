import os
import time
from Global_Variables import Global_Variables ## Call Class to set or Use global Variables
from Ping_Test import Ping_Check
# from Discover_New_IPs import Discover_IPs
from Discover_New_IPs import  Main_Fun_Call_Discover
from datetime import datetime

Class_of_Global_Variables=Global_Variables()

Directory_Path_Scripts = Class_of_Global_Variables.Directory_Path_Scripts
Ping_Test_Script = Class_of_Global_Variables.Ping_Test_Script
Discover_New_IPs_Script = Class_of_Global_Variables.Discover_New_IPs_Script

class Loop_Scripts:


	def __init__(self):

		print("\n==============================================")
		print ("Welcome to Init in Loop Script")
		print("==============================================\n")


	def Run_Ping(self) :
		for i in range (4) :
			print ("\n########################################################################")
			print(f"START Run_Ping {i+1}\n")
			# os.system('python3  /home/khayat/Automation/Ping_Test.py')
			# os.system('python ' +Directory_Path_Scripts + '/'+Ping_Test_Script)

			# Test=Ping_Test.Main_Fun_Call()
			Test_Ping_Here=Ping_Check()
			Test_Ping_Here.Main_Fun_Call_Ping()

			print(f"\nEND Run_Ping {i+1}")
			print ("########################################################################")
			print (f"sleep {i+1} \n")
			time.sleep(3)


		print ("\n\n Ping Test is finishined let's take a break and Continue to Automation Script ^_^ \n\n")
		time.sleep(3)

	def Run_Discover(self):

		for i in range (10) :
			print(f"\nSTART Run_Discover {i+1}\n")
			print ("\n########################################################################")
			# os.system('python3 /home/khayat/Automation/Discover_New_IPs.py')
			# os.system('python ' +Directory_Path_Scripts + '/'+Discover_New_IPs_Script)
			Main_Fun_Call_Discover()
			# Lets_Discover=Discover_IPs()
			# Lets_Discover.Main_Fun_Call_Discover()

			print(f"\nEND  Run_Discover {i+1}")
			print ("########################################################################")
			print (f"sleep {i+1} \n")
			time.sleep(3)

	def Main_fun_Loop_Script(self):

		print("\n==============================================")
		print ("Welcome to LOOP Script")
		print("==============================================\n")

		start_time_Run_Ping = datetime.now()
		self.Run_Ping()
		elapsed_time_Run_Ping = str(datetime.now() - start_time_Run_Ping)
		
		start_time_Run_Discover = datetime.now()
		self.Run_Discover()
		elapsed_time_Run_Discover =str(datetime.now() - start_time_Run_Discover)

		print(f"\n\tElapsed time for Run_Ping in Loop_Scripts : {elapsed_time_Run_Ping}"  )
		print(f"\n\tElapsed time for Run_Discover in Loop_Scripts : {elapsed_time_Run_Discover}"  )


Loop_Scripts_Run=Loop_Scripts()
Loop_Scripts_Run.Main_fun_Loop_Script()
