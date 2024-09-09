import sys
from zipfile import ZipFile
from sys import argv
from os.path import exists


class MyTerminal:
    def __init__(self, file_system):
        self.fs = file_system
        self.cur_d = ''
        self.polling = False

    def start_polling(self):
        self.polling = True
        while self.polling:
            enter = input(f'user:~{self.cur_d}$ ').strip()
            if len(enter) > 0:
                self.command_dispatcher(enter)
        print('stop polling...')

    def command_dispatcher(self, command):
        params = command.split()
        if params[0] == 'exit':
            self.polling = False


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
            terminal.start_polling()
    else:
        print("Модель файловой системы с таким названием отсутствует")
        return


def test_func():
    with open('way.xml', 'rt') as f:
        path = f.readline().strip()

    with ZipFile(path, 'a') as my_zip:
        print(my_zip.namelist())

        with my_zip.open('desktop/shop list.txt', 'r') as f:
            s = f.read()
            s = s.decode('UTF-8')

    print(s)


if __name__ == '__main__':
    main()
