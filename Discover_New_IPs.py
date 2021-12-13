# ls | wc -l ## commad to see numbers of files on the directory
# ssh 192.168.1.2 -o Kexalgorithms=+diffie-hellman-group1-sha1  ## to solve problem while connecting from client that have mismatch on Diffe
## Or u can add this to
	# KexAlgorithms diffie-hellman-group1-sha1,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha25>
	# Ciphers 3des-cbc,blowfish-cbc,aes128-cbc,aes128-ctr,aes256-ctr
##  to  nano /etc/ssh/ssh_config
# ssh-keygen -A
# service ssh restart
# path for ntc-templates TestFSM /usr/local/lib/python3.8/dist-packages/ntc_templates/templates/ 
#export NET_TEXTFSM=/usr/local/lib/python3.8/dist-packages/ntc_templates/templates/


import threading
from datetime import datetime
from netmiko import ConnectHandler
from netmiko import ssh_exception
from netmiko.ssh_exception import (
		NetMikoTimeoutException,
		NetMikoAuthenticationException,
		SSHException
)


from Useful_Fun import *  ### my Module of Functions
from Global_Variables import Global_Variables 	# Global variables from another package

from socket import error as socket_error
import re
import os
import os.path
import json
from multiprocessing.dummy import Pool as ThreadPool
import time 
import math

from array import *
import scp
import codecs
import subprocess

''' After SetConfig it exit config mode but after SendConfig Still in config mode ALSO u can send sho ip int br after SendConfig'''


# Device_Type=[ 'cisco_ios','cisco_ios_telnet']
Device_Type=[ 'cisco_ios_telnet','cisco_ios']






Username_Device=["cisco","css"]
Passowrd_Device=["cisco","css"]
Passowrd_Device_Enable=["cisco","cs"]




Profile_Archive_IP=[[]]
##################################################################
	########## Variables For Paths and File name
##################################################################

# ===============================================================
# ===============================================================

Class_of_Global_Variables=Global_Variables() ## Call Class to set or Use global Variables

Directory_Path = Class_of_Global_Variables.Directory_Path
Source_IPs_File = Class_of_Global_Variables.Source_IP_File_for_Automation
FailedIPs_Cumulative_File = Class_of_Global_Variables.FailedIPs_Cumulative_File
Worked_IPs_Old_File = Class_of_Global_Variables.Finished_IPs_Old_File
New_Discovered_IPs_File =  Class_of_Global_Variables.New_Discovered_IPs_File
Hardware_Modules_File = Class_of_Global_Variables.Hardware_Modules_File
Sub_Directory_Path_for_Backup = Class_of_Global_Variables.Sub_Directory_Path_for_Backup
Dict_all_IP_Usr_Pass_Ena=Class_of_Global_Variables.Dict_all_IP_Usr_Pass_Ena
New_Dict_IPs_File=Class_of_Global_Variables.New_Dict_IPs_File
Pattern_Filter_in_CDP=Class_of_Global_Variables.Pattern_Filter_in_CDP



##################################################################
####################### This is Main Class ##########################
##################################################################

Global_Output=[]
Hostname_Output_list=[]
Configuration_Output_list=[]
Configuration_Output_ID2_list=[]
Configuration_Output_ID254_list=[]
FailedIps=[]
IPs_ForIteration=[]
Worked_IPs_Old=[] ## For not repeating dicovering worked IPs after removing them from S file
Worked_IPs_Now=[] ## For not repeating Old worked IPs 

count=0
ConfigurationTest_Boolen =0 	## to Return from Recursion
num_New=[]						## for New IPs
num=[]						## for New IPs
All_Hardware_Module_List=[]
Hardware_IP_Empty_List=[]

Show_Output_SOR=''
Configuration_Output_ID2=''
Configuration_Output_ID254=''
Configuration_Router=""
Configuration_Switch=""
Configuration_Output=""

print("\n==============================================")
print ("Welcome to Init in Discover_IPs Script")
print("==============================================\n")


##################################################################
####################### Get Source IPs from file ##########################
##################################################################
def Set_Globals():
	global Show_Output_SOR
	global Configuration_Output_ID2
	global Configuration_Output_ID254
	global Configuration_Router
	global Configuration_Switch
	global Configuration_Output
	global All_Hardware_Module_List
	global Hardware_IP_Empty_List

	global Global_Output
	global Hostname_Output_list
	global Configuration_Output_list
	global Configuration_Output_ID2_list
	global Configuration_Output_ID254_list
	global FailedIps
	global IPs_ForIteration
	global Worked_IPs_Old
	global Worked_IPs_Now 
	global num_New
	global num
	global count
	global ConfigurationTest_Boolen 

	Show_Output_SOR=''
	Configuration_Output_ID2=''
	Configuration_Output_ID254=''
	Configuration_Router=""
	Configuration_Switch=""
	Configuration_Output=""
	All_Hardware_Module_List=[]
	Hardware_IP_Empty_List=[]

	Global_Output=[]
	Hostname_Output_list=[]
	Configuration_Output_list=[]
	Configuration_Output_ID2_list=[]
	Configuration_Output_ID254_list=[]
	FailedIps=[]
	IPs_ForIteration=[]
	Worked_IPs_Old=[] ## For not repeating dicovering worked IPs after removing them from S file
	Worked_IPs_Now=[] ## For not repeating Old worked IPs 
	num_New=[]						## for New IPs
	num=[]						## for New IPs
	count=0
	ConfigurationTest_Boolen =0 	## to Return from Recursion

