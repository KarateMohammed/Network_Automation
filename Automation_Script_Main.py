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
# from paramiko import SSHClient
# import paramiko
import codecs
import subprocess

''' After SetConfig it exit config mode but after SendConfig Still in config mode ALSO u can send sho ip int br after SendConfig'''


# Device_Type=[ 'cisco_ios','cisco_ios_telnet']
Device_Type=[ 'cisco_ios_telnet','cisco_ios']


# Username_Device=["cisco"]
# Passowrd_Device=["cisco"]
# Passowrd_Device_Enable=["cisco","cs"]

Global_Output=[]
Hostname_Output_list=[]
Configuration_Output_list=[]
Configuration_Output_ID2_list=[]
Configuration_Output_ID254_list=[]
FailedIps=[]
IPs_ForIteration=[]
Worked_IPs_Old=[] ## For not repeating dicovering worked IPs after removing them from S file 
count=0
ConfigurationTest_Boolen =0
num_New=[]

All_Hardware_Module_List=[]
Hardware_IP_Empty_List=[]

Configuration_Output_ID2=''
Configuration_Output_ID254=''
Configuration_Router=""
Configuration_Switch=""



##################################################################
####################### Get IPs from file ##########################
##################################################################
with open('/home/khayat/s.txt', 'r') as file:
		num =file.read().splitlines()
num= list(dict.fromkeys(num))


# with open('/home/khayat/s.txt', 'a') as file:
# 	for i in num_New:
# 		file.write((str(i)+"\n"))
# file.close()

##############################################################################
##################### The main Function of configuration ##################### 
##############################################################################

def ConfigurationTest(ip,Device_Type_Num= 0,User_Pass_Num= 0,Passowrd_Enable_Num=0):
		global num_New # so we can edit it in this Function 
