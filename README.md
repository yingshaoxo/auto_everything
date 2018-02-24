# auto_everything
Linux system automation

#### Installation
`pip3 install auto_everything`

#### Import
```
from auto_everything import Base
b = Base()
```

#### Run command & get reply
```
reply = b.run_command('uname -a')
print(reply)
```

#### Run program
`b.run_program('firefox')`

#### Run python script
`b.run_py('your_python_file_path')`

#### Run bash script
`b.run_sh('your_.sh_file_path')`

#### Detect if a program or script is running
```
status = base.is_running('terminal')
print(status)
```

#### Demo
```
from auto_everything import Base
base = Base()

v2ray_path = '/opt/v2ray/v2ray'
chrome_path = '/opt/google/chrome/google-chrome'

# open v2ray
status = base.is_running('v2ray')
if status != True:
    base.run_program(v2ray_path)

# open chrome
status = base.is_running('chrome')
if status != True:
    base.run_program(chrome_path)
```