def Get_IPs_to_Iterate() :
	global num
	print("Before num Full_Source_Path")
	Full_Source_Path=Directory_Path+"/"+Source_IPs_File
	with open(Full_Source_Path, 'r') as file:
			num =file.read().splitlines()
	file.close()
	num= Remove_Deplicated_In_List(num)
	print("num")
	print(num)
	print("After Full_Source_Path")


# ================================================================
####################### Get Old Worked IPs from file #################
# ================================================================
def Get_IPs_From_WorkedIPs() :
	global Worked_IPs_Old
	print("Before Worked_IPs_Old File")
	Full_Source_Path=Directory_Path+"/"+Worked_IPs_Old_File
	with open(Full_Source_Path, 'r') as file:
			Worked_IPs_Old =file.read().splitlines()
	file.close()
	Worked_IPs_Old= Remove_Deplicated_In_List(Worked_IPs_Old)
	print ("Worked_IPs_Old")
	print (Worked_IPs_Old)

##############################################################################
##################### The main Function of configuration ##################### 
##############################################################################

def ConfigurationTest(ip,Device_Type_Num= 0,User_Pass_Num= 0,Passowrd_Enable_Num=0):

		print("\n==============================================")
		print ("Welcome to ConfigurationTest Function in Discover_IPs Script")
		print("==============================================\n")

		global num_New # so we can edit it in this Function 
		global Configuration_Output_list  
		global Hostname_Output_list
		global Worked_IPs_Old
		global num

		if ConfigurationTest_Boolen==1 :
				return ConfigurationTest_Boolen==1

	# If increment of Num is out of range for User_Pass_Num and Device_Type_Num return 1
		elif User_Pass_Num >= len(Username_Device)   :
				print (f"Username Not in Range For IP\t{ip}\n")
				return ConfigurationTest_Boolen==1
		elif Device_Type_Num >= len (Device_Type) :
				print (f"Connection type Not in Range For IP\t{ip}\n")
				return ConfigurationTest_Boolen==1
		elif Passowrd_Enable_Num>=len(Passowrd_Device_Enable) :
				print (f"Enable Pass Not in Range For IP\t{ip}\n")
				return ConfigurationTest_Boolen==1


