import requests
from bs4 import BeautifulSoup
import os
import json

BASE_URL = 'https://www.archdaily.com/'
BASE_FOLDER_ROOT = 'D:\Archdaily'


def project_url(soup):
    link_list = []
    for article in soup.find_all('div', class_='afd-post-stream clearfix'):
        article_title = article.h3.span.text
        # accept only project article
        if '/' in article_title:
            link = article.find('a', class_='afd-title--black-link')['href']
            link_list.append(f'https://archdaily.com/{link}')
    return link_list


def project_info(soup):
    # remove unwanted svg tags
    for graphic in soup.find_all('svg'):
        graphic.decompose()

    # parse the building info into a dictionary
    info_dict = {}
    # get project name
    name = soup.find('h1',
                     class_='afd-title-big afd-title-big--full afd-title-big--bmargin-big afd-relativeposition')
    info_dict['Name'] = name.get_text().split('/')[0]

    # get category
    info_dict['Category'] = soup.find('div', class_='afd-specs__header-category').get_text(strip=True)
    # get project_loc
    info_dict['Location'] = soup.find('div', class_='afd-specs__header-location').get_text(strip=True)

    # get architect_url
    architect_url_link = soup.find('div', class_='afd-specs__architects').contents[2].a['href']
    architect_url_full_link = f'{BASE_URL}/{architect_url_link}'
    r = requests.get(architect_url_full_link).text
    studio_soup = BeautifulSoup(r, 'lxml')
    studio_url = studio_soup.find('a', class_='afd-share__button')['href']
    info_dict['Url'] = studio_url

    # get rest of the info
    infos = soup.find_all('li', class_='afd-specs__item')
    for info in infos:
        content = info.get_text(strip=True)
        content_list = content.split(':')
        info_dict[content_list[0]] = content_list[1]

    return info_dict


def write_to_text(detail, title):
    filename1 = f'{title}_info.txt'
    filename2 = f'{title}_info_list.txt'
    with open(filename1, 'w', encoding='utf-8') as f:
        for k, v in detail.items():
            f.writelines(f'{k}: {v}')
            f.write('\n')
    with open(filename2, 'w', encoding='utf-8') as f:
        json.dump(detail, f)


def project_text(soup, name):
    # remove extra tags
    for extra_text in soup.find_all('em'):
        extra_text.decompose()

    contents = soup.find_all('p')
    contents_with_whitespace = [content.get_text(strip=True) for content in contents]
    contents_without_whitespace = list(filter(None, contents_with_whitespace))

    filename = f'{name}_content.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for content in contents_without_whitespace[6:-1]:
            f.write('\t')
            f.writelines(content)
            f.write('\n')


def project_pics(soup, name):
    img_url_list = [img.img['data-src'].replace('thumb', 'large') for img in
                    soup.find_all('a', class_='gallery-thumbs-link')]

    for i, url in enumerate(img_url_list):
        response = requests.get(url)
        imagename = f'{name}_{i}.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)


def main():
    request = requests.get(BASE_URL).text
    soup = BeautifulSoup(request, 'lxml')

    for url in project_url(soup)[:3]:
        # read the entire project page
        r = requests.get(url).text
        project_source = BeautifulSoup(r, 'lxml')

        # extract project info
        project_detail = project_info(project_source)
        title = project_detail['Name']

        # create new directory
        path = os.path.join(BASE_FOLDER_ROOT, title)
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)

        # write project info
        write_to_text(project_detail, title)
        # extract project description
        project_text(project_source, title)
        # extract project photos
        project_pics(project_source, title)


if __name__ == '__main__':
    main()
