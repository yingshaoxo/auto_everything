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
