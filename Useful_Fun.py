
import re
import os
import os.path


from array import *
import scp
from paramiko import SSHClient
import paramiko
import codecs
import subprocess

# class Useful_Fun :

#############  Check ping ##################
def ping_is_successful(ping_result):
		return True if '!' in ping_result else False

#############  Check Date of Cetifaction ##################
def CheckDateOfCertifcation(date_output , CheckOn):
		return True if str(CheckOn) in date_output else False




##############################################################################
##################### The Get_Interfaces_Status Function ##################### 
##############################################################################

def Get_All_Inter(Description_to_Lines_List=[]):
	counter_num=0
	List_each_Line=[]
	Description_to_Lines_List = Description_to_Lines_List.splitlines()
	for i in Description_to_Lines_List :
		String_whole_Line=i.lstrip() ### remove leading Spaces
		String_whole_Line = re.sub(" +"," ",String_whole_Line)  ### Replace repeated spaces with single space
		List_String_Line =String_whole_Line.split() ###  change String into list 
		if len(List_String_Line)<6:   ## esc any empty string
			continue                
		List_each_Line.insert (counter_num ,List_String_Line[0:1]) ### append first  element in list to global list
		List_each_Line[counter_num ].append (List_String_Line[-5]) ### append Status element in list to global list
		List_each_Line[counter_num ].append (List_String_Line[-4]) ### append Vlan element  in list to global list
		counter_num=counter_num+1
	List_each_Line.pop(0) # Pop the first index which is the header

	return List_each_Line


def Get_Ports_Status (List_of_Lines=[]):
	Returned_List={"trunk":[],"connected":[],"notconnect" : [], "disabled":[],"err":[] , "access":[], "routed":[] }
	for x in List_of_Lines :
		if x[-1]=="trunk":
			Returned_List["trunk"].append(x[0])
		elif x[-1]== "routed" :
			Returned_List["routed"].append(x[0])
		else :
			Returned_List["access"].append(x[0])
		if x[-2]=="connected" :
			Returned_List["connected"].append(x[0])
		elif x[-2]=="notconnect" :
			Returned_List["notconnect"].append(x[0])
		elif x[-2]=="disabled" :
			Returned_List["disabled"].append(x[0])
		elif "err" in x[-2]  :
			Returned_List["err"].append(x[0])
	return Returned_List



##############################################################################
##################### The Get_CDP_Neighbors Function  ##################### 
##############################################################################

def Get_CDP_Neighbors (CDP_ALL_string="" , Old_IP_list=[]) :

	CDP_Lines_List=CDP_ALL_string.splitlines()  # change output to list of lines
	CDP_IPs_List=[]
	New_IPs_list=[]
	# change list of line to list of IPs wihtout IP address sentence
	for i in CDP_Lines_List :
		j=i.lstrip("IP address: ")
		CDP_IPs_List.append(j)

	# check on each ip if it's in the mangement range or not and append it to new list if it's not exsit in the IPs list
	for i in CDP_IPs_List :
		if "172" in i :
			# check on the IP to add it to the list
			if i not in Old_IP_list :
				New_IPs_list.append(i)
	New_IPs_list= list(dict.fromkeys(New_IPs_list))
	return New_IPs_list       


##############################################################################
##################### The Get_Interfaces_IP Function  ##################### 
##############################################################################
def Get_Interfaces_IP(Description_All_Interfaces):

		List_each_Line=[]
		UP_ports=[]
		Down_ports=[]
		AdminDown_ports=[]
		counter_num=0
		Return_Counter=0
		Return_All_Lists=[]
		Description_to_Lines_List=Description_All_Interfaces.splitlines()  # change output to list of lines
		for i in Description_to_Lines_List :
			String_whole_Line=i.lstrip() ### remove leading Spaces
			String_whole_Line = re.sub(" +"," ",String_whole_Line)  ### Remove repeated spaces
			List_String_Line =String_whole_Line.split() ###  change String into list 
			if len(List_String_Line)==0:   ## esc any empty string
				continue                
			List_each_Line.insert (counter_num ,List_String_Line[0:2]) ### append first 2 element in list to global list
			List_each_Line[counter_num ].append (List_String_Line[-2]) ### append last element in list (Protocol) to global list
			List_each_Line[counter_num ].append (List_String_Line[-1]) ### append second last element (Status) in list to global list
			
			counter_num=counter_num+1
		List_each_Line.pop(0) # Pop the first index which is the header
		Return_All_Lists =List_each_Line  # List of interaces, IPs, Protocol, Status  

		return Return_All_Lists


    
##############################################################################
##################### The Validate Function for IPs ##################### 
##############################################################################

def Validate_ip(ip):
	if len(ip)<=0 :
		return False
	a = ip.split('.')
	if len(a) != 4:
		return False
	for x in a:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True


def Validate_List_ip(ip_List) :
	Pop_Index_List=[]
	for x in range(len(ip_List)) :
		ip_List[x] = re.sub(" +","",ip_List[x])  ### Remove repeated spaces 

	for x in range(len(ip_List)) :
		ip_List[x]=ip_List[x].strip()
		if not Validate_ip(ip_List[x]) :   # Call Validate ip Function  
			Pop_Index_List.append(x)		# append invalid index to pop them later  

	Pop_Index_List.reverse() # Reverse list to begain from the last index to avoid error of end list 
	for i in Pop_Index_List :
		ip_List.pop(i)
	return ip_List


##############################################################################
##################### The SCP Function of configuration ##################### 
##############################################################################

def loginandcopy(hostname='10.231.0.84',uname='khyat',pwd='P@ssw0rd',sfile='a1.py',tfile='a1.py'):
		try:
				client = SSHClient()
				client.load_system_host_keys()
				client.connect(hostname,port=22,username=uname,password=pwd)
		except paramiko.AuthenticationException:
				print("Authentication failed, please verify your credentials: %s")
		except paramiko.SSHException as sshException:
				print("Unable to establish SSH connection: %s" % sshException)
		except paramiko.BadHostKeyException as badHostKeyException:
				print("Unable to verify server's host key: %s" % badHostKeyException)
		except Exception as e:
				print(e.args)
		try:
				GetTransport=client.get_transport()
				scpclient = scp.SCPClient(GetTransport)
				scpclient.put(sfile,tfile)
		except scp.SCPException as e:
				print("Operation error: %s", e) 
# loginandcopy('10.231.0.84','khyat','P@ssw0rd','a1.py','a1.py')

