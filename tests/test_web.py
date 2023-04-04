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
        print(element.get_attribute("aria-label"))