import unittest 
from selenium import webdriver  
import unittest
import json
from selenium.webdriver.common.by import By
from ..src.database import Database
import time

class BaseTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)

        with open('config-test.json') as config_file:
            self.config = json.load(config_file)
            
        self.host          = self.config["host"]
        self.port          = self.config["port"]
        self.database_path = self.config["database"]

        self.database = Database(database_path=self.database_path, read_sql_file=False)

        self.driver = webdriver.Chrome()

        self.user_email = "user@user.com"
        self.user_pass = "user"

    def access_application(self):
        """ access application """
        self.driver.maximize_window()
        address = "http://"+self.host+":"+str(self.port)
        self.driver.get(address)
        self.assertTrue(len(self.driver.window_handles) == 1)
        self.driver.switch_to.window(self.driver.current_window_handle)

    def click_home(self):
        """ clicks headers home button"""
        self.driver.find_element(By.NAME, "home-button").click()
        time.sleep(0.5)
        self.assertEqual(self.driver.title, "Página Inicial")

    def click_logout(self):
        """ clicks headers logout button"""
        self.driver.find_element(By.NAME, "logout-button").click()
        time.sleep(0.5)
        self.assertEqual(self.driver.title, "Login")

    def login(self, user, password, user_exists=True):
        """ login with given credentials """
        self.assertTrue(self.driver.title == "Login")
        self.driver.find_element(By.NAME, "email").send_keys(user)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "login-button").click()
        time.sleep(0.5)

        if user_exists:
            self.assertEqual(self.driver.title, "Página Inicial")
        else:
            self.assertEqual(self.driver.title, "Login")

    def click_create(self):
        self.driver.find_element(By.ID, "create-btn").click()

