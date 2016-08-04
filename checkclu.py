import os
import sys

img_path = "/mnt/clean_data/img/"
aux_path = "/mnt/clean_data/aux/"
s3_path = "s3://digitas-admin/home/yi.cheng/aux_data"
file = open("/home/ubuntu/yi/extracted_features/cluster_data",'r')
index = " " + sys.argv[1]

os.system("sudo rm " + aux_path + "*")

for line in file:
	if index in line:
		name = line.split(" ")[0] + ".png"
		os.system("cp " + img_path + name + " " + aux_path)

os.system("aws s3 cp " + aux_path + " " + s3_path + " --recursive --sse")
