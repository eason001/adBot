###Welcome to adBot 
###Version: v 1.4.2
###Author: Yi Ren Cheng

import sys
import pp
import time
import logging
import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import tempfile
import itertools as IT
import os
import re
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from PIL import Image
from skimage import filters
from skimage.color import rgb2gray
from skimage import feature
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity
from scipy import ndimage as ndi
import math
from skimage.morphology import skeletonize

def as_gray(image_filter, image, *args, **kwargs):
    gray_image = rgb2gray(image)
    return image_filter(gray_image, *args, **kwargs)

@adapt_rgb(as_gray)
def original_gray(image):
    return image

@adapt_rgb(as_gray)
def skeleton_gray(image):
    return skeletonize(image)

@adapt_rgb(as_gray)
def canny_gray(image,p):
    return feature.canny(image,sigma=p)

@adapt_rgb(as_gray)
def sobel_gray(image):
    return filters.sobel(image)

@adapt_rgb(as_gray)
def roberts_gray(image):
    return filters.roberts(image)

		
def scrape(n,l,root,file_array,timeout):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    import logging
    url_path = './urls.txt'
    img_path = root + '/data/img/'
    src_path = root + '/data/src/'
    img_ext = '.png'
    src_ext = '.txt'
    file = open(url_path,'r')
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    start_pointer = l*n
    end_pointer = (l+1)*n
    if end_pointer > len(file_array):
	end_pointer = len(file_array)
    for i in range(start_pointer,end_pointer):
	url = file_array[i]
	url = 'http://' + url.split()[0]
        domain = url.split('.')[1]
	print "from " + domain + " ->"
	print "processing... " + url
	logging.info("from " + domain + " ->")
	logging.info("processing... " + url)
        try:
		driver.get(url)
		img_name = uniquify(img_path + domain + img_ext)
		src_name = uniquify(src_path + domain + src_ext)
        	driver.get_screenshot_as_file(img_name)
		print img_name + " saved successfully!"
		logging.info(img_name + " saved successfully!")
        	html_source = driver.page_source
		f = open(src_name,'w')
		f.write(html_source.encode('utf-8'))
		f.close()
		print src_name + " saved successfully!"
		logging.info(src_name + " saved successfully!")
	except TimeoutException:
		print "Ops, timeout occurred loading " + domain
		logging.info("Ops, timeout occurred loading " + domain)
		continue
	except Exception,e:
		print domain + " failed: " + str(e)
		logging.info(domain + " failed: " + str(e))
		continue
    file.close()
    driver.close()

    print "All jobs DONE~!"
    logging.info("All jobs DONE~!")

def scrape_m():
	root = raw_input("enter an output path: ")	
	n_cores = raw_input("enter the number of jobs: ")	
	timeout = raw_input("timeout in sec: ")

	if root == '':
		root = "."
	if n_cores != '' and n_cores != '0':
		n_cores = int(n_cores)
	else:
		n_cores = 1
	if  timeout != '':
		timeout = int(timeout)
	else:
		timeout = 30 

	if not os.path.exists(root + "/data"):
    		os.makedirs(root+"/data/img")
    		os.makedirs(root+"/data/src")
		
	if n_cores > multiprocessing.cpu_count():
		n_cores = multiprocessing.cpu_count()

	file_array=[]
	try:
       		with open('./urls.txt') as f:
			for l in f:
        			file_array.append(l)
		t_lines = len(file_array)
		print "len: ", len(file_array)
    	except IOError:
        	print "Error opening file: please check your path and permission."
        	logging.info("Error opening file: please check your path and permission.")

	if t_lines < n_cores:		
		n_cores = t_lines
 
        ppservers = ()
	job_server = pp.Server(n_cores, ppservers=ppservers)
        print "Starting pp with", job_server.get_ncpus(), "workers"	
        logging.info("Starting pp with" + str(job_server.get_ncpus()) + "workers")	
	
	if n_cores == 1:
		n_lines = t_lines
		scrape(n_lines,0,root,file_array,timeout)
	elif n_cores > 1:
		n_lines = t_lines / (n_cores-1)
		lines = []
		for i in range(n_cores):
			lines.append(i)
		start_time = time.time()
		jobs = [(line, job_server.submit(scrape,(n_lines,line,root,file_array,timeout),(uniquify,))) for line in lines]
		for line, job in jobs:
    			print "Job " + str(line) + "..."
			print job()
    			logging.info("Job " + str(line) + "...")
			logging.info(job())

		print "Time elapsed: ", time.time() - start_time, "s"
		job_server.print_stats()
        else:
		print "No job to run, please check your input file urls.txt."
	

