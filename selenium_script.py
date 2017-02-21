import time
import thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

def init_driver():
	driver = webdriver.Chrome()
	driver.wait = WebDriverWait(driver, 5)
	return driver

def tempMailStart(driver):
	driver.get("https://temp-mail.org/en/")
	try:
		email_box = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='mail']")))
		return email_box.get_attribute("value")
	except TimeoutException:
		print("Wrong XPATH")


def clubpengu(driver, password, email, name):
	driver.get("https://secured.clubpenguin.com/penguin/create")
	try:
		# Input the email data
		emailf = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@name='email']")))
		emailf.send_keys(email)

		# Input the name data
		namef = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@name='name']")))
		namef.send_keys(name)

		# Input the password data
		passwordf = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@name='pass']")))
		passwordf.send_keys(password)

		# Click on the terms of service box
		terms = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@name='terms']")))
		driver.execute_script("arguments[0].click();", terms)

		# Clicks on one of the captcha buttons (hopefully it works out that it's the correct one)
		rng = driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@name='captcha']")))
		driver.execute_script("arguments[0].click();", rng)
		#driver1.execute_script("arguments[0].click();", rng) # A second attempt at the captcha

		# This is suppesed to make it so all of the text forms get verified by clicking between them
		ActionChains(driver).move_to_element(emailf).click().perform()
		ActionChains(driver).move_to_element(namef).click().perform()
		ActionChains(driver).move_to_element(passwordf).click().perform()


		# Click the submit button after everything has been verified
		driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@name='op']"))).click()
	except TimeoutException:
		print("Something didn't verify or the Captcha failed")

def tempMailVerify(driver):
	try:
		driver.wait = WebDriverWait(driver, 20)
		#driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='click-to-refresh']"))).click()
		driver.get("https://temp-mail.org/en/")
		driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Club')]"))).click()
		driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Activate Penguin*')]"))).click()
	except TimeoutException:
		print("Misclicked email")



if __name__ == "__main__":
	name = raw_input("What name will you use?")
	pengu_driver = init_driver()
	mail_driver = init_driver()
	email = tempMailStart(mail_driver)
	clubpengu(pengu_driver, "qawsed", email, name)
	time.sleep(10)
	tempMailVerify(mail_driver)
	

	#time.sleep(5)
	pengu_driver.quit()