# If increment of Num is in range for User_Pass_Num and Device_Type_Num contune
		else :

				iosv_l2={
						'device_type': str(Device_Type[Device_Type_Num]),  ##### Type of connection SSH/Telnet
						'ip':str(ip),
						'username': Username_Device[User_Pass_Num],
						'password': Passowrd_Device[User_Pass_Num],
						'global_delay_factor': 10, #  if there is authentication problem allow this
						# 'secret':'cs'
						'secret':Passowrd_Device_Enable[Passowrd_Enable_Num],
						# 'timeout':10
						 'session_timeout': 6 	#  if there is authentication problem allow this
								}

				try:
						Conf_Variables=[]  # To check if any faliure on the configuration after sending it
						net_connect = ConnectHandler(**iosv_l2)
						# print(net_connect.find_prompt())

		############ function to check output to send any confirmation message as pass or confirmation of yes or no
						def SpecialConfirmation ( command , message , reply):
								net_connect.config_mode()    #To enter config mode
								print ("SpecialConfirmation Config")
								try :
										if Device_Type[Device_Type_Num] == "cisco_ios_telnet" :
												print ("First Write Telnet")
												net_connect.remote_conn.write(str(command)+'\n' )
										else :
												net_connect.remote_conn.sendall(str(command)+'\n' )
								except : 
										print ("Exception For Sendall ")
								print ("SpecialConfirmation Before Sleep")
								time.sleep(3)
								print ("SpecialConfirmation after Sleep")
								if Device_Type[Device_Type_Num] == "cisco_ios_telnet" :
										print ("First READ Telnet")
										output = net_connect.remote_conn.read_very_eager().decode("utf-8", "ignore")
								else :
										output = net_connect.remote_conn.recv(65535).decode('utf-8')
								ReplyAppend=''
								print ("SpecialConfirmation output")
								print (output)
								try :
										if str(message) in output:
												for i in range(0,(len(reply))):
														ReplyAppend+=str(reply[i])+'\n'
												if Device_Type[Device_Type_Num] == "cisco_ios_telnet" :
														print ("SECOND Telnet")
														net_connect.remote_conn.write(ReplyAppend)
														output = net_connect.remote_conn.read_very_eager().decode("utf-8", "ignore") 
												else :
														net_connect.remote_conn.sendall(ReplyAppend)
														output = net_connect.remote_conn.recv(65535).decode('utf-8') 
										print (output)
								except :
										print ("Confirmation Exception Error")
								return output



						print ("Entered Device Successfully \t"+ip +"\n")

		######################################################################
		################ Here Is The Cisco Configuration  ####################
		######################################################################
						# Dict_Path=Directory_Path+'/'+New_Dict_IPs_File
						print ("check enable mode for "+str(ip))
						if not net_connect.check_enable_mode() :
							net_connect.enable()
							# Temp_Dict_k_Enable={"k_Enable" :Passowrd_Device_Enable[Passowrd_Enable_Num]}
							print ("entered enable mode for "+str(ip))
						# else :
						# 	Temp_Dict_k_Enable={"k_Enable" :''}
						print ("Already on enable mode for "+str(ip))


						# Temp_Dict_k_ip={}
						# Temp_Dict_k_ip[ip]={}
						# Temp_Dict_Connection_type={"Connection_type":Device_Type[Device_Type_Num]}
						# Temp_Dict_k_Username={"k_Username":Username_Device[User_Pass_Num]}
						# Temp_Dict_k_Password={"k_Password":Passowrd_Device[User_Pass_Num]}


						# Temp_Dict_k_ip[ip].update(Temp_Dict_Connection_type)
						# Temp_Dict_k_ip[ip].update(Temp_Dict_k_Username)
						# Temp_Dict_k_ip[ip].update(Temp_Dict_k_Password)
						# Temp_Dict_k_ip[ip].update(Temp_Dict_k_Enable)
						# Dict_all_IP_Usr_Pass_Ena.update(Temp_Dict_k_ip)
						# print (f"Dict_all_IP_Usr_Pass_Ena[{ip}]")
						# print (Dict_all_IP_Usr_Pass_Ena[ip])
						# Temp_Dict_k_ip.popitem()
						# print("After POP Temp_Dict_k_ip")
						# print(Temp_Dict_k_ip)

						# Temp_Dict_fake_Key= [*Temp_Dict_fake.keys()]


						# with open(Dict_Path) as convert_file:
						# 	data=convert_file.read()
						# convert_file.close()
						# os.chmod(fullpath, 0o777)  ## to use it with full permisson
						# data=json.loads(data)
						# print("Dict:", data)
						# print("Type:", type(data))

						# if not Temp_Dict_fake_Key[0] in Dict_all_IP_Usr_Pass_Ena.keys():
						# 	print("A new Key ")
						# 	print("Temp_Dict_fake.keys()")
						# 	print(Temp_Dict_fake.keys())

						# 	data=json.dumps(Temp_Dict_fake)
						# 	with open(Dict_Path, 'a') as convert_file:
						# 		convert_file.write(data)
						# 	os.chmod(fullpath, 0o777)  ## to use it with full permisson
						# 	convert_file.close()

						# else :
						# 	print("An old Key ")



				##################################################################
				########### Check if in config mode or not to exit config mode
				##################################################################
						if net_connect.check_config_mode() :
								net_connect.exit_config_mode()
								print ("After exiting config to perform show commands "+str(ip))
						print ("After checking config to perform show commands "+str(ip))

		######################################################################



						# print ("Terminal length \n")
						# ## Try this First
						# Configuration_Output=""
						# Configuration_Switch=""
						# Configuration_Router=""
						# Configuration_Output=net_connect.send_command_timing("termin len 0"+'\n\n' )

						# ##### it's here to check if it exists in old worked ip file and to add it to list to append it later to old worked ip
						# ##### this if is for not creating file since it's already a worked up just do the discover cdp for it
						# if ip not in Worked_IPs_Old :
						# 	print(f"IP {ip} not in Old Worked IPs excute the commands")
						# 	Configuration_Output=net_connect.send_command_timing("show run "+'\n\n'  ,strip_prompt=False,strip_command=False)
						# 	Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch=net_connect.send_command_timing("show fex  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show fex status   "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show fex detail  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show inventory  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show module switch all  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show module  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show etherchan summa  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Output+=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Switch+=net_connect.send_command_timing("show interfaces status  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Output+=net_connect.send_command_timing("show inter desc "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Router=net_connect.send_command_timing("show mpl l2 vc "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Router+=net_connect.send_command_timing("show ip ospf int br "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Router+=net_connect.send_command_timing("show ip ospf neighbor "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Output+=net_connect.send_command_timing("show version "+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	Configuration_Output+=net_connect.send_command_timing("show cdp neighbors "+'\n\n' ,strip_prompt=False,strip_command=False)

						# 	# print ("\n\n\n\n===============================\n\n\n")
						# 	# print (Configuration_Switch)
						# 	# print ("\n\n\n\n===============================\n\n\n")
						# 	# print (Configuration_Output)
						# 	# print ("\n\n\n\n===============================\n\n\n")
						# 	# print (Configuration_Router)
						# 	# print ("\n\n\n\n===============================\n\n\n")


						# 	################### for ARP ###############################################################
						# ######################################################################

						# 	# Configuration_Output_ID2=net_connect.send_command_timing("show ip arp vrf ID2 "+'\n\n'  ,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output_ID254=net_connect.send_command_timing("show ip arp vrf ID254 "+'\n\n'  ,strip_prompt=False,strip_command=False)
						# ######################################################################

							
						# 	# Configuration_Output=net_connect.send_command_timing("termin len 0"+'\n\n',delay_factor=5)
						# 	# Configuration_Output=net_connect.send_command_timing("show run "+'\n\n' ,delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Switch=net_connect.send_command_timing("show fex  "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Switch+=net_connect.send_command_timing("show interfaces status  "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output+=net_connect.send_command_timing("show inter desc "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Router=net_connect.send_command_timing("show ip ospf neighbor "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output+=net_connect.send_command_timing("show version "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# 	# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
							
						# 	Show_Output_SOR=""
						# 	# Show_Output_SOR=Configuration_Switch + Configuration_Output + Configuration_Router

						# 	Show_Output=""
						# 	Show_Output=Configuration_Switch + Configuration_Output + Configuration_Router

						# 	show_Summary=[]
						# 	show_Summary.append(str(Show_Output))
						# 	Configuration_Output_list = []
						# 	# Configuration_Output_list.append(str(Show_Output))
						# 	Configuration_Output_list.append(str(Show_Output_SOR))
						# 	# print("Configuration_Output_list 	Main")
						# 	# print(Configuration_Output_list)
						# 	# print("\n\nConfiguration_Switch Main ")
						# 	# print(Configuration_Switch)


						# 	print("After getting show commands")
						
						# else :
						# 	print (f"IP {ip} in Worked Old IPs don't excute the commands")

				###########################################################################################################
						############################ Use TEXTFSM Template to get Show version ############################
				###########################################################################################################
						try :		# Try For TextFSM
							# Show_Version_TEXTFSM_List=net_connect.send_command_timing("show version "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True, textfsm_template="/home/khayat/Textfsm_Templates/cisco_ios_show_version.textfsm")
							# Test_Expect=net_connect.send_command("show ip inte br "+'\n\n' ,strip_prompt=False,strip_command=False)
							# print ("\t\tTest_Expect")
							# print (Test_Expect)
							Show_Version_TEXTFSM_List=net_connect.send_command_timing("show version "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True)
							Show_Version_TEXTFSM_Dict = Show_Version_TEXTFSM_List[0]  # this is because the output is in list then in Dict 
							# print (type(Show_Version_TEXTFSM_List))  
							# print ("Show_Version_TEXTFSM_List")
							# print ((Show_Version_TEXTFSM_List[0]))
							# print (type(Show_Version_TEXTFSM_Dict))
							# print ((Show_Version_TEXTFSM_Dict))
							# print ("\n\n\n")
							# print ("\t\tConfiguration_Output_TEXTFSM")
							# for k,v in Show_Version_TEXTFSM_Dict.items() :
							# 	print (f"{k} :: {v}")

							if Show_Version_TEXTFSM_Dict["hardware"] : 
								Hardware_IP = "\t\t"+str(Show_Version_TEXTFSM_Dict["hardware"][0]) + f"		{ip}___" + str(Show_Version_TEXTFSM_Dict["hostname"])
								All_Hardware_Module_List.append(Hardware_IP)
							else :
								Hardware_IP_Empty_List.append(ip+"   Hardware Empty")
							Hostname_Output=ip+".__"+str(Show_Version_TEXTFSM_Dict["hostname"])

						except Exception as e:
							print ('Exception in show version\t' +ip)
							FailedIps.append(ip+"   Exception in show version")
							IPs_ForIteration.append(ip)

			###########################################################################################################

						print (f"This is after getting Show Version for IP\t{ip}")

				###########################################################################################################
				##################      Get each interfaces status using Script     ##################################################
				###########################################################################################################
						# List_Of_Inter=net_connect.send_command_timing("show interface status "+'\n\n')
						# # print ("\t\tList_Of_Inter")
						# List_of_Lines= Get_All_Inter(List_Of_Inter)
						# print ("\t\tList_of_Lines\n")
						# print (List_of_Lines)
						# print ("\t\tGet_Ports_Status")
						# Returned_List=Get_Ports_Status(List_of_Lines)

						# for i in Returned_List :
						#   print (f"key\t{i}\tValue\t{Returned_List.get(i)} ")

				# ###########################################################################################################
				# ##################        Get each interfaces IP using Script     ##################################################
				# ###########################################################################################################
						# IPs_All_Interfaces=net_connect.send_command_timing("show ip interface br "+'\n\n')
						
						# Inter_IPs= Get_Interfaces_IP(IPs_All_Interfaces)

						# for x in Inter_IPs :
						#   if x[-1] =="up" and x[-2]=="up" :
						#       print (x)
						#       print (x[1])


				##################################################################
				########### Check if in config mode or not to exit config mode
				##################################################################
						# if not net_connect.check_config_mode() :
						# 		net_connect.config_mode()
						# 		print ("After entering config "+str(ip))
						# print ("After checking config to perform configuration commands  "+str(ip))

				######################################################################
				################ Set list of configuration  ###########################
				######################################################################
						# List_cmd=[f"inte {Returned_List["disabled"][0]}","no shutd","ip add 192.168.100.100 255.255.255.0"]
						# print ("Returned_List[disabled][0]")
						# print (Returned_List.get("disabled")[0])
						# Temp=str(Returned_List.get("disabled")[0])
						# List_cmd=[f"inte {Temp}","no shutd"]
						# Output_Setting_Inter=net_connect.send_config_set(config_commands=List_cmd)
						# print ("Output_Setting_Inter")
						# print (Output_Setting_Inter)

				##################################################################
				########### Check if in config mode or not to exit config mode
				##################################################################
						if net_connect.check_config_mode() :
								net_connect.exit_config_mode()
								print ("After exiting config "+str(ip))
						print ("After checking config for CDP command\t"+str(ip))

				###########################################################################################################
				##################      Add new IPs from CDP Command     ##################################################
				###########################################################################################################
					
					###############################################################################
						######################## Using Script for cdp neighbors to get New IPs	
					###############################################################################

						# CDP_ALL=net_connect.send_command_timing("show cdp neighbors detail | i IP address: "+'\n\n')
						# print ("\t\tGet_CDP_Neighbors")
						# num_New = list(num_New) + list(Get_CDP_Neighbors (CDP_ALL , num, Pattern_Filter_in_CDP=Pattern_Filter_in_CDP))

					###############################################################################
						######################## Using TextFSM for cdp neighbors	
					###############################################################################

																																									

						try :	
							# print(f"\n\n\nConfiguration_Switch Before Try {ip}")
							# print(Configuration_Switch)
							# print(f"\n\nConfiguration_Output_list Before Try  {ip}")
							# print(Configuration_Output_list)
							# print("\n\n\n")

							Show_CDP_Details_TEXTFSM_List=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True)
							check_list= isinstance(Show_CDP_Details_TEXTFSM_List, list)
							if check_list :
								print("\n\nHey It's Not Empty List.")
								for n in Show_CDP_Details_TEXTFSM_List :
									Show_CDP_Details_TEXTFSM_Dict = n  # this is because the output is in list then in Dict 
								# print (type(Show_CDP_Details_TEXTFSM_List))
								# print (Show_CDP_Details_TEXTFSM_List)
								# print (type(Show_CDP_Details_TEXTFSM_Dict))
								# print (Show_CDP_Details_TEXTFSM_Dict)
								# print (type(Show_CDP_Details_TEXTFSM_Dict["management_ip"]))
									# print (Show_CDP_Details_TEXTFSM_Dict["management_ip"])
									Manag_IP=Show_CDP_Details_TEXTFSM_Dict["management_ip"]
									if Pattern_Filter_in_CDP in Manag_IP :
										if Manag_IP not in num and Manag_IP not in num_New and Manag_IP not in Worked_IPs_Old :
											num_New.append(Show_CDP_Details_TEXTFSM_Dict["management_ip"])
							else :
								print("\n\n Hey It's Emptyyyyyy :(")

						except Exception as e:
							print ('Exception in show cdp neighbors \t' +ip)
							FailedIps.append(ip+"   Exception in show cdp neighbors ")
							IPs_ForIteration.append(ip)
				###########################################################################################################
				################    Example on confirmation message Function
				###########################################################################################################


						# if ip =="192.168.233.13":
						#       print (str (SpecialConfirmation("crypto key generate rsa general-keys" ,"modulus" ,"1024")))


				###########################################################################################################
				###########################################################################################################
						if net_connect.check_config_mode() :
								net_connect.exit_config_mode()
						print ("After last check config "+str(ip))


		################################################################################
		####################### Test Ping For Rang Of IP  ##############################
		################################################################################

						# Active_ping_ip=[]
						# InActive_ping_ip=[]
						# Sub_Ip_ping="2.0.32."
						# for x in range(1,255) :
						# 	print (x)
						# 	Ip_ping=Sub_Ip_ping+str(x)
						# 	ping_result=net_connect.send_command_timing("ping  "+Ip_ping+'\n\n' ,strip_prompt=False,strip_command=False)
						# 	# print (ping_result)
						# 	# ping_is_successful(ping_result) 
						# 	# print (ping_is_successful(ping_result)) 
						# 	# print (type(ping_is_successful(ping_result))) 

						# 	if ping_is_successful(ping_result) :
						# 		Active_ping_ip.append(Ip_ping)
						# 	else :
						# 		InActive_ping_ip.append(Ip_ping)
						# print ("Active_ping_ip")
						# for x in Active_ping_ip :
						# 	print (x)

						# print ("\n\n\nInActive_ping_ip")
						# for x in InActive_ping_ip :
						# 	print (x)



		############### Append Configuration Variables to Global Variable ##########

						# Conf_Variables.append(Hostname_Output)
						# print (Configuration_Output)
						# Conf_Variables.append(Configuration_Output)
		############### Search in Configuration if any command error and return its IP ################
						for y in Conf_Variables:
								if "% Invalid input detected at '^' marker." in y :
										FailedIps.append(ip+"   Invalid input")
