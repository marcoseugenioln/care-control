from flask import Flask, redirect, url_for, request, render_template, Blueprint, flash, session, abort, jsonify
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

LOG_TYPE_INPUT     = 0
LOG_TYPE_ALARM_ON  = 1
LOG_TYPE_ALARM_OFF = 2

def get_log_type(type_id):
    if type_id == 0:
        return "Registro"
    elif type_id == 1:
        return "Alarme Ligado"
    elif type_id == 2:
        return "Alarme Desligado"
    else:
        return ""

@app.route("/")
def index():
    if 'logged_in' in session:
        if session['logged_in'] != True:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return render_template('index.html')
        
################################################################################################## 
 
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

##################################################################################################

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

##################################################################################################
@app.route('/patient', methods=['GET', 'POST'])
def patient():
    return render_template(
        'patient/index.html',
        has_patient=database.has_patient(session['user_id']),
        patients=database.get_patient(session['is_admin'], session['user_id']),
        is_admin=session['is_admin']
    )

@app.route('/patient/create', methods=['GET', 'POST'])
def create_patient():

    if (request.method == 'POST'):
        database.insert_patient( request.form['patient_name'],  request.form['birth_date'], session['user_id'])
    
    return redirect(url_for('patient'))

@app.route('/patient/delete/<id>', methods=['GET', 'POST'])
def delete_patient(id):
    database.delete_patient(id)
    return redirect(url_for('patient'))

@app.route('/patient/update/<id>', methods=['GET', 'POST'])
def update_patient(id):
    if (request.method == 'POST'):
        database.update_patient(
            id,
            request.form['patient_name'],
            request.form['birth_date'],
        )
    return redirect(url_for('patient'))

##################################################################################################

@app.route('/event', methods=['GET', 'POST'])
def event():
    return render_template(
        'event/index.html',
        events=database.get_events(),
        user_id = session['user_id'],
        is_admin = session['is_admin']
    )

@app.route('/event/create', methods=['GET', 'POST'])
def create_event():
    if (request.method == 'POST'):
        database.insert_event(
            request.form['event_description'],
            request.form['is_input_event'],
        )
    return redirect(url_for('event'))

@app.route('/event/delete/<id>', methods=['GET', 'POST'])
def delete_event(id):
    database.delete_event(id)
    return redirect(url_for('event'))

@app.route('/event/update/<id>', methods=['GET', 'POST'])
def update_event(id):
    if (request.method == 'POST'):
        database.update_event(
            id,
            request.form['event_description'],
            request.form['is_input_event'],
        )

    return redirect(url_for('event'))

##################################################################################################
@app.route('/caregiver', methods=['GET', 'POST'])
def caregiver():
    return render_template(
        'caregiver/index.html',
        caregivers=database.get_caregivers(session['is_admin'], session['user_id']),
        patients=database.get_patient(True, session['user_id']),
        user_id = session['user_id'],
        is_admin = session['is_admin']
    )

@app.route('/caregiver/create', methods=['GET', 'POST'])
def create_caregiver():
    if (request.method == 'POST'):

        if session['is_admin']:
            patient_id = request.form['patient_id']
        else:
            patient_id = database.get_patient_id_from_user_id(session['user_id'])

        database.insert_caregiver(
            patient_id,
            request.form['name'],
            request.form['start_shift'],
            request.form['end_shift'],
        )
    return redirect(url_for('caregiver'))

@app.route('/caregiver/delete/<id>', methods=['GET', 'POST'])
def delete_caregiver(id):
    database.delete_caregiver(id)
    return redirect(url_for('caregiver'))

@app.route('/caregiver/update/<id>', methods=['GET', 'POST'])
def update_caregiver(id):
    if (request.method == 'POST'):

        if session['is_admin']:
            patient_id = request.form['patient_id']
        else:
            patient_id = database.get_patient_id_from_user_id(session['user_id'])

        database.update_caregiver(
            id,
            patient_id,
            request.form['name'],
            request.form['start_shift'],
            request.form['end_shift'],
        )

    return redirect(url_for('caregiver'))



