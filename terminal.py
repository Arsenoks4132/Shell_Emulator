from zipfile import ZipFile
from os import remove


class MyTerminal:
    def __init__(self, file_system: ZipFile):
        self.fs = file_system
        self.cur_d = ''
        self.polling = False

    def start_polling(self):
        self.polling = True
        while self.polling:
            message = f'user:~{self.cur_d}$ '
            enter = input(message).strip()
            if len(enter) > 0:
                self.command_dispatcher(enter)
        print('stop polling...')

    def command_dispatcher(self, command):
        params = command.split()
        if params[0] == 'exit':
            self.polling = False
            return
        elif params[0] == 'cd':
            temp_dir = self.cd(params[1:])
            if temp_dir is not None:
                self.cur_d = temp_dir
        elif params[0] == 'ls':
            self.ls(params[1:])
        elif params[0] == 'cat':
            self.cat(params[1:])
        elif params[0] == 'head':
            self.head(params[1:])
        elif params[0] == 'touch':
            self.touch(params[1:])
        else:
            print("Команда не найдена")

    def cd(self, params):
        if len(params) == 0:
            return ''
        directory = params[-1]

        directory = directory.strip('/')
        directory = directory.split('/')

        new_directory = self.cur_d[:-1].split('/')
        if new_directory == ['']:
            new_directory = []
        for i in directory:
            if i == '..':
                if len(new_directory) > 0:
                    new_directory.pop()
                else:
                    print('Некорректный путь до директории')
                    return
            else:
                new_directory.append(i)

        new_path = '/'.join(new_directory) + '/'
        if new_path == '/':
            return ''

        for file in self.fs.namelist():
            if file.startswith(new_path):
                return new_path
        print('Директория с таким названием отсутствует')

    def ls(self, params):
        work_directory = self.cur_d
        if len(params) > 0:
            work_directory = self.cd((params[-1], ))
            if work_directory is None:
                return

        files = set()
        for file in self.fs.namelist():
            if file.startswith(work_directory):
                ls_name = file[len(work_directory):]
                if '/' in ls_name:
                    ls_name = ls_name[:ls_name.index('/')]
                files.add(ls_name)
        print(*filter(lambda x: len(x) > 0, sorted(files)), sep='\n')

    def cat(self, params):
        file = params[-1]
        try:
            with self.fs.open(self.cur_d + file, 'r') as read_file:
                print(read_file.read().decode('UTF-8'))
        except:
            print('Неправильное название файла')

    def head(self, params):
        file = params[-1]

        try:
            with self.fs.open(self.cur_d + file, 'r') as read_file:
                data = read_file.read().decode('UTF-8').split('\n')
        except:
            print('Неправильное название файла')
            return

        flag = params[0]
        n = 10
        if flag.startswith('-'):
            try:
                n = int(flag[1:])
            except:
                n = 10
                print('Флаг указан неверно, выведено 10 записей:\n')
        print(*data[:n], sep='\n')

    def touch(self, params):
        file = params[-1]

        file_temp = '__temp__' + file
        try:
            f = open(file_temp, 'w')
            f.close()
        except:
            print('Не удалось создать файл')
            return

        try:
            self.fs.write(file_temp, self.cur_d + file)
        except:
            print('Не удалось создать файл')
            return

        try:
            remove(file_temp)
        except:
            pass
