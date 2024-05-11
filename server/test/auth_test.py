from .base_test import BaseTest
from selenium.webdriver.common.by import By
import unittest
import time

class AuthTest(BaseTest):

    def test_auth(self):
        ''' register account and login '''

        user     = "user"
        password = "user"

        self.database.delete_user(self.database.get_user_id(user, password))

        self.access_application()

        self.assertTrue(self.driver.title == "Login")
        self.driver.find_element(By.NAME, "register-button").click()
        self.assertTrue(self.driver.title == "Registrar-se")

        self.driver.find_element(By.NAME, "email").send_keys(user)
        self.driver.find_element(By.NAME, "new_password").send_keys(password)
        self.driver.find_element(By.NAME, "c_password").send_keys(password)
        self.driver.find_element(By.NAME, "create-button").click()

        self.assertTrue(self.database.user_exists(user, password))

        self.login(user=user, password=password)

        self.click_logout()

        self.database.delete_user(self.database.get_user_id(user, password))

        ''' login with unexisting account'''
        user     = "user"
        password = "user"
        self.database.delete_user(self.database.get_user_id(user, password))
        self.access_application()
        self.login(user=user, password=password, user_exists=False)

if __name__ == '__main__':
    unittest.main()



