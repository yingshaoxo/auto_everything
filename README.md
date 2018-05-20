# auto_everything
Linux system automation

#### Installation
`pip3 install auto_everything`

#### Import
```
from auto_everything.base import Terminal
t = Terminal()
```

#### Run command
```
t.run('sudo apt update', wait=True)
```

#### Run command & get reply
```
reply = t.run_command('uname -a')
print(reply)
```

#### Run program
`t.run_program('firefox')`

#### Run python script
`t.run_py('your_python_file_path')`

#### Run bash script
`t.run_sh('your_.sh_file_path')`

#### Detect if a program or script is running
```
status = t.is_running('terminal')
print(status)
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
sleep(3)
d.quit()
```
