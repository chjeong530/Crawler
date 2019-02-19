#-*- coding: utf-8 -*-
import os
import time
import shutil
import logging
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys


class Crawler:
    def __init__(self):
        self.real_path = None
        self.category = None
        self.page_down_step = 10
        self.page_more_step = 3
        self.time_step = 2
        self.log = None
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.option.add_argument('--window-size=1920x1080')
        self.option.add_argument('--disable-gpu')

    def set_logging(self):
        self.log = logging.getLogger("Crawler")
        self.log.setLevel(logging.INFO)

        stream_hander = logging.StreamHandler()
        file_hander = logging.FileHandler("crawl.log")

        self.log.addHandler(stream_hander)
        self.log.addHandler(file_hander)

        self.log.info("Start Image Crawling !!!")


    def get_categories_list(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
        return lines

    def write_image(self, image_data, category):
        for i, data in enumerate(image_data):
            img_src = data['style']
            split_text = 'url('
            start_index = img_src.find(split_text) + len(split_text)
            end_index = img_src[start_index:].find(')') + start_index
            img_url = "http://"+ str(img_src[start_index:end_index]).replace("\"", "")
            img_url = img_url.replace("////", "//")
            write_file_name = "{0:04d}.jpg".format(i) 
            print("{index} : {url}".format(index=write_file_name, url=img_url))

            img = urlopen(img_url, timeout=60)
            with open(os.path.join(os.path.join(self.real_path, category),write_file_name), 'wb') as f:
                try:
                    ### Don't use. no timeout option
                    # urllib.request.urlretrieve(img_url, os.path.join(os.path.join(self.real_path, category),write_file_name))
                    f.write(img.read())
                except:
                    print("Error")
                else:
                    print("Done")


    def main(self):

        ### Linux
        # driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=self.option)

        ### Windows
        driver = webdriver.Chrome("chromedriver", chrome_options=self.option)
        categories_list = self.get_categories_list('categories_list')
        self.real_path = os.path.join(os.getcwd(), 'data')
        print(self.real_path)

        if os.path.isdir(self.real_path):
            shutil.rmtree(self.real_path)
        os.mkdir(self.real_path)

        for category in categories_list:
            if " " in category:
                seach_key_word = category.replace(" ", "%20")
            else:
                seach_key_word = category
            print(seach_key_word)

            if not os.path.isdir(os.path.join(self.real_path, category)):
                os.mkdir(os.path.join(self.real_path, category))

            url_info = "https://www.flickr.com/search/?text=" + seach_key_word
            print("Start ==============================================")
            print(url_info)
            driver.get(url_info)

            # 화면 스크롤 아래로 내리기 5회
            body = driver.find_element_by_tag_name('body')

            for j in range(self.page_more_step):
                for i in range(self.page_down_step):
                    ### cannot use headless mode
                    # driver.implicitly_wait(2)
                    time.sleep(self.time_step)
                    ### execute js -> cannot use headless mode
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    body.send_keys(Keys.PAGE_DOWN)
                    print(i)

                ### 더 보기 클릭
                try:
                    driver.find_element_by_class_name("alt").click()
                except common.exceptions.NoSuchElementException as e:
                    print("Error : {}".format(e))
                else:
                    print("click [{}]".format(j))

            # driver.implicitly_wait(2)
            time.sleep(self.time_step)
            html = driver.page_source
            # html = urlopen(url_info)
            soup = BeautifulSoup(html, 'html.parser')
            image_data = soup.findAll('div', {'class':"view photo-list-photo-view requiredToShowOnServer awake"}) + \
                                soup.findAll('div', {'class':"view photo-list-photo-view awake"})

            print(len(image_data))
            self.write_image(image_data, category)
            print("End ================================================\n\n")

if __name__=="__main__":
    crawler = Crawler()
    crawler.main()
