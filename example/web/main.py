from auto_everything.web import Selenium
from time import sleep

from auto_everything.terminal import Terminal
t = Terminal()

t.kill("chrome")

my_selenium = Selenium("https://www.google.com", headless=False, user_data_dir="/home/yingshaoxo/.config/google-chrome/")
d = my_selenium.driver

# get input box
xpath = '/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input'
elements = my_selenium.wait_until_exists(xpath)

# text inputing
elements[0].send_keys('\b' * 20, "yingshaoxo")

# click search button
elements = my_selenium.wait_until_exists('//input[@value="Google Search"]')
if len(elements):
    elements[0].click() # d.execute_script("arguments[0].click();", elements[0])

# exit
sleep(30)
d.quit()
