from .base_test import BaseTest
from selenium.webdriver.common.by import By
import unittest
import time

class AuthTest(BaseTest):

    def test_auth(self):

        user     = "user"
        password = "user"

        self.database.delete_user(self.database.get_user_id(user, password))

        self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.maximize_window()

        address = "http://"+self.host+":"+str(self.port)
        self.driver.get(address)

        self.assertTrue(len(self.driver.window_handles) == 1)
        self.assertTrue(self.driver.title == "Login")

        self.driver.find_element(By.NAME, "register-button").click()
        self.assertTrue(self.driver.title == "Registrar-se")

        self.driver.find_element(By.NAME, "email").send_keys(user)
        self.driver.find_element(By.NAME, "new_password").send_keys(password)
        self.driver.find_element(By.NAME, "c_password").send_keys(password)
        self.driver.find_element(By.NAME, "create-button").click()
        self.assertTrue(self.database.user_exists(user, password))

        self.assertTrue(self.driver.title == "Login")
        self.driver.find_element(By.NAME, "email").send_keys(user)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "login-button").click()
        self.assertTrue(self.driver.title == "Página Inicial")
        self.database.delete_user(self.database.get_user_id(user, password))




if __name__ == '__main__':
    unittest.main()



