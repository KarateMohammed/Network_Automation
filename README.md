# Network_Automation
Network Automation  for traditional network



Things you need to do before running scripts :: 
----------------------------
1- set username . password and enable password
2- set Directory_Path in global variables file
3- set number of iteration in Loop_Scripts
4- set Pattern_Filter_in_CDP in Global_Variables.py
5- set All_Hardware_Module_Test_1 in Global variables


Loop_Scripts :: 
----------------------------
 execute scripts many times
 	First :: Ping_Test.py
 			import Useful_Fun script
 			put active ips in file 
 			put inactive ips in file 
 			pass active ips to new file to use it in automation


 	Second	:: Discover_New_IPs




