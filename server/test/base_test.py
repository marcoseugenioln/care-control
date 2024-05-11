import unittest 
from selenium import webdriver  
import unittest
import json
from selenium.webdriver.common.by import By
from ..src.database import Database

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

