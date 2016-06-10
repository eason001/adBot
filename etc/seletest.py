import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from pyvirtualdisplay import Display


def main():
	driver = webdriver.Firefox()

def getSubCategory(argument):
    switcher = {
        3: "Action",
        4: "Puzzle",
        6: "Card/Casino",
	9: "Arcade",
	10: "Sports",
    }
    return switcher.get(argument, "Others")

def TZsubmit():
	p_id = '135769'
	p_name = 'Wolf and Sheep'
	sellingEndDate = '2025-12-30'
	comment = 'testing' #optional
	description = 'testing'
	tags = p_name
	category = 'Entertainment'
	age = 'All'
	#dlurl = 'http://go.openmobileappmall.com?op=dlman&pd=123691&sig=266ef7ef3e506b4d71693a824570ecb5'
	rooturl = '/home/yi/openM/tz_upload/'
	fileURL = rooturl + 'com_brodski_android_wolfandsheep_2_6_0_arm_1_0_119.tpk'
	iconURL = rooturl + 'thumb512.png'
	screenURL1 = rooturl + 'screenshot_1.jpg'
	screenURL2 = rooturl + 'screenshot_2.jpg'
	screenURL3 = rooturl + 'screenshot_1.jpg'
	screenURL4 = rooturl + 'screenshot_2.jpg'
	youtubeURL = '' # optional
	support_email = 'support@openmobileww.com'
	supportURL = 'support.openmobileww.com' #optional
	privacyURL = '' #optional
	price = 0
	partner = 'Wolf and Sheep'

	username = 'tzs-seller@openmobileww.com'
	password = 'ACL4TIZ3N4OMWW'
	url = 'https://seller.tizenstore.com/'
	#url = 'https://seller.tizenstore.com/product/content/inputformbasic.as'


	#display = Display(visible=0, size=(1024, 768))
	#display.start()
	#driver = webdriver.Firefox()
	driver = webdriver.Chrome()
	driver.maximize_window()
	driver.get(url)
	wait = WebDriverWait(driver,3600)#3600s

	try:
			element = wait.until(EC.presence_of_element_located((By.ID, 'emailIDLogin')))
			element.send_keys(username)
			time.sleep(1)
			element = wait.until(EC.presence_of_element_located((By.ID, 'passwordLogin')))
			element.send_keys(password)
			element.submit()

			wait.until(lambda d: d.title !="")
			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_area > a:nth-child(1) > span:nth-child(1)')))
			element.click()

		####Binary#####

			wait.until(lambda d: d.title !="")
			element = wait.until(EC.presence_of_element_located((By.ID, 'contentName')))
			element.send_keys(p_name)
			print 'uploading binary file...'
			element = wait.until(EC.presence_of_element_located((By.ID, 'binaryUploadBtn')))
			element.click()

			ele = driver.find_elements_by_name('App')
			ele[1].send_keys(fileURL)
			print 'file uploaded!'
		#driver.implicitly_wait(20)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#divBinaryUpload > div.btnArea > a.btnBlue')))
			element.click()

			time.sleep(5)
			wait.until(lambda d: d.title !="")

			element = wait.until(EC.visibility_of_element_located((By.ID, 'appComment____')))
			element.send_keys(comment)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#submit')))
			element.click()

			element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#confirmMsg > p.popBtnArea > a:nth-child(1)')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#save')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#comment > p.popBtnArea > a')))
			element.click()#Pressing OK

		#######Sales######
			print 'filling sales information...'
			element = wait.until(EC.presence_of_element_located((By.ID, 'registerTab1')))
			element.click()

			if float(price)!=0:
				element = wait.until(EC.presence_of_element_located((By.ID, 'priceTypePaid')))
				element.click()
				element = wait.until(EC.presence_of_element_located((By.ID, 'stdUsdPrice')))
				element.send_keys(price)
				element = wait.until(EC.presence_of_element_located((By.ID, 'autoInput')))
				element.click()

			element = wait.until(EC.presence_of_element_located((By.ID, 'sellingEndDate')))
			element.send_keys(sellingEndDate)

			element = wait.until(EC.presence_of_element_located((By.ID, 'ageLimit')))
			element.send_keys(age)

			element = wait.until(EC.presence_of_element_located((By.ID, 'parentCategoryId')))
			element.send_keys(category)

			if category == 'Games':
				element = wait.until(EC.presence_of_element_located((By.ID, 'categoryId')))
				element.send_keys(getSubCategory(subcategory))

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#save')))
				element.click()

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmMsg > p.popBtnArea > a:nth-child(1)')))
				element.click()#Pressing Confirm

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#comment > p.popBtnArea > a')))
				element.click()#Pressing OK

			else:
				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#save')))
				element.click()

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#comment > p.popBtnArea > a')))
				element.click()#Pressing OK

			print 'sales information complete!'
		#######Display######
			print 'uploading icons and screenshoots...'
			element = wait.until(EC.presence_of_element_located((By.ID, 'registerTab2')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#viewItemContentDesc_ENG')))
			element.send_keys(description)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#itemContentTag_ENG')))
			element.send_keys(tags)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > input:nth-child(45)')))
			element.send_keys(iconURL)

			ele = driver.find_elements_by_name('ScreenImage1')
			for e in ele:
				if e.get_attribute("type")=='file':
					e.send_keys(screenURL1)
			ele = driver.find_elements_by_name('ScreenImage2')
			for e in ele:
				if e.get_attribute("type")=='file':
					e.send_keys(screenURL2)
			ele = driver.find_elements_by_name('ScreenImage3')
			for e in ele:
				if e.get_attribute("type")=='file':
					e.send_keys(screenURL3)
			ele = driver.find_elements_by_name('ScreenImage4')
			for e in ele:
				if e.get_attribute("type")=='file':
					e.send_keys(screenURL4)

			print 'icons and screenshots uploaded!'
			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#youTubeURL____')))
			element.send_keys(youtubeURL)

			if partner != '' or partner != None:
				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#trCopyrightHolder > td:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(2)')))
				element.click()
				element = wait.until(EC.presence_of_element_located((By.ID, 'copyrightHolder____')))
				element.clear()
				element.send_keys(partner)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#supportedEMail')))
			element.send_keys(support_email)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#supportedSiteUrl____')))
			element.send_keys(supportURL)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#privacyPolicyUrl____')))
			element.send_keys(privacyURL)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#save')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#comment > p.popBtnArea > a')))
			element.click()#Pressing OK
			print 'new app is registered successfully!'
		#######SUBMIT######
			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#submit')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmMsg > p.popBtnArea > a:nth-child(1)')))
			element.click()#confirm

	except:
			e = sys.exc_info()[1]
			print str(e)
			if 'Element is not clickable at point ' and 'id="ie6_bugBasic"' in  str(e):
				print 'Error: Package ID already exists for app id: ' + p_id
				return 'Error: Package ID already exists for app id: ' + p_id
			else:
				return str(e)		
	#driver.close()
	#display.stop()
	return "New App has submitted successfully with id: " + p_id

############################################ UPDATE ################################################################

def TZupdate():
	p_id = 'rn3czZdnNx'
	p_name = 'Fish Escape'
	
	#dlurl = 'http://go.openmobileappmall.com?op=dlman&pd=123691&sig=266ef7ef3e506b4d71693a824570ecb5'
	rooturl = '/home/yi/openM/tz_upload/'
#'iec_fishescape_en_hd_1_0_3_arm_2_0_5_Z3.tpk'
#'iec_fishescape_en_hd_1_0_4_arm_2_0_4_Z1.tpk'
	option = 0
	aux_option = 0
	filename = 'iec_fishescape_en_hd_1_0_3_arm_2_0_5_Z3.tpk'
	if 'Z3.tpk' in filename:
		option = 3
	else:
		option = 1
	fileURL = rooturl + filename

	username = 'tzs-seller@openmobileww.com'
	password = 'ACL4TIZ3N4OMWW'
	url = 'http://seller.tizenstore.com'

	#display = Display(visible=0, size=(1024, 768))
	#display.start()
	#driver = webdriver.Firefox()
	driver = webdriver.Chrome()
	driver.maximize_window()
	driver.get(url)
	wait = WebDriverWait(driver,3600)#3600s

	try:
##### lOG IN #####
			element = wait.until(EC.presence_of_element_located((By.ID, 'emailIDLogin')))
			element.send_keys(username)
			time.sleep(2)
			element = wait.until(EC.presence_of_element_located((By.ID, 'passwordLogin')))
			element.send_keys(password)
			element.submit()
			
			wait.until(lambda d: d.title !="")
			url = 'http://seller.tizenstore.com/product/summarycontent/list.as'
			driver.get(url)
##### SEARCH APP #####
			print 'Searching app ' + p_name + ' ...'
			wait.until(lambda d: d.title !="")
			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#spanContentName > input:nth-child(1)')))
			element.send_keys(p_name)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#spanContentName > a:nth-child(5)')))
			element.click()
			
			ele = driver.find_elements_by_id('tdApplicationTitle')
			print len(ele)
			if len(ele)>1:		
				print 'more than one app with the name ' + p_name		
				return 'more than one app with the name ' + p_name
			if len(ele)==0:	
				print 'app ' + p_name + " is not found"			
				return 'app ' + p_name + " is not found"
			print 'app found! Ready to update ...'
#### UPDATE APP ####	
				
			element = wait.until(EC.presence_of_element_located((By.ID, 'tdPreValidationStatus')))
			if 'Registering' in element.text:
				element.click()
				
			elif 'Ready' not in driver.find_element_by_id('tdValidationStatus').text:
				element = wait.until(EC.presence_of_element_located((By.ID, 'tdOnSaleStatus')))
				element.click()

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#DW_ContentsWrap > div.detailTopWrap > div > p > a')))
				element.click()
			else:
				print 'App ' + p_name + ' is already in validation process, it could not be updated unless the current validation is canceled'
				return 'App ' + p_name + ' is already in validation process, it could not be updated unless the current validation is canceled'

			print 'Trying to find previous versions'
			ele_text = driver.find_elements_by_id('spanFileName') 
			ele_btn = driver.find_elements_by_css_selector('#trBryfileNm > td.td02 > span.btn > a')
			print 'Older version found, preparing to desactivate ...'
			if ('Z3.tpk' in ele_text[0].text and option == 3) or ('Z3.tpk' not in ele_text[0].text and option == 1):
				print 'we are in the option 1'
				aux_option = 1
				ele_btn[0].click()

				element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmMsg > p:nth-child(2) > a:nth-child(1)')))
				element.click()
				print 'Previous version desactivated successfully'
			
			else:
				try:
					if ('Z3.tpk' in ele_text[1].text and option == 3) or ('Z3.tpk' not in ele_text[1].text and option == 1):
						print 'we are in the option 2'
						aux_option = 2
						ele_btn[1].click()
						
						element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmMsg > p:nth-child(2) > a:nth-child(1)')))
						element.click()
						print 'Previous version desactivated successfully'
					else:
						print 'option 3: this is a new app version'
						aux_option = 3
				except:
					e = sys.exc_info()[1]
					print str(e)
				
			time.sleep(5)
			wait.until(lambda d: d.title !="")

			url = driver.current_url
			driver.get(url)
			
			time.sleep(5)
			wait.until(lambda d: d.title !="")
			
			print 'Updating app ' + p_name + ' ...'	
			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#binaryUploadBtn')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > input:nth-child(31)')))
			element.send_keys(fileURL)

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btnArea > a:nth-child(1)')))
			element.click()
			
			time.sleep(5)
			wait.until(lambda d: d.title !="")

			url = driver.current_url
			driver.get(url)
			
			time.sleep(5)
			wait.until(lambda d: d.title !="")

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#submit > span')))
			element.click()

			element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmMsg > p.popBtnArea > a:nth-child(1)')))
			element.click()#confirm

	except:
			e = sys.exc_info()[1]
			print str(e)
			if 'Element is not clickable at point ' and 'id="ie6_bugBasic"' in  str(e):
				print 'exception is ' + driver.current_url + ' and option is ' + str(aux_option)
				try:
					time.sleep(5)
					wait.until(lambda d: d.title !="")

					url = driver.current_url
					driver.get(url)

					time.sleep(5)
					wait.until(lambda d: d.title !="")
					ele_btn = driver.find_elements_by_css_selector('#trBryfileNm > td.td02 > span.btn > a')

					if (aux_option == 1):
						ele_btn[0].click()
						print 'HERE 1'
					if (aux_option == 2):
						print 'HERE 2'
						ele_btn[1].click()
				except:
					e = sys.exc_info()[1]
					print str(e)
				print 'Error: ' + p_name + ' is already updated to the latest version'
				return 'Error: ' + p_name + ' is already updated to the latest version'
			else:
				return str(e)		
	#driver.close()
	#display.stop()
	print "App " + p_name + " is updated successfully!"
	return "App " + p_name + " is updated successfully!"

if __name__=="__main__":
	#TZupdate()
	main()
