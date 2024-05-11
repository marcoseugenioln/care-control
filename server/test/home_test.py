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
        address = "http://"+self.host+":"+str(self.port)
        self.driver.get(address)
        self.assertTrue(len(self.driver.window_handles) == 1)

        self.assertTrue(self.driver.title == "Login")
        self.driver.find_element(By.NAME, "email").send_keys("user@user.com")
        self.driver.find_element(By.NAME, "password").send_keys("user")
        self.driver.find_element(By.NAME, "login-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "event-button").click()
        self.assertEqual(self.driver.title, "Eventos")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "alarm-button").click()
        self.assertEqual(self.driver.title, "Alarmes")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "caregiver-button").click()
        self.assertEqual(self.driver.title, "Cuidadores")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "patient-button").click()
        self.assertEqual(self.driver.title, "Paciente")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "user-button").click()
        self.assertEqual(self.driver.title, "Usuário")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "historic-button").click()
        self.assertEqual(self.driver.title, "Historico")
        self.driver.find_element(By.NAME, "home-button").click()
        self.assertEqual(self.driver.title, "Página Inicial")

        self.driver.find_element(By.NAME, "logout-button").click()
        self.assertEqual(self.driver.title, "Login")

if __name__ == '__main__':
    unittest.main()



