-- user table definition
CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT(300) UNIQUE,
	password TEXT(64),
	is_admin INTEGER DEFAULT (0)
);

-- caregiver table definition
CREATE TABLE IF NOT EXISTS caregiver (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	patient_id INTEGER,
	name TEXT(120) NOT NULL UNIQUE,

	start_shift TIME,
	end_shift TIME,

	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (patient_id) REFERENCES patient(id)
);

-- patient table definition
CREATE TABLE IF NOT EXISTS patient (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
    name TEXT(120) NOT NULL UNIQUE,
    birth DATE,

	FOREIGN KEY (user_id) REFERENCES user(id)
);

-- alarm table definition
CREATE TABLE IF NOT EXISTS alarm (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	patient_id INTEGER,
	event_id INTEGER,
	alarm_time TIME,

	FOREIGN KEY (patient_id) REFERENCES patient(id),
	FOREIGN KEY (event_id) REFERENCES event(id)
);

-- event table definition
CREATE TABLE IF NOT EXISTS event (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT(120) UNIQUE,
	is_input INTEGER DEFAULT (0)
);

-- historic table definition
CREATE TABLE IF NOT EXISTS historic (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	patient_id INTEGER,
    log_datetime DATETIME,
	log_message TEXT(300),
	FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

-- device table definition
CREATE TABLE IF NOT EXISTS device (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	patient_id INTEGER,

	name TEXT(100) NOT NULL,
	
	event_button_1 INTEGER,
	event_button_2 INTEGER,
	event_button_3 INTEGER,

	FOREIGN KEY (patient_id) REFERENCES patient(id),
	FOREIGN KEY (event_button_1) REFERENCES event(id),
	FOREIGN KEY (event_button_2) REFERENCES event(id),
	FOREIGN KEY (event_button_3) REFERENCES event(id)
);

--########################################################
--#          DADOS DE "REAIS" PARA PRODUÇÃO              #
--########################################################

INSERT OR IGNORE INTO user (email, password, is_admin) VALUES
('root@root.com', 'root', 1),
('marcos@root.com', 'root', 1),
('castilho@root.com', 'root', 1),
('user@user.com', 'user', 0),
('caco@alternativac.com.br', 'EstudoUnivesp123', 0);

INSERT OR IGNORE INTO event (description, is_input) VALUES
('Micção', 1),
('Defecação', 1),
('Aspiração de tráqueo', 1),
('Drenagem', 1),
('Paciente Adormeceu', 1),
('Paciente Acordou', 1),
('Remedio A', 0),
('Remedio B', 0),
('Remedio C', 0),
('Remedio D', 0),
('Remedio E', 0),
('Fisioterapia', 0);

