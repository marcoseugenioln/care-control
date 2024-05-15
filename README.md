
### Instalando ambiente
- Instalar [Python](https://www.python.org/downloads/)
- Instalar [Git](https://git-scm.com/downloads)

- Abrir o prompt de comando e clonar o repositório usando o comando:
```bash
    git clone https://github.com/marcoseugenioln/care-control.git
```

- Abrir o prompt de comando na pasta do repositório e executar o comando:
```bash
    pip install -r requirements.txt
```

### Executando Aplicação
- no arquivo `config.json` sao mantidas as configuracoes
```json
    {
        "host" : "192.168.1.6", -> ip do computador que vai hospedar a aplicacao
        "port" : 3000, -> porta a ser usado
        "debug"  : false, -> modo debug do flask
        "schema" : "server/src/schema.sql", -> schema do banco de dados
        "database" : "server/src/schema.db", -> arquivo do banco de dados
        "log_file" : "site-log.log" -> arquivo de log
    }
```
- Abrir o terminal na pasta do repositório e executar o comando:
```bash
   run_test config.json
```

- Abrir o navegador e inserir  a url http://`host`:`port`/ como configurado

## GIT
Dicas de como usar o git:

### Clonar o repositorio (dowload para trabalho)
```bash
    git clone https://github.com/marcoseugenioln/care-control.git
```

### Criando a area de trabalho pessoal
```bash
    git branch <nome_do_branch>
    git checkout <nome_do_branch>
```
### Adicionando conteúdo

### Listar o que mudou
```bash
    git status 
```
### Adicionar mudanca
```bash
    git add <nome_do_arquivo>
```

### Salvar trabalho local
```bash
    git commit -a -m "Esplicação do que mudou"
```
### Salvar na github
Precisa ser cadastrado como contribuinte do projeto
```bash
    git push
```
