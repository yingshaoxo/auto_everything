from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Selenium():
    """
    It's a wrap of selenium
    """

    def __init__(self, url, headless=False, timeout=600, user_data_dir=None):
        '''
        user_data_dir:
        /home/yingshaoxo/.config/google-chrome/
        '''
        try:
            options = Options()
            if headless == False:
                if user_data_dir:
                    options.add_argument(f'user-data-dir={user_data_dir}')
                    options.add_argument(f'--disable-web-security')
                    options.add_argument(f'--allow-running-insecure-content')
                    options.add_experimental_option('excludeSwitches', ['enable-automation'])
                self.driver = webdriver.Chrome(chrome_options=options)
            else:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                self.driver = webdriver.Chrome(chrome_options=options)
        except Exception as e:
            print(str(e) + "\n---------\n")
            try:
                self.driver = webdriver.Firefox()
            except Exception as e:
                print(e)
                self.driver = webdriver.PhantomJS()

        self.driver.get(url)

        self.driver.set_page_load_timeout(timeout)
        # self.driver.implicitly_wait(timeout)

    def wait_until_exists(self, xpath, timeout=20):
        """
        wait elements to be exist in an webpage, return those elements

        Parameters
        ----------
        xpath: string 
            you can get it by using F12 at your browser

        timeout: int
            how many seconds you want to wait
        """
        try:
            w = WebDriverWait(self.driver, timeout)
            w.until(presence_of_element_located((By.XPATH, xpath)))
            elements = self.driver.find_elements_by_xpath(xpath)
            return elements
        except TimeoutException as e:
            print(e)
            elements = self.driver.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            print(e)
            return []

    def click(self, element):
        """
        click an element
        """
        self.driver.execute_script("arguments[0].click();", element)
