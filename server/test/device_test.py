import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest
import time

class DeviceTest(BaseTest):

    def test_device(self):
        """ test device user mode """
        self.access_application()
        self.login(self.user_email, self.user_pass)
        self.driver.find_element(By.NAME, "device-button").click()
        self.assertEqual(self.driver.title, "Dispositivos")

        """ create device """
        self.driver.find_element(By.NAME, "name").send_keys("test")
        self.click_create()
        devices=self.database.get_device(False, self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(devices) == 1)

        device_id = devices[0][0]
        name = devices[0][2]
        button_1 = devices[0][3]
        button_2 = devices[0][4]
        button_3 = devices[0][5]

        self.assertTrue(self.driver.find_element(By.NAME, "device-" + str(device_id)))

        """ update device """
        self.driver.find_element(By.NAME, "name").clear()
        self.driver.find_element(By.NAME, "name").send_keys("TEST")

        self.driver.find_element(By.ID, "button-1-" + str(device_id)).click()
        self.driver.find_element(By.ID, "button-1-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-1-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-1-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-1-" + str(device_id)).send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "button-2-" + str(device_id)).click()
        self.driver.find_element(By.ID, "button-2-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-2-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-2-" + str(device_id)).send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "button-3-" + str(device_id)).click()
        self.driver.find_element(By.ID, "button-3-" + str(device_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "button-3-" + str(device_id)).send_keys(Keys.ENTER)

        self.driver.find_element(By.NAME, "update-device-" + str(device_id)).click()

        devices=self.database.get_device(False, self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(devices) == 1)

        name = devices[0][2]
        new_button_1 = devices[0][3]
        new_button_2 = devices[0][4]
        new_button_3 = devices[0][5]

        self.assertEqual(name, 'TEST')
        self.assertIsNot(new_button_1, button_1)
        self.assertIsNot(new_button_2, button_2)
        self.assertIsNot(new_button_3, button_3)

        """ delete device """
        self.driver.find_element(By.NAME, "delete-device-" + str(device_id)).click()
        try:
            self.driver.find_element(By.NAME, "device-" + str(device_id))
            self.fail("user not removed")
        except:
            pass

        devices=self.database.get_device(False, self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(devices) == 0)

if __name__ == '__main__':
    unittest.main()

