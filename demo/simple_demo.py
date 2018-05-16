from auto_everything.base import Terminal
from selenium import l

t = Terminal()
s = Super()

t.run_py('/root/Music_town/app/app.py')
t.run_py('/root/Web-Math-Chat/app/app.py')
t.run_py('/root/Local_Show/app/app.py /var/www/html/download')

if not t.is_running('Xiaoya/Telegram.py'):
    t.run_py('/root/Xiaoya/Telegram.py')

if 'aria2' not in t.run_command('docker ps'):
    t.run_command('docker restart aria2')

if not t.is_running('/usr/local/shadowsocksr/shadowsocks/server.py'):
        t.run_program('python /usr/local/shadowsocksr/shadowsocks/server.py -c /etc/shadowsocksr/user-config.json')

s.keep_running(1)
