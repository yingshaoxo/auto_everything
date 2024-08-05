# yingshaoxo x11 open_on_not_open_ui

You should run this script with the target url service address: 
```bash
python3 a_window.py 'http://localhost:7777' '600x800'
```

You have to create a server similar to "./ui_service.py" to render image.

## Limitation
Python is 60 times slower than c if you loop a 1920x1080x4 list.

That is why this version is only about 1 frame/picture per second.
