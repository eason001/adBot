###Welcome to ibot 
###Version: v2.1
###Author: Yi Ren Cheng

import sys
import pp
import time
import glob
import multiprocessing
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
import tempfile
import itertools as IT
import os

def main(root):
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
    print "lets start..."
    
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
	main(root)