def uniquify(path, sep = ''):
    import tempfile
    import itertools as IT
    import os

    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename

def aws():
	print "Transfering data with AWS S3 (USE ABSOLUTE PATH)"
	print "i.e. s3://digitas-admin/home/<user_name>/ <--> /home/ubuntu/<dir_path>"
	from_path = raw_input("from: ")
	to_path = raw_input("to: ")	

	if from_path == '':
		from_path = "s3://digitas-admin/home/yi.cheng/"
	elif from_path.split()[0] == 's3':
		from_path = "s3://digitas-admin/home/yi.cheng/" + from_path.split()[1]
	elif from_path.split()[0] == '.':
		from_path = os.getcwd() + "/" + from_path.split()[1]

	if to_path == '':
		to_path = os.getcwd() + "/"
	elif to_path.split()[0] == 's3':
		to_path = "s3://digitas-admin/home/yi.cheng/" + to_path.split()[1]
	elif to_path.split()[0] == '.':
		to_path = os.getcwd() + "/" + to_path.split()[1]

	try:
		os.system("aws s3 cp " + from_path + " " + to_path + " --recursive --sse")
	except Exception,e:
		print "failed: " + str(e)

def clean():
	limit_size = 2451971 # 21565
	while True:
		print 'Cleaning data'
		print '1 - Remove garbage data'
		print '0 - Back to main menu'
		user_input = raw_input("Choose option: ")
		if user_input == '0' or user_input == '':
			unused_var = os.system("clear")
			main()	
		elif user_input == '1':
			cln_path = raw_input("Enter a data path to clean: ")
			img_dir = cln_path + "/img/"
			src_dir = cln_path + "/src/"
			countI = 0
			countS = 0
			rm_flag = "N"

			try:
        			for file in os.listdir(img_dir):
                			if file.endswith(".png") and int(os.stat(img_dir + file).st_size) <= limit_size:
                        			countI += 1
				rm_flag = raw_input(str(countI) + " garbage data found, do you want remove all of them (Y/N): ")
			except OSError:
				pass
		
			countI = 0			
			if rm_flag == 'Y' or rm_flag == 'Yes' or rm_flag == 'y' or rm_flag == 'yes':
				try:
        				for file in os.listdir(img_dir):
                				if file.endswith(".png") and int(os.stat(img_dir + file).st_size) <= limit_size:
							fileS = file.split(".")[0] + '.txt'
							if os.path.isfile(src_dir + fileS):
								os.remove(src_dir + fileS)
								countS += 1 
                        				os.remove(img_dir + file)
							countI += 1
					print "number of garbage img files removed: " + str(countI)
					print "number of garbage src files removed: " + str(countS)			
				except OSError:
        				pass
			else:
				unused_var = os.system("clear")
				clean()
				
		else:
			unused_var = os.system("clear")
			clean()

