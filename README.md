# auto_everything
Linux(mainly ubuntu) automation

#### Installation
```bash
sudo pip3 install auto_everything
```

or

```bash
wget https://github.com/yingshaoxo/auto_everything/raw/master/env_setup.sh
sudo bash env_setup.sh
```

#### Magic
```bash
wget https://github.com/yingshaoxo/auto_everything/raw/master/demo/install_YouCompleteMe.py
python3 install_YouCompleteMe.py
```

#### Get involved
```
You know, one man's work is kind of boring, so if you have any better way to implement some function, feel free to pull a request.
```
___


## Basic API
#### Import
```python
from auto_everything.base import Terminal
t = Terminal()
```

#### Run a command & get reply
```python
reply = t.run_command('uname -a')
print(reply)
```

#### Run commands & wait until it was finished
```python
commands = """
sudo apt update
uname -a
"""
t.run(commands, wait=True)
```

#### Run a program
```python
t.run_program('firefox')
```

#### Run a python script
```python
t.run_py('your_file.py')
```

#### Run a bash script
```python
t.run_sh('your_file.sh')
```

#### Detect if a program or script is running
```python
status = t.is_running('terminal')
print(status)
```

#### Kill it
```python
t.kill('terminal')
```

___


## For simplify Python development
#### Import
```python
from auto_everything.base import Python
py = Python()
```

#### Turn `Python Class` into a `Command Line Program`
```python
py.fire(your_class_name)
```

#### Make it `global executable`:
```python
py.make_it_global_runnable(executable_name="Tools")
```

#### Example
Let's assume you have a file named `Tools.py`:

```python
from auto_everything.base import Python
py = Python()

class Tools():
    def hi(self):
        print("Hi, Python!")

py.fire(Tools)
py.make_it_global_runnable(executable_name="MyTools")
```

After the first running of this script by `python3 Tools.py hi`, you would be able to use `MyTools` to run this script at anywhere within your machine:
```bash
yingshaoxo@pop-os:~$ MyTools hi
Hi, Python!

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
os_ = OS()

python_packages = os_.list_python_packages()
lubuntu_packages = os_.list_packages()

print(python_packages)
print(lubuntu_packages)
```

#### Install or Uninstall a Python package
```python
from auto_everything.base import OS
os_ = OS()

os_.install_python_package("any_package_name")
os_.uninstall_python_package("any_package_name")
```

#### Install or Uninstall a Lubuntu package
```python
from auto_everything.base import OS
os_ = OS()

os_.install_package("any_package_name")
os_.uninstall_package("any_package_name")
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
elements = my_selenium.wait_until_exists(xpath)

# text inputing
elements[0].send_keys('\b' * 20, "yingshaoxo")

# click search button
elements = my_selenium.wait_until_exists('//input[@value="Google Search"]')
if len(elements):
    elements[0].click() # d.execute_script("arguments[0].click();", elements[0])

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
