###Welcome to ibot 
###Version: v2.2
###Author: Yi Ren Cheng

import sys
import pp
import time
import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
import tempfile
import itertools as IT
import os
		
def main(n,l,root,display):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from pyvirtualdisplay import Display
    url_path = root + '/urls.txt'
    img_path = root + '/data/img/'
    src_path = root + '/data/src/'
    img_ext = '.png'
    src_ext = '.txt'
    file = open(url_path,'r')
    timeout = 30 #30 secs for timeout
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    i=0
    while True:
        url = file.readline().strip()
	url = 'http://' + url.split()[0] # url number
	print url
        if url == '' or i == (l+1)*n:
            break
        if i < l*n:
	    i += 1
	    continue
        i += 1
        domain = url.split('.')[1]
	print domain + "..."
        try:
		driver.get(url)
		img_name = uniquify(img_path + domain + img_ext)
		src_name = uniquify(src_path + domain + src_ext)
        	driver.get_screenshot_as_file(img_name)
		print img_name + " saved successfully!"
        	html_source = driver.page_source
		f = open(src_name,'w')
		f.write(html_source.encode('utf-8'))
		f.close()
		print src_name + " saved successfully!"
	except TimeoutException:
		print "Ops, timeout occurred loading " + domain
		continue
	except:
		print domain + " failed for unknown reason..."
		continue
    file.close()
    driver.close()

    print "All jobs DONE~!"


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
	url = 'http://' + url.split()[0] # url number
	print url
        if url == '':
            break
        domain = url.split('.')[1]
	print domain + "..."
        try:
		driver.get(url)
		img_name = uniquify(img_path + domain + img_ext)
		src_name = uniquify(src_path + domain + src_ext)
        	driver.get_screenshot_as_file(img_name)
		print img_name + " saved successfully!"
        	html_source = driver.page_source
		f = open(src_name,'w')
		f.write(html_source.encode('utf-8'))
		f.close()
		print src_name + " saved successfully!"
	except TimeoutException:
		print "Ops, timeout occurred loading " + domain
		continue
	except:
		print domain + " failed for unknown reason..."
		continue
    file.close()
    driver.close()
    display.stop()
    print "All jobs DONE~!"

def main_m(root,n_cores):

	try:
       		with open(root + '/urls.txt') as f:
            		t_lines =  sum(1 for _ in f)
    	except IOError:
        	print "Error opening file: please check your path and permission."

	if t_lines < n_cores:		
		n_cores = t_lines
 
        display = Display(visible=0, size=(1024, 768))
        display.start()

        ppservers = ()
	job_server = pp.Server(n_cores, ppservers=ppservers)
        print "Starting pp with", job_server.get_ncpus(), "workers"	

	n_lines = t_lines / (n_cores-1)
        lines = []
	for i in range(n_cores):
		lines.append(i)
	start_time = time.time()
	jobs = [(line, job_server.submit(main,(n_lines,line,root,display))) for line in lines]
	for line, job in jobs:
    		print "Job " + str(line) + "..."
		print job()

	print "Time elapsed: ", time.time() - start_time, "s"
	job_server.print_stats()

	display.stop()

def uniquify(path, sep = ''):
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

