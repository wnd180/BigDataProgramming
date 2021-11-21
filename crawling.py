from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('/Users/kwonseongjung/Downloads/chromedriver')
driver.implicitly_wait(3)
driver.get('https://www.code.go.kr/stdcode/regCodeL.do')

# 로그인 버튼을 눌러주자.
driver.find_element_by_xpath('//*[@id="contents"]/form/table/tbody/tr[2]/td/div/div/a[2]').click()

sleep(3) #3초간 기다림

driver.close()