def compress():
	from PIL import Image
	
	compress_path = raw_input("Enter an image path to compress: ")
	cutfile_path = raw_input("Enter a path for output text file: ")
	gray_flag = raw_input("Compress it in Grayscale (Y/N): ")	
        filter = raw_input("Input a filter (default: grayscale): ")

	if gray_flag == '':
		gray_flag = 'N'
	
	if compress_path == '':
		compress_path = './data/img/'
	if cutfile_path == '':
		cutfile_path = './'
	
	if not os.path.isdir(compress_path) or not os.path.isdir(cutfile_path):
		print "Directory does not exist, please enter a valid path."
		compress()
	
	cutfile = open(cutfile_path + '/compressed_data', 'w')

	T_size = (80,20)
	L_size = (35,65)
	R_size = (35,65)

	T_box = (1, 1, 1400, 350)
	L_box = (1, 350, 350, 1000)
	R_box = (1050, 350, 1400, 1000)

        canny_sigma = 1
	counter = 0
	max_count = 4
	i = 0
	n_files = 0

        for file in os.listdir(compress_path):
                if file.lower().endswith(('.png','.jpg','.jpeg','.gif')):
                        n_files += 1

	for file in os.listdir(compress_path):
	    if file.lower().endswith(('.png','.jpg','.jpeg','.gif')):		
                i += 1
                print("compressing..." + file + ' ' +  str(i) + '/' + str(n_files))
        	im = Image.open(compress_path + "/" + file)
        	cutfile.write(file.split(".")[0])
        ######Filters####
                if filter == 'grayscale':
                        im = original_gray(np.array(im))
                        im = Image.fromarray(np.uint8(im*255))
                if filter == 'sobel':
                        im = 1-sobel_gray(np.array(im))
                        im = Image.fromarray(np.uint8(im*255))
                if filter == 'roberts':
                        im = 1-roberts_gray(np.array(im))
                        im = Image.fromarray(np.uint8(im*255))
                if filter == 'canny':
                        im = 1-canny_gray(np.array(im),canny_sigma)
                        im = Image.fromarray(np.uint8(im*255))
                if filter == 'skeleton':
                        im = 1-skeleton_gray(np.array(im))
                        im = Image.fromarray(np.uint8(im*255))

	######TOP REGION######
        	region = im.crop(T_box)
        	region.thumbnail(T_size)
		if gray_flag == 'Y' or gray_flag == 'Yes' or gray_flag == 'y' or gray_flag == 'yes':
			region = region.convert('LA')
			max_count = 2        	
		imarray = list(region.getdata())
        	for item in imarray:
			counter = 0
			for x in item:
				counter += 1
				if counter < max_count:
                			cutfile.write(" " + str(x))

	######LEFT REGION######
        	region = im.crop(L_box)
        	region.thumbnail(L_size)
		if gray_flag == 'Y' or gray_flag == 'Yes' or gray_flag == 'y' or gray_flag == 'yes':
			region = region.convert('LA') 
			max_count = 2       	
	        imarray = list(region.getdata())
        	for items in imarray:
			counter = 0
			for x in item:
				counter += 1
				if counter < max_count:
                			cutfile.write(" " + str(x))

	######RIGHT REGION######
        	region = im.crop(R_box)
        	region.thumbnail(R_size)
		if gray_flag == 'Y' or gray_flag == 'Yes' or gray_flag == 'y' or gray_flag == 'yes':
			region = region.convert('LA') 
			max_count = 2       	
	        imarray = list(region.getdata())
        	for items in imarray:
			counter = 0
			for x in item:
				counter += 1
				if counter < max_count:
                			cutfile.write(" " + str(x))

        	cutfile.write('\n')

	cutfile.close()

	inputfile = open(cutfile_path + '/compressed_data', 'r')
	for line in inputfile:
		input_n = len(line.split(" "))
		print "compressed data set has " + str(input_n) + " features"
		break
	
	inputfile.close()

