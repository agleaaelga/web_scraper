#!/usr/bin/env python3

from selenium import webdriver
import time
import re
import os
import requests
from pinterest import caption

IMG_URL_PATTERN = re.compile(r'https://i\.pinimg\.com/originals/.*\.(jpg|png|gif)')


class PinterestDriver:
    def __init__(self, pinterst_link, email, password):
        option = webdriver.ChromeOptions()
        self.url = pinterst_link
        self.driver = webdriver.Chrome(options=option)
        self.driver.get(pinterst_link)
        self.email = email
        self.password = password

    def resize_window(self):
        self.driver.maximize_window()

    def login(self):
        self.driver.find_element_by_xpath('//*[@id="HeaderContent"]/div/div[3]/div[1]/button/div').click()
        time.sleep(3)
        print('Entering email...')
        self.driver.find_element_by_id('email').send_keys(self.email)
        time.sleep(3)
        print('Entering password...')
        self.driver.find_element_by_id('password').send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div/div/div/div['
                                          '3]/form/div[5]/button').click()
        time.sleep(5)
        print('Finish Login.')

    def scroll(self):
        self.driver.execute_script('window.scrollBy(0,2500)')  # scroll page by 2500 pixels each time

    def has_reach_btm(self):
        top_h = self.driver.execute_script('return document.documentElement.scrollTop')
        client_h = self.driver.execute_script('return document.documentElement.clientHeight')
        scroll_h = self.driver.execute_script("return document.documentElement.scrollHeight")
        return client_h + top_h == scroll_h

    def get_url_dict(self):
        img_dict = {}
        results = self.driver.find_elements_by_tag_name('img')
        for result in results:
            if result.get_attribute('srcset'):
                img_description = result.get_attribute('alt')
                img_src = get_original_url(IMG_URL_PATTERN, result.get_attribute('srcset'))
                img_dict[img_src] = img_description
        return img_dict

    def get_title(self):
        return self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]'
                                                 '/main/header/div/div[1]/h1').text

    def get_author(self):
        board_author = self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[1]'
                                                         '/main/header/div/div[1]/h2/a').text
        return re.search(r'[0-9a-zA-Z]*', board_author).group()

    def close(self):
        self.driver.close()


def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        print('Creating directory...')


def get_img_url(pattern, str_list):
    match_list = [pattern.search(ele) for ele in str_list]
    return [match.group() for match in match_list if match]


def get_original_url(pattern, string):
    return re.search(pattern, string).group()


def write_file(name, url_dict):
    for i, (k, v) in enumerate(url_dict.items()):
        response = requests.get(k)
        img_filename = f'{name}_{i}.jpg'
        with open(img_filename, 'wb') as f:
            f.write(response.content)
        caption.caption_jpg(img_filename, v)
        print_num_images_saved(i)


def log(main_url, url_dict, board_name):
    filename = f'{board_name}_URL.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'{board_name} \n{main_url}\n\n'
                f'Number of images: {len(url_dict)}\n')
        for k, v in url_dict.items():
            f.write(f'{k}:\t {v}\n')


def display_dict(dic):
    print(f'Number of urls: {len(dic)}')
    for k, v in dic.items():
        print(f'{k}: {v}')


def print_num_images_saved(index:int):
    if index % 25 == 0:
        print(f'Saved {index} images!')

