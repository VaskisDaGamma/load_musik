import ruy_zvukofon_com
import yandex_music

if __name__ == '__main__':
    text = '''
    1. yandex
    2. ruy_zvukofon_com
    3. ru_hitmotop_com
    4. musify_club
    5. load_for_list'''

    print(text)

    user_input = input('Введи номер для продолжения: ')

    if user_input == '1':
        yandex_music.main()
    elif user_input == '2':
        input_url = input('Введи url со списком песен: ')
        input_dir = input('Введи каталог для сохранения: ')

        ruy_zvukofon_com.download_music(input_url, input_dir)
    elif user_input == '3':
        pass
    elif user_input == '4':
        pass
    elif user_input == '5':
        pass
