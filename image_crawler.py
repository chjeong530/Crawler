#-*- coding: utf-8 -*-
import os
import time
import shutil
import logging
from urllib import parse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys

class Crawler:
    def __init__(self):
        self.real_path = None
        self.category = None
        self.image_page = 300
        self.page_more_step = 3
        self.time_step = 2
        self.log = None
        self.type = "pixabay"
        # self.type = "pexels"
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('--headless')
        # self.option.add_argument('--no-sandbox')
        # self.option.add_argument('--disable-dev-shm-usage')
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

    def write_image(self, index, img_url, category, page=1):
        # 403: Forbidden Error
        try:
            req = Request(img_url, headers={'User-Agent':'Mozilla/5.0'})
        except:
            print("Req Error")
            print(img_url)
        else:
            try:
                img = urlopen(req, timeout=60)
            except:
                print("URL Error")
                print(img_url)
            else:
                print(index)

                file_page = "{0:02d}".format(page)
                file_index = "{0:04d}".format(index)
                file_name = "{type}_{page}_{index}.jpg".format(page=file_page, index=file_index, type=self.type)
                print("{index} : {url}".format(index=file_name, url=img_url))
                real_path = "./data/"
                with open(os.path.join(os.path.join(real_path, category), file_name), 'wb') as f:
                    # with open(os.path.join(os.path.join(self.real_path, category),write_file_name), 'wb') as f:
                    try:
                        ### Don't use. no timeout option
                        # urllib.request.urlretrieve(img_url, os.path.join(os.path.join(self.real_path, category),write_file_name))
                        f.write(img.read())
                        # print(write_file_name)
                    except:
                        print("Write Error")
                    else:
                        print("Done")
                        # csvfile write
                        # filename,w,h,url
                        return index + 1

            return index


    def get_image_url(self, image_data, category, page=1):
        index = 1
        if self.type == "google":
            for i, image in enumerate(image_data):
                try:
                    image.click()
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    # image_data = soup.find('img', {'class':'n3VNCb'})
                    image_link = soup.find_all('a', {'class': 'wXeWr islib nfEiy mM5pbd'})
                    if image_link[i].has_key('href'):
                        text = image_link[i]['href']
                        text = text[text.find('imgurl') + len('imgurl='):]
                        text = text[:text.find('&')]
                        img_url = parse.unquote(text)
                        index = self.write_image(index, img_url, category)
                    else:
                        print(image_link[i])
                except Exception as e:
                    print(e)
        elif self.type == "pixabay":
            main_url = "https://pixabay.com/images/download"
            for i, image in enumerate(image_data):
                image = image.find('img')
                if image.has_key('src') and not 'gif' in image['src']:
                    img_url = image['src']
                    img_url = img_url.replace("__340", "_1280")
                    # img_url = main_url + img_url[img_url.rfind('/'):]
                    index = self.write_image(index, img_url, category, page)
                elif image.has_key('data-lazy'):
                    img_url = image['data-lazy']
                    img_url = img_url.replace("__340", "_1280")
                    # img_url = main_url + img_url[img_url.rfind('/'):]
                    index = self.write_image(index, img_url, category, page)
                else:
                    print(image)

        elif self.type == "pexels":
            main_url = "https://www.pexels.com"
            for i, image in enumerate(image_data):
                if image.has_key('href'):
                    img_url = main_url+image['href']
                    index = self.write_image(index, img_url, category)
                else:
                    print(image)

    def main(self):
        ### Linux
        # driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=self.option)

        ### Windows
        self.driver = webdriver.Chrome("chromedriver80", chrome_options=self.option)
        categories_list = self.get_categories_list('categories_list')
        self.real_path = os.path.join(os.getcwd(), 'data')
        print(self.real_path)

        if not os.path.isdir(self.real_path):
            # shutil.rmtree(self.real_path)
            # print("remove")
            os.mkdir(self.real_path)

        categories_list = ["random"]
        for category in categories_list:
            if " " in category:
                search_key_word = category.replace(" ", "%20")
            else:
                search_key_word = category
            print(search_key_word)

            if not os.path.isdir(os.path.join(self.real_path, category)):
                os.mkdir(os.path.join(self.real_path, category))

            # flickr
            # url_info = "https://www.flickr.com/search/?text=" + search_key_word

            if self.type == "google":
                # google
                url_info = "https://www.google.com/search?q=" + search_key_word + "&tbm=isch"

                print("Start ==============================================")
                print(url_info)
                self.driver.get(url_info)
                # 화면 스크롤 아래로 내리기 5회
                body = self.driver.find_element_by_tag_name('body')
                i = 0
                while(1):
                    check_more_btn = self.driver.find_element_by_class_name("mye4qd")
                    check_done_btn = body.find_element_by_class_name("OuJzKb")

                    if check_more_btn.is_displayed() == True:
                        check_more_btn.click()
                    elif check_done_btn.is_displayed() == True:
                        print("total click [{}]".format(i))
                        break
                    else:
                        body.send_keys(Keys.END)
                        i += 1
                        print("press end key [{}]".format(i))

                time.sleep(self.time_step)
                image_data = body.find_elements_by_xpath('//*[@id="islrg"]/div/div/a[1]/div[1]/img')

                print(len(image_data))
                # self.write_image(driver, image_data, category)
                self.get_image_url(image_data, category)
                print("End ================================================\n\n")

            elif self.type == "pixabay":
                for page in range(1, self.image_page+1):
                    # pixabay
                    # url_info = "https://pixabay.com/images/search/" + search_key_word +'/?pagi='+str(page)
                    url_info = "https://pixabay.com/images/search/?pagi="+str(page)

                    print("Start ==============================================")
                    print(url_info)
                    self.driver.get(url_info)
                    body = self.driver.find_element_by_tag_name('body')
                    for i in range(5):
                        body.send_keys(Keys.END)
                    time.sleep(self.time_step)

                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    image_page = soup.find("div", {"class": "flex_grid credits search_results"})
                    image_data = image_page.find_all('div', {'class': 'item'})
                    print(len(image_data))
                    # self.write_image(driver, image_data, category)
                    self.get_image_url(image_data, category, page)
                    print("End ================================================\n\n")

            elif self.type == "pexels":
                # pexels
                url_info = "https://www.pexels.com/ko-kr/search/" + search_key_word

                print("Start ==============================================")
                print(url_info)
                self.driver.get(url_info)
                body = self.driver.find_element_by_tag_name('body')
                for i in range(self.image_page*5):
                    body.send_keys(Keys.END)

                time.sleep(self.time_step)

                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                image_page = soup.find("div", {"class": "photos__column"})
                image_data = image_page.find_all('a', {'download': 'true'})
                print(len(image_data))
                # self.write_image(driver, image_data, category)
                self.get_image_url(image_data, category)
                print("End ================================================\n\n")

if __name__=="__main__":
    crawler = Crawler()
    crawler.main()
