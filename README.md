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

#### Get involved
```
You know, one man's work is kind of boring, so if you have any better way to implement some function, feel free to pull a request.
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
#### Turn `Python Class` into a `Command Line Program`
```
py.fire(your_class_name)
```

___


## Advanced API
#### Create(start) or Cancel(stop) a systemd serviece
```python
from auto_everything.base import Super
s = Super(username="root")

s.service("service_name", "your_python_file_path")
```

___


## System management
#### Get package list
```python
from auto_everything.base import OS
_os = OS()

python_packages = _os.list_python_packages()
lubuntu_packages = _os.list_packages()

print(python_packages)
print(lubuntu_packages)
```

#### Install or Uninstall a Python package
```python
from auto_everything.base import OS
_os = OS()

_os.install_python_package("any_package_name")
_os.uninstall_python_package("any_package_name")
```

#### Install or Uninstall a Lubuntu package
```python
from auto_everything.base import OS
_os = OS()

_os.install_package("any_package_name")
_os.uninstall_package("any_package_name")
```

___


## Anothers
#### Web automation
```python
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
```python
from auto_everything.base import IO
io = IO()

io.write("hi.txt", "Hello, world!")
print(io.read("hi.txt"))

io.append("hi.txt", "\n\nI'm yingshaoxo.")
print(io.read("hi.txt"))
```
