# auto_everything

Linux automation

#### Donation

[<img src="https://github.com/yingshaoxo/yingshaoxo/raw/master/become_a_patron_button.png" width="200">](https://www.patreon.com/bePatron?u=45200693)

#### Installation (For Python >= 3.10)

```bash
curl -sSL https://install.python-poetry.org | python3
poetry add auto_everything

or

sudo pip3 install auto_everything
```

> Full Installation: `poetry add auto_everything --extras all`

#### Installation (For 3.5 <= Python < 3.10)

```bash
poetry add auto_everything==3.9

or

sudo pip3 install auto_everything==3.9
```

#### Magic

```bash
python3 -m auto_everything
```

or

```bash
curl -sSL https://github.com/yingshaoxo/auto_everything/raw/master/env_setup.sh | bash

wget -O - https://github.com/yingshaoxo/auto_everything/raw/master/example/install_YouCompleteMe.py | python3
```

#### Docs

https://yingshaoxo.github.io/auto_everything

---

## Basic API

#### Import

```python
from auto_everything.terminal import Terminal
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

---

## For simplify Python development

#### Import

```python
from auto_everything.python import Python
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

---

## For simplify general server and client development


#### Define YRPC Protocols

```grpc
service Greeter {
    rpc say_hello (hello_request) returns (HelloReply);
}

enum UserStatus {
    OFFLINE = 0;
    ONLINE = 1;
}

message hello_request {
   string name = 1;
   UserStatus user_status = 2;
   repeated UserStatus user_status_list = 3;
}

message HelloReply {
    string message = 1;
}
```

#### Generate Python, Flutter, Typescript code

```python
from auto_everything.develop import YRPC
yrpc = YRPC()

for language in ["python", "dart", "typescript"]:
    yrpc.generate_code(
        which_language=language,
        input_folder="/home/yingshaoxo/CS/protocol_test/protocols",
        input_files=["english.proto"],
        output_folder="/Users/yingshaoxo/CS/protocol_test/generated_yrpc"
    )
```

> Here, we only use python to do the server part job.

#### Then, you can use it like this:

```python
from generated_yrpc.english_rpc.py import *

class NewService(Service_english):
    async def say_hello(self, item: hello_request) -> HelloReply:
        reply = HelloReply()
        reply.message = item.name
        return reply

service_instance = NewService()
run(service_instance, port="6060")
```

```dart
void main() async {
  var client = Client_english(
    service_url: "http://127.0.0.1:6060",
    error_handle_function: (error_message) {
      print(error_message);
    },
  );

  var request = hello_request(
    name: "yingshaoxo"
  )
  var result = await client.say_hello(item: request);
  if (result != null) {
    print(result);
  }
}
```

___

## Others

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

files = disk.get_files(folder=".", type_limiter=[".mp4"])
files = disk.sort_files_by_time(files)
pprint(files)
```

#### Easy Store

```python
from auto_everything.disk import Store
store = Store("test")

store.set("author", "yingshaoxo")
store.delete("author")
store.set("author", {"email": "yingshaoxo@gmail.com", "name": "yingshaoxo"})
print(store.get_items())

print(store.has_key("author"))
print(store.get("author", default_value=""))
print(store.get("whatever", default_value="alsjdasdfasdfsakfla"))

store.reset()
print(store.get_items())
```

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

