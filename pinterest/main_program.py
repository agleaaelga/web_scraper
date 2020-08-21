from pinterest import pinterest_scraper, img_caption
import os, re, time

BASE_DIR = 'D:\\Pinterest'
URL_LIST = ['https://www.pinterest.com/1starchitecture/bedrooms/',
            'https://www.pinterest.com/1starchitecture/architecture-portfolio/',
            'https://www.pinterest.com/archeyesnews/architecture-plans/',
            'https://www.pinterest.com/archeyesnews/architects-drawings/',
            'https://www.pinterest.com/archeyesnews/architecture-retrospective/',
            'https://www.pinterest.com/archeyesnews/architecture-models/']
IMG_URL_PATTERN = re.compile(r'https://i\.pinimg\.com/originals/.*\.(jpg|png|gif)')
EMAIL = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')


def main():
    start_time = time.time()
    for url in URL_LIST[:1]:
        img_urls = {}
        pin = pinterest_scraper.PinterestDriver(url, email=EMAIL, password=PASSWORD)

        # Get name and author of Pinterest board
        board_title = pin.get_title()
        author = pin.get_author()
        folder_name = f'{board_title}_{author}'

        # Create image folder
        file_dir = os.path.join(BASE_DIR, folder_name)
        pinterest_scraper.create_dir(file_dir)
        os.chdir(file_dir)

        pin.resize_window()
        pin.login()

        # Scroll page by fixed pixels and save image urls into a list until page reaches bottom
        img_urls.update(pin.get_url_dict())
        while not pin.has_reach_btm():
            pin.scroll()
            print('Scrolling down...')
            time.sleep(5)
            img_urls.update(pin.get_url_dict())
        print('Reached bottom!')

        # Close current window
        pin.close()
        print("Time: --- %s seconds ---" % round((time.time() - start_time), 2))

        # Log Url information
        print('Logging information...')
        pinterest_scraper.log(url, img_urls, board_title)

        # Save images to disk (temporary until write a new function to get more info about image)
        print('Saving images...')
        pinterest_scraper.write_file(board_title, img_urls)

    print("total time: --- %s seconds ---" % round((time.time() - start_time), 2))


if __name__ == '__main__':
    main()