# def ConfigurationTest(ip,Device_Type_Num= 0,User_Pass_Num= 0):

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
						'global_delay_factor': 15, #  if there is authentication problem allow this
						# 'secret':'cs'
						'secret':Passowrd_Device_Enable[Passowrd_Enable_Num],
						# 'timeout':10
						 'session_timeout':10 	#  if there is authentication problem allow this
								}

				try:
						# time.sleep(3)
						Conf_Variables=[]  # To check if any faliure on the configuration after sending it
						net_connect = ConnectHandler(**iosv_l2)
						# print(net_connect.find_prompt())

		############ function to check output to send any confirmation message as pass or confirmation of yes or no
						def SpecialConfirmation (command , message , reply):
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
						print ("check enable mode for "+str(ip))
						if not net_connect.check_enable_mode() :
								net_connect.enable()
								print ("entered enable mode for "+str(ip))

				##################################################################
				########### Check if in config mode or not to exit config mode
				##################################################################
						if net_connect.check_config_mode() :
								net_connect.exit_config_mode()
								print ("After exiting config to perform show commands "+str(ip))
						print ("After checking config to perform show commands "+str(ip))

		######################################################################



						print ("Terminal length \n")
						## Try this First
						Configuration_Output=""
						Configuration_Output=net_connect.send_command_timing("termin len 0"+'\n\n' )
						# Configuration_Output=net_connect.send_command_timing("show run "+'\n\n'  ,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Switch=net_connect.send_command_timing("show fex  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Switch+=net_connect.send_command_timing("show interfaces status  "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show inter desc "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Router=net_connect.send_command_timing("show ip ospf neighbor "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show version "+'\n\n' ,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors "+'\n\n' ,strip_prompt=False,strip_command=False)
						################### for ARP ###############################################################
					######################################################################

						# Configuration_Output_ID2=net_connect.send_command_timing("show ip arp vrf ID2 "+'\n\n'  ,strip_prompt=False,strip_command=False)
						# Configuration_Output_ID254=net_connect.send_command_timing("show ip arp vrf ID254 "+'\n\n'  ,strip_prompt=False,strip_command=False)
					######################################################################

						
						# Configuration_Output=net_connect.send_command_timing("termin len 0"+'\n\n',delay_factor=5)
						# Configuration_Output=net_connect.send_command_timing("show run "+'\n\n' ,delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Switch=net_connect.send_command_timing("show fex  "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Switch+=net_connect.send_command_timing("show interfaces status  "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show inter desc "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Router=net_connect.send_command_timing("show ip ospf neighbor "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show version "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)
						# Configuration_Output+=net_connect.send_command_timing("show cdp neighbors "+'\n\n',delay_factor=5,strip_prompt=False,strip_command=False)


				###########################################################################################################
						############################ Use TEXTFSM Template to get Show version ############################
				###########################################################################################################
						try :
							# Show_Version_TEXTFSM_List=net_connect.send_command_timing("show version "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True, textfsm_template="/home/khayat/Textfsm_Templates/cisco_ios_show_version.textfsm")
							# Test_Expect=net_connect.send_command("show ip inte br "+'\n\n' ,strip_prompt=False,strip_command=False)
							# print ("\t\tTest_Expect")
							# print (Test_Expect)
							Show_Version_TEXTFSM_List=net_connect.send_command_timing("show version "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True)
							Show_Version_TEXTFSM_Dict = Show_Version_TEXTFSM_List[0]  # this is because the output is in list then in Dict 
							# print (type(Show_Version_TEXTFSM_List))  
							# print ((Show_Version_TEXTFSM_List))
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
							Worked_IPs_Old.append(ip)

						except Exception as e:
						      print ('Exception in show version\t' +ip)
						      FailedIps.append(ip+"   Exception in show version")
						      IPs_ForIteration.append(ip)

			###########################################################################################################


						# Hostname_Output=net_connect.send_command("show run | i hostname"+'\n\n')

						# Configuration_Output+=net_connect.send_command_timing("show ip inte br "+'\n\n',strip_prompt=False,strip_command=False)
						
						print (f"This is after getting SHOW for IP\t{ip}")

						# Hostname_Output=net_connect.send_command("show run | i hostname"+'\n\n',delay_factor=5)



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
						if not net_connect.check_config_mode() :
								net_connect.config_mode()
								print ("After entering config "+str(ip))
						print ("After checking config to perform configuration commands  "+str(ip))

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
						# num_New = list(num_New) + list(Get_CDP_Neighbors (CDP_ALL , num))

					###############################################################################
						######################## Using TextFSM for cdp neighbors	
					###############################################################################
						try :	
							Show_CDP_Details_TEXTFSM_List=net_connect.send_command_timing("show cdp neighbors detail "+'\n\n'  ,strip_prompt=False,strip_command=False, use_textfsm=True)
							for n in Show_CDP_Details_TEXTFSM_List :
								Show_CDP_Details_TEXTFSM_Dict = n  # this is because the output is in list then in Dict 
							# print (type(Show_CDP_Details_TEXTFSM_List))
							# print (Show_CDP_Details_TEXTFSM_List)
							# print (type(Show_CDP_Details_TEXTFSM_Dict))
							# print (Show_CDP_Details_TEXTFSM_Dict)
							# print (type(Show_CDP_Details_TEXTFSM_Dict["management_ip"]))
								# print (Show_CDP_Details_TEXTFSM_Dict["management_ip"])
								if "172." in Show_CDP_Details_TEXTFSM_Dict["management_ip"] :
									if Show_CDP_Details_TEXTFSM_Dict["management_ip"] not in num and Show_CDP_Details_TEXTFSM_Dict["management_ip"] not in num_New and Show_CDP_Details_TEXTFSM_Dict["management_ip"] not in Worked_IPs_Old :
										num_New.append(Show_CDP_Details_TEXTFSM_Dict["management_ip"])

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
						Hostname_Output_list.append(Hostname_Output)
						test=Configuration_Switch
						test+= Configuration_Output
						test+=Configuration_Router
						Configuration_Output_list.append(test)

						Configuration_Output_ID2_list.append(Configuration_Output_ID2)
						Configuration_Output_ID254_list.append(Configuration_Output_ID254)


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
						if '111' in f"Type {socket_err}" : 
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
start_time = datetime.now()

# ===============================================================================
#=============  Calling Main Function and Run Threads  ==========================
# ===============================================================================

#####################################################################
################## Controling number of processing  ##################
#####################################################################

FailedExceptionIps=[]
thread_counter=0

num=Validate_List_ip (num) 	## Call Validate Function to remove unvalid IPs 

for x in num:
		ConfigurationTest_Boolen==0
		thread_counter+=1
		if (thread_counter % 100)==0 :
			print (f"\n\n\nSleep  {thread_counter}\n\n\n")
			time.sleep(20)
			print ("\n\n\nAfter Sleep\n\n\n")
		print (f"\t\tWe are Processing this IP  {x}\n")
		try:
				my_thread = threading.Thread(target=ConfigurationTest, args=(x,0,0))
				my_thread.start()
		except Exception:
				FailedExceptionIps.append(num[x])

