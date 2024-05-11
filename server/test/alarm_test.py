import unittest
from selenium.webdriver.common.by import By
from .base_test import BaseTest

class AlarmTest(BaseTest):

    def test_alarm(self):

        self.access_application()
        self.login("user@user.com", "user")

        self.driver.find_element(By.NAME, "alarm-button").click()
        self.assertEqual(self.driver.title, "Alarmes")

if __name__ == '__main__':
    unittest.main()



