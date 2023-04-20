import argparse
import requests
import time

from art import tprint
from bs4 import BeautifulSoup
from tqdm import tqdm

def text_red(text):
    return('\033[31m {}' .format(text) + text_wite(''))

def text_yellow(text):
    return('\033[33m {}' .format(text) + text_wite(''))

def text_blue(text):
    return('\033[34m {}' .format(text) + text_wite(''))

def text_wite(text):
    return('\033[37m {}' .format(text))

def search_track(search_name):
    url_base = 'https://ru.hitmotop.com/search?q='

    url = url_base + search_name

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    list_search = []

    items_music_list = soup.findAll('li', {'tracks__item track mustoggler'})
    for item in items_music_list:
        dic_info_musik = {}
        dic_info_musik['title'] = item.find('div', {'track__desc'}).text
        dic_info_musik['name_track'] = item.find('div', {'track__title'}).text.strip()
        dic_info_musik['href'] = item.find('a', {'track__download-btn'}).get('href')

        list_search.append(dic_info_musik)

    return list_search

def download_music(url, dir_download):
    print(text_yellow(f'[*] Получаю ссылки для скачивания'))

    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')

    music_list = soup.find('ul', {'class': 'tracks__list'})
    items = music_list.find_all('a', {'class': 'track__download-btn'})

    list_ref_music = []
    for item in tqdm(items):
        if item is None or item == '':
            continue
        href = item.get('href')
        list_ref_music.append(href)

        time.sleep(0.01)

    print(text_yellow(f'[*] Список ссылок'))
    for href in list_ref_music:
        print(f'{href}')

    user_select = input(text_yellow(text_blue(f'>> Всего треков для скачивания {len(list_ref_music)}. Скачать всё в {dir_download} (y/n)?')))
    if user_select == 'y':
        print(text_yellow(f'[!] Начинаю загрузку'))
        for href in tqdm(list_ref_music, desc='Total'):
            try:
                split_href = href.split('/')

                r = requests.get(href, stream=True)
                chunk_size = 1024

                name_file = dir_download + split_href[len(split_href) - 1]
                with open(name_file, 'wb') as f:
                    for data in tqdm(r.iter_content(chunk_size=chunk_size), desc=name_file, ncols=0):
                        f.write(data)

                    tqdm.write(text_blue(f'[+] Загрузка файла {name_file} завершена'))
            except Exception as e:
                tqdm.write(text_red(f'[-] Что-то пошло не так {e}'))

        print(text_yellow(f'[!] Загрузка завершена'))
    else:
        print(text_red('[!] Загрузка отменена пользователем'))

if __name__ == '__main__':
    tprint('hitmotop')

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('dir')

    args = parser.parse_args()

    url = args.url
    dir_download = args.dir + '/'

    download_music(url, dir_download)