from selenium import webdriver  
import unittest
import json
import os
from selenium.webdriver.common.by import By

class AuthTest(unittest.TestCase):

    def test_auth(self):
         # Opening JSON file
        config_file = open('config.json')
        config = json.load(config_file)
        config_file.close()

        xpath_file = open(os.path.realpath(os.path.dirname(__file__)) + '\\xpath.json')
        xpath = json.load(xpath_file)
        xpath_file.close()

        with webdriver.Chrome() as driver:

            driver.switch_to.window(driver.current_window_handle)

            driver.maximize_window()

            address = "http://"+config["host"]+":"+str(config["port"])

            driver.get(address)

            assert len(driver.window_handles) == 1

            self.assertTrue(driver.title == "Login")

            driver.find_element(By.NAME, "register_button")

            self.assertTrue(driver.title == "Registrar-se")

if __name__ == '__main__':
    unittest.main()



