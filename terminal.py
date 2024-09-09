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

    def cd(self, params):
        if len(params) == 0:
            self.cur_d = ''
            return
        directory = params[-1]
        if directory.startswith('-'):
            print('Директория с таким названием отсутствует')
            return
        directory = directory.split('/')
        new_directory = self.cur_d.split('/')
        if new_directory == ['']:
            new_directory = []
        for i in directory:
            if i == '..':
                if len(new_directory) > 0:
                    new_directory.pop()
                else:
                    print('Директория с таким названием отсутствует')
                    return
            else:
                new_directory.append(i)

        new_path = '/'.join(new_directory) + '/'
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
        print(*sorted(files), sep='\n')