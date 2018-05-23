# auto_everything
Linux system automation

#### Installation
```
sudo apt install python3
sudo apt install python3-pip
pip3 install auto_everything
```

#### Import
```
from auto_everything.base import Terminal
t = Terminal()
```

#### Run a command & get reply
```
reply = t.run_command('uname -a')
print(reply)
```

#### Run commands & wait until it was finished
```
commands = """
sudo apt update
uname -a
"""
t.run(commands, wait=True)
```

#### Run a program
`t.run_program('firefox')`

#### Run a python script
`t.run_py('your_python_file_path')`

#### Run a bash script
`t.run_sh('your_.sh_file_path')`

#### Detect if a program or script is running
```
status = t.is_running('terminal')
print(status)
```

#### Keep a function running
```
from auto_everything.base import Python
py = Python()

i = 0

@py.loop
def count():
    global i
    i += 1
    print(i)

count()
```

#### Create a systemd serviece
```
from auto_everything.base import Super
s = Super(username="yingshaoxo")

s.start_service("service_name", "your_python_file_path")
#s.stop_service("service_name")
```

#### Web automation
```
from auto_everything.web import Selenium
from time import sleep

my_selenium = Selenium("https://www.google.com")
d = my_selenium.driver

# get input box
xpath = '//*[@id="lst-ib"]'
element = my_selenium.wait_until_exists(xpath)

# text inputing
element.send_keys('\b' * 20, "yingshaoxo")

# click search button
element = my_selenium.wait_until_exists('//*[@id="tsf"]/div[2]/div[3]/center/input[1]')
element.click() # d.execute_script("arguments[0].click();", element)

# exit
"""
sleep(3)
d.quit()
"""
```
