-- usuario definition
CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT(300),
	password TEXT(64),
	is_admin INTEGER DEFAULT (0),
	CONSTRAINT usuario_un UNIQUE (email)
);

CREATE TABLE acompanhado (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
    nome TEXT(120) NOT NULL,
    datanasc TEXT(10),
    acompanhante TEXT(200),
	CONSTRAINT acompanhado_un UNIQUE (nome),
	CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE historico (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
    data TEXT(19),
    log TEXT(250) NOT NULL,
	CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE dispositivo (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	acompanhando_id INTEGER,
	guid TEXT(36) NOT NULL,
	nome TEXT(50) NOT NULL,
	alarme1_tme TEXT(5),
	alarme1_log TEXT(50),
	alarme1_evt INTEGER(1),
	alarme2_tme TEXT(5),
	alarme2_log TEXT(50),
	alarme2_evt INTEGER(1),
	alarme3_tme TEXT(5),
	alarme3_log TEXT(50),
	alarme3_evt INTEGER(1),
	alarme4_tme TEXT(5),
	alarme4_log TEXT(50),
	alarme4_evt INTEGER(1),
	alarme5_tme TEXT(5),
	alarme5_log TEXT(50),
	alarme5_evt INTEGER(1),
	evento1_log TEXT(50),
	evento2_log TEXT(50),
	evento3_log TEXT(50),
	CONSTRAINT dispositivo_un UNIQUE (guid),
	CONSTRAINT dispositivo_un2 UNIQUE (user_id, nome),
	CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user(id),
	CONSTRAINT acompanhado_fk FOREIGN KEY (acompanhando_id) REFERENCES acompanhado(id)
);


--########################################################
--#          DADOS DE "REAIS" PARA PRODUÇÃO              #
--########################################################

INSERT OR IGNORE INTO user (email, password, is_admin) VALUES 
('root@root.com', 'root', 1),
('marcos@root.com', 'root', 1),
('castilho@root.com', 'root', 1),
('user@user.com', 'user', 0),
('caco@alternativac.com.br', 'EstudoUnivesp123', 1);


