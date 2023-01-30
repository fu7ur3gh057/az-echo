from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver


class SeleniumClient:
    def __init__(self):
        self.driver = webdriver.Remote('http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

    def scroll_down(self):
        pass
