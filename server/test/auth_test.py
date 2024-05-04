from selenium import webdriver  
from selenium.webdriver.edge.service import Service as EdgeService  
import unittest
import json

class AuthTest(unittest.TestCase):

    def test_auth(self):
         # Opening JSON file
        config_file = open('config.json')
        config = json.load(config_file)
        config_file.close()

        with webdriver.Edge() as driver:
            address = "http://"+config["host"]+":"+str(config["port"])
            print(address)
            driver.get(address)
            print(driver.title)
            self.assertTrue(driver.title == "Login")

if __name__ == '__main__':
    unittest.main()



