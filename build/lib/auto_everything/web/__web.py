from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class Selenium():
    def __init__(self, url):
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            print(e)
            self.driver = webdriver.Edge()
        self.driver.get(url)
        
    def wait_until_exists(self, xpath, timeout=600):
        try:
            w = WebDriverWait(self.driver, timeout)
            w.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return self.driver.find_element_by_xpath(xpath)
        except Exception as e:
            print(e)
            return None
