# auto_everything

Linux automation

#### Help Wanted

I lost my job for almost a year. If you wish to see me alive, please buy me some food:

* Paypal: https://paypal.me/yingshaoxo
* Patron: https://www.patreon.com/bePatron?u=45200693

<!-- [<img src="https://github.com/yingshaoxo/yingshaoxo/raw/master/become_a_patron_button.png" width="200">](https://www.patreon.com/bePatron?u=45200693) -->

#### Installation (For Python >= 3.10)

```bash
curl -sSL https://install.python-poetry.org | python3
poetry add "git+https://github.com/yingshaoxo/auto_everything.git@dev"

or

sudo pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev"

or

sudo pip3 install "git+https://github.com/yingshaoxo/auto_everything.git@dev" --break-system-packages
```

> What the fuck the `debian` or `pip` or `python community` is thinking of? Why we can't use pip to directly install a package?

> Those **assohle** who in charge never want to make things easy, are they?

#### Installation (For 3.5 <= Python < 3.10)

```bash
poetry add auto_everything==3.9

or

sudo pip3 install auto_everything==3.9
```

#### Magic

```bash
sudo su

curl -sSL https://github.com/yingshaoxo/auto_everything/raw/master/env_setup.sh | bash

wget -O - https://github.com/yingshaoxo/auto_everything/raw/master/example/install_YouCompleteMe.py | python3

exit

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

## For simplifying python development

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

## For simplifying general `server and client` development


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

#### Generate `Python, Flutter, Typescript` code

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
from generated_yrpc.english_rpc import *

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

  var result = await client.say_hello(
    item: hello_request(name: "yingshaoxo")
  );
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

#### Encryption and Decryption

```python
encryption_and_decryption = EncryptionAndDecryption()

a_dict = encryption_and_decryption.get_secret_alphabet_dict("hello, world")

a_sentence = "I'm yingshaoxo."

encrypted_sentence = encryption_and_decryption.encode_message(a_secret_dict=a_dict, message=a_sentence)
print()
print(encrypted_sentence)
> B'i ybjdqahkxk.

decrypted_sentence = encryption_and_decryption.decode_message(a_secret_dict=a_dict, message=encrypted_sentence)
print(decrypted_sentence)
> I'm yingshaoxo.
```

#### JWT Tool (Json-Web-Token Tool) 
```python
jwt_tool  = JWT_Tool()

secret = "I'm going to tell you a secret: yingshaoxo is the best."

a_jwt_string = jwt_tool.my_jwt_encode(data={"name": "yingshaoxo"}, a_secret_string_for_integrity_verifying=secret)
print(a_jwt_string)
> eyJhbGciOiAiTUQ1IiwgInR5cCI6ICJKV1QifQ==.eyJuYW1lIjogInlpbmdzaGFveG8ifQ==.583085987ba46636662dc71ca6227c0a

original_dict = jwt_tool.my_jwt_decode(jwt_string=a_jwt_string, a_secret_string_for_integrity_verifying=secret)
print(original_dict)
> {'name': 'yingshaoxo'}

fake_jwt_string = "aaaaaa.bbbbbb.abcdefg"
original_dict = jwt_tool.my_jwt_decode(jwt_string=fake_jwt_string, a_secret_string_for_integrity_verifying=secret)
print(original_dict)
> None
```

#### Web automation

```python
from auto_everything.web import Selenium

my_selenium = Selenium("https://www.google.com", headless=False)
d = my_selenium.driver

# get input box
xpath = '//*[@id="lst-ib"]'
elements = my_selenium.wait_until_elements_exists(xpath)
if len(elements) == 0:
    exit()

# text inputing
elements[0].send_keys('\b' * 20, "yingshaoxo")

# click search button
elements = my_selenium.wait_until_elements_exists('//input[@value="Google Search"]')
if len(elements):
    elements[0].click()

# exit
my_selenium.sleep(30)
d.quit()
```

