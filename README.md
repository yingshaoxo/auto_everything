# auto_everything
Linux(mainly ubuntu) automation

#### Installation
```
wget https://github.com/yingshaoxo/auto_everything/raw/master/env_setup.sh
sudo bash env_setup.sh
```

#### Magic
```
wget https://github.com/yingshaoxo/auto_everything/raw/master/demo/install_YouCompleteMe.py
sudo python3 install_YouCompleteMe.py
```

___


## Basic API
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

#### Kill it
```
t.kill('terminal')
```

___


## For simplify Python development
#### Check out object information
```
from auto_everything.base import Terminal, Python
t = Terminal()
py = Python()

py.help(t)
```

___


## Advanced API
#### Keep a function running
```
from auto_everything.base import Python
py = Python()

i = 0

@py.loop(thread=False)
def count():
    global i
    i += 1
    print(i)

count()

print("Welcome to my world!")
```

#### Create(start) or Cancel(stop) a systemd serviece
```
from auto_everything.base import Super
s = Super(username="root")

s.service("service_name", "your_python_file_path")
```

___


## Package management
#### Install or Uninstall a Python package
```
from auto_everything.base import Python
py = Python()

py.install_package("any_package_name")
py.uninstall_package("any_package_name")
```

#### Install or Uninstall a Lubuntu package
```
from auto_everything.base import Terminal
t = Terminal()

t.install_package("any_package_name")
t.uninstall_package("any_package_name")
```

___


## Anothers
#### Web automation
```
from auto_everything.web import Selenium
from time import sleep

my_selenium = Selenium("https://www.google.com", headless=False)
d = my_selenium.driver

# get input box
xpath = '//*[@id="lst-ib"]'
element = my_selenium.wait_until_exists(xpath)[0]

# text inputing
element.send_keys('\b' * 20, "yingshaoxo")

# click search button
element = my_selenium.wait_until_exists('//input[@value="Google Search"]')[0]
element.click() # d.execute_script("arguments[0].click();", element)

# exit
sleep(30)
d.quit()
```

#### Simpler IO
```
from auto_everything.base import IO
io = IO()

io.write("hi.txt", "Hello, world!")
print(io.read("hi.txt"))

io.append("hi.txt", "\n\nI'm yingshaoxo.")
print(io.read("hi.txt"))
```
