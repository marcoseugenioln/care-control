import sqlite3
import logging
import os

logger = logging.getLogger('werkzeug')

class Database():

    def __init__(self, 
                 database_path="schema.db", 
                 schema_file="schema.sql",
                 read_sql_file=True):

        logger.info('starting database connection')
        self.connection = sqlite3.connect(database_path, check_same_thread=False, timeout=10)
        self.query = self.connection.cursor()
        logger.info('Database connected.')

        if read_sql_file:
            with open(schema_file, 'r') as sql_file:
                sql_script = sql_file.read()

            self.query.executescript(sql_script)
            self.connection.commit()

    def user_exists(self, email: str, password: str) -> bool:

        self.query.execute(f"SELECT * FROM user WHERE email == '{email}' AND password == '{password}'")
        logger.info(f"SELECT * FROM user WHERE email == '{email}' AND password == '{password}'")

        account = self.query.fetchone()

        if not account:
            return False
        
        return True
    
    def get_user_id(self, email: str, password: str):
        logger.info(f"SELECT id FROM user WHERE email == '{email}' AND password == '{password}';")
        self.query.execute(f"SELECT id FROM user WHERE email == '{email}' AND password == '{password}';")
        user_id = self.query.fetchone()
        if user_id:   
            return user_id[0]
        else:
            return str(0)

    def get_admin(self, user_id):
        logger.info(f"SELECT is_admin FROM user WHERE id == {user_id};")
        self.query.execute(f"SELECT is_admin FROM user WHERE id == {user_id};")
        is_admin = self.query.fetchone()

        if int(is_admin[0]) == 0:
            return False
        
        return True
    
    def insert_user(self, email: str, password: str, is_admin: str) -> bool:
        self.query.execute(f"INSERT OR IGNORE INTO user(email, password, is_admin) values ('{email}', '{password}', {is_admin});")
        logger.info(f"INSERT OR IGNORE INTO user(email, password, is_admin) values ('{email}', '{password}', {is_admin});")
        self.connection.commit()
        return True

    def get_user_email(self, user_id: int) -> str:
        self.query.execute(f"SELECT email FROM user WHERE id == {user_id}")
        logger.info(f"SELECT email FROM user WHERE id == {user_id}")
        email = self.query.fetchone()
        if email:
            return email[0]
        else:
            return ""

    def get_user_password(self, user_id: int) -> str:
        self.query.execute(f"SELECT password FROM user WHERE id == {user_id}")
        logger.info(f"SELECT password FROM user WHERE id == {user_id}")
        password = self.query.fetchone()
        if password:
            return password[0]
        else:
            return ""
    
    def get_users(self):
        self.query.execute(f"SELECT id, email, password FROM user")
        logger.info(f"SELECT id, email, password FROM user")
        users = self.query.fetchall()        
        return users
    
    def alter_password(self, user_id, password):
        self.query.execute(f"UPDATE user SET password = '{password}' WHERE id == {user_id}")
        logger.info(f"UPDATE user SET password = '{password}' WHERE id == {user_id}")
        self.connection.commit()

    def alter_email(self, user_id, email):
        self.query.execute(f"UPDATE user SET email = '{email}' WHERE id == {user_id}")
        logger.info(f"UPDATE user SET email = '{email}' WHERE id == {user_id}")
        self.connection.commit()

    def delete_user(self, id):
        self.query.execute(f"DELETE FROM user WHERE id == {id};")
        logger.info(f"DELETE FROM user WHERE id == {id};")
        self.connection.commit()

    def update_user(self, user_id, email, password, is_admin):
        logger.info(f"UPDATE user SET email = '{email}', password = '{password}', is_admin = {is_admin} WHERE id == {user_id};")
        self.query.execute(f"UPDATE user SET email = '{email}', password = '{password}', is_admin = {is_admin} WHERE id == {user_id};")
        self.connection.commit()

    ##################################################################################################
    def get_device(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute(f"SELECT id, patient_id, name, event_button_1, event_button_2, event_button_3 FROM device;")
            logger.info(f"SELECT id, patient_id, name, event_button_1, event_button_2, event_button_3 FROM device;")
            return self.query.fetchall()
        else:
            patient_id = self.get_patient_id_from_user_id(user_id)

            self.query.execute(f"SELECT id, patient_id, name, event_button_1, event_button_2, event_button_3 FROM device WHERE patient_id = {patient_id};")
            logger.info(f"SELECT id, patient_id, name, event_button_1, event_button_2, event_button_3 FROM device WHERE patient_id = {patient_id};")
            return self.query.fetchall()
        
    def insert_device(self, patient_id, name) -> bool:
        self.query.execute(f"INSERT OR IGNORE INTO device(patient_id, name) values ({patient_id}, '{name}');")
        logger.info(f"INSERT OR IGNORE INTO device(patient_id, name) values ({patient_id}, '{name}');")
        self.connection.commit()
        return True

    def delete_device(self, id):
        self.query.execute(f"DELETE FROM device WHERE id = {id};")
        logger.info(f"DELETE FROM device WHERE id = {id};")
        self.connection.commit()

    def update_device(self, id, patient_id, name, event_button_1, event_button_2, event_button_3):

        self.query.execute(f"UPDATE device SET patient_id = {patient_id}, name = '{name}', event_button_1 = {event_button_1}, event_button_2 = {event_button_2}, event_button_3 = {event_button_3} WHERE id = {id};")
        logger.info(f"UPDATE device SET patient_id = {patient_id}, name = '{name}', event_button_1 = {event_button_1}, event_button_2 = {event_button_2}, event_button_3 = {event_button_3} WHERE id = {id};")
        self.connection.commit()

    def has_device(self, user_id):

        patient_id = self.get_patient_id_from_user_id(user_id)

        self.query.execute(f"SELECT id, name, event_button_1, event_button_2, event_button_3 FROM device WHERE patient_id = {patient_id};")
        logger.info(f"SELECT id, name, event_button_1, event_button_2, event_button_3 FROM device device patient_id = {patient_id};")

        if self.query.fetchone():
            return True
        else:
            return False
        
    def get_button_event_id(self, device_id, button_id):
        if button_id == 1:
            self.query.execute(f"SELECT event_button_1 FROM device WHERE id = {device_id};")
            logger.info(f"SELECT event_button_1 FROM device WHERE id = {device_id};")
        elif button_id == 2:
            self.query.execute(f"SELECT event_button_2 FROM device WHERE id = {device_id};")
            logger.info(f"SELECT event_button_2 FROM device WHERE id = {device_id};")
        elif button_id == 3:
            self.query.execute(f"SELECT event_button_3 FROM device WHERE id = {device_id};")
            logger.info(f"SELECT event_button_3 FROM device WHERE id = {device_id};")
        else:
            return str(0)
        
        event_id = self.query.fetchone()
        if event_id:
            return event_id[0]
        else:
            return str(0)
        
    def get_alarm_event_id(self, alarm_id):
        self.query.execute(f"SELECT event_id FROM alarm WHERE id = {alarm_id};")
        logger.info(f"SELECT event_id FROM alarm WHERE id = {alarm_id};")
        event_id = self.query.fetchone()
        if event_id:
            return event_id[0]
        else:
            return str(0)

    def get_patient_by_device_id(self, device_id):
        self.query.execute(f"SELECT patient_id FROM device WHERE id = {device_id};")
        logger.info(f"SELECT patient_id FROM device WHERE id = {device_id};")
        patient_id = self.query.fetchone()
        if patient_id:
            return patient_id[0]
        else:
            return str(0)

    ##################################################################################################

    def get_patient(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute("SELECT id, name, birth FROM patient;")
            logger.info("SELECT id, name, birth FROM patient;")
            return self.query.fetchall()
        else:
            self.query.execute(f"SELECT id, name, birth FROM patient WHERE user_id = {user_id};")
            logger.info(f"SELECT id, name, birth FROM patient WHERE user_id = {user_id};")
            return self.query.fetchall()
    
    def get_patient_name(self, patient_id):
        logger.info(f"SELECT name FROM patient WHERE id = {patient_id};")
        self.query.execute(f"SELECT name FROM patient WHERE id = {patient_id};")
        patient_name = self.query.fetchone()
        if patient_name:
            return patient_name[0]
        else:
            return str()
    
    def has_patient(self, user_id : int) -> bool:
        self.query.execute(f"SELECT id, name, birth FROM patient WHERE user_id = {user_id};")
        logger.info(f"SELECT id, name, birth FROM patient WHERE user_id = {user_id};")

        if self.query.fetchone():
            return True
        else:
            return False

    def insert_patient(self, patient_name: str, birth_date: str, user_id: int) -> bool:
        self.query.execute(f"INSERT OR IGNORE INTO patient(user_id, name, birth) values ({user_id}, '{patient_name}', DATE('{birth_date}'));")
        logger.info(f"INSERT OR IGNORE INTO patient(user_id, name, birth) values ({user_id}, '{patient_name}', DATE('{birth_date}'));")
        self.connection.commit()

        return True

    def delete_patient(self, id):
        self.query.execute("DELETE FROM patient WHERE id = ?;", ((id,)))
        logger.info(f"DELETE FROM patient WHERE id = {id};")
        self.connection.commit()

    def update_patient(self, id, patient_name, birth_date):
        self.query.execute(f"UPDATE patient SET name = '{patient_name}', birth = DATE('{birth_date}') WHERE id = {id};")
        logger.info(f"UPDATE patient SET name = '{patient_name}', birth = DATE('{birth_date}') WHERE id = {id};")
        self.connection.commit()

    ##################################################################################################
        
    def get_historic(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute(f"SELECT id, patient_id, event_id, log_datetime, log_type FROM historic;")
            logger.info(f"SELECT id, patient_id, event_id, log_datetime, log_type FROM historic;")
            return self.query.fetchall()
        else:
            patient_id = self.get_patient_id_from_user_id(user_id)

            self.query.execute(f"SELECT id, patient_id, event_id, log_datetime, log_type FROM historic WHERE patient_id = {patient_id};")
            logger.info(f"SELECT id, patient_id, event_id, log_datetime, log_type FROM historic WHERE patient_id = {patient_id};")
            return self.query.fetchall()
    
    def delete_historic(self, patient_id):
        self.query.execute("DELETE FROM historic WHERE patient_id = ?;", ((patient_id,)))
        logger.info(f"DELETE FROM historic WHERE patient_id = {patient_id};")
        self.connection.commit()

    def delete_all_historic(self):
        self.query.execute(f"DELETE FROM historic;")
        logger.info(f"DELETE FROM historic;")
        self.connection.commit()

    def log_message(self, patient_id, event_id, log_type):
        logger.info(f"INSERT INTO historic(patient_id, event_id, log_datetime, log_type) values ({patient_id}, {event_id}, DATETIME('now', 'localtime'), {log_type});")
        self.query.execute(f"INSERT INTO historic(patient_id, event_id, log_datetime, log_type) values ({patient_id}, {event_id}, DATETIME('now', 'localtime'), {log_type});")
        self.connection.commit()

        return True

    ##################################################################################################

    def get_events(self):
        self.query.execute("SELECT id, description, is_input FROM event;")
        logger.info("SELECT id, description, is_input FROM event;")
        return self.query.fetchall()
    
    def get_event_description(self, event_id):
        logger.info(f"SELECT description FROM event WHERE id = {event_id};")
        self.query.execute(f"SELECT description FROM event WHERE id = {event_id};")

        description = self.query.fetchone()
        if description:
            return description[0]
        else:
            return str()
    
    def insert_event(self, event_description, is_input_event):
        self.query.execute(f"INSERT OR IGNORE INTO event(description, is_input) values ('{event_description}', {is_input_event});")
        logger.info(f"INSERT OR IGNORE INTO event(description, is_input) values ('{event_description}', {is_input_event});")
        self.connection.commit()
        return True
    
    def delete_event(self, id):
        self.query.execute(f"DELETE FROM event WHERE id == {id};")
        logger.info(f"DELETE FROM event WHERE id == {id};")
        self.connection.commit()

    def update_event(self, id, event_description, is_input_event):
        self.query.execute(f"UPDATE event SET description = '{event_description}', is_input = {is_input_event} WHERE id = {id};")
        logger.info(f"UPDATE event SET description = '{event_description}', is_input = {is_input_event} WHERE id = {id};")
        self.connection.commit()

    ##################################################################################################
    def get_caregivers(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute("SELECT id, patient_id, name, start_shift, end_shift FROM caregiver;")
            logger.info(f"SELECT id, patient_id, name, start_shift, end_shift FROM caregiver;")
            return self.query.fetchall()
        else:
            patient_id = self.get_patient_id_from_user_id(user_id)

            self.query.execute(f"SELECT id, patient_id, name, start_shift, end_shift FROM caregiver WHERE patient_id = {patient_id};")
            logger.info(f"SELECT id, patient_id, name, start_shift, end_shift FROM caregiver WHERE patient_id = {patient_id};")
            return self.query.fetchall()
        
    def get_patient_id_from_user_id(self, user_id):
        self.query.execute(f"SELECT id FROM patient WHERE user_id = {user_id};")
        logger.info(f"SELECT id FROM patient WHERE user_id = {user_id};")

        patient_id = self.query.fetchone()
        if patient_id:
            return patient_id[0]
        else:
            return str(0)
        
    def insert_caregiver(self, patient_id, name, start_shift, end_shift) -> bool:
        self.query.execute(f"INSERT OR IGNORE INTO caregiver(patient_id, name, start_shift, end_shift) values ({patient_id}, '{name}', TIME('{start_shift}'), TIME('{end_shift}'));")
        logger.info(f"INSERT OR IGNORE INTO caregiver(patient_id, name, start_shift, end_shift) values ({patient_id}, '{name}', TIME('{start_shift}'), TIME('{end_shift}'));")
        self.connection.commit()
        return True

    def delete_caregiver(self, id):
        self.query.execute(f"DELETE FROM caregiver WHERE id = {id};")
        logger.info(f"DELETE FROM caregiver WHERE id = {id};")
        self.connection.commit()

    def update_caregiver(self, id, patient_id, name, start_shift, end_shift):
        self.query.execute(f"UPDATE caregiver SET patient_id = {patient_id}, name = '{name}', start_shift = TIME('{start_shift}'), end_shift = TIME('{end_shift}') WHERE id = {id};")
        logger.info(f"UPDATE caregiver SET patient_id = {patient_id}, name = '{name}', start_shift = TIME('{start_shift}'), end_shift = TIME('{end_shift}') WHERE id = {id};")
        self.connection.commit()

    ##################################################################################################

    def get_alarms(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute("SELECT id, patient_id, event_id, alarm_time FROM alarm;")
            logger.info(f"SELECT id, user_id, nome, guid FROM alarm;")
            return self.query.fetchall()
        else:
            patient_id = self.get_patient_id_from_user_id(user_id)

            self.query.execute(f"SELECT id, patient_id, event_id, alarm_time from alarm WHERE patient_id ={patient_id};")
            logger.info(f"SELECT id, patient_id, event_id, alarm_time from alarm WHERE patient_id ={patient_id};")
            return self.query.fetchall()

    def insert_alarm(self, patient_id, event_id, alarm_time) -> bool:
        self.query.execute(f"INSERT OR IGNORE INTO alarm(patient_id, event_id, alarm_time) values ({patient_id}, {event_id}, TIME('{alarm_time}'));")
        logger.info(f"INSERT OR IGNORE INTO alarm(patient_id, event_id, alarm_time) values ({patient_id}, {event_id}, TIME('{alarm_time}'));")
        self.connection.commit()
        return True

    def delete_alarm(self, id):
        self.query.execute(f"DELETE FROM alarm WHERE id = {id};")
        logger.info(f"DELETE FROM alarm WHERE id = {id};")
        self.connection.commit()

    def update_alarm(self, id, patient_id, event_id, alarm_time):
        self.query.execute(f"UPDATE alarm SET patient_id = {patient_id}, event_id = {event_id}, alarm_time = TIME('{alarm_time}') WHERE id = {id};")
        logger.info(f"UPDATE alarm SET patient_id = {patient_id}, event_id = {event_id}, alarm_time = TIME('{alarm_time}') WHERE id = {id};")
        self.connection.commit()

    def get_next_alarm(self, device_id):
        patient_id = self.get_patient_by_device_id(device_id)
        self.query.execute(f"SELECT id FROM alarm WHERE patient_id = {patient_id} AND alarm_time >= TIME('now', 'localtime') ORDER BY alarm_time ASC LIMIT 1;")
        logger.info(f"SELECT id FROM alarm WHERE patient_id = {patient_id} AND alarm_time >= TIME('now', 'localtime') ORDER BY alarm_time ASC LIMIT 1;")

        alarm_id = self.query.fetchone()

        if alarm_id:
            return alarm_id[0]
        else:
            return str(0)
    
    def get_alarm_time(self, alarm_id):
        self.query.execute(f"SELECT alarm_time FROM alarm WHERE id = {alarm_id};")
        logger.info(f"SELECT alarm_time FROM alarm WHERE id = {alarm_id};")

        alarm_id = self.query.fetchone()
        if alarm_id:
            return alarm_id[0]
        else:
            return str(0)