def reduce():
	from pyspark import SparkContext
	from pyspark.sql import SQLContext, Row
	from pyspark.ml.feature import PCA
	from pyspark.mllib.feature import PCA as PCAmllib
	from pyspark.mllib.linalg import Vectors
	from pyspark import SparkConf, SparkContext

	input_file = raw_input("Enter input data set (absolute path required): ")
	output_path = raw_input("Enter a path for output data (must be an empty directory): ")	

	if input_file == '':
		input_file = os.getcwd() + '/data/compressed_data/compressed_data'

	if output_path == '':
		output_path = os.getcwd()
	
	if not os.path.isfile(input_file):
		print "Input File do not exist."
		reduce()
	if not os.path.isdir(output_path):
		print "Directory path is invalid."
		reduce()
	
	inputfile = open(input_file, 'r')
	for line in inputfile:
		input_n = len(line.split(" "))
		print "Selected data set has " + str(input_n) + " features"
		break
	
	inputfile.close()
	
	reduced_n = raw_input("Enter the number of features you want to reduce to: ")
	if int(reduced_n) >= input_n:
		print "reduced features must be smaller than input features."
		reduce()

	try:
		os.system("export _JAVA_OPTIONS='-Xms1g -Xmx40g'")
		if os.path.isdir(output_path + "/reducedFeatures"):
			os.system("rm -r " + output_path + "/reducedFeatures")
	except Exception,e:
		print "failed: " + str(e)

	print "Please select a dimension reduction method:"
	print "1 - PCA"
	print "x - Back"
	option = raw_input("Choose option: ")

	if option == '1':

		conf = (SparkConf().set("spark.driver.maxResultSize", "5g"))
		sc = SparkContext(conf=conf)
		sqlContext = SQLContext(sc)
		lines = sc.textFile(input_file).map(lambda x:x.split(" "))
		lines = lines.map(lambda x:(x[0],[float(y) for y in x[1:]]))
		df = lines.map(lambda x: Row(labels=x[0],features=Vectors.dense(x[1]))).toDF()

		###with ml
		pca = PCA(k=int(reduced_n),inputCol="features", outputCol="pca_features")
		model = pca.fit(df)
		outData = model.transform(df)
		pcaFeatures = model.transform(df).select("labels","pca_features")

		###Write out
		pcaFeatures.rdd.repartition(1).saveAsTextFile(output_path + "/reducedFeatures")

		outputfile = open(output_path + '/reduced_data', 'w')
		inputfile = open(output_path + '/reducedFeatures/part-00000', 'r')
		for line in inputfile:
        		x = line.split("[")[1].split("]")[0]
        		x = re.sub(',','',x)
        		y = line.split("'")[1]
			outputfile.write(y + " " + x + '\n')
		inputfile.close()
		outputfile.close()	
		sc.stop()
		print "Dimension reduction finished!"
		main()
	
	if option == 'x':
		main()

	print "invalid option"
	main()
				
