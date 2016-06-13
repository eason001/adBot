import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display



def main():
    url_path = '/home/ubuntu/yi-ad-proj/urls.txt'
    img_path = '/home/ubuntu/yi-ad-proj/img/'
    src_path = '/home/ubuntu/yi-ad-proj/src/'
    img_ext = '.png'
    src_ext = '.txt'
    timeout = 30 #30 secs for timeout
    file = open(url_path,'r')

    display = Display(visible=0, size=(1024, 768))
    display.start()
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.set_page_load_timeout(timeout)

    while True:
        url = file.readline().strip()
        if url == '':
            break
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
	main()
