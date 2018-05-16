from auto_everything.web import Selenium
from time import sleep

my_selenium = Selenium("https://www.google.com")
d = my_selenium.driver

# get input box
xpath = '//*[@id="lst-ib"]'
element = my_selenium.wait_until_exists(xpath)

# text inputing
element.send_keys('\b' * 20, "yingshaoxo")

# click search button
element = my_selenium.wait_until_exists('//*[@id="tsf"]/div[2]/div[3]/center/input[1]')
element.click() # d.execute_script("arguments[0].click();", element)

# exit
sleep(3)
d.quit()
