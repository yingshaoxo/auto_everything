from auto_everything.terminal import Terminal

terminal = Terminal()

result = terminal.run_python_code(code="""
import os

print("fuck you")
print(os.listdir("."))
""", cwd="~/Downloads")

print()
print(result)