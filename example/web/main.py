from auto_everything.web import Selenium, WebElement
from auto_everything.disk import Disk
from auto_everything.network import Network
from auto_everything.terminal import Terminal
from auto_everything.io import IO

selenium = Selenium()
disk = Disk()
network = Network()
terminal = Terminal()
io_ = IO()

selenium.go_to(url="https://chilloutai.com/nsfw")

elements = selenium.wait_until_elements_exists(xpath='//img')

def get_close_element() -> WebElement | None:
    result = None
    elements = selenium.wait_until_elements_exists(xpath='//span')
    for element in elements:
        if element.get_attribute('class') == "ant-modal-close-x": #type: ignore
            result = element
    return result

def get_information_I_need() -> str:
    text: str = ""
    elements = selenium.wait_until_elements_exists(xpath='//div[contains(@class, "ant-modal-body")]//div[contains(@class, "mt-4")]')
    for element in elements:
        if "提示词" in element.text:
            text += "\n\n" + element.text
            break
    return text.strip()

def download_picture(url: str):
    file_name = url.split("/")[-1]
    network.download(url, f'./data/{file_name}', )

for index, element in enumerate(elements):
    if index == 0:
        continue

    selenium.click(element)
    selenium.sleep(3)
    url = element.get_attribute('src') #type: ignore
    download_picture(url)
    file_name = url.split("/")[-1]
    pure_name, _ = disk.get_stem_and_suffix_of_a_file(file_name)
    info = get_information_I_need()
    io_.write("./data/"+pure_name+".txt", info)

    close_icon = get_close_element()
    if close_icon != None:
        selenium.click(close_icon)

    selenium.sleep(3)