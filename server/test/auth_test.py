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
            driver.find_element(By.NAME, "register-button").click()
            self.assertTrue(driver.title == "Registrar-se")
            driver.find_element(By.NAME, "email").send_keys("user")
            driver.find_element(By.NAME, "new_password").send_keys("user")
            driver.find_element(By.NAME, "c_password").send_keys("user")
            driver.find_element(By.NAME, "create-button").click()
            self.assertTrue(database.user_exists("user", "user"))
            self.assertTrue(driver.title == "Login")
            driver.find_element(By.NAME, "email").send_keys("user")
            driver.find_element(By.NAME, "password").send_keys("user")
            driver.find_element(By.NAME, "login-button").click()
            self.assertTrue(driver.title == "Página Inicial")



if __name__ == '__main__':
    unittest.main()



