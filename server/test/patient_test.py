import unittest
from selenium.webdriver.common.by import By
from .base_test import BaseTest
import time

class PatientTest(BaseTest):

    def test_patient(self):
        """ test patient user mode """
        self.access_application()
        self.login(self.user_email, self.user_pass)
        self.driver.find_element(By.NAME, "patient-button").click()
        self.assertEqual(self.driver.title, "Paciente")

        """ create patient """
        self.driver.find_element(By.NAME, "patient_name").send_keys("test")
        self.driver.find_element(By.NAME, "birth_date").send_keys("01042000")
        self.click_create()
        self.assertTrue(self.database.has_patient(self.database.get_user_id(self.user_email, self.user_pass)))
        patient_id = self.database.get_patient_id_from_user_id(self.database.get_user_id(self.user_email, self.user_pass))
        self.assertTrue(self.driver.find_element(By.NAME, "patient-" + str(patient_id)))

        """ update patient """
        self.driver.find_element(By.NAME, "patient_name").clear()
        self.driver.find_element(By.NAME, "birth_date").clear()
        self.driver.find_element(By.NAME, "patient_name").send_keys("TEST")
        self.driver.find_element(By.NAME, "birth_date").send_keys("02052020")
        self.driver.find_element(By.NAME, "update-patient-" + str(patient_id)).click()
        self.assertEqual(self.driver.find_element(By.NAME, "patient_name").get_attribute('value'), "TEST")
        self.assertEqual(self.driver.find_element(By.NAME, "birth_date").get_attribute('value'), "2020-05-02")

        """ delete patient """
        self.driver.find_element(By.NAME, "delete-patient-" + str(patient_id)).click()
        try:
            self.driver.find_element(By.NAME, "patient-" + str(patient_id))
            self.fail("user not removed")
        except:
            pass
        self.assertFalse(self.database.has_patient(self.database.get_user_id(self.user_email, self.user_pass)))

if __name__ == '__main__':
    unittest.main()

