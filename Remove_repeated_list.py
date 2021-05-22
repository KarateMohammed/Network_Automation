##########################################################################
	###### this is script to remove repeated string in new file ####
##########################################################################
import os

with open('/home/khayat/All_Hardware_Module.txt', 'r') as file:
		num =file.read().splitlines()
file.close()

print (f"Len of num before removing repeated IPs is {len(num)}  {type(num)}")
num= list(dict.fromkeys(num))
print (f"Len of num after removing repeated IPs is {len(num)}  {type(num)}")

with open('/home/khayat/All_Hardware_Module_New.txt', 'a') as file:
	for i in num:
		file.write((str(i)+"\n"))
file.close()


with open('/home/khayat/All_Hardware_Module_New.txt', 'r') as file:
		num =file.read().splitlines()
file.close()

print (f"Len of num after creating file and removing repeated IPs is {len(num)}  {type(num)}")

