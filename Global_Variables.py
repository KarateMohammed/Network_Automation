class Global_Variables:
	Directory_Path="/home/khayat"
	Source_IP_File_for_Ping="d.txt"
	Pinged_New_and_Old_IP_File="active.txt"
	Source_IP_File_for_Automation="s.txt"

	Pattern_Filter_in_CDP= "172."	## Pattern to filter in cdp neighbor command
	FailedIPs_Cumulative_File ="FailedIPs_Cumulative.txt"
	Finished_IPs_Old_File="Worked_IPs_Old.txt"
	New_Discovered_IPs_File="s_New.txt"
	Hardware_Modules_File="All_Hardware_Module_Test_1.txt"
	Sub_Directory_Path_for_Backup="/home/khayat/Test_New_Auto"
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

