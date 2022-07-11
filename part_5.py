from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time
import random
import requests
import os
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

    # ставим лайк по прямой ссылке
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

    # собираем ссылки на посты ползователя
    def get_all_posts_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(3)
        wrong_userpage = '/html/body/div[1]/section/main/div/div/h2'

        if self.xpath_exists(wrong_userpage):
            print('No such user')
            self.close_browser()

        else:
            time.sleep(3)
            posts_count = int(browser.find_element(By.XPATH,
                                                   '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[1]/div/span').text)
            loops_count = int(posts_count / 12)

            posts_urls_user = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
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

    # ставим лайки по ссылке на аккаунт пользователя
    def many_likes(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(3)
        browser.get(userpage)
        time.sleep(3)

        with open(f'{file_name}.txt', 'r') as file_open:
            url_list = file_open.readlines()
            for line in url_list:
                browser.get(line)
                time.sleep(3)
                like_button = '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
                browser.find_element(By.XPATH, like_button).click()
                time.sleep(2)

        browser.close()
        browser.quit()

    # скачиваем контент
    def download_content(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split('/')[-2]
        time.sleep(3)
        browser.get(userpage)
        time.sleep(3)

        # создаем папку с им пользователя
        if os.path.exists(f'{file_name}'):
            print('Папка уже существует')

        else:
            os.mkdir(file_name)

        downloaded_content_links = []
        with open(f'{file_name}.txt', 'r') as file_open:
            url_list = file_open.readlines()
            for line in url_list[0:5]:
                browser.get(line)
                time.sleep(5)
                ing_src = '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div[1]/img'
                post_id = line.split('/')[-2]

                if self.xpath_exists(ing_src):
                    downloaded_content_links.append(line)
                    img_src_url = browser.find_element(By.XPATH, ing_src).get_attribute('src')

                    # сохраняем фото
                    get_img = requests.get(img_src_url)
                    with open(f'{file_name}/{file_name}_{post_id}_img.jpg', 'wb') as img_file:
                        img_file.write(get_img.content)

                else:
                    print('Другой контент')

        with open('content_links.txt', 'a') as content_links_file:
            for line in downloaded_content_links:
                content_links_file.write(line)

        browser.close()
        browser.quit()


my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_content('https://www.instagram.com/sashulia_freelance/')