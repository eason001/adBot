import sys
import pp
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display



def main(n, root):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from pyvirtualdisplay import Display
    url_path = root + '/urls.txt'
    img_path = root + '/img/'
    src_path = root + '/src/'
    img_ext = '.png'
    src_ext = '.txt'
    timeout = 30 #30 secs for timeout
    file = open(url_path,'r')

    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    for i, line in enumerate(file):
    #while True:
        #url = file.readline().strip()
        if line == '' or i == n:
            break
        if i < n:
	    continue
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

    driver.close()
    display.stop()
    file.close()
    print "All jobs DONE~!"

if __name__=="__main__":
	root = sys.argv[1]
	n_cores = int(sys.argv[2])
        ppservers = ()
	job_server = pp.Server(n_cores, ppservers=ppservers)
        print "Starting pp with", job_server.get_ncpus(), "workers"	
	#job1 = job_server.submit(main, (n_cores,))
        #job1()        
	try:
       		with open(root + 'urls.txt') as f:
            		t_lines =  sum(1 for _ in f)
    	except IOError:
        	print "Error opening file: please check your path and permission."
	n_lines = t_lines / n_cores
        for i in range(n_cores+1):
		lines[i] = n_lines * (i+1)
	start_time = time.time()
	#inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
	jobs = [(line, job_server.submit(main,(line,root))) for line in lines]
	for line, job in jobs:
    		print "Job " + line + "..."
		print job()

	print "Time elapsed: ", time.time() - start_time, "s"
	job_server.print_stats()
