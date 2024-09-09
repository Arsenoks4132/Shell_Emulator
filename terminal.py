from zipfile import ZipFile


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
            self.cd(params[1:])
        elif params[0] == 'ls':
            self.ls()
        elif params[0] == 'cat':
            self.cat(params[1:])

    def cd(self, params):
        if len(params) == 0:
            self.cur_d = ''
            return
        directory = params[-1]
        if directory.startswith('-'):
            print('Не указана директория для перехода')
            return

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
            self.cur_d = ''
            return

        for file in self.fs.namelist():
            if file.startswith(new_path):
                self.cur_d = new_path
                return
        print('Директория с таким названием отсутствует')

    def ls(self):
        files = set()
        for file in self.fs.namelist():
            if file.startswith(self.cur_d):
                ls_name = file[len(self.cur_d):]
                if '/' in ls_name:
                    ls_name = ls_name[:ls_name.index('/')]
                files.add(ls_name)
        print(*filter(lambda x: len(x) > 0, sorted(files)), sep='\n')

    def cat(self, params):
        file = params[-1]
        if file.startswith('-'):
            print('Не указана директория для перехода')
            return
        try:
            with self.fs.open(self.cur_d + file, 'r') as read_file:
                print(read_file.read().decode('UTF-8'))
        except:
            print('Неправильное название файла')