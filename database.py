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

    def get_suppliers(self):
        self.query.execute("SELECT id, nome FROM fornecedor")
        suppliers = self.query.fetchall()
        return suppliers
    
    def get_supplier(self, id):
        self.query.execute(f"SELECT nome FROM fornecedor WHERE id == {id}")
        supplier = self.query.fetchone()[0]
        return supplier
    
    def insert_supplier(self, name):
        self.query.execute(f"INSERT OR IGNORE INTO fornecedor (nome) VALUES ('{name}');")
        logger.info(f"INSERT OR IGNORE INTO fornecedor (nome) VALUES ('{name}');")
        self.connection.commit()
        return True
    
    def delete_supplier(self, id):
        self.query.execute(f"DELETE FROM fornecedor WHERE id == {id};")
        logger.info(f"DELETE FROM fornecedor WHERE id == {id};")
        self.connection.commit()

    def update_supplier(self, id, supplier_name):
        self.query.execute(f"UPDATE fornecedor SET nome = '{supplier_name}' WHERE id == {id};")
        logger.info(f"UPDATE fornecedor SET nome = '{supplier_name}' WHERE id == {id};")
        self.connection.commit()
    
    def get_materials(self):
        self.query.execute("SELECT id, fornecedor_id, nome, valor, estoque, estoque_minimo FROM material")
        materials = self.query.fetchall()
        return materials
    
    def insert_material(self, supplier_id, name, value, stock, min_stock):
        self.query.execute(f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        logger.info(f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        self.connection.commit()
        return True
    
    def update_material(self, id, supplier_id, name, value, stock, min_stock):
        self.query.execute(f"UPDATE material SET fornecedor_id = {supplier_id}, nome = '{name}', valor = {value}, estoque = {stock}, estoque_minimo = {min_stock} WHERE id == {id};")
        logger.info(f"UPDATE material SET fornecedor_id = {supplier_id}, nome = '{name}', valor = {value}, estoque = {stock}, estoque_minimo = {min_stock} WHERE id == {id};")
        self.connection.commit()

    def delete_material(self, id):
        self.query.execute(f"DELETE FROM material WHERE id == {id};")
        logger.info(f"DELETE FROM material WHERE id == {id};")
        self.connection.commit()

    def get_material_value(self, material_id):
        self.query.execute(f"SELECT valor FROM material WHERE id = { material_id }")
        logger.info(f"SELECT valor FROM material WHERE id = { material_id }")
        value = self.query.fetchone()[0]
        return value
    
    def get_material_name(self, material_id):
        self.query.execute(f"SELECT nome FROM material WHERE id = { material_id }")
        logger.info(f"SELECT nome FROM material WHERE id = { material_id }")
        name = self.query.fetchone()[0]
        return name

    def get_orders(self):
        self.query.execute("SELECT id, usuario_id, data, status FROM pedido")
        orders = self.query.fetchall()
        return orders

    def get_works(self):
        self.query.execute(
            "SELECT t.id id, u.email email, t.dia data, t.nome nome, t.status status, SUM(m.valor*it.quantidade) valor " 
            "FROM trabalho t "
            "LEFT JOIN item_trabalho it ON (t.id = it.trabalho_id) " 
            "LEFT JOIN material m ON (it.material_id = m.id) "
            "LEFT JOIN usuario u ON t.usuario_id = u.id "
            "GROUP BY t.id, u.email, t.dia, t.nome, t.status "
            ";")
        orders = self.query.fetchall()
        return orders

    def get_works_material(self):
        self.query.execute(
            "SELECT m.id, m.nome || ' - QTD: ' || estoque || ' - R$ ' || valor material "
            "FROM material m ORDER BY material;")
        rowsd = self.query.fetchall()
        return rowsd

    def get_open_order_id(self):
        self.query.execute("SELECT id FROM pedido WHERE status == 1")
        order_id = self.query.fetchone()[0]
        return order_id


    def insert_order(self, supplier_id, name, value, stock, min_stock):
        self.query.execute(f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        logger.info(f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        self.connection.commit()
        return True

    def insert_work(self, user_id, name, dia):
        self.query.execute("INSERT OR IGNORE INTO trabalho (usuario_id, nome, dia) VALUES (?, ?, ?);", (user_id, name, dia))
        self.connection.commit()
        return True

    def insert_work_item(self, trabalho_id, material_id, mat_qtd):
        self.query.execute("INSERT INTO item_trabalho (trabalho_id, material_id, quantidade) VALUES(?, ?, ?);", (trabalho_id, material_id, mat_qtd))
        self.connection.commit()
        return True

    def update_work_item(self, material_id, mat_qtd, id):
        self.query.execute("UPDATE item_trabalho SET material_id=?, quantidade=? WHERE id=?;", (material_id, mat_qtd, id))
        self.connection.commit()
        return True

    def delete_work_item(self, id):
        self.query.execute("DELETE FROM item_trabalho WHERE id=?;", (id, ))
        self.connection.commit()
        return True

    def update_work(self, user_id, id, name, dia):
        self.query.execute("UPDATE trabalho SET dia=?, nome=? WHERE usuario_id=? AND id=?;", (dia, name, user_id, id))
        self.connection.commit()
        return True

    def close_work(self, id):
        self.query.execute("UPDATE material SET estoque = estoque - fqtd FROM "
                            "    (SELECT usado.material_id, fqtd FROM "
                            "        (SELECT material_id, SUM(quantidade) fqtd FROM item_trabalho it WHERE it.trabalho_id = ? GROUP BY material_id) usado "
                            "    LEFT JOIN "
                            "        (SELECT m.id material_id, m.estoque FROM material m) estoque "
                            "    ON usado.material_id = estoque.material_id) baixa "
                            "WHERE id = material_id", (id,))
        self.query.execute("UPDATE trabalho SET status=0 WHERE id=?;", (id,))
        self.connection.commit()
        return True

    def delete_work(self, user_id, id):
        self.query.execute("DELETE FROM item_trabalho WHERE id=?;", (id,))
        self.query.execute("DELETE FROM trabalho WHERE id=?;", (id,))
        self.connection.commit()
        return True

    def insert_order(self, supplier_id, name, value, stock, min_stock):
        self.query.execute(
            f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        logger.info(
            f"INSERT OR IGNORE INTO material (fornecedor_id, nome, valor, estoque, estoque_minimo) VALUES ({supplier_id}, '{name}', {value}, {stock}, {min_stock});")
        self.connection.commit()
        return True

    def update_order(self, id, supplier_id, name, value, stock, min_stock):
        self.query.execute(f"UPDATE material SET fornecedor_id = {supplier_id}, nome = '{name}', valor = {value}, estoque = {stock}, estoque_minimo = {min_stock} WHERE id == {id};")
        logger.info(f"UPDATE material SET fornecedor_id = {supplier_id}, nome = '{name}', valor = {value}, estoque = {stock}, estoque_minimo = {min_stock} WHERE id == {id};")
        self.connection.commit()

    def delete_order(self, id):
        self.query.execute(f"DELETE FROM pedido WHERE id == {id};")
        logger.info(f"DELETE FROM pedido WHERE id == {id};")
        self.connection.commit()

    def get_order_items(self, order_id):
        self.query.execute(f"SELECT id, material_id, quantidade FROM item WHERE pedido_id == {order_id}")
        items = self.query.fetchall()
        return items

    def get_work_items(self, trabalho_id):
        self.query.execute("SELECT t.trabalho_id id, t.material_id, m.nome, t.quantidade, m.estoque "
            "    FROM "
            "        (SELECT id trabalho_id, material_id, quantidade FROM item_trabalho WHERE trabalho_id == ?) t "
            "    INNER JOIN "
            "        (SELECT id material_id, nome, estoque FROM material) m "
            "    ON m.material_id = t.material_id ", (trabalho_id,))
        items = self.query.fetchall()
        return items

    def insert_empty_item(self):
        self.query.execute(f"INSERT INTO item (pedido_id, material_id, quantidade) VALUES ({self.get_open_order_id()}, 0, 0);")
        logger.info(f"INSERT INTO item (pedido_id, material_id, quantidade) VALUES ({self.get_open_order_id()}, 0, 0);")
        self.connection.commit()
        return True
    
    def delete_item(self, id):
        self.query.execute(f"DELETE FROM item WHERE id == {id};")
        logger.info(f"DELETE FROM item WHERE id == {id};")
        self.connection.commit()

    def update_item(self, id, material_id, quantity):
        self.query.execute(f"UPDATE item SET material_id = {material_id}, quantidade = {quantity} WHERE id == {id};")
        logger.info(f"UPDATE item SET material_id = {material_id}, quantidade = {quantity} WHERE id == {id};")
        self.connection.commit()

    def new_order(self):
        self.query.execute(f"INSERT INTO pedido DEFAULT VALUES;")
        logger.info(f"INSERT INTO pedido DEFAULT VALUES;")
        self.connection.commit()

    def close_order(self, user_id):
        self.query.execute(f"UPDATE pedido SET usuario_id = {user_id}, data = DATE('now'), status = 0;")
        logger.info(f"UPDATE pedido SET usuario_id = {user_id}, data = DATE('now'), status = 0;")
        self.connection.commit()

    def get_stock(self, material_id):
        self.query.execute(f"SELECT estoque FROM material WHERE id = {material_id}")
        logger.info(f"SELECT estoque FROM material WHERE id = {material_id}")

        stock = self.query.fetchone()[0]
        return int(stock)

    def get_work_status(self, trabalho_id):
        self.query.execute("SELECT status FROM trabalho WHERE id=?;", (trabalho_id,))
        estado = self.query.fetchone()[0]
        return int(estado)

    def add_to_stock(self, material_id, quantity):
        current_stock = self.get_stock(material_id)
        self.query.execute(f"UPDATE material SET estoque = {current_stock + quantity} WHERE id = {material_id}")
        logger.info(f"UPDATE material SET estoque = {current_stock + quantity} WHERE id = {material_id}")

    def add_order_items_to_stock(self):
        for item_id, material_id, qtd in self.get_order_items(self.get_open_order_id()):
            self.add_to_stock(material_id, qtd)
        
    def order_service(self, user_id):

        self.add_order_items_to_stock()
        self.close_order(user_id)
        self.new_order()

    def get_item_value(self, item_id):
        self.query.execute(f"SELECT material_id, quantidade FROM item WHERE id == {item_id};")
        logger.info(f"SELECT material_id, quantidade FROM item WHERE id == {item_id};")

        response = self.query.fetchone()

        material_id = response[0]
        quantity = response[1]

        item_value = self.get_material_value(material_id) * quantity

        return item_value

    def get_order_value(self, order_id):

        order_value = 0

        for item_id, material_id, quantidade in self.get_order_items(order_id):
            order_value = order_value + self.get_item_value(item_id)
        
        return order_value

    def get_work_value(self, order_id):

        order_value = 0

        for item_id, material_id, quantidade in self.get_work_items(order_id):
            order_value = order_value + self.get_item_value(item_id)

        return order_value

