from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time
import random


def hashtag_search(usermane, password, hashtag):
    browser = webdriver.Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/instabot/chromedriver')

    try:
        browser.get('https://www.instagram.com/')
        time.sleep(5)

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(usermane)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, 4):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)

            hrefs = browser.find_elements(By.TAG_NAME, 'a')

            posts_urls = [element.get_attribute('href') for element in hrefs if '/p/' in element.get_attribute('href')]

            for url in posts_urls:
                try:
                    browser.get(url)
                    like_button = browser.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                    time.sleep(random.randrange(3 , 10))
                except Exception as ex:
                    print(ex)
                    browser.close()
                    browser.quit()
        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


hashtag_search(username, password, 'nature')