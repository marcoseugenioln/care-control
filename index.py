from flask import Flask, redirect, url_for, request, render_template, Blueprint, flash, session, abort
from flask import Flask
from database import Database
import logging

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('site-log.log')
logger.addHandler(handler)

app = Flask(__name__)
app.secret_key = '1234'
site = Blueprint('site', __name__, template_folder='templates')

database = Database()

@app.route("/")
def index():
    if 'logged_in' in session:
        if session['logged_in'] != True:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return render_template('index.html')
        
    
@app.route('/login', methods=['GET', 'POST'])
def login():

    is_login_valid = True

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        
        email = request.form['email']
        password = request.form['password']

        if database.user_exists(email, password):

            user_id = database.get_user_id(email, password)

            logger.info(f"user_id: {user_id}")
            session['logged_in'] = True
            session['user_id'] = user_id
            session['is_admin'] = database.get_admin(user_id)

            return redirect(url_for(f'index'))
        else:
            is_login_valid = False
    
    return render_template('auth/login.html', is_login_valid = is_login_valid)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')

    if 'user_id' in session:    
        session.pop('user_id')
    
    if 'is_admin' in session:
        session.pop('is_admin')

    return redirect(url_for(f'login'))

    
@app.route("/register", methods=['GET','POST'])
def register():

    is_logged = False

    if (request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'password_c' in request.form):
        
        email = request.form['email']
        password = request.form['password']
        password_c = request.form['password_c']

        if database.insert_user(email, password, password_c):
            return redirect(url_for('login'))   

        if 'logged_in' in session:
            if session['logged_in'] == True:
                is_logged = True                 
    
    return render_template('auth/register.html', logged_in = is_logged)

@app.route('/fornecedor', methods=['GET', 'POST'])
def fornecedor():
    
    return render_template('fornecedor/index.html', fornecedores = database.get_suppliers(), is_admin = session['is_admin'])

@app.route('/fornecedor/create', methods=['GET', 'POST'])
def create_fornecedor():
    
    if (request.method == 'POST' and 'supplier_name' in request.form):
        
        supplier_name = request.form['supplier_name']

        if database.insert_supplier(supplier_name):
            return redirect(url_for('fornecedor'))  
        
    return redirect(url_for('fornecedor'))

@app.route('/fornecedor/update/<id>', methods=['GET', 'POST'])
def update_fornecedor(id):
    
    if (request.method == 'POST' and 'supplier_name' in request.form):
        
        supplier_name = request.form['supplier_name']

        if database.update_supplier(id, supplier_name):
            return redirect(url_for('fornecedor'))  
        
    return redirect(url_for('fornecedor'))

@app.route('/fornecedor/delete/<id>', methods=['GET', 'POST'])
def delete_fornecedor(id):
    
    database.delete_supplier(id)
    return redirect(url_for('fornecedor'))

@app.route('/material', methods=['GET', 'POST'])
def material():
    
    return render_template(
        'material/index.html', 
        get_supplier = database.get_supplier,
        materiais = database.get_materials(), 
        fornecedores = database.get_suppliers(), 
        is_admin = session['is_admin']
        )

@app.route('/material/create', methods=['GET', 'POST'])
def create_material():
    
    if (request.method == 'POST' and 'supplier_id' in request.form and 'name' in request.form and 'value' in request.form and 'stock' in request.form and 'min_stock' in request.form):
        
        supplier_id = request.form['supplier_id']
        name = request.form['name']
        value = request.form['value']
        stock = request.form['stock']
        min_stock = request.form['min_stock']

        if database.insert_material(supplier_id, name, value, stock, min_stock):
            return redirect(url_for('material'))  
        
    return redirect(url_for('material'))

@app.route('/material/update/<id>', methods=['GET', 'POST'])
def update_material(id):
    
    if (request.method == 'POST' and 'supplier_id' in request.form and 'name' in request.form and 'value' in request.form and 'stock' in request.form and 'min_stock' in request.form):
        
        supplier_id = request.form['supplier_id']
        name = request.form['name']
        value = request.form['value']
        stock = request.form['stock']
        min_stock = request.form['min_stock']

        if database.update_material(id, supplier_id, name, value, stock, min_stock):
            return redirect(url_for('material'))  
        
    return redirect(url_for('material'))

@app.route('/material/delete/<id>', methods=['GET', 'POST'])
def delete_material(id):
    
    database.delete_material(id)
    return redirect(url_for('material'))

@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    
    return render_template(
        'usuario/index.html', 
        get_admin=database.get_admin, 
        usuarios = database.get_users(), 
        current_user_id = session['user_id'],
        current_user_email = database.get_user_email(session['user_id']),
        current_user_password = database.get_user_password(session['user_id']),
        is_admin = session['is_admin']
        )

@app.route('/usuario/create', methods=['GET', 'POST'])
def create_usuario():
    
    if (request.method == 'POST' and 'email' in request.form and 'new_password' in request.form ):
        
        email = request.form['email']
        new_password = request.form['new_password']

        if('is_admin' in request.form):
            is_admin = request.form['is_admin']
        else:
            is_admin = "0"

        if database.insert_user(email, new_password, is_admin):
            if 'user_id' in session:
                return redirect(url_for('usuario'))

        return redirect('/login')