#########################################################################################################


						print ("Terminal length \n")
						## Try this First
						Configuration_Output=""
						Configuration_Switch=""
						Configuration_Router=""
						Configuration_Output=net_connect.send_command_timing("termin len 0"+'\n\n' )

						##### it's here to check if it exists in old worked ip file and to add it to list to append it later to old worked ip
						##### this if is for not creating file since it's already a worked up just do the discover cdp for it
						if ip not in Worked_IPs_Old :
							print(f"IP {ip} not in Old Worked IPs excute the commands")
							Configuration_Output=net_connect.send_command_timing("show run "+'\n\n'  ,strip_prompt=False,strip_command=False)
							Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch=net_connect.send_command_timing("show fex  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show fex status   "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show fex detail  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show inventory  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show module switch all  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show module  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show etherchan summa  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Output+=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Switch+=net_connect.send_command_timing("show interfaces status  "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Output+=net_connect.send_command_timing("show inter desc "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Router=net_connect.send_command_timing("show mpl l2 vc "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Router+=net_connect.send_command_timing("show ip ospf int br "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Router+=net_connect.send_command_timing("show ip ospf neighbor "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Output+=net_connect.send_command_timing("show version "+'\n\n' ,strip_prompt=False,strip_command=False)
							Configuration_Output+=net_connect.send_command_timing("show cdp neighbors "+'\n\n' ,strip_prompt=False,strip_command=False)

							Show_Output_SOR=""
							Show_Output_SOR=Configuration_Switch + Configuration_Output + Configuration_Router
							Show_Output=""
							Show_Output=Configuration_Switch + Configuration_Output + Configuration_Router
							show_Summary=[]
							show_Summary.append(str(Show_Output))
							Configuration_Output_list = []
							# Configuration_Output_list.append(str(Show_Output))
							Configuration_Output_list.append(str(Show_Output_SOR))

							print("After getting show commands")

							print (f"IP {ip} not in worked IP append hostname")
							Hostname_Output_list.append(Hostname_Output)
							file_name =Hostname_Output+".txt"

							try :
								# Overwrite_Old_File (path=Sub_Directory_Path_for_Backup ,file_name= file_name, Unknown_Lists=Configuration_Output_list)
								Overwrite_Old_File (path=Sub_Directory_Path_for_Backup ,file_name= file_name, Unknown_Lists=show_Summary)
								print(f"\nAfter Saving Configuration in {Hostname_Output}")
								# print("\n\nshow_Summary")
								# print(show_Summary)
								# print(f"\nAfter Configuration_Output_list {ip}")
								# print(Configuration_Output_list)
								# Configuration_Output_list=[]
								# print("\n")

							except Exception as e:
								print ('Exception in Saving File \t' +ip)
								FailedIps.append(ip+"   Exception in Saving File ")
								IPs_ForIteration.append(ip)

						else :
							print (f"IP {ip} in Worked Old IPs don't excute the commands")
														
							##### it's here to check if it exists in old worked ip file and to add it to list to append it later to old worked ip
						if ip not in Worked_IPs_Old : 
							print(f"IP not in Worked_IPs_Old :: {ip}")
							Worked_IPs_Now.append(ip)

						# Configuration_Output_ID2_list.append(Configuration_Output_ID2)
						# Configuration_Output_ID254_list.append(Configuration_Output_ID254)


		############### SAVE Output IN FILES  #######################
						Global_Output.append(Hostname_Output)
						print ("Exiting  "+str(ip))
						net_connect.disconnect()
						print ("After Exiting  "+str(ip))



################### Exception ###################################


				except ( NetMikoAuthenticationException) as  netmikoAuthenticationException:
						# print ('Authentication Failure\t' + ip)
						print (str (User_Pass_Num) +"   " +str(Username_Device[User_Pass_Num])+ " failed Authentication\t"+ip)
						################ Print error from msg from the main Lib  
						print(f"netmikoAuthenticationException : {netmikoAuthenticationException}\n")
						User_Pass_Num+=1
				# If it tried all users and pass and failed add it to failedIps
						if User_Pass_Num >= len(Username_Device) :
								FailedIps.append(ip+"   Authentication Error ")
								IPs_ForIteration.append(ip)
						# if User_Pass_Num < len(Username_Device) :
						#       print("this is Authentication  "+str(ip)+" Device_Type "+str(Device_Type[Device_Type_Num])+" Username_Device " +str(Username_Device[User_Pass_Num])+" Passowrd_Device " +str(Passowrd_Device[User_Pass_Num]))
				# Recursive function
						return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num,Passowrd_Enable_Num )


				except (ValueError):
						print (str (Passowrd_Enable_Num)+"\tEnable Authentication\t"+ip)
						Passowrd_Enable_Num+=1
						if Passowrd_Enable_Num>=len(Passowrd_Device_Enable):
								FailedIps.append(ip+"   Enable Authentication Error ")
								IPs_ForIteration.append(ip)
						return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num ,Passowrd_Enable_Num) 


				except socket_error as socket_err :
						################ Print error from msg from the main Lib  
						print(f"Socket Error: \n{socket_err}\t for IP {ip}  trying another type of Connection\n")
						print ("Continue")
						if '111' in f"Type {socket_err}" or '10061' in f"Type {socket_err}" :
							Device_Type_Num+=1
							if  Device_Type_Num >= len(Device_Type) :
									FailedIps.append(ip+"   Socket or connection type Error")
									IPs_ForIteration.append(ip)
							return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num ,Passowrd_Enable_Num)
						if '113' in f"Type {socket_err}" :
							FailedIps.append(ip+"   No route to the host")
							IPs_ForIteration.append(ip)
							return ConfigurationTest_Boolen==1
						FailedIps.append(ip+"   Socket or connection type Error")
						IPs_ForIteration.append(ip)
						return ConfigurationTest_Boolen==1


				except (NetMikoTimeoutException) as netmikoTimeoutException:
						# print ('Timeout  Failure\t' + ip)
						print (str (Device_Type_Num)+"\tTimeoutException\t"+ip)
						################ Print error from msg from the main Lib  
						print(f"netmikoTimeoutException : \n{netmikoTimeoutException}\n")
						Device_Type_Num+=1
						if  Device_Type_Num >= len(Device_Type) :
								FailedIps.append(ip+"   Timeout Error")
								IPs_ForIteration.append(ip)
						# if  Device_Type_Num < len(Device_Type) :
						#       print("this is Timeout "+str(ip)+" Device_Type "+str(Device_Type[Device_Type_Num])+" Username_Device " +str(Username_Device[User_Pass_Num])+" Passowrd_Device " +str(Passowrd_Device[User_Pass_Num]))
						return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num ,Passowrd_Enable_Num)



				# except (paramiko.ssh_exception.SSHException) as sshException :
				except (SSHException) as sshException :
						# print ('SSH  Failure\t' + ip)
						print (str (Device_Type_Num)+"\tSSHException\t"+ip +"\n")
						################ Print error from msg from the main Lib  
						print(f"Unable to establish SSH connection: \n{sshException}\t for IP {ip}\n")
						Device_Type_Num+=1
						if  Device_Type_Num >= len(Device_Type) :
								FailedIps.append(ip+"   SSHException Error ")
								IPs_ForIteration.append(ip)
						# if  Device_Type_Num < len(Device_Type) :
						#       print("this is SSHException "+str(ip)+" Device_Type "+str(Device_Type[Device_Type_Num])+" Username_Device " +str(Username_Device[User_Pass_Num])+" Passowrd_Device " +str(Passowrd_Device[User_Pass_Num]))
						return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num ,Passowrd_Enable_Num)

				except (ValueError):
						print (str (Passowrd_Enable_Num)+"   "+str(Passowrd_Device_Enable[Passowrd_Enable_Num]) +" Failed Enable Authentication\t"+ip)
						Passowrd_Enable_Num+=1
						if Passowrd_Enable_Num>=len(Passowrd_Device_Enable):
								FailedIps.append(ip+"   Enable Authentication Error ")
								IPs_ForIteration.append(ip)
						return ConfigurationTest (ip ,Device_Type_Num ,User_Pass_Num ,Passowrd_Enable_Num) 

				except (EOFError) as eof_Error:
						################ Print error from msg from the main Lib  
						print(f"eof_Error : \n{eof_Error}\n")
						# print ('End of File wihle attempting device\t' +ip)
						FailedIps.append(ip+"   EOFError")
						IPs_ForIteration.append(ip)
						# print("this is EOFError "+str(ip)+" Device_Type "+str(Device_Type[Device_Type_Num])+" Username_Device " +str(Username_Device[User_Pass_Num])+" Passowrd_Device " +str(Passowrd_Device[User_Pass_Num]))
						return ConfigurationTest_Boolen==1
						
		###################################################################
		######### if you want to show error , comment next lines if you want to show which Ips have error remove comment  ##############
		###################################################################
				# except Exception as e:
				#       # print ('End of File wihle attempting device\t' +ip)
				#       FailedIps.append(ip+"   Exception as e")
				#       # print("this is EOFError "+str(ip)+" Device_Type "+str(Device_Type[Device_Type_Num])+" Username_Device " +str(Username_Device[User_Pass_Num])+" Passowrd_Device " +str(Passowrd_Device[User_Pass_Num]))
				#       return ConfigurationTest_Boolen==1


		####################################################################

		return ConfigurationTest_Boolen==1

#	================================================================================= #
#	========================	Thread Fun 	========================================== #
#	================================================================================= #
def Start_Threads() :
	# global num
	print("\n==============================================")
	print ("Welcome to Start_Threads Function")
	print("==============================================\n")

	global num_New
	global IPs_ForIteration
	global num
	start_time = datetime.now()

	Set_Globals()

	# ===============================================================================
	#=============  Calling Main Function and Run Threads  ==========================
	# ===============================================================================

	#####################################################################
	################## Controling number of processing  ##################
	#####################################################################

	FailedExceptionIps=[]
	thread_counter=0

	Get_IPs_to_Iterate()  # to iniate num list of ips
	Get_IPs_From_WorkedIPs()  # to get Worked ips and put it in a list of ips
	print(num)
	num=Validate_List_ip (num) 	## Call Validate Function to remove unvalid IPs 
	print(f"After Validating num List {num}\n")
	for x in num:
			print("\ninside main Thread loop")

			ConfigurationTest_Boolen==0
			thread_counter+=1
			if (thread_counter % 100)==0 :
				print (f"\n\nSleep  {thread_counter}\n\n")
				time.sleep(20)
				print ("\n\nAfter Sleep\n\n")
			print (f"\t\tWe are Processing this IP  {x}\n")
			try:
					my_thread = threading.Thread(target=ConfigurationTest, args=(x,0,0))
					my_thread.start()
			except Exception:
					FailedExceptionIps.append(num[x])

	main_thread = threading.current_thread()
	for some_thread in threading.enumerate():
			if some_thread != main_thread:
					print(some_thread)
					some_thread.join()

	# loginandcopy('10.231.0.84','khyat','P@ssw0rd','a1.py','a1.py')

	print ("\nAfter Finishing operations on devices\n")
	####################################################################################################
	###################    Add new IPs and Remove Deplicated IPs   #####################################
	####################################################################################################

	#################################################################################
		######	To ""ADD"" new Discovered IPs in File Called Source_IPs_File ######
	#################################################################################
	IPs_ForIteration=Remove_Deplicated_In_List (IPs_ForIteration)	# to Remove Deplicated IPs
	New_and_inactive_IPs=IPs_ForIteration+num_New

		### overwrite the old file and keep just inactive IPs and New Discovered to iterate it again
	Overwrite_Old_File (path=Directory_Path ,file_name= Source_IPs_File, Unknown_Lists=New_and_inactive_IPs)

	#################################################################################
		######	To ""ADD"" Failed IPs in File Called FailedIPs_Cumulative_File ######
	#################################################################################
	Overwrite_Old_File (path=Directory_Path ,file_name= FailedIPs_Cumulative_File, Unknown_Lists=FailedIps)

	#############################################################################################################################
		########## Add worked IPs to Old Worked IPs in a file to avoid repeating it againg during discovering new IPs ####
	#############################################################################################################################
	Append_to_Old_File(path=Directory_Path, file_name=Worked_IPs_Old_File ,Unknown_Lists=Worked_IPs_Now)

	##################################################################################################################################################################
		######	To ""Save"" new Discovered IPs alone in a File Called Source_IPs_File this is for many ilteration in the loop Script ######
	##################################################################################################################################################################

	# Overwrite_Old_File (path=Directory_Path ,file_name= New_Discovered_IPs_File, Unknown_Lists=num_New)

	##################################################

	#################################################################################
		######	To ""Save"" All Hardware Module  ######
	#################################################################################
	Append_to_Old_File(path=Directory_Path,file_name=Hardware_Modules_File ,Unknown_Lists=All_Hardware_Module_List)


	####################################################################################################
	####################################################################################################
	num_New=Remove_Deplicated_In_List (num_New)	# to Remove Deplicated IPs
	num=Remove_Deplicated_In_List (num)	# to Remove Deplicated IPs
	if len(num_New) != 0 :
		print ("\n\t\tNew Discovered IPs from cdp neighbors in num_New")
		print (f"\t\tNumber of New Discovered IPs {len(num_New)}")
	else :
		print("\n\tNo New Discovered IPs from cdp neighbors")


	if len(Hostname_Output_list)!=0 :
		for i in Hostname_Output_list :
				print ("\t\t"+i)


	if len(FailedIps)!=0 :
		print("\n\t\tFailedIps")
		for i in FailedIps :
				print('\t  '+i)
		print(f"\t\tLength of the Failed IPs  {len(FailedIps)}")

		############# these are the failed IPs while running threads together 
	if len(FailedExceptionIps)!=0 : 
		print("\tFailed IPs in the main thread")
		print(FailedExceptionIps)
	# print (FailedIps)


	if len(num_New)!=0 :
		print ("\n\t\tNew Discovered IPs from cdp neighbors in num_New")
		print (num_New)
		print (f"\t\tNumber of New Discovered IPs {len(num_New)}")
		print (f"\t\tNumber of All IPs {len(num)+len(num_New)}")
	print(f"\t\tLength of the Hostname_Output_list IPs {len(Hostname_Output_list)}")
	print(f"\t\tLength of the IPs in the num  {len(num)}")

		############# these are the Hardware module 
	# if len(All_Hardware_Module_List)!= 0:
	# 	print("\n\n\t\tAll Hardware Module List\n")
	# 	for hardware in All_Hardware_Module_List :
	# 		print(hardware)


		############# these are the empty Hardware module in the show version 
	if len(Hardware_IP_Empty_List)!=0:
		print ("\t\tHardware Empty IPs")
		for c in Hardware_IP_Empty_List :
			print(c)
		print (f"\t\tNumber of All Hardware Empty IPs {len(Hardware_IP_Empty_List)}")

	print("\n\tElapsed time: " + str(datetime.now() - start_time))


# ================================================================================================ #
# ===============================		It's the Main Function for Discover ================================ #
# ================================================================================================ #
def Main_Fun_Call_Discover():
	print("\n==============================================")
	print ("Welcome to Discover Script")
	print("==============================================\n")


	start_time = datetime.now()
	Start_Threads()
	print("\n\tElapsed time for Discover_IPs Script : " + str(datetime.now() - start_time))

	print ("\n\nHey We Have Finished Successfully From Discovering. ^_^ ^_^ \n")


if __name__== "__main__" :

	print("\nThis is Run Main of Main_of_Discover_Script")
	Main_Fun_Call_Discover()
