from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException


class InstagramBot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(executable_path='/Users/ekaterinagirgenson/Proga/PycharmProjects/instabot/chromedriver')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com/')
        time.sleep(5)

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

    def like_photos_by_hashtag(self, hashtag):

        browser = self.browser
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
                like_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
                browser.find_element(By.XPATH, like_button).click()
                time.sleep(random.randrange(3, 10))

            except Exception as ex:
                print(ex)
                self.close_browser()

    # проверяем существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    #ставим лайк по прямой ссылке
    def put_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(2)

        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'

        if self.xpath_exists(wrong_userpage):
            print('No such post')
            self.close_browser()

        else:
            time.sleep(3)

            like_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
            browser.find_element(By.XPATH, like_button).click()


    #ставим лайки по ссылке на аккаунт пользователя
    def many_likes(self, userpage):

            browser = self.browser
            browser.get(userpage)
            time.sleep(3)
            wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'

            if self.xpath_exists(wrong_userpage):
                print('No such user')
                self.close_browser()

            else:
                time.sleep(3)
                posts_count = int(browser.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text)
                loops_count = int(posts_count / 12)

                posts_urls_user = []
                for i in range(0, loops_count):
                    hrefs = browser.find_elements(By.TAG_NAME,'a')
                    posts_urls = [element.get_attribute('href') for element in hrefs if
                                  '/p/' in element.get_attribute('href')]

                    for href in posts_urls:
                        posts_urls_user.append(href)

                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(3)

                file_name = userpage.split('/')[-2]

                set_posts_urls = set(posts_urls_user)

                with open(f'{file_name}.txt', 'a') as file:
                    for posts_url in set_posts_urls:
                        file.write(posts_url + '\n')

                with open(f'{file_name}.txt', 'r') as file_open:
                    url_list = file_open.readlines()
                    for line in url_list:
                        browser.get(line)
                        time.sleep(3)
                        like_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
                        browser.find_element(By.XPATH,like_button).click()
                        time.sleep(2)

            browser.close()
            browser.quit()

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.many_likes('https://www.instagram.com/girgenson.k/')

