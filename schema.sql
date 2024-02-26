-- usuario definition
CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT(300),
	password TEXT(64),
	is_admin INTEGER DEFAULT (0),
	CONSTRAINT usuario_un UNIQUE (email)
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