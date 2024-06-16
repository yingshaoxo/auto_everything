# auto_everything

Linux automation

> My package dependence is not stable yet, I am considering switch the base python version back to static python2.7 or tinypy or micropython. (The current one is python3.10, I have a statically amd64 build in: https://gitlab.com/yingshaoxo/use_docker_to_build_static_python3_binary_executable)

> But it is hard to make sure everything working fine 20 years later. Because I can't make sure 20 years later you can still buy a hardware that could allow you to run python2.7 or tinypy or old version of micropython. (Maybe you simply can't download a python2.7 binary or source code, or can't compile it since you don't have an old GCC.)

#### Installation (For Python == 3.10)

```bash
Just copy the 'auto_everything' folder, then put it into the root folder of your project or "/usr/local/lib/python3.10/dist-packages/" or "<your_compiled_local_python>/Lib/", so that you can directly import it.
```

```bash
python3 -m pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev" --break-system-packages

# Use github on care, you may get banned(404) by saying the 'fuck' word: https://yingshaoxo.xyz/pictures/github/index.html
```

```bash
# For amd64 linux machine, you can get a statically compiled python3.10 by doing following.

sudo su
curl -sSL https://gitlab.com/yingshaoxo/use_docker_to_build_static_python3_binary_executable/-/raw/master/install.sh?ref_type=heads | bash
```

> What the fuck the `debian` is thinking of? Why we can't use pip to directly install a package anymore? **debian/ubuntu linux branch** want to force people to let their package go through **a strict censorship process** so that they can decide which software is good, which is not?

> 'export PATH=$PATH:/**/bin/' still working fine.

> Where is the freedom? My dear people! 

> What is the difference between `pip install` and `apt install`? Simply because **pypi has more freedom**?

> 2025: Actually, I found pypi is also not free any more, they let the package publish more and more complex and painful. (Without 2 Factor Verifying, you can't even login your pypi account.) I think you better create your own hardware and launch a new software distrubution platform. You would have totally freedom in your kindom if you created that world by yourself.

> I even found VPS(remote server computer) is also not stable, they force you to update systems, in new system, they will always have a background process that is doing a monitor for your user's data. And consider of censorship from bad law reason, I think you should also create your own physical network.

> "More code, more bug, more dependencies, more unstable, remember that. --- yingshaoxo"

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

#### Http server and client

```
Just have a look at "http_.py", we keep http1.1 not upgrade for simplifying and secure reason.
```

# Yingshaoxo machine learning ideas

## For natual language process
We treat every char as an id or tensor element

In GPU based machine learning algorithm, you will often do things with [23, 32, 34, 54]

But now, it becomes ['a', 'b', 'c', 'd'], or ASCII number [0, 255].


<!--
### For text summary
For the self attention mechanism, it is using word apperance counting dict. You could think it as a dict, multiple key link to one same value, for all those multiple key string, if a word show up a lot of time, it is likely a important word.
(You can think this as a TV show, for the same envirnoment, if a person only show once, it is not the main character, it is not important. But if a character show a lot times, you can almost see it at any eposide, then it is a important character)

For one sequence or list, If its importance number less than average(half of 'its sequence importance sum'), you remove it

Or you could do this: if that word does not appear again in the following sentences of the input_text in your database, you treat it as not important text.
-->


### For translation
long sequence (meaning group) -> long sequence (meaning group)

what you do -> 你干什么
It depends on -> 这取决于

(It depends on) (what you do) -> 这取决于 你干什么

meaning group can be get automatically, all you have to do is count continues_words appearance time. the more time a continuse_words appear, the more likely it is a meaning group

It all can be summaryed as "divide and conquer"


<!--
### For question and answer
For context information extraction, you have to use the question. If one sentence of the context should at the bottom of the question, you keep it, otherwise, you remove it

Then, for the other context, you do a simple sort
-->

### For text generation or completion
```
one char predict next char
two char predict next char
...
one word predict next word
two words predict next word
three words predict next word
...
```

when you use it, use it from bottom to top, use longest sequence to predict the next word first.

> the more level you make, the more accurate it would be.

> It is dict based next word generator, so the speed is super quick.

> Don't expect this method will have high accuracy becuase the logic is simple, it can only be used for punctuate adding if you use previous words and next words to predict the center character.

<!--
> This method was created by yingshaoxo. it only need cpu than gpu. it can beat gpt4 with an old computer if you have big dataset (30GB) and big memory to hold the dict.
-->


### For general AI
<!--
```
General AI algorithm:

Natural language -> Python programming language -> Go through CPU -> If it is working, add weights to that sentence, if it is not working, minus weights for that sentence -> use long sub_string weights to generate more following natural language sentences -> execute more programming language that was translated from natural language -> it is a never end loop, but if the storage is about to blow, we need to find a way to do compression and find more way to store data.

Those code are generated in real time. For each response, it generate different algorithm or code. It adopts to any situation.

#yingshaoxo
```
-->

```python
#yingshaoxo: I could give you a template for general AI, if you ask 100000 people to work on one AI project, and do hard coding, each person write if else logic for 3 years, do not do repeat work. A general AI could be made if your have no dependence and not get spying in offline. Because that hard coding countless functions will cover almost all language level question and answer case in normal life.

from auto_everything.terminal import Terminal
terminal = Terminal()

global_memory_dict = {}

def update_global_dict_based_on_new_information(input_text):
    global global_memory_dict
    # find a way to simplify the input_text as pure json 5 type data
    global_memory_dict.update(dict({"input_text": input_text}))

def natual_language_to_task_code(input_text):
    global global_memory_dict
    # You have to let the machine generate different code or algorithm for different input_text, so that each time the reply is different.
    code = generate_machine_code_from_memory_and_input_text(global_memory_dict, input_text)
    return code

def execute_code(code):
    global global_memory_dict
    import json
    # For example, execute python code. 
    previous_info_code = f"""
        memory_dict = json.loads('{json.dumps(global_memory_dict)}')
    """
    result = terminal.run_python_code(previous_info_code + code)
    return result

while True:
    input_text = input("What you want to say? ")

    update_global_dict_based_on_new_information("question:\n" + input_text)

    code = natual_language_to_task_code(input_text)
    result = execute_code(code)
    print(result)

    update_global_dict_based_on_new_information("my_answer_and_experiment_result:\n" + result)
```