@app.route('/usuario/update/<id>', methods=['GET', 'POST'])
def update_usuario(id):
    if (request.method == 'POST' and 'email' in request.form and 'new_password' in request.form and 'is_admin' in request.form):
        
        email = request.form['email']
        new_password = request.form['new_password']
        is_admin = request.form['is_admin']

        database.update_user(id, email, new_password, is_admin)
        return redirect(url_for('usuario'))  
        
    return redirect(url_for('usuario'))

@app.route('/usuario/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    database.delete_user(id)
    return redirect(url_for('usuario'))

@app.route('/pedido', methods=['GET', 'POST'])
def pedido():
    return render_template(
        'pedido/index.html',
        get_user_email=database.get_user_email,
        get_order_value=database.get_order_value,
        items = database.get_order_items(database.get_open_order_id()),
        materiais = database.get_materials(), 
        fornecedores = database.get_suppliers(),
        pedidos = database.get_orders(),
        view_order = False,
        view_order_id = 0,
        is_admin = session['is_admin']
        )

@app.route('/trabalho', methods=['GET', 'POST'])
def trabalho():
    return render_template(
        'trabalho/index.html',
        trabalhos=database.get_works(),
        )

@app.route('/trabalho/view/<id>', methods=['GET', 'POST'])
def trabalho_view(id):
    return render_template(
        'trabalho/index.html',
        trabalhos=database.get_works(),
        trabalho_itens=database.get_work_items(id),
        trabalho_id=id,
        materiais_para_trabalho=database.get_works_material(),
        trabalho_status=database.get_work_status(id),
    )

@app.route('/trabalho/close/<id>', methods=['GET', 'POST'])
def trabalho_close(id):
    if (request.method == 'POST' and session['user_id']):
        database.close_work(id)
    return render_template(
        'trabalho/index.html',
        trabalhos=database.get_works(),
        trabalho_itens=database.get_work_items(id),
        trabalho_id=id,
        materiais_para_trabalho=database.get_works_material(),
        trabalho_status=database.get_work_status(id),
        )

@app.route('/item_trabalho/create', methods=['GET', 'POST'])
def item_trabalho_create():
    if (request.method == 'POST' and session['user_id']):
        database.insert_work_item(request.form['trabalho_id'], request.form['material_id'], request.form['mat_qtd'])
    return redirect(f"/trabalho/view/{request.form['trabalho_id']}")

@app.route('/item_trabalho/update/<id>', methods=['GET', 'POST'])
def item_trabalho_update(id):
    if (request.method == 'POST' and session['user_id']):
        database.update_work_item(request.form['material_id'], request.form['mat_qtd'], id)
    renda = f"/trabalho/view/{request.form['trabalho_id']}"
    return redirect(renda)

@app.route('/item_trabalho/delete/<id>', methods=['GET', 'POST'])
def item_trabalho_delete(id):
    if (request.method == 'POST' and session['user_id']):
        database.delete_work_item(id)
    renda = f"/trabalho/view/{request.form['trabalho_id']}"
    return redirect(renda)

@app.route('/trabalho/create', methods=['GET', 'POST'])
def trabalho_create():
    if (request.method == 'POST' and session['user_id']):
        database.insert_work(session['user_id'], request.form['name'], request.form['dia'])
    return redirect(url_for('trabalho'))

@app.route('/trabalho/delete/<id>', methods=['GET', 'POST'])
def trabalho_delete(id):
    if (request.method == 'POST' and session['user_id']):
        database.delete_work(session['user_id'], id)
    return redirect(url_for('trabalho'))

@app.route('/trabalho/update/<id>', methods=['GET', 'POST'])
def trabalho_update(id):
    if (request.method == 'POST' and session['user_id']):
        database.update_work(session['user_id'], id, request.form['name'], request.form['dia'])
    return redirect(url_for('trabalho'))

@app.route('/pedido/close', methods=['GET', 'POST'])
def close_pedido():
    database.order_service(session['user_id'])
    return redirect(url_for('pedido'))

@app.route('/pedido/view/<id>', methods=['GET', 'POST'])
def view_pedido(id):
    return render_template(
        'pedido/index.html',
        get_user_email=database.get_user_email,
        get_item_value=database.get_item_value,
        get_material_name=database.get_material_name,
        get_order_value=database.get_order_value,
        items = database.get_order_items(database.get_open_order_id()),
        materiais = database.get_materials(), 
        fornecedores = database.get_suppliers(),
        pedidos = database.get_orders(),
        closed_order_items = database.get_order_items(id),
        view_order_items = True,
        view_order_id = int(id),
        is_admin = session['is_admin']
        )

@app.route('/item/create', methods=['GET', 'POST'])
def create_item():
    database.insert_empty_item()
    return redirect(url_for('pedido'))

@app.route('/item/update', methods=['GET', 'POST'])
def update_item():

    if (request.method == 'POST' and 'material_id' in request.form and 'quantity' in request.form and 'item_id' in request.form):
        
        item_id = request.form['item_id']
        material_id = request.form['material_id']
        quantity = request.form['quantity']

        database.update_item(item_id, material_id, quantity)
        return redirect(url_for('pedido'))
    
    return redirect(url_for('pedido'))

@app.route('/item/delete/<id>', methods=['GET', 'POST'])
def delete_item(id):
    database.delete_item(id)
    return redirect(url_for('pedido'))


if __name__ == '__main__':
    app.run(debug=True)