import json
import os.path
import time
import requests
from alive_progress import alive_bar
from art import tprint

import seach_and_load

def get_ref_track_download(id_albom, id_track):
    date_milliseconds = int(time.time()*1000)

    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    #headers = {'User-Agent': user_agent}

    url = f'https://music.yandex.ru/api/v2.1/handlers/track/{id_track}:{id_albom}/web-auto_playlists-playlist_of_the_day-track-main/download/m?hq=0&external-domain=music.yandex.ru&overembed=no&__t={date_milliseconds}'
    #re = requests.get(url, headers=headers)
    re = requests.get(url)

    print(re.text)

def load_music(url_base, dir_download):

    url_base = 'https://music.yandex.ru/handlers/playlist.jsx?owner=yamusic-daily&kinds=101674234&light=true&madeFor=&withLikesCount=true&forceLogin=true&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.6447825241930731'

    if url_base == '':
        print('Не указан url_base, работа программы завершена')
        return

    '''
    if dir_download == '':
        print('Не указан dir_download, работа программы завершена')
        return

    if not os.path.exists(dir_download):
        print(f'Нет такого каталога {dir_download}')
        return
    '''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}

    re = requests.get(url_base, headers=headers)

    data_json = json.loads(re.text)
    for track in data_json['playlist']['tracks']:
        id_albums = track['albums'][0]['id']
        id_track = track['id']

        get_ref_track_download(id_albums, id_track)

        break # для отладки

def get_list_music(url_base_user, dir_download):
    """
    :param url_base_user: это ссылка, которая возвращает именно json, смотреть в инспекторе браузера
    :param dir_download: папка для сохранения
    :return:
    """

    # url_base_user - это ссылка именно на то, что возвращает список треков в формате json, см. пример
    if url_base_user == '':
        url_base = 'https://music.yandex.ru/handlers/playlist.jsx?owner=yamusic-daily&kinds=101674234&light=true&madeFor=&withLikesCount=true&forceLogin=true&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.988498582421822'
    else:
        url_base = url_base_user

    if not os.path.exists(dir_download):
        print(f'Нет такого каталога {dir_download}')
        return

    re = requests.get(url_base)

    data_json = json.loads(re.text)
    list_track = []

    input_user = input('Это сборник (0) или альбом(1)? ')
    if input_user == '0':
        tracks = data_json['playlist']['tracks']
        with alive_bar(len(tracks), title='Формирую список треков') as bar:
            for track in tracks:
                artist = ''
                for name_artist in track['artists']:
                    artist += name_artist['name'] + ' '

                name_track = track['title']
                list_track.append(artist + '- ' + name_track)
                bar()
    else:
        artists = data_json['artists']
        artist = artists[0]['name']

        tracks = data_json['volumes']
        for track in tracks[0]:
            name_track = track['title']
            list_track.append(artist + '- ' + name_track)

    seach_and_load.load_musk(list_track, dir_download, False)

def main():
    tprint('yandex grub')
    user_mode = input('0 - качаем с yandex (пока не работает), 1 - на yandex получаем только список (качаем на сторонних сайтах): ')
    user_input_addr = input('Введи адрес плейлиста: ')
    user_dir = input('Введи папку, куда будем сохранять: ')

    if user_mode == '1':
        get_list_music(user_input_addr, user_dir)
    elif user_mode == '0':
        print('Данный режим в разработке, пока не доступен')
        #load_music(user_input_addr, user_dir)
    else:
        print('Не правильно указан режим, укажи 0 или 1')

if __name__ == '__main__':
    main()