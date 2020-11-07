# auto_everything
Linux(mainly ubuntu) automation

#### Donation
[<img src="https://github.com/yingshaoxo/yingshaoxo/raw/master/become_a_patron_button.png" width="200">](https://www.patreon.com/bePatron?u=45200693)


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

#### Docs
https://yingshaoxo.github.io/auto_everything

___


## Basic API
#### Import
```python
from auto_everything.base import Terminal
t = Terminal()
```

#### Run a command and get reply
```python
reply = t.run_command('uname -a')
print(reply)
```

#### Run commands and get direct screen output
```python
commands = """
sudo apt update
uname -a
"""
t.run(commands)
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
    def push(self, comment):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def undo(self):
        t.run("""
git reset --mixed HEAD~1
""")

    def reset(self):
        t.run("""
git reset --hard HEAD^
""")

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


## Others
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

#### Quick File Operation
```python
from auto_everything.disk import Disk
from pprint import pprint
disk = Disk()

files = disk.get_files(".")
files = disk.sort_files_by_time(files)
pprint(files)
```

#### Easy Store
```python
from auto_everything.disk import Store
store = Store("test")

store.set("author", "yingshaoxo")
store.set("author", {"email": "yingshaoxo@gmail.com", "name": "yingshaoxo"})
print(store.get_items())

print(store.has_key("author"))
print(store.get("author", ""))
print(store.get("whatever", default_value="alsjdasdfasdfsakfla"))

store.reset()
print(store.get_items())
```