main_thread = threading.currentThread()
for some_thread in threading.enumerate():
		if some_thread != main_thread:
				print(some_thread)
				some_thread.join()

# loginandcopy('10.231.0.84','khyat','P@ssw0rd','a1.py','a1.py')

print ("\nAfter Finishing operations on devices\n")
####################################################################################################
###################    Add new IPs and Remove Deplicated IPs   #####################################
####################################################################################################
num_New= list(dict.fromkeys(num_New))  # to Remove Deplicated IPs
num= list(dict.fromkeys(num))  # to Remove Deplicated IPs
if len(num_New) != 0 :
	print ("\n\t\tNew Discovered IPs from cdp neighbors in num_New")
	# print (num_New)
	print (f"\n\t\tNumber of New Discovered IPs {len(num_New)}")

#################################################################################
	######	To ""ADD"" new Discovered IPs in File Called s.txt ######
#################################################################################

IPs_ForIteration = list(dict.fromkeys(IPs_ForIteration))  # to Remove Deplicated IPs
### overwrite on the old file and keep just inactive IPs to iterate it again
fullpath = os.path.join("/home/khayat", "s.txt")
file1 = codecs.open(fullpath, encoding='utf-8',mode="w+")
for i in IPs_ForIteration :
	file1.write((str(i)+"\n"))
for i in num_New:
	file1.write((str(i)+"\n"))	
os.chmod("/home/khayat/s.txt", 0o777)  ## to use it with full permisson
file1.close()


#################################################################################
	######	To ""ADD"" Failed IPs in File Called FailedIPs_Cumulative.txt ######
#################################################################################

fullpath = os.path.join("/home/khayat", "FailedIPs_Cumulative.txt")
file2 = codecs.open(fullpath, encoding='utf-8',mode="w+")
for i in IPs_ForIteration :
	file2.write((str(i)+"\n"))
os.chmod("/home/khayat/FailedIPs_Cumulative.txt", 0o777)  ## to use it with full permisson
file2.close()

#############################################################################################################################
	########## Add worked IPs to Old Worked IPs in a file to avoid repeating it againg during discovering new IPs ####
#############################################################################################################################
with open('/home/khayat/Worked_IPs_Old.txt', 'a') as file:
	for i in Worked_IPs_Old:
		file.write((str(i)+"\n"))
os.chmod("/home/khayat/s.txt", 0o777)  ## to use it with full permisson
file.close()

##################################################################################################################################################################
	######	To ""Save"" new Discovered IPs alone in a File Called s.txt this is for many ilteration in the loop Script ######
##################################################################################################################################################################
# # #new file for only new IPs
# # if os.path.exists("/home/khayat/s_New.txt"):
# # 	os.remove("/home/khayat/s_New.txt")
# # else:
# # 	print("The file s_New does not exist") 

# # with open('/home/khayat/s_New.txt', 'a') as file1:
# #   for i in num_New:
# #       file1.write((str(i)+"\n"))
# # file1.close()


# fullpath = os.path.join("/home/khayat", "s_New.txt")
# file1 = codecs.open(fullpath, encoding='utf-8',mode="w+")
# for i in num_New:
# 	file1.write((str(i)+"\n"))
# os.chmod("/home/khayat/s_New.txt", 0o777)  ## to use it with full permisson
# file1.close()

##################################################

#################################################################################
	######	To ""Save"" All Hardware Module  ######
#################################################################################

with open('/home/khayat/All_Hardware_Module.txt', 'a') as file:
	for i in All_Hardware_Module_List:
		file.write((str(i)+"\n"))
file.close()



####################################################################################################
	############# To Save File in the same host you have run script on it ##############
####################################################################################################
# file_counter =0
# for f in range (0, len(Hostname_Output_list)) :
# 		file_counter+=1
# 		if (file_counter % 100)==0 :
# 			print (f"\nsleep {file_counter}\n")
# 			time.sleep(20)
# 		fullpath = os.path.join("/home/khayat/Karate_Backup_10", Hostname_Output_list[f]+".txt")
# 		file1 = codecs.open(fullpath, encoding='utf-8',mode="w+")
# 		# file1 = codecs.open("/Karate_Backup_8/"+Hostname_Output_list[f]+".txt", encoding='utf-8',mode="w+")
# 		file1.write(Configuration_Output_list[f])
# 		file1.close()

#################################################################################
			#########     This for vrf ID2 arp #################
