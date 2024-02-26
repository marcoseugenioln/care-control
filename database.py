import sqlite3
import logging

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

        self.query.execute(f"SELECT * FROM usuario WHERE email == '{email}' AND password == '{password}'")
        logger.info(f"SELECT * FROM usuario WHERE email == '{email}' AND password == '{password}'")

        account = self.query.fetchone()

        if not account:
            return False
        
        return True
    
    def get_user_id(self, email: str, password: str):
        logger.info(f"SELECT id FROM usuario WHERE email == '{email}' AND password == '{password}';")
        self.query.execute(f"SELECT id FROM usuario WHERE email == '{email}' AND password == '{password}';")
        user_id = self.query.fetchone()[0]   
        return user_id

    def get_admin(self, user_id):
        logger.info(f"SELECT is_admin FROM usuario WHERE id == {user_id};")
        self.query.execute(f"SELECT is_admin FROM usuario WHERE id == {user_id};")
        is_admin = self.query.fetchone()

        if int(is_admin[0]) == 0:
            return False
        
        return True
    
    def insert_user(self, email: str, password: str, is_admin: str) -> bool:        
        self.query.execute(f"INSERT OR IGNORE INTO usuario(email, password, is_admin) values ('{email}', '{password}', {is_admin});")
        logger.info(f"INSERT OR IGNORE INTO usuario(email, password, is_admin) values ('{email}', '{password}', {is_admin});")
        self.connection.commit()
        return True
    
    def get_user_email(self, user_id: int) -> str:
        self.query.execute(f"SELECT email FROM usuario WHERE id == {user_id}")
        logger.info(f"SELECT email FROM usuario WHERE id == {user_id}")
        email = self.query.fetchone()[0]
        return email

    def get_user_password(self, user_id: int) -> str:
        self.query.execute(f"SELECT password FROM usuario WHERE id == {user_id}")
        logger.info(f"SELECT password FROM usuario WHERE id == {user_id}")
        password = self.query.fetchone()[0]
        return password
    
    def get_users(self):
        self.query.execute(f"SELECT id, email, password FROM usuario")
        logger.info(f"SELECT id, email, password FROM usuario")
        users = self.query.fetchall()        
        return users
    
    def alter_password(self, user_id, password):
        self.query.execute(f"UPDATE usuario SET password = '{password}' WHERE id == {user_id}")
        logger.info(f"UPDATE usuario SET password = '{password}' WHERE id == {user_id}")
        self.connection.commit()

    def alter_email(self, user_id, email):
        self.query.execute(f"UPDATE usuario SET email = '{email}' WHERE id == {user_id}")
        logger.info(f"UPDATE usuario SET email = '{email}' WHERE id == {user_id}")
        self.connection.commit()

    def delete_user(self, id):
        self.query.execute(f"DELETE FROM usuario WHERE id == {id};")
        logger.info(f"DELETE FROM usuario WHERE id == {id};")
        self.connection.commit()

    def update_user(self, user_id, email, password, is_admin):
        logger.info(f"UPDATE usuario SET email = '{email}', password = '{password}', is_admin = {is_admin} WHERE id == {user_id};")
        self.query.execute(f"UPDATE usuario SET email = '{email}', password = '{password}', is_admin = {is_admin} WHERE id == {user_id};")
        self.connection.commit()