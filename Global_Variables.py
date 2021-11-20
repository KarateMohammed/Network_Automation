class Global_Variables:
	Directory_Path="D:/Scripts"
	# Directory_Path="/home/khayat"
	Source_IP_File_for_Ping="d.txt"
	Pinged_New_and_Old_IP_File="active.txt"
	Source_IP_File_for_Automation="s.txt"

	Pattern_Filter_in_CDP= "172."	## Pattern to filter in cdp neighbor command
	FailedIPs_Cumulative_File ="FailedIPs_Cumulative.txt"
	Finished_IPs_Old_File="Worked_IPs_Old.txt"
	New_Discovered_IPs_File="s_New.txt"
	New_Dict_IPs_File="Dict_IPs.json"
	Hardware_Modules_File="All_Hardware_Module_11.txt"
	# Sub_Directory_Path_for_Backup="/home/khayat/Karate_Backup_11"
	Sub_Directory_Path_for_Backup="D:/Scripts/Karate_Backup_Test"
	# Dict_all_IP_Usr_Pass_Ena={"ip":{"Connection_type":'',"k_Username":'',"k_Password":'',"k_Enable":''}}
	Dict_all_IP_Usr_Pass_Ena={}
	def __init (
		self,
		Directory_Path=Directory_Path,
		Source_IP_File_for_Ping=Source_IP_File_for_Ping,
		Pinged_New_and_Old_IP_File=Pinged_New_and_Old_IP_File,
		Source_IP_File_for_Automation=Source_IP_File_for_Automation,
		Pattern_Filter_in_CDP=Pattern_Filter_in_CDP,
		FailedIPs_Cumulative_File=FailedIPs_Cumulative_File,
		Finished_IPs_Old_File=Finished_IPs_Old_File,
		New_Discovered_IPs_File=New_Discovered_IPs_File,
		Hardware_Modules_File=Hardware_Modules_File,
		Sub_Directory_Path_for_Backup=Sub_Directory_Path_for_Backup) :

		self.Directory_Path=Directory_Path,
		self.Source_IP_File_for_Ping=Source_IP_File_for_Ping,
		self.Pinged_New_and_Old_IP_File=Pinged_New_and_Old_IP_File,
		self.Source_IP_File_for_Automation=Source_IP_File_for_Automation,
		self.Pattern_Filter_in_CDP=Pattern_Filter_in_CDP,
		self.FailedIPs_Cumulative_File=FailedIPs_Cumulative_File,
		self.Finished_IPs_Old_File=Finished_IPs_Old_File,
		self.New_Discovered_IPs_File=New_Discovered_IPs_File,
		self.Hardware_Modules_File=Hardware_Modules_File,
		self.Sub_Directory_Path_for_Backup=Sub_Directory_Path_for_Backup
		self.Dict_all_IP_Usr_Pass_Ena=Dict_all_IP_Usr_Pass_Ena
		self.New_Dict_IPs_File=New_Dict_IPs_File
