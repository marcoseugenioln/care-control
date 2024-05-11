from selenium import webdriver  
import unittest
import json
from selenium.webdriver.common.by import By
from ..src.database import Database
from .base_test import BaseTest

class HomeTest(BaseTest):

    def test_home(self):

        self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.maximize_window()

        self.access_application()
        self.login("user@user.com", "user")

        self.driver.find_element(By.NAME, "event-button").click()
        self.assertEqual(self.driver.title, "Eventos")
        self.click_home()

        self.driver.find_element(By.NAME, "alarm-button").click()
        self.assertEqual(self.driver.title, "Alarmes")
        self.click_home()

        self.driver.find_element(By.NAME, "caregiver-button").click()
        self.assertEqual(self.driver.title, "Cuidadores")
        self.click_home()

        self.driver.find_element(By.NAME, "patient-button").click()
        self.assertEqual(self.driver.title, "Paciente")
        self.click_home()

        self.driver.find_element(By.NAME, "user-button").click()
        self.assertEqual(self.driver.title, "Usuário")
        self.click_home()

        self.driver.find_element(By.NAME, "historic-button").click()
        self.assertEqual(self.driver.title, "Historico")
        self.click_home()

        self.click_logout()

if __name__ == '__main__':
    unittest.main()



