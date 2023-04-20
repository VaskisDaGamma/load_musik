import argparse
import tabulate
import requests

from art import tprint
from alive_progress import alive_bar
from musify_club import  search_track as search_musify_club
from ru_hitmotop_com import search_track as search_hitmotop
from ruy_zvukofon_com import search_track as search_zvukofon

def text_red(text):
    return('\033[31m {}' .format(text) + text_wite(''))

def text_yellow(text):
    return('\033[33m {}' .format(text) + text_wite(''))

def text_blue(text):
    return('\033[34m {}' .format(text) + text_wite(''))

def text_wite(text):
    return('\033[37m {}' .format(text))

def load_list_music(list_ref_music, dir_download):
    print(text_yellow(f'\n[!] Начинаю загрузку\n'))

    list_error = []

    with alive_bar(len(list_ref_music), dual_line=True) as bar:
        for dic_ref_music in list_ref_music:
            if dic_ref_music['href'] != '':
                bar.text = f'--> загрузка: {dic_ref_music["title"]} - {dic_ref_music["name_track"]}'
            else:
                print(text_red(f'\n[-] Не обнаружена ссылка для трека {dic_ref_music["name_track"]}'))
                list_error.append(dic_ref_music["href"])
                bar()
                continue

            try:
                r = requests.get(dic_ref_music['href'], timeout=30)

                split_href = dic_ref_music['href'].split('/')

                name_file = dir_download + '/' + split_href[len(split_href) - 1]
                with open(name_file, 'wb') as f:
                    f.write(r.content)
                    bar()
            except requests.Timeout as e:
                print(text_red(f'[-] Таймаут превышен. Не удалось загрузить ссылке {dic_ref_music["href"]}'))
                list_error.append(dic_ref_music["href"])
                bar()

    if len(list_error) > 0:
        print(text_red(f'[-] Не все файлы удалось загрузить, смотри файл load_error.txt'))

        with open(dir_download + '/load_error.txt', 'w') as f:
            f.write(str(list_error))

    print(text_yellow(f'\n[!] Загрузка завершена'))

def load_musk(name_file_search, dir_download, read_file=True):
    list_download = []

    if read_file:
        read_file = open(name_file_search, 'r')
        lines_file = read_file.readlines()
        read_file.close()
    else:
        lines_file = name_file_search

    with alive_bar(len(lines_file)) as bar:
        for line in lines_file:
            # https://ru.hitmotop.com
            print(text_yellow(f'[!] Поиск {line.strip()} на {"https://ru.hitmotop.com"}'))
            list_search_site = search_hitmotop(line)

            if len(list_search_site) == 0:
                # https://ruy.zvukofon.com
                print(text_yellow(f'[!] Поиск {line.strip()} на {"https://ruy.zvukofon.com"}'))

                list_search_site = search_zvukofon(line)

            if len(list_search_site) == 0:
                # https://musify.club
                print(text_yellow(f'[!] Поиск {line.strip()} на {"https://musify.club"}'))
                list_search_site = search_musify_club(line)

            # создаю список для вывода пользователю
            list_user_select = []
            if len(list_search_site) > 1:
                for i, item_music in enumerate(list_search_site):
                    list_user = [str(i), item_music['title'], item_music['name_track']]

                    list_user_select.append(list_user)
                    # ограничим список найденных до 5
                    if i == 4:
                        break

                print(tabulate.tabulate(list_user_select, tablefmt='grid'))

                with bar.pause():
                    print(text_blue('Набери 99, чтобы пропустить'))
                    select_user = input(text_blue(f'[>>] Найдено более одного трека по запросу "{line.strip()}", введи номер '))

                if select_user != '99':
                    while True:
                        try:
                            list_download.append(list_search_site[int(select_user)])

                            break
                        except Exception as e:
                            print(tabulate.tabulate(list_user_select, tablefmt='grid'))

                    print(text_yellow(f'\n[+] Файл {list_search_site[int(select_user)]} добавлен на скачивание\n'))

                bar()
            elif len(list_search_site) == 1:
                print(text_yellow(f'\n[+] Файл {list_search_site[0]} добавлен на скачивание\n'))
                list_download.append(list_search_site[0])
                bar()
            else:
                print(text_red(f'\n[-] По запросу "{line.strip()}" ничего не найдено\n'))
                bar()

    load_list_music(list_download, dir_download)

if __name__ == '__main__':
    tprint('XUY ZABEY')

    parser = argparse.ArgumentParser()
    parser.add_argument('name_file_search')
    parser.add_argument('dir_download')

    args = parser.parse_args()

    name_file_search = args.name_file_search
    dir_download = args.dir_download

    load_musk(name_file_search, dir_download)