from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebBrowser :
    
    def __init__(self):
        
        chrome_options = Options()
        
        chrome_options.binary_location = "/usr/bin/google-chrome"
        
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")

        # Block images and stylesheets for faster loading
        chrome_prefs = {
            "profile.default_content_setting_values": {
                "images": 2,
                "javascript": 1,
                "stylesheet": 2,
            }
        }
        
        chrome_options.add_experimental_option("prefs", chrome_prefs)

        service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def findElementByTagName(self, value : str):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, value))
        )

    def findElementByCss(self, value : str):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, value))
        )

    def findElementByAttribute(self, balise : str, attribute : str, value : str):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//{balise}[@{attribute}='{value}']"))
        )
    
    def findElementsByClassName(self, class_name : str):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return self.driver.find_elements(By.CLASS_NAME, class_name)

    def waitUntilTitleContains(self) : 
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Dashboard")
        )
        return
    
    def waitUntilAttributeAppears(self, balise : str, attribute : str, value : str, expected_content : str) : 
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_attribute(
                (By.XPATH, f"//{balise}[@{attribute}='{value}']"),
                "content",
                expected_content
            )
        )

    def waitPageIsReady(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )