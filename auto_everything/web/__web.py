from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class Net():
    def wait_until_have_internet(self, test_url="https://baidu.com"):
        from urllib.request import urlopen
        from time import sleep
        while 1:
            try:
                urlopen("https://baidu.com")
                break
            except Exception as e:
                sleep(1)


class Selenium():
    def __init__(self, url):
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            print(e)
            try:
                self.driver = webdriver.Firefox()
            except Exception as e:
                print(e)
                self.driver = webdriver.PhantomJS()
        self.driver.get(url)
        
    def wait_until_exists(self, xpath, timeout=600):
        try:
            w = WebDriverWait(self.driver, timeout)
            w.until(EC.presence_of_element_located((By.XPATH, xpath)))
            elements = self.driver.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            print(e)
            return None

    def click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
