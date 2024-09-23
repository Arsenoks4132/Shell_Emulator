from zipfile import ZipFile
from os import remove
from window_mode import Window


class MyTerminal:
    def __init__(self, file_system: ZipFile):
        self.fs = file_system
        self.cur_d = ''
        self.polling = False
        self.window = None

    def attach(self, window: Window):
        self.window = window
        self.window.write(f'user:~{self.cur_d}$ ')

    def output(self, message, end='\n'):
        if self.window is None:
            print(message)
        else:
            self.window.write(message + end)

    def start_polling(self):
        self.polling = True
        while self.polling:
            message = f'user:~{self.cur_d}$ '
            enter = input(message).strip()
            if len(enter) > 0:
                self.command_dispatcher(enter)
        self.output('stop polling...')

    def command_dispatcher(self, command):
        if self.window is not None:
            self.output(command)

        params = command.split()
        if params[0] == 'exit':
            if self.window is None:
                self.polling = False
            else:
                self.window.stop_polling()
                return
        elif params[0] == 'cd':
            temp_dir = self.cd(params[1:])
            if temp_dir is not None:
                self.cur_d = temp_dir
        elif params[0] == 'ls':
            self.output(self.ls(params[1:]))
        elif params[0] == 'cat':
            self.output(self.cat(params[1:]))
        elif params[0] == 'head':
            self.output(self.head(params[1:]))
        elif params[0] == 'touch':
            self.touch(params[1:])
        else:
            self.output("Команда не найдена")

        if self.window is not None:
            self.output(f'user:~{self.cur_d}$ ', end='')

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
                    self.output('Некорректный путь до директории')
                    return
            else:
                new_directory.append(i)

        new_path = '/'.join(new_directory) + '/'
        if new_path == '/':
            return ''

        for file in self.fs.namelist():
            if file.startswith(new_path):
                return new_path
        self.output('Директория с таким названием отсутствует')

    def ls(self, params):
        work_directory = self.cur_d
        if len(params) > 0:
            work_directory = self.cd((params[-1],))
            if work_directory is None:
                return ''

        files = set()
        for file in self.fs.namelist():
            if file.startswith(work_directory):
                ls_name = file[len(work_directory):]
                if '/' in ls_name:
                    ls_name = ls_name[:ls_name.index('/')]
                files.add(ls_name)
        return '\n'.join(filter(lambda x: len(x) > 0, sorted(files)))

    def cat(self, params):
        file = params[-1]
        try:
            with self.fs.open(self.cur_d + file, 'r') as read_file:
                return read_file.read().decode('UTF-8')
        except:
            return 'Неправильное название файла'

    def head(self, params):
        file = params[-1]

        try:
            with self.fs.open(self.cur_d + file, 'r') as read_file:
                data = read_file.read().decode('UTF-8').split('\n')
        except:
            return 'Неправильное название файла'

        flag = params[0]
        n = 10
        if flag.startswith('-'):
            try:
                n = int(flag[1:])
            except:
                n = 10
                return 'Флаг указан неверно, выведено 10 записей:\n'
        return '\n'.join(data[:n])

    def touch(self, params):
        file = params[-1]

        file_temp = '__temp__' + file
        try:
            f = open(file_temp, 'w')
            f.close()
        except:
            self.output('Не удалось создать файл')
            return

        try:
            self.fs.write(file_temp, self.cur_d + file)
        except:
            self.output('Не удалось создать файл')
            return

        try:
            remove(file_temp)
        except:
            pass
