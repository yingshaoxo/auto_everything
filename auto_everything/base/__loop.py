import time

def log(text):
    with open('log', 'a') as f:
        f.write("\n"*2 + text + '  ' + str(time.time()))

while 1:
    log('running')
    time.sleep(3)
