from selenium import webdriver
from selenium.webdriver.support.expected_conditions import presence_of_element_located #type: ignore
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class Selenium():
    """
    It's a wrap of selenium
    """

    def __init__(self, url: str | None = None, headless: bool = False, timeout: int = 600, user_data_dir: str | None = None, use_firefox: bool = False):
        '''
        user_data_dir:
        /home/yingshaoxo/.config/google-chrome/
        '''
        self.driver: webdriver.Chrome | webdriver.Firefox | None = None
        self.By = By
        self.Keys = Keys

        try:
            if (use_firefox == True):
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                options = webdriver.FirefoxOptions()
                if (headless == True):
                    options.add_argument("-headless") #type: ignore
                    options.add_argument("-width=1920") #type: ignore
                    options.add_argument("-height=1080") #type: ignore
                if (user_data_dir != None):
                    options.add_argument("-profile") #type: ignore
                    options.add_argument(user_data_dir) #type: ignore
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            else:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from webdriver_manager.chrome import ChromeDriverManager
                options = webdriver.ChromeOptions()
                if (headless == True):
                    options.add_argument("--headless") #type: ignore
                    options.add_argument('--disable-gpu') #type: ignore
                    # options.add_argument('--start-maximized') #type: ignore
                    options.add_argument("--window-size=1920,1080") #type: ignore
                options.add_argument(f"--no-sandbox") #type: ignore
                options.add_argument(f"--disable-dev-shm-usage") #type: ignore
                if (user_data_dir != None):
                    options.add_argument(f'--disable-web-security') #type: ignore
                    options.add_argument(f'--allow-running-insecure-content') #type: ignore
                    options.add_argument(f'--user-data-dir={user_data_dir}') #type: ignore
                    # options.add_argument(f'--profile-directory="Profile 1"')
                    options.add_experimental_option('excludeSwitches', ['enable-automation']) #type: ignore
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except Exception as e:
            print(str(e) + "\n---------\n")
            self.driver = webdriver.PhantomJS() #type: ignore

        if (self.driver == None):
            raise Exception("self.driver is None, can't work because of it")
        
        if (url != None):
            self.driver.get(url) #type: ignore

        self.driver.set_page_load_timeout(timeout) #type: ignore
    
    def sleep(self, seconds: float | int):
        sleep(seconds)
    
    def go_to(self, url: str):
        self.driver.get(url) #type: ignore

    def go_back(self):
        self.driver.back() #type: ignore
    
    def find_elements(self, by: str = By.ID, value: str | None = None) -> list[WebElement]:
        """
        elements = find_elements(Selenium().By.CLASS_NAME, 'foo')
        """
        return self.driver.find_elements(by=by, value=value) #type: ignore

    def find_element(self, by: str = By.ID, value: str | None = None) -> WebElement | None:
        """
        element_or_none = find_element(Selenium().By.TAG_NAME, 'input')
        """
        element_: WebElement | None = None
        try:
            element_ = self.driver.find_element(by=by, value=value) #type: ignore
        except Exception as e:
            print(f"error: {e}")
            element_ = None
        return element_
    
    def wait_until_elements_exists(self, xpath: str, timeout_in_seconds: int = 20) -> list[WebElement]:
        """
        wait elements to be exist in an webpage, then return those elements as a list

        Parameters
        ----------
        xpath: string 
            you can get it by using F12 at your browser

        timeout_in_seconds: int
            how many seconds you want to wait
        """
        return self.wait_until_exists(xpath=xpath, timeout=timeout_in_seconds)
    
    def wait_until_exists(self, xpath: str, timeout: int = 20) -> list[WebElement]:
        try:
            w = WebDriverWait(self.driver, timeout)
            w.until(presence_of_element_located((By.XPATH, xpath))) #type: ignore
            elements = self.driver.find_elements(by=By.XPATH, value=xpath)  #type: ignore
            return elements
        except TimeoutException as e:
            print(e)
            elements = self.driver.find_elements(by=By.XPATH, value=xpath)  #type: ignore
            return elements
        except Exception as e:
            print(e)
            return []

    def click(self, element: WebElement):
        """
        click an element
        """
        self.driver.execute_script("arguments[0].click();", element) #type: ignore
