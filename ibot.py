###Welcome to ibot 
###Version: v2.1
###Author: Yi Ren Cheng

import sys
import pp
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display

		
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
        	driver.get_screenshot_as_file(img_path + domain + img_ext)
		print img_path + domain + img_ext + " saved successfully!"
        	html_source = driver.page_source
		f = open(src_path + domain + src_ext,'w')
		f.write(html_source.encode('utf-8'))
		f.close()
		print src_path + domain + src_ext + " saved successfully!"
	except TimeoutException:
		print "Ops, timeout occurred loading " + domain
		continue
	except:
		print domain + " failed for unknown reason..."
		continue
    file.close()
    driver.close()

    print "All jobs DONE~!"

if __name__=="__main__":
	root = sys.argv[1]
        n_cores = 8
	try:
       		with open(root + '/urls.txt') as f:
            		t_lines =  sum(1 for _ in f)
    	except IOError:
        	print "Error opening file: please check your path and permission."

	if len(sys.argv)>2:
		n_cores = int(sys.argv[2])

	if t_lines < n_cores:		
		n_cores = t_lines
 
        display = Display(visible=0, size=(1024, 768))
        display.start()

        ppservers = ()
	job_server = pp.Server(n_cores, ppservers=ppservers)
        print "Starting pp with", job_server.get_ncpus(), "workers"	

	n_lines = t_lines / n_cores
        lines = []
	for i in range(n_cores+1):
		lines.append(i)
	start_time = time.time()
	jobs = [(line, job_server.submit(main,(n_lines,line,root,display))) for line in lines]
	for line, job in jobs:
    		print "Job " + str(line) + "..."
		print job()

	print "Time elapsed: ", time.time() - start_time, "s"
	job_server.print_stats()

	display.stop()
