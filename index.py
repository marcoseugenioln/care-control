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

@app.route('/user', methods=['GET', 'POST'])
def user():
    
    return render_template(
        'user/index.html', 
        get_admin=database.get_admin, 
        users = database.get_users(), 
        current_user_id = session['user_id'],
        current_user_email = database.get_user_email(session['user_id']),
        current_user_password = database.get_user_password(session['user_id']),
        is_admin = session['is_admin']
        )

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    
    if (request.method == 'POST' and 'email' in request.form and 'new_password' in request.form ):
        
        email = request.form['email']
        new_password = request.form['new_password']

        if('is_admin' in request.form):
            is_admin = request.form['is_admin']
        else:
            is_admin = "0"

        if database.insert_user(email, new_password, is_admin):
            if 'user_id' in session:
                return redirect(url_for('user'))

        return redirect('/login')

@app.route('/user/update/<id>', methods=['GET', 'POST'])
def update_user(id):
    if (request.method == 'POST' and 'email' in request.form and 'new_password' in request.form and 'is_admin' in request.form):
        
        email = request.form['email']
        new_password = request.form['new_password']
        is_admin = request.form['is_admin']

        database.update_user(id, email, new_password, is_admin)
        return redirect(url_for('user'))  
        
    return redirect(url_for('user'))

@app.route('/user/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    database.delete_user(id)
    return redirect(url_for('user'))

@app.route('/device', methods=['GET', 'POST'])
def device():
    return render_template(
        'device/index.html',
        devices=database.get_devices(session['is_admin'], session['user_id']),
    )

@app.route('/device/create', methods=['GET', 'POST'])
def create_device():
    if (request.method == 'POST'):
        database.insert_device(
            request.form['nome'],
            request.form['guid'],
            session['user_id'],
        )
    return redirect(url_for('device'))

@app.route('/device/delete/<id>', methods=['GET', 'POST'])
def delete_device(id):
    database.delete_device(id)
    return redirect(url_for('device'))

@app.route('/device/update/<id>', methods=['GET', 'POST'])
def update_device(id):
    if (request.method == 'POST'):
        database.update_device(
            id,
            request.form['nome'],
            request.form['guid'],
        )
    return redirect(url_for('device'))

@app.route('/follow', methods=['GET', 'POST'])
def follow():
    return render_template(
        'follow/index.html',
        follows=database.get_follow(session['is_admin'], session['user_id']),
    )

@app.route('/follow/create', methods=['GET', 'POST'])
def create_follow():
    if (request.method == 'POST'):
        database.insert_follow(
            request.form['nome'],
            request.form['datan'],
            request.form['acomp'],
            session['user_id'],
        )
    return redirect(url_for('follow'))

@app.route('/follow/delete/<id>', methods=['GET', 'POST'])
def delete_follow(id):
    database.delete_follow(id)
    return redirect(url_for('follow'))

@app.route('/follow/update/<id>', methods=['GET', 'POST'])
def update_follow(id):
    if (request.method == 'POST'):
        database.update_follow(
            id,
            request.form['nome'],
            request.form['datan'],
            request.form['acomp'],
        )
    return redirect(url_for('follow'))

@app.route('/hist/<id>', methods=['GET', 'POST'])
def hist(id):
    return render_template(
        'hist/index.html',
        onwname=database.get_own_name(id),
        logs=database.get_log(id),
    )

@app.route('/device/edit/<id>', methods=['GET', 'POST'])
def devide_edit(id):
    if (request.method == 'GET'):
        return render_template(
            'device/edit.html',
            folist=database.get_folist(session['is_admin'], session['user_id']),
            devdat=database.get_devdet(id),
        )
    if (request.method == 'POST'):
        id,
        request.form[''],
        request.form[''],
        request.form[''],
        return redirect(url_for('device'))
        pass

if __name__ == '__main__':
    app.run(debug=True)