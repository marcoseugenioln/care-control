from selenium import webdriver  
import unittest
import json
from selenium.webdriver.common.by import By
from ..src.database import Database

class HomeTest(unittest.TestCase):

    def test_home(self):
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
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "event-button").click()
            self.assertEqual(driver.title, "Eventos")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "alarm-button").click()
            self.assertEqual(driver.title, "Alarmes")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "caregiver-button").click()
            self.assertEqual(driver.title, "Cuidadores")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "patient-button").click()
            self.assertEqual(driver.title, "Paciente")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "user-button").click()
            self.assertEqual(driver.title, "Usuário")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "historic-button").click()
            self.assertEqual(driver.title, "Historico")
            driver.find_element(By.NAME, "home-button").click()
            self.assertEqual(driver.title, "Página Inicial")

            driver.find_element(By.NAME, "logout-button").click()
            self.assertEqual(driver.title, "Login")

if __name__ == '__main__':
    unittest.main()



