###Welcome to ibot 
###Version: v2.2
###Author: Yi Ren Cheng

import sys
import pp
import time
import multiprocessing
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
import tempfile
import itertools as IT
import os
		
def main(n,l,root,display):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    import logging
    url_path = root + '/urls.txt'
    img_path = root + '/data/img/'
    src_path = root + '/data/src/'
    img_ext = '.png'
    src_ext = '.txt'
    file = open(url_path,'r')
    timeout = 30 #30 secs for timeout
#    driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    i=0
    while True:
        url = file.readline().strip()
	#print url
        if url == '' or i == (l+1)*n:
            break
        if i < l*n:
	    i += 1
	    continue
        i += 1
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


def main_s(root):
    url_path = root + '/urls.txt'
    img_path = root + '/data/img/'
    src_path = root + '/data/src/'
    img_ext = '.png'
    src_ext = '.txt'
    file = open(url_path,'r')
    timeout = 30 #30 secs for timeout
    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    i=0
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
#	except:
#		print domain + " failed for unknown reason..."
#		continue
	except Exception, e:
    		print 'Failed: '+ str(e)
    		logging.info('Failed: '+ str(e))
		continue
    file.close()
    driver.close()
    display.stop()
    print "All jobs DONE~!"
    logging.info("All jobs DONE~!")

def main_m(root,n_cores):

	try:
       		with open(root + '/urls.txt') as f:
            		t_lines =  sum(1 for _ in f)
    	except IOError:
        	print "Error opening file: please check your path and permission."
        	logging.info("Error opening file: please check your path and permission.")

	if t_lines < n_cores:		
		n_cores = t_lines
 
        display = Display(visible=0, size=(1024, 768))
        display.start()

        ppservers = ()
	job_server = pp.Server(n_cores, ppservers=ppservers)
        print "Starting pp with", job_server.get_ncpus(), "workers"	
        logging.info("Starting pp with" + str(job_server.get_ncpus()) + "workers")	

	n_lines = t_lines / (n_cores-1)
        lines = []
	for i in range(n_cores):
		lines.append(i)
	start_time = time.time()
	jobs = [(line, job_server.submit(main,(n_lines,line,root,display),(uniquify,))) for line in lines]
	for line, job in jobs:
    		print "Job " + str(line) + "..."
		print job()
    		logging.info("Job " + str(line) + "...")
		logging.info(job())

	print "Time elapsed: ", time.time() - start_time, "s"
	job_server.print_stats()

	display.stop()

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

if __name__=="__main__":
	logging.basicConfig(filename='/mnt/yi-ad-proj/debug.log',level=logging.INFO)
	root = sys.argv[1]
	mode = 0
        n_cores = multiprocessing.cpu_count()

	if len(sys.argv)>2:
		mode = 1
		n_cores = int(sys.argv[2])
		
	if n_cores > multiprocessing.cpu_count():
		n_cores = multiprocessing.cpu_count()

	if  mode == 0:
		main_s(root)
	else:
		main_m(root,n_cores)

