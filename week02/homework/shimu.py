from selenium import webdriver
import time

try:
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome 2.app/Contents/MacOS/Google Chrome"
    chrome_driver_binary = '/usr/local/bin/chromedriver'
    browser = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    browser.get('https://shimo.im/welcome')
    time.sleep(1)

    btm1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]')
    btm1.click()
    
    time.sleep(1)

    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys('xxxxxxxx')
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys('12345678')

    time.sleep(1)

    btm1 = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
    btm1.click()
except Exception as e:
    print(e)
# finally:    
    # browser.close()   