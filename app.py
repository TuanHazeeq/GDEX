from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get('http://127.0.0.1:8000/')
try:
    wait = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/button')))

    usernameField = driver.find_element(by=By.XPATH, value='//*[@id="id_username"]')
    usernameField.send_keys('tuanhazeeq')

    passwordField = driver.find_element(by=By.XPATH, value='//*[@id="id_password"]')
    passwordField.send_keys('test1234')

    button = driver.find_element(by=By.XPATH, value='/html/body/div[2]/form/button')
    button.click()

    wait = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/button')))

    addListField = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/input')
    addListField.send_keys('Shopping List')

#addListButton = driver.find_element_by_xpath('/html/body/div[2]/div/div/button')
#button.click()

#deletetest2 = driver.find_element_by_xpath('/html/body/div[2]/ul/li[2]/button')
#deletetest2.click()
finally:
    driver.quit()