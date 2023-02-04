from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self, url) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
    
    def get_url(self) -> str:
        return self.driver.current_url
    
    def select_value_for_xpath(self, xpath, value) -> None:
        Select(self.driver.find_element(By.XPATH, xpath)).select_by_value(value)
    
    def save_image_from_xpath(self, xpath, path) -> None:
        image = self.driver.find_element(By.XPATH, xpath)
        image = image.screenshot_as_png

        with open(path, 'wb') as f:
            f.write(image)
    
    def input_text_to_xpath(self, xpath, value) -> None:
        self.driver.find_element(By.XPATH, xpath).send_keys(value)
    
    def click_to_xpath(self, xpath) -> None:
        self.driver.find_element(By.XPATH, xpath).click()
    
    def find_element(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def find_elements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)