#################################################################################
# for f in range (0, len(Hostname_Output_list)) :
#       file1 = codecs.open(Hostname_Output_list[f]+"__ID2.txt", encoding='utf-8',mode="w+")
#       file1.write(Configuration_Output_ID2_list[f])
#       file1.close()


		
#################################################################################
			#########     This for vrf ID254 arp #################
#################################################################################
# for f in range (0, len(Hostname_Output_list)) :
#       file1 = codecs.open(Hostname_Output_list[f]+"__ID254.txt", encoding='utf-8',mode="w+")
#       file1.write(Configuration_Output_ID254_list[f])
#       file1.close()

##################################################################################################
############### Thread For SCP to send and save file to on remote linux server ######################
##################################################################################################
# for x in Hostname_Output_list:
#       try:
#               # X is text that  you want to save , x+'.txt' is filename 
#               z=x+".txt"
#               my_thread2 = threading.Thread(target=loginandcopy, args=('172.100.130.110','root','toor',z,(z)))
#               # my_thread2 = threading.Thread(target=loginandcopy, args=('172.100.130.171','root','toor',(x),(x+'.txt')))
#               my_thread2.start()
#       except Exception:
#               print (" Thread Of Copying\t"+ x+"\n")
# main_thread = threading.currentThread()
# for some_thread in threading.enumerate():
#       if some_thread != main_thread:
#               print(some_thread)
#               some_thread.join()


		# subprocess.call(["rm",z ])


# subprocess.call(["rm", Global_Output[0]])
# loginandcopy('10.231.0.84','khyat','P@ssw0rd',Global_Output[0],Global_Output[0])
# loginandcopy('172.100.130.171','root','toor',"Karate.txt","Karate.txt")
# FileNameRm ="Karate"+".txt"

# for n in Hostname_Output_list:
#       try:
#               # X is text that  you want to save , x+'.txt' is filename 
#               m=n+".txt"
#               my_thread2 = threading.Thread(target=subprocess.call, args=('rm',m,(m)))
#               my_thread2.start()
#       except Exception:
#               print (" Thread Of Deleting\t"+ n+"\n")
# main_thread = threading.currentThread()
# for some_thread in threading.enumerate():
#       if some_thread != main_thread:
#               print(some_thread)
#               some_thread.join()

# for n in Hostname_Output_list: 
#       m=n+".txt"
#       subprocess.call(["rm",m ])

# for y in Hostname_Output_list :
#       FileNameRm=y+".txt"
#       subprocess.call(["rm",FileNameRm ])
####################################################################################################
####################################################################################################


# print ("\n\tOutput Summary ")
# for i in Global_Output :
#       print ("\t\t"+i)
#       time.sleep(1)
if len(Hostname_Output_list)!=0 :
	for i in Hostname_Output_list :
			print ("\t\t"+i)


if len(FailedIps)!=0 :
	print("\n\t\tFailedIps")
	for i in FailedIps :
			print('\t  '+i)
	print(f"\n\t\tLength of the Failed IPs  {len(FailedIps)}")
print(f"\n\t\tLength of the Hostname_Output_list IPs {len(Hostname_Output_list)}")
# print(f"\n\t\tLength of the num_New IPs {len(num_New)}")
print(f"\n\t\tLength of the IPs in the num  {len(num)}")

	############# these are the failed IPs while running threads together 
if len(FailedExceptionIps)!=0 : 
	print("\n\tFailed IPs in the main thread")
	print(FailedExceptionIps)
# print (FailedIps)


if len(num_New)!=0 :
	print ("\n\t\tNew Discovered IPs from cdp neighbors in num_New")
	print (num_New)
	print (f"\n\t\tNumber of New Discovered IPs {len(num_New)}")
	print (f"\n\t\tNumber of All IPs {len(num)+len(num_New)}")

	############# these are the Hardware module 
# if len(All_Hardware_Module_List)!= 0:
# 	print("\n\n\t\tAll Hardware Module List\n")
# 	for hardware in All_Hardware_Module_List :
# 		print(hardware)


	############# these are the empty Hardware module in the show version 
if len(Hardware_IP_Empty_List)!=0:
	print ("\n\t\tHardware Empty IPs")
	for c in Hardware_IP_Empty_List :
		print(c)
	print (f"\n\t\tNumber of All Hardware Empty IPs {len(Hardware_IP_Empty_List)}")

print("\n\tElapsed time: " + str(datetime.now() - start_time))
