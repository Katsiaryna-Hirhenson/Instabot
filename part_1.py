from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time


def login(usermane, password):
    browser = webdriver.Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/instabot/chromedriver')

    try:
        browser.get('https://www.instagram.com/')
        time.sleep(10)

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(usermane)

        time.sleep(5)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(10)
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


login(username, password)