# auto_everything
Linux system automation

#### Installation
`pip3 install auto_everything'

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

