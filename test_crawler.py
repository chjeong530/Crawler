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

search_key_word = "person"
url_info = "https://www.google.com/search?q=" + search_key_word + "&tbm=isch"

driver = webdriver.Chrome("chromedriver80")
driver.get(url_info)
body = driver.find_element_by_tag_name("body")

body.send_keys(Keys.END)
driver.excute_script()

check_more_btn = body.find_element_by_class_name("mye4qd")
check_more_btn.is_displayed()
if check_more_btn == True:
    check_more_btn.click()
check = body.find_element_by_class_name("OuJzKb")
check.is_displayed()

# image_data = soup.find('img', {'class':'rg_i'})
# image_url = image_data['src']


# 이미지 클릭 리스트
images = body.find_elements_by_xpath('//*[@id="islrg"]/div/div/a[1]/div[1]/img')
tot_image = len(images)
print(tot_image)

images[24].click()
for image in images:
    image.click()
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
image_data = soup.find_all('a', {'class': 'wXeWr islib nfEiy mM5pbd'})
# image_data = soup.find('img', {'class':'n3VNCb'})

images = body.find_elements_by_xpath('//*[@id="islrg"]/div/div/a/div')
#Sva7


images = body.find_elements_by_xpath('//*[@id="islrg"]/div/div')
images = body.find_elements_by_xpath('//*[@id="rg_s"]/div/a[1]')

image_data = soup.find_all('a', {'class': 'rg_l'})



try:
    # img = urlopen("https://miro.medium.com/max/1050/1*lTEHN86OS67Nf-3-jUM73w.jpeg")
    img = urlopen("https://i2-prod.mirror.co.uk/incoming/article20663198.ece/ALTERNATES/s1200b/2_Screen-Shot-2019-10-20-at-215756JPG.jpg")
except:
    print("error")
else:
    print("ok")







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

search_key_word = "person"
url_info = "https://pixabay.com/images/search/ " + search_key_word
# url_info = "https://www.google.com/search?q=" + search_key_word + "&tbm=isch"

driver = webdriver.Chrome("chromedriver80")
driver.get(url_info)
body = driver.find_element_by_tag_name("body")

body.send_keys(Keys.END)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
image_page = soup.find("div", {"class":"flex_grid credits search_results"})
image_data = image_page.find_all('div', {'class': 'item'})






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

search_key_word = "person"
url_info = "https://www.pexels.com/ko-kr/search/" + search_key_word
# url_info = "https://www.google.com/search?q=" + search_key_word + "&tbm=isch"

driver = webdriver.Chrome("chromedriver80")
driver.get(url_info)
body = driver.find_element_by_tag_name("body")

body.send_keys(Keys.END)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
