from pinterest import pinterest_scraper, img_caption
import os,re

BASE_DIR = 'D:\\Pinterest'
URL_LIST = ['https://www.pinterest.com/1starchitecture/architecture-portfolio/',
            'https://www.pinterest.com/archeyesnews/architecture-plans/',
            'https://www.pinterest.com/archeyesnews/architects-drawings/',
            'https://www.pinterest.com/archeyesnews/architecture-retrospective/',
            'https://www.pinterest.com/archeyesnews/architecture-models/']
IMG_URL_PATTERN = re.compile(r'https://i\.pinimg\.com/originals/.*\.(jpg|png|gif)')
EMAIL = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')


