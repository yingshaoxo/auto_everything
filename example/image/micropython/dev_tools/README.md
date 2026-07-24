# micropython dev tools for linux

```python
import ys_pyboard

pyb = ys_pyboard.Pyboard('/dev/ttyACM0')
pyb.enter_raw_repl()

print("start:")
result = pyb.exec('print(1+1)')
print("get result:")
print(result)

#print(pyb.list_files_and_folders("."))
#pyb.upload_file("hi.py", "/main.py")
#pyb.upload_file("hi.py", "/test/hi.py")
#pyb.delete_file_or_folder("/test")

pyb.exit_raw_repl()
```

> If you want to handle files in sd card, use `open()` to read or write.

## thinking

So far, the chinese version pyboard 1.1 plus is the best. It has 60+ free pin for using, and it has built-in SD card loader. And when you connect your chip to computer, it will show you a storage where you can directly change the main.py in your flash storage or SD card storage to do the programming.

## fix permission

sudo usermod -a <username> -G dialout
sudo reboot