##################################################################################################
@app.route('/alarm', methods=['GET', 'POST'])
def alarm():
    return render_template(
        'alarm/index.html',
        alarms=database.get_alarms(session['is_admin'], session['user_id']),
        patients=database.get_patient(True, session['user_id']),
        events=database.get_events(),
        user_id = session['user_id'],
        is_admin = session['is_admin']
    )

@app.route('/alarm/create', methods=['GET', 'POST'])
def create_alarm():
    if (request.method == 'POST'):
        if session['is_admin']:
            patient_id = request.form['patient_id']
        else:
            patient_id = database.get_patient_id_from_user_id(session['user_id'])

        database.insert_alarm(
            patient_id,
            request.form['event_id'],
            request.form['alarm_time'],
        )
    return redirect(url_for('alarm'))

@app.route('/alarm/delete/<id>', methods=['GET', 'POST'])
def delete_alarm(id):
    database.delete_alarm(id)
    return redirect(url_for('alarm'))

@app.route('/alarm/update/<id>', methods=['GET', 'POST'])
def update_alarm(id):
    if (request.method == 'POST'):
        database.update_alarm(
            id,
            request.form['event_description'],
            request.form['is_input_event'],
        )

    return redirect(url_for('alarm'))

##################################################################################################
@app.route('/device', methods=['GET', 'POST'])
def device():

    if session['is_admin']:
        has_device=True
    else:
        has_device=database.has_device(session['user_id'])
    
    return render_template(
        'device/index.html',
        devices=database.get_device(session['is_admin'], session['user_id']),
        patients=database.get_patient(True, session['user_id']),
        events=database.get_events(),
        user_id=session['user_id'],
        is_admin=session['is_admin'],
        has_device=has_device,
    )

@app.route('/device/create', methods=['GET', 'POST'])
def create_device():
    if (request.method == 'POST'):

        if session['is_admin']:
            patient_id = request.form['patient_id']
        else:
            patient_id = database.get_patient_id_from_user_id(session['user_id'])

        database.insert_device(
            patient_id,
            request.form['name'],
        )
    return redirect(url_for('device'))

@app.route('/device/delete/<id>', methods=['GET', 'POST'])
def delete_device(id):
    database.delete_device(id)
    return redirect(url_for('device'))

@app.route('/device/update/<id>', methods=['GET', 'POST'])
def update_device(id):
    if (request.method == 'POST'):

        if session['is_admin']:
            patient_id = request.form['patient_id']
        else:
            patient_id = database.get_patient_id_from_user_id(session['user_id'])

        database.update_device(
            id,
            patient_id,
            request.form['name'],
            request.form['event_button_1'],
            request.form['event_button_2'],
            request.form['event_button_3'],
        )
    return redirect(url_for('device'))

@app.route('/device/input/<device_id>/<button_id>', methods=['GET', 'POST'])
def device_input(device_id, button_id):

    patient_id = database.get_patient_by_device_id(device_id)
    logger.info("patient_id: " + str(patient_id))

    button_event_id = database.get_button_event_id(device_id, int(button_id))
    logger.info("button_event_id: " + str(button_event_id))

    database.log_message(patient_id, button_event_id, LOG_TYPE_INPUT)

    return redirect(url_for('historic'))

@app.route('/device/alarm-on/<device_id>', methods=['GET', 'POST'])
def device_alarm_on(device_id):
    logger.info("alarm on")

@app.route('/device/alarm-off/<device_id>', methods=['GET', 'POST'])
def device_alarm_off(device_id):
    logger.info("alarm off")
##################################################################################################

@app.route('/historic', methods=['GET', 'POST'])
def historic():

    return render_template(
        'historic/index.html',
        user_id=session['user_id'],
        is_admin=session['is_admin'],
        get_patient_name=database.get_patient_name,
        get_event_description=database.get_event_description,
        get_log_type=get_log_type,
        historic=database.get_historic(session['is_admin'], session['user_id'])
    )

if __name__ == '__main__':

    DEBUG   = True
    HOST_IP = "127.0.0.1"
    PORT    = 3000

    app.run(host=HOST_IP, port=PORT, debug=DEBUG)
