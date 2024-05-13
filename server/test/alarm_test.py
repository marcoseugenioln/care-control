import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest

import time

class AlarmTest(BaseTest):

    def test_alarm(self):
        """ test patient user mode """
        self.access_application()
        self.login(self.user_email, self.user_pass)

        self.driver.find_element(By.NAME, "alarm-button").click()
        self.assertEqual(self.driver.title, "Alarmes")

        """ create patient """
        self.driver.find_element(By.NAME, "event_id").click()
        self.driver.find_element(By.NAME, "event_id").send_keys(Keys.ENTER)
        self.driver.find_element(By.NAME, "alarm_time").click()
        self.driver.find_element(By.NAME, "alarm_time").send_keys("0630")
        self.click_create()

        alarms=self.database.get_alarms(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(alarms) == 1)
        self.assertEqual(alarms[0][3], '06:30:00')

        alarm_id = alarms[0][0]
        event_id = alarms[0][2]
        self.driver.find_element(By.NAME, "alarm-" + str(alarm_id))
        
        """ update alarm """
        self.driver.find_element(By.ID, "event-id-" + str(alarm_id)).click()
        self.driver.find_element(By.ID, "event-id-" + str(alarm_id)).send_keys(Keys.DOWN)
        self.driver.find_element(By.ID, "event-id-" + str(alarm_id)).send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "alarm-time-" + str(alarm_id)).click()
        self.driver.find_element(By.ID, "alarm-time-" + str(alarm_id)).send_keys("1000")

        self.driver.find_element(By.NAME, "update-alarm-" + str(alarm_id)).click()

        alarms=self.database.get_alarms(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(alarms) == 1)
        self.assertEqual(alarms[0][3], '10:00:00')
        self.assertIsNot(event_id, alarms[0][2])

        """ delete patient """
        self.driver.find_element(By.NAME, "delete-alarm-" + str(alarm_id)).click()
        try:
            self.driver.find_element(By.NAME, "alarm-" + str(alarm_id))
            self.fail("alarm not removed")
        except:
            pass
        self.assertFalse(self.database.has_patient(self.database.get_user_id(self.user_email, self.user_pass)))
        alarms=self.database.get_alarms(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(alarms) == 0)

if __name__ == '__main__':
    unittest.main()

