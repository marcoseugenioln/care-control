import sqlite3
import logging
from datetime import datetime


logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('site-log.log')
logger.addHandler(handler)

class Database():

    def __init__(self):
        logger.info('starting database connection')
        self.connection = sqlite3.connect('schema.db', check_same_thread=False, timeout=10)
        self.query = self.connection.cursor()
        logger.info('Database connected.')

        with open('schema.sql', 'r') as sql_file:
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
        user_id = self.query.fetchone()[0]   
        return user_id

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
        email = self.query.fetchone()[0]
        return email

    def get_user_password(self, user_id: int) -> str:
        self.query.execute(f"SELECT password FROM user WHERE id == {user_id}")
        logger.info(f"SELECT password FROM user WHERE id == {user_id}")
        password = self.query.fetchone()[0]
        return password
    
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

    def get_devices(self, isadm, uid):
        self.query.execute("SELECT id, nome, guid FROM device WHERE (? OR user_id = ?);", (isadm, uid))
        logger.info(f"SELECT id, user_id, nome, guid FROM device WHERE ({isadm} OR user_id = {uid});")
        return self.query.fetchall()
    ##################################################################################################

    def insert_device(self, device: str, guid: str, uid: int) -> bool:
        self.query.execute("INSERT OR IGNORE INTO device(user_id, nome, guid) values (?, ?, ?);", (uid, device, guid))
        logger.info(f"INSERT OR IGNORE INTO device(user_id, nome, guid) values ({uid}, {device}, {guid});")
        self.connection.commit()
        return True

    def delete_device(self, id):
        self.query.execute("DELETE FROM device WHERE id = ?;", ((id,)))
        logger.info(f"DELETE FROM device WHERE id = {id};")
        self.connection.commit()

    def update_device(self, id, nome, guid):
        self.query.execute("UPDATE device SET nome = ?, guid = ? WHERE id =?;", (nome, guid, id))
        logger.info(f"UPDATE device SET nome = {nome}, guid = {guid} WHERE id = {id};")
        self.connection.commit()
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

    def has_patient(self, user_id):
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
    def save_log(self, id, logstr):
        agora = datetime.now()
        agorastr = agora.strftime("%d-%m-%Y %H:%M:%S")
        self.query.execute(
            "INSERT OR IGNORE INTO historico(patient_id, data, log) values (?, ?, ?);",
            (id, agorastr, logstr))
        self.connection.commit()

    def get_own_name(self, id):
        self.query.execute("SELECT nome || ' - ' || datanasc FROM patient WHERE id = ?;", ((id,)))
        return self.query.fetchone()[0]

    def get_log(self, id):
        self.query.execute("SELECT id, data, log FROM historico WHERE patient_id = ?;", ((id,)))
        logger.info(f"SELECT id, data, log FROM historico WHERE patient_id = {id};")
        return self.query.fetchall()

    def get_folist(self, isadm, uid):
        self.query.execute("SELECT id, nome || ' - ' || datanasc AS nome FROM patient WHERE (? OR user_id = ?);", (isadm, uid))
        logger.info(f"SELECT id, nome || ' - ' || datanasc FROM patient WHERE ({isadm} OR user_id = {uid});")
        return self.query.fetchall()

    def get_devdet(self, id):
        logger.info(f"SELECT id, user_id, acompanhando_id, guid, nome, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme, alarme2_log, alarme2_evt, alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log, alarme4_evt, alarme5_tme, alarme5_log, alarme5_evt, evento1_log, evento2_log, evento3_log FROM device WHERE id =  {id});")
        self.query.execute("SELECT id, user_id, acompanhando_id, guid, nome, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme, alarme2_log, alarme2_evt, alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log, alarme4_evt, alarme5_tme, alarme5_log, alarme5_evt, evento1_log, evento2_log, evento3_log FROM device WHERE id = ?;", ((id, )))
        return self.query.fetchall()

    def update_devdet(self, id, user_id, acompanhando_id, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme,
                      alarme2_log, alarme2_evt, alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log,
                      alarme4_evt, alarme5_tme, alarme5_log, alarme5_evt, evento1_log, evento2_log, evento3_log):

        self.query.execute(
            "UPDATE device SET acompanhando_id = ?, alarme1_tme = ?, alarme1_log = ?, alarme1_evt = ?,"
            " alarme2_tme = ?, alarme2_log = ?, alarme2_evt = ?, alarme3_tme = ?, alarme3_log = ?, alarme3_evt = ?,"
            " alarme4_tme = ?, alarme4_log = ?, alarme4_evt = ?, alarme5_tme = ?, alarme5_log = ?, alarme5_evt = ?,"
            " evento1_log = ?, evento2_log = ?, evento3_log = ? WHERE id = ?",
            (acompanhando_id, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme, alarme2_log, alarme2_evt,
             alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log, alarme4_evt, alarme5_tme, alarme5_log,
             alarme5_evt, evento1_log, evento2_log, evento3_log, id))
        logger.info(f"UPDATE device SET acompanhando_id = { acompanhando_id }, alarme1_tme = { alarme1_tme },"
                    " alarme1_log = { alarme1_log }, alarme1_evt = { alarme1_evt }, alarme2_tme = { alarme2_tme },"
                    " alarme2_log = { alarme2_log }, alarme2_evt = { alarme2_evt }, alarme3_tme = { alarme3_tme },"
                    " alarme3_log = { alarme3_log }, alarme3_evt = { alarme3_evt }, alarme4_tme = { alarme4_tme },"
                    " alarme4_log = { alarme4_log }, alarme4_evt = { alarme4_evt }, alarme5_tme = { alarme5_tme },"
                    " alarme5_log = { alarme5_log }, alarme5_evt = { alarme5_evt }, evento1_log = { evento1_log },"
                    " evento2_log = { evento2_log }, evento3_log = { evento3_log } WEHRE id = { id }")
        self.connection.commit()
        pass

    def get_devguid(self, guid):
        logger.info(f"SELECT guid, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme, alarme2_log, alarme2_evt,"
                    " alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log, alarme4_evt, alarme5_tme,"
                    " alarme5_log, alarme5_evt, evento1_log, evento2_log, evento3_log"
                    " FROM device WHERE guid =  {guid});")
        self.query.execute("SELECT guid, alarme1_tme, alarme1_log, alarme1_evt, alarme2_tme, alarme2_log,"
                           " alarme2_evt, alarme3_tme, alarme3_log, alarme3_evt, alarme4_tme, alarme4_log,"
                           " alarme4_evt, alarme5_tme, alarme5_log, alarme5_evt, evento1_log, evento2_log,"
                           " evento3_log FROM device WHERE guid = ?;", ((guid, )))
        return self.query.fetchone()

    def get_devlog(self, guid):
        logger.info(f"SELECT acompanhando_id, evento1_log, evento2_log, evento3_log FROM device WHERE guid =  {guid});")
        self.query.execute("SELECT acompanhando_id, evento1_log, evento2_log, evento3_log FROM device WHERE guid = ?;", ((guid, )))
        return self.query.fetchone()
      
    ##################################################################################################

    def get_events(self):
        self.query.execute("SELECT id, description, is_input FROM event;")
        logger.info("SELECT id, description, is_input FROM event;")
        return self.query.fetchall()
    
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
            patient_id = self.get_pateint_id_from_user_id(user_id)

            self.query.execute(f"SELECT id, patient_id, name, start_shift, end_shift FROM caregiver WHERE patient_id = {patient_id};")
            logger.info(f"SELECT id, patient_id, name, start_shift, end_shift FROM caregiver WHERE patient_id = {patient_id};")
            return self.query.fetchall()
        
    def get_pateint_id_from_user_id(self, user_id):
        self.query.execute(f"SELECT id FROM patient WHERE user_id = {user_id};")
        logger.info(f"SELECT id FROM patient WHERE user_id = {user_id};")
        return self.query.fetchone()[0]
        
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
        self.query.execute(f"UPDATE caregiver SET patient_id = {patient_id}, name = {name}, start_sift = TIME('{start_shift}'), end_shift = TIME('{end_shift}') WHERE id = {id};")
        logger.info(f"UPDATE caregiver SET patient_id = {patient_id}, name = {name}, start_sift = TIME('{start_shift}'), end_shift = TIME('{end_shift}') WHERE id = {id};")
        self.connection.commit()

    ##################################################################################################

    def get_alarms(self, is_admin, user_id):
        if bool(is_admin):
            self.query.execute("SELECT id, patient_id, event_id, alarm_time FROM alarm;")
            logger.info(f"SELECT id, user_id, nome, guid FROM alarm;")
            return self.query.fetchall()
        else:
            patient_id = self.get_pateint_id_from_user_id(user_id)

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
        self.query.execute(f"UPDATE alarm SET patient_id = {patient_id}, event_id = {event_id} alarm_time = {alarm_time} WHERE id = {id};")
        logger.info(f"UPDATE alarm SET patient_id = {patient_id}, event_id = {event_id} alarm_time = {alarm_time} WHERE id = {id};")
        self.connection.commit()