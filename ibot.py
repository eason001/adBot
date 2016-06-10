import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display



def main():
    url_path = '/home/ubuntu/yi-ad-proj/urls.txt'
    img_path = '/home/ubuntu/yi-ad-proj/img/'
    src_path = '/home/ubuntu/yi-ad-proj/src/'
    file = open(url_path,'r')
    display = Display(visible=0, size=(1024, 768))
    display.start()

    while True:
        url = file.readline().strip()
        if url == '':
            break
        domain = url.split('.')[1]
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        driver.get_screenshot_as_file(img_path + domain + '.png')
        html_source = driver.page_source
	f = open(src_path + domain + '.txt','w')
	f.write(html_source.encode('utf-8'))
	f.close()
        #wait = WebDriverWait(driver, 3600)  # 3600s
        driver.close()
    display.stop()

if __name__=="__main__":
	main()
