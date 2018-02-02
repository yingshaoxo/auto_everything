# Usage
# python3 demo.py ffmpeg convert ~/Videos

import sys
args = sys.argv[1:]
if len(args) == 0:
    print('no args are giving')
    exit()
else:
    print(args)

import os
import logging
current_dir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(filename=os.path.join(current_dir, 'whatsup.log'), level=logging.INFO)

from auto_everything import Base, Batch
base = Base()
batch = Batch()

logging.info('start')


if args[0] == 'boot':
    ssr_path = '/opt/shadowsocksr/shadowsocks/local_run.sh'
    v2ray_path = '/opt/v2ray/v2ray'
    chrome_path = '/opt/google/chrome/google-chrome'

    # open ssr
    base.run_program('sudo bash ' + ssr_path)

    # open v2ray
    status = base.is_running('v2ray')
    if status != True:
       base.run_program(v2ray_path)

    # open chrome
    status = base.is_running('chrome')
    if status != True:
        base.run_program(chrome_path)

elif args[0] == 'ffmpeg':
    import shlex
    convert_command = ''
    speedup_command = ''
    is_folder = False

    def get_command(file_path):
        global convert_command, speedup_command
        convert_command = """ffmpeg -i {put_in} -crf 18 -pix_fmt yuv420p -c:a copy {put_in}_converted.mp4""".format(put_in=shlex.quote(file_path))
        speedup_command = """ffmpeg -i {put_in} -vf "setpts=0.5*PTS" -r 50 -c:v mpeg4 -b:v 1500k -af "atempo=2" {put_in}_speedup.mp4""".format(put_in=shlex.quote(file_path))

    def make_sure_env():
        global convert_command, speedup_command, is_folder
        try:
            if 'not installed' in base.run_command('ffmpeg'):
                print('apt install ffmpeg')
                exit()
            if os.path.isfile(args[2]):
                get_command(args[2])
            elif os.path.isdir(args[2]):
                is_folder = True
            else:
                print('you just gave me a wrong file path')
                exit()
        except Exception as e:
            print(e)
            print('something was going wrong\n1. give me a file path\n2. ffmpeg have to be installed: apt install ffmpeg')
            exit()

    if args[1] == 'convert':
        make_sure_env()
        if is_folder:
            files = batch.get_current_directory_files(args[2]) 
            for f in files:
                get_command(f)
                base.run_program(convert_command)
        else:
            base.run_program(convert_command)

    elif args[1] == 'speedup':
        make_sure_env()
        if is_folder:
            files = batch.get_current_directory_files(args[2]) 
            for f in files:
                get_command(f)
                base.run_program(speedup_command)
        else:
            base.run_program(speedup_command)

    else:
        print('what function you would like? speedup or convert?')
        exit()


logging.info('done')
