from selenium import webdriver  
import unittest
import json
from selenium.webdriver.common.by import By
from ..src.database import Database

class AuthTest(unittest.TestCase):

    def test_auth(self):
        # Opening JSON file
        with open('config-test.json') as config_file:
            config = json.load(config_file)

        database = Database(database_path=config["database"], read_sql_file=False)

        with webdriver.Chrome() as driver:
            driver.switch_to.window(driver.current_window_handle)
            driver.maximize_window()
            address = "http://"+config["host"]+":"+str(config["port"])
            driver.get(address)
            self.assertTrue(len(driver.window_handles) == 1)
            self.assertTrue(driver.title == "Login")
            driver.find_element(By.NAME, "email").send_keys("user@user.com")
            driver.find_element(By.NAME, "password").send_keys("user")
            driver.find_element(By.NAME, "login-button").click()
            self.assertTrue(driver.title == "Página Inicial")

if __name__ == '__main__':
    unittest.main()



