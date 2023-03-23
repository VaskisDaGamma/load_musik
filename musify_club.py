import argparse
import tabulate
import time
import requests

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
    url_base = 'https://musify.club'

    url = url_base + '/search?searchText=' + search_name

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    list_search = []

    items_music_list = soup.findAll('div', {'playlist__item'})
    for item in items_music_list:
        dic_info_musik = {}
        dic_info_musik['title'] = item.find('a').text
        dic_info_musik['name_track'] = item.find('a', {'strong'}).text.strip()
        dic_info_musik['href'] = url_base + item.find('a', {'no-ajaxy yaBrowser'}).get('href')

        list_search.append(dic_info_musik)

    return list_search

def load_list_music(list_ref_music, dir_download):
    print(text_yellow(f'[!] Начинаю загрузку'))

    list_error = []
    for dic_ref_music in tqdm(list_ref_music):
        if dic_ref_music['name'] is None:
            tqdm.write(text_red(f'[-] Трек {dic_ref_music["href"]} не доступен для скачивания'))

            list_error.append(dic_ref_music['href'] + '\n')
        else:
            try:
                r = requests.get(dic_ref_music['href'])

                name_file = dir_download + dic_ref_music['name']
                with open(name_file, 'wb') as f:
                    f.write(r.content)
                    tqdm.write(text_blue(f'[+] Загрузка файла {name_file} завершена'))
            except Exception as e:
                tqdm.write(text_red(f'[-] Что-то пошло не так {e}'))

    if len(list_error) > 0:
        print(text_red(f'[-] Не все файлы удалось загрузить, смотри файл load_error.txt'))

        with open(dir_download + '/load_error.txt', 'w') as f:
            f.writelines(list_error)

    print(text_yellow(f'[!] Загрузка завершена'))

def download_music(url, dir_download):
    print(text_yellow(f'[*] Получаю ссылки для скачивания'))

    url_base = 'https://musify.club'
    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')

    music_list = soup.find('div', {'class': 'playlist playlist--hover'})
    items = music_list.find_all('a', {'class': 'no-ajaxy yaBrowser'})

    list_ref_music = []
    for item in tqdm(items):
        href = url_base + item.get('href')
        name_track = item.get('download')

        if name_track != None:
            name_track = name_track.replace('/', '_')

        time.sleep(0.01)

        dic_ref_music = {'href': href, 'name': name_track}

        list_ref_music.append(dic_ref_music)

    print(text_yellow(f'[*] Список ссылок'))
    print(tabulate.tabulate(list_ref_music, headers='keys', tablefmt='pipe'))

    user_select = input(text_blue(f'>> Всего треков для скачивания {len(list_ref_music)}. Скачать всё в {dir_download} (y/n)?'))
    if user_select == 'y':
        load_list_music(list_ref_music, dir_download)
    else:
        print(text_red('[!] Загрузка отменена пользователем'))

if __name__ == '__main__':
    tprint('musify')

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('dir')

    args = parser.parse_args()

    url = args.url
    dir_download = args.dir + '/'

    download_music(url, dir_download)
