from zipfile import ZipFile
from sys import argv
from os.path import exists
from window_mode import Window
from terminal import MyTerminal


def main():
    if len(argv) > 1:
        config_file = argv[1]
    else:
        print("Отсутствует необходимый аргумент: путь к конфигурационному файлу")
        return

    if exists(config_file):
        with open(config_file) as config:
            fs_path = config.readline().strip()
    else:
        print("Конфигурационный файл с таким названием отсутствует")
        return

    if exists(fs_path):
        with ZipFile(fs_path, 'a') as file_system:
            terminal = MyTerminal(file_system)
            if len(argv) > 2 and argv[2] == '-cli':
                terminal.start_polling()
            else:
                window = Window(terminal)
                window.start_polling()

    else:
        print("Модель файловой системы с таким названием отсутствует")
        return


if __name__ == '__main__':
    main()
