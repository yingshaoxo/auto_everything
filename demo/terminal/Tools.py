#!/usr/bin/env /usr/bin/python3
from auto_everything.python import Python
from auto_everything.terminal import Terminal
py = Python()
t = Terminal()


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

    def image_compress(self, image):
        t.run(f"""
convert {image} -sampling-factor 4:2:0 -strip -quality 85 -adaptive-resize 60% -interlace JPEG -colorspace RGB compressed_{image}
        """) #-gaussian-blur 0.05 


py.fire(Tools)
py.make_it_global_runnable(executable_name="Tools")
