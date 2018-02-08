import os
import sys
import shlex, subprocess

import re
import getpass


class Base():
    def __init__(self):
        self.py_version = '{major}.{minor}'.format(major=str(sys.version_info[0]), minor=str(sys.version_info[1])) 
        if float(self.py_version) < 3.5:
            print('We only support Python >= 3.5 Versions')
            exit()

        self.current_dir = os.getcwd()
        self._current_file_path = os.path.join(self.current_dir, sys.argv[0])

        # if os.path.exists(os.path.join(self.current_dir, 'nohup.out')):
        #     os.remove(os.path.join(self.current_dir, 'nohup.out'))

    def run_command(self, c):
        args_list = shlex.split(c)
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)

    def run_program(self, name):
        args_list = shlex.split(name)
        args_list = ['nohup'] + args_list
        p = subprocess.Popen(args_list)

    def run_py(self, file_path):
        process_name = os.path.join(*file_path.split(os.sep)[-2:])
        if process_name not in self.run_command('ps x'):
            self.run_program('python{version} {path} &'.format(version=self.py_version, path=os.path.abspath(file_path)))

    def is_running(self, name):
        if name in self.run_command('ps x'):
            return True
        else:
            return False

    def kill(self, name):
        args_list = shlex.split('sudo pkill {name}'.format(name=name))
        result = subprocess.run(args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        return str(result.stdout)


class Batch():
    def __init__(self):
        pass

    def get_current_directory_files(self, directory):
        directory = os.path.abspath(directory)
        files_and_dir = os.listdir(directory)
        files = [os.path.join(directory, f) for f in files_and_dir if os.path.isfile(os.path.join(directory, f))]
        return files


class Super():
    def __init__(self, username=os.getlogin()): #getpass.getuser()):
        self.__base = Base()
        self.__id = '# ' + self.__base._current_file_path
        self.__username = username
        self.__crontab_path = '/var/spool/cron/crontabs/{username}'.format(username=self.__username) 
        
        if os.geteuid() != 0:
            self.__root = False
        else:
            self.__root = True

    def __clear_crontab(self):
        with open(self.__crontab_path, 'w') as f:
            f.write('')

    def __crontab_text_to_dict(self):
        if os.path.exists(self.__crontab_path) == False:
            with open(self.__crontab_path, 'w') as f:
                f.write('')

        with open(self.__crontab_path, 'r') as f:
            text = f.read()

        id_list = re.findall(r'# .+', text, re.MULTILINE)
        id_list = [i.strip(' \n') for i in id_list if i.strip(' \n') != '']

        command_list = re.split(r'# .+', text, re.MULTILINE)
        command_list = [i.strip(' \n') for i in command_list if i.strip(' \n') != '']

        if len(id_list) != len(command_list):
            self.__clear_crontab()
            return dict()

        dict_ = dict()
        for index, id_ in enumerate(id_list):
            dict_.update({id_: command_list[index]}) 

        return dict_

    def __dict_to_crontab(self, dict_):
        text = ''
        for id_, command in dict_.items():
            text = text + '\n\n' + id_ + '\n' + command

        text = '\n\n' + text.strip('\n ') + '\n'
        with open(self.__crontab_path, 'w') as f:
            f.write(text)

    def __restart_crontab(self):
        self.__base.run_command('sudo service cron restart')

    def keep_running(self, args=''):
        if not self.__root:
            print('Super class need root permission.')
            return

        command = '*/1 * * * * export DISPLAY=:0; /usr/bin/python{py_version} {path} {args}'.format(py_version=self.__base.py_version, path=self.__base._current_file_path, args=args)

        dict_ = self.__crontab_text_to_dict()
        dict_.update({self.__id: command})

        if self.__crontab_text_to_dict() != dict_:
            self.__dict_to_crontab(dict_)
            self.__restart_crontab()

    def stop_running(self):
        if not self.__root:
            print('Super class need root permission.')
            return

        dict_ = self.__crontab_text_to_dict()
        if self.__id in dict_.keys():
            del dict_[self.__id]
        self.__dict_to_crontab(dict_)
        self.__restart_crontab()
        
    
if __name__ == "__main__":
    b = Base()
    s = Super()
    #if b.is_running('firefox'):
    #    b.kill('firefox')
