import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest

import time

class CaregiverTest(BaseTest):

    def test_caregiver(self):
        """ test patient user mode """
        self.access_application()
        self.login(self.user_email, self.user_pass)

        self.driver.find_element(By.NAME, "caregiver-button").click()
        self.assertEqual(self.driver.title, "Cuidadores")

        """ create caregiver """
        self.driver.find_element(By.NAME, "name").click()
        self.driver.find_element(By.NAME, "name").send_keys('test')
        self.driver.find_element(By.NAME, "start_shift").click()
        self.driver.find_element(By.NAME, "start_shift").send_keys("0600")
        self.driver.find_element(By.NAME, "end_shift").click()
        self.driver.find_element(By.NAME, "end_shift").send_keys("1800")
        self.click_create()

        caregivers=self.database.get_caregivers(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(caregivers) == 1)
        
        caregiver_id = caregivers[0][0]
        name = caregivers[0][2]
        start_shift = caregivers[0][3]
        end_shift = caregivers[0][4]

        self.assertEqual(name, 'test')
        self.assertEqual(start_shift, '06:00:00')
        self.assertEqual(end_shift, '18:00:00')

        self.driver.find_element(By.NAME, "caregiver-" + str(caregiver_id))
        
        """ update caregiver """
        self.driver.find_element(By.ID, "name-" + str(caregiver_id)).click()
        self.driver.find_element(By.ID, "name-" + str(caregiver_id)).clear()
        self.driver.find_element(By.ID, "name-" + str(caregiver_id)).send_keys('TEST')

        self.driver.find_element(By.ID, "start-shift-" + str(caregiver_id)).click()
        self.driver.find_element(By.ID, "start-shift-" + str(caregiver_id)).send_keys("0700")
        self.driver.find_element(By.ID, "end-shift-" + str(caregiver_id)).click()
        self.driver.find_element(By.ID, "end-shift-" + str(caregiver_id)).send_keys("1900")

        self.driver.find_element(By.NAME, "update-caregiver-" + str(caregiver_id)).click()

        caregivers=self.database.get_caregivers(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(caregivers) == 1)
        name = caregivers[0][2]
        start_shift = caregivers[0][3]
        end_shift = caregivers[0][4]

        self.assertEqual(name, 'TEST')
        self.assertEqual(start_shift, '07:00:00')
        self.assertEqual(end_shift, '19:00:00')

        """ delete caregiver """
        self.driver.find_element(By.NAME, "delete-caregiver-" + str(caregiver_id)).click()
        try:
            self.driver.find_element(By.NAME, "caregiver-" + str(caregiver_id))
            self.fail("alarm not removed")
        except:
            pass
        self.assertFalse(self.database.has_patient(self.database.get_user_id(self.user_email, self.user_pass)))
        caregivers=self.database.get_caregivers(is_admin=False, user_id=self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(len(caregivers) == 0)

if __name__ == '__main__':
    unittest.main()

