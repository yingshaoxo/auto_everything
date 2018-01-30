# auto_everything
Linux system automation

#### Installation
`pip3 install auto_everything`

#### Import
```
from auto_everything import Base
base = Base()
```

#### Run command & get reply
```
reply = base.run_command('uname -a')
print(reply)
```

#### Run program
`base.run_program('firefox')`


#### Run python script
`base.run_py('your_python_file_path')`


#### Detect if a program or script is running
```
status = base.is_running('terminal')
print(status)
```

#### Demo
```
#!/usr/bin/env python3
import os
import logging
current_dir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(filename=os.path.join(current_dir, 'whatsup.log'), level=logging.INFO)


from auto_everything import Base as Auto
auto = Auto()

logging.info('start')

v2ray_path = '/opt/v2ray/v2ray'
chrome_path = '/opt/google/chrome/google-chrome'

# open v2ray
status = auto.is_running('v2ray')
if status != True:
    auto.run_program(v2ray_path)

# open chrome
status = auto.is_running('chrome')
if status != True:
    auto.run_program(chrome_path)

logging.info('done')
```
