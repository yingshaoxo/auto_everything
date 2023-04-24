from time import sleep
from auto_everything.web import Selenium 

def test_selenium_1():
    selenium = Selenium()
    selenium.go_to(url="https://www.bing.com")
    selenium.sleep(3)
    element = selenium.find_element(by=selenium.By.ID, value="sb_form_q")
    if element != None:
        element.send_keys("yingshaoxo" + selenium.Keys.ENTER) #type: ignore
    selenium.sleep(10)

def test_selenium_2():
    selenium = Selenium()
    selenium.go_to(url="https://www.bing.com")
    elements = selenium.wait_until_elements_exists(xpath='//*[@id="sb_form_q"]', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        element.send_keys("yingshaoxo" + selenium.Keys.ENTER) #type: ignore
    selenium.sleep(10)

def test_selenium_3():
    selenium = Selenium()
    selenium.go_to(url="https://www.bing.com")
    selenium.go_to(url="https://baidu.com")
    selenium.sleep(3)
    selenium.go_back()
    selenium.sleep(10)

def test_selenium_4():
    selenium = Selenium()
    selenium.go_to(url="https://baidu.com")
    elements = selenium.wait_until_elements_exists(xpath='//*[@id="kw"]', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        element.send_keys("yingshaoxo") #type: ignore
        selenium.click(element=element)
    selenium.sleep(10)

def test_selenium_5():
    selenium = Selenium(use_firefox=True)
    selenium.go_to(url="https://www.bing.com")
    elements = selenium.wait_until_elements_exists(xpath='//*[@id="sb_form_q"]', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        element.send_keys("yingshaoxo" + selenium.Keys.ENTER) #type: ignore
    selenium.sleep(10)

def test_selenium_6():
    selenium = Selenium(headless=True)
    selenium.go_to(url="https://www.google.com")
    elements = selenium.wait_until_elements_exists(xpath=r'(//input)[2]', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        print()
        print(element.get_attribute("aria-label")) #type: ignore

def test_selenium_7():
    selenium = Selenium()
    selenium.go_to(url="https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy")
    elements = selenium.wait_until_elements_exists(xpath=r'//body', timeout_in_seconds=20)
    for i in range(10):
        selenium.scroll(relative_y=100)
        sleep(0.5)
    selenium.scroll(y=10000)
    sleep(10)

def test_selenium_8():
    selenium = Selenium()
    selenium.go_to(url="https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy")
    elements = selenium.wait_until_elements_exists(xpath=r'//*[@id="sidebar-quicklinks"]', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        for i in range(10):
            selenium.scroll(element=element, relative_y=100)
            sleep(0.5)
        selenium.scroll(element=element, y=10000)
    sleep(10)

def test_selenium_9():
    selenium = Selenium()
    selenium.go_to(url="https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy")
    elements = selenium.wait_until_elements_exists(xpath=r'//html', timeout_in_seconds=20)
    if len(elements) > 0:
        element = elements[0]
        for i in range(10):
            selenium.scroll(element=element, relative_y=100)
            sleep(0.5)
        selenium.scroll(element=element, y=10000)
    sleep(10)