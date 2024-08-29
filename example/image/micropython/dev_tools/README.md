# micropython dev tools for linux

```python
import ys_pyboard

pyb = ys_pyboard.Pyboard('/dev/ttyACM0')
pyb.enter_raw_repl()

print("start:")
result = pyb.exec('print(1+1)')
print("get result:")
print(result)

pyb.exit_raw_repl()
```

> If you want to handle files in sd card, use `open()` to read or write.
