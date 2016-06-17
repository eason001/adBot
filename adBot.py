###Welcome to adBot 
###Version: v 1.3.1
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
	url = 'http://' + url.split()[0] # url number
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


def scrape_s(root,timeout):
    url_path = './urls.txt'
    img_path = root + '/data/img/'
    src_path = root + '/data/src/'
    img_ext = '.png'
    src_ext = '.txt'
    file = open(url_path,'r')
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(timeout)

    while True:
        url = file.readline().strip()
	print url
	logging.info(url)
        if url == '':
            break
	url = 'http://' + url.split()[0] # url number
        domain = url.split('.')[1]
	print domain + "..."
        logging.info(domain + "...")
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
	except Exception, e:
    		print 'Failed: '+ str(e)
    		logging.info('Failed: '+ str(e))
		continue
    file.close()
    driver.close()
    print "All jobs DONE~!"
    logging.info("All jobs DONE~!")

def scrape_m(root,n_cores,timeout):
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

def Choose(x):
    unused_var = os.system("clear")
    if x == '1':
	root = raw_input("enter an output path: ")	
	n_cores = raw_input("enter the number of jobs: ")	
	timeout = raw_input("timeout in sec: ")
	mode = 0

	if root == '':
		root = "."
	if n_cores != '':
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

	if n_cores>1:
		mode = 1
		
	if n_cores > multiprocessing.cpu_count():
		n_cores = multiprocessing.cpu_count()

	if  mode == 0:
		scrape_s(root,timeout)
	else:
		scrape_m(root,n_cores,timeout)
     
    elif x == '2':
	while True:
		print 'Cleaning data'
		print '0 - Back to main menu'
		user_input = raw_input("Choose option: ")
		if user_input == '0' or user_input == '':
			unused_var = os.system("clear")
			main()	
    elif x == '0':
	sys.exit()

def main():
	while True:
#		unused_var = os.system("clear")
		print "Welcome to adBot v 1.3.1"
		print "please choose one of the follow options:"
		print "1 - Scraing data (input file: ./urls.txt)"
		print "2 - Cleaning data"
		print "0 - Exit"
		user_input = raw_input("Choose option: ")	
		Choose(user_input)

if __name__=="__main__":

	logging.basicConfig(filename='./debug.log',level=logging.INFO)
	main()


