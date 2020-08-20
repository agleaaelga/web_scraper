from selenium import webdriver
import time
import re
import os
import requests

BASE_DIR = 'D:\\Pinterest'
URL_LIST = ['https://www.pinterest.com/1starchitecture/architecture-portfolio/',
            'https://www.pinterest.com/archeyesnews/architecture-plans/',
            'https://www.pinterest.com/archeyesnews/architects-drawings/',
            'https://www.pinterest.com/archeyesnews/architecture-retrospective/',
            'https://www.pinterest.com/archeyesnews/architecture-models/']
IMG_URL_PATTERN = re.compile(r'https://i\.pinimg\.com/originals/.*\.(jpg|png|gif)')
EMAIL = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')


class PinterestDriver:
    def __init__(self, pinterst_link, email, password):
        option = webdriver.ChromeOptions()
        self.url = pinterst_link
        self.driver = webdriver.Chrome(options=option)
        self.driver.get(pinterst_link)
        self.email = email
        self.password = password

    def resize_window(self):
        # self.driver.set_window_size(1920, 1080)
        self.driver.maximize_window()

    def login(self):
        self.driver.find_element_by_xpath('//*[@id="HeaderContent"]/div/div[3]/div[1]/button/div').click()
        time.sleep(3)
        print('Entering credential...')
        self.driver.find_element_by_id('email').send_keys(self.email)
        time.sleep(3)
        self.driver.find_element_by_id('password').send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div/div/div/div['
                                          '3]/form/div[5]/button').click()
        time.sleep(5)
        print('Finish Login.')

    def scroll(self):
        self.driver.execute_script('window.scrollBy(0,2500)')

    def has_reach_btm(self):
        top_h = self.driver.execute_script('return document.documentElement.scrollTop')
        client_h = self.driver.execute_script('return document.documentElement.clientHeight')
        scroll_h = self.driver.execute_script("return document.documentElement.scrollHeight")
        return client_h + top_h == scroll_h

    def get_url_dict(self):
        i = 1
        img_dict = {}
        results = self.driver.find_elements_by_tag_name('img')
        for result in results:
            if result.get_attribute('srcset'):
                img_title = format_filename(result.get_attribute('alt'))
                # in case of empty alt, have board title as image filename
                img_title = self.replace_empty_name(img_title)
                # rename duplicate name
                if img_title in img_dict.keys():
                    img_title = f'{img_title}_{i}'
                    i += 1
                else:
                    i = 1
                img_src = get_original_url(IMG_URL_PATTERN, result.get_attribute('srcset'))
                img_dict[img_title] = img_src
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

    def replace_empty_name(self,name):
        return self.get_title() if not name else name


def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        print('Creating directory')


def shorten_oversize_string(string):
    return string[:200] if len(string) > 200 else string


def rename_duplicate_file(item, dic, i):
    pass


def get_img_url(pattern, str_list):
    match_list = [pattern.search(ele) for ele in str_list]
    return [match.group() for match in match_list if match]


def get_original_url(pattern, string):
    return re.search(pattern, string).group()


def write_file(name, url_dict):
    for k, v in url_dict.items():
        response = requests.get(v)
        k = shorten_oversize_string(k)
        img_filename = f'{k}.jpg'
        with open(img_filename, 'wb') as f:
            f.write(response.content)


def log(main_url, url_dict, board_name):
    filename = f'{board_name}_URL.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'{board_name} \n{main_url}\n\n'
                f'Number of images: {len(url_dict)}\n')
        for k, v in url_dict.items():
            f.write(f'{k}:{v}\n')


def display_dict(dic):
    print(f'Number of urls: {len(dic)}')
    for k, v in dic.items():
        print(f'{k}: {v}')


def format_filename(string):
    return re.sub(r'[\\/:*?"|,(\xa0)]', '', string).replace('  ', '_')


# Deal with possible key errors from the overlapping part of two dictionaries
def update(dict1, dict2):
    val1 = list(dict1.values())
    for k, v in dict2.copy().items():
        if v in val1:
            # new_k = list(dict1.keys())[val1.index(v)]
            # dict2[new_k] = dict2.pop(k)
            dict2.pop(k)
    return dict1.update(dict2)


def main():
    start_time = time.time()
    # print(start_time)
    for url in URL_LIST[:1]:
        img_urls = {}
        pin = PinterestDriver(url, email=EMAIL, password=PASSWORD)

        # Get name and author of Pinterest board
        board_title = pin.get_title()
        author = pin.get_author()
        folder_name = f'{board_title}_{author}'

        # Create image folder
        file_dir = os.path.join(BASE_DIR, folder_name)
        create_dir(file_dir)
        os.chdir(file_dir)

        pin.resize_window()
        pin.login()

        # Scroll page by fixed pixels and save image urls into a list until page reaches bottom
        update(img_urls, pin.get_url_dict())
        display_dict(img_urls)
        # while not pin.has_reach_btm():
        #     pin.scroll()
        #     print('Scrolling down...')
        #     time.sleep(5)
        #     update(img_urls, pin.get_url_dict())
        # print('Reached bottom!')
        #
        #
        #
        # # Close current window
        # pin.close()
        #
        # # Save images to disk (temporary until write a new function to get more info about image)
        # print('Saving images...')
        # write_file(board_title, img_urls)
        #
        # # Log Url information
        # print('Logging information...')
        # log(url, img_urls, board_title)

    print("--- %s seconds ---" % round((time.time() - start_time), 2))


if __name__ == '__main__':
    main()