def cluster():
	from pyspark import SparkContext
	from pyspark.sql import SQLContext, Row
	from pyspark.ml.feature import PCA
	from pyspark.mllib.feature import PCA as PCAmllib
	from pyspark.mllib.linalg import Vectors
	from pyspark import SparkConf, SparkContext
	from pyspark.ml.clustering import KMeans
	from numpy import array
	from math import sqrt

	input_file = raw_input("Enter input data set (absolute path required): ")
	output_path = raw_input("Enter a path for output data (must be an empty directory): ")	

	if input_file == '':
		input_file = os.getcwd() + '/data/reduced_data/reduced_data'

	if output_path == '':
		output_path = os.getcwd()
	
	if not os.path.isfile(input_file):
		print "Input File do not exist."
		cluster()
	if not os.path.isdir(output_path):
		print "Directory path is invalid."
		cluster()
	
	try:
		os.system("export _JAVA_OPTIONS='-Xms1g -Xmx40g'")
		if os.path.isdir(output_path + "/clusterFeatures"):
			os.system("rm -r " + output_path + "/clusterFeatures")
	except Exception,e:
		print "failed: " + str(e)

	print "Please select a clustering method:"
	print "1 - KMeans"
	print "x - Back"
	option = raw_input("Choose option: ")

	if option == '1':

		conf = (SparkConf().set("spark.driver.maxResultSize", "5g"))
		sc = SparkContext(conf=conf)
		sqlContext = SQLContext(sc)
		lines = sc.textFile(input_file).map(lambda x:x.split(" "))
		lines = lines.map(lambda x:(x[0],[float(y) for y in x[1:]]))
		df = lines.map(lambda x: Row(labels=x[0],features=Vectors.dense(x[1]))).toDF()
		pdf = df.toPandas()
		###with ml
		kmeans = KMeans(k=2, seed=1,initSteps=5, tol=1e-4, maxIter=20, initMode="k-means||", featuresCol="features")
        	model = kmeans.fit(df)
       	 	kmFeatures = model.transform(df).select("features", "prediction")
		
		###Evaluation
		rows = kmFeatures.collect()
		WSSSE = 0
		for i in rows:
    			WSSSE += sqrt(sum([x**2 for x in (model.clusterCenters()[i[1]]-i[0])]))
		print("Within Set Sum of Squared Error = " + str(WSSSE))

		###Write out
		kmFeatures.rdd.repartition(1).saveAsTextFile(output_path + "/clusterFeatures")

		outputfile = open(output_path + '/cluster_data', 'w')
		inputfile = open(output_path + '/clusterFeatures/part-00000', 'r')
		for line in inputfile:
        		x = line.split("=")[2].split(")")[0]
        		x = re.sub(',','',x)
        		outputfile.write(x+'\n')
		inputfile.close()
		outputfile.close()	
		sc.stop()
		print "Data Clustering finished!"
		main()
	
	if option == 'x':
		main()

	print "invalid option"
	main()
	
def extract():
    input_path = raw_input("Enter input data path (absolute path required): ")
    if not os.path.isdir(input_path):
	print "Directory path is invalid."
	main()
    output = open(input_path + "/extracted_features",'w')
    src_path = input_path + "/src"
    img_path = input_path + "/img"
    output.write("file_name ads_pattern external_links \n")
    for file in os.listdir(src_path):
	txt_file = open(src_path + "/" + file,'r')
        ad_count = 0
        ex_count = 0
        domain = file.split(".")[0].rstrip('1234567890')
        for line in txt_file:
                ad_count += len(re.findall("_ad_|_ads_|-ad-|-ads-", line))
                link = line.split("href=\"http://www.")
                for i in range(len(link)):
                        if i!=0 and not link[i].startswith(domain):
                                ex_count += 1

                links = line.split("href=\"https://www.")
                for i in range(len(links)):
                        if i!=0 and not links[i].startswith(domain):
                                ex_count += 1

        print file + " has " + str(ad_count) + " ads   " + str(ex_count) + " links"
	output.write(file.split(".")[0] + " " + str(ad_count) + " " + str(ex_count) + "\n")
	txt_file.close()
    output.close()
    main()

def Choose(x):
    unused_var = os.system("clear")
    if x == '1':
	scrape_m()
        main()

    elif x == '2':
	clean()

    elif x == '3':
	compress()

    elif x == '4':
	reduce()

    elif x == '5':
	cluster()

    elif x == '6':
	extract()

    elif x == 'a':
	aws()
   
    elif x == '0':
	sys.exit()
   
    else:
	unused_var = os.system("clear")
	main()

def main():
	while True:
		print "Welcome to adBot v 1.3.1"
		print "please choose one of the follow options:"
		print "1 - Scraping data (input file: ./urls.txt)"
		print "2 - Cleaning data"
		print "3 - 3C Steps (Cutting -> Compressing -> Converting)"
		print "4 - Dimension Reduction"
		print "5 - Clustering"
		print "6 - Feature Extraction"
		print "a - Transfering data with AWS S3"
		print "0 - Exit"
		user_input = raw_input("Choose option: ")	
		Choose(user_input)

if __name__=="__main__":

	logging.basicConfig(filename='./debug.log',level=logging.INFO)
	main()


