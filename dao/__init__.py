import requests
import psycopg2


def conectarDB():
    return connect_cloud()


def conectar_localBD():
    con = psycopg2.connect(
        host='localhost',
        database='compila',
        user='postgres',
        password='admin'
    )

    return con


def connect_cloud():
    con = psycopg2.connect(
        host='dpg-cnqu14uct0pc73cpbt20-a.oregon-postgres.render.com',
        database='compilacloud',
        user='compilacloud_user',
        password='1qw4gv3Mmh1eIQc5JK4LXgqgamx4zw8Q'
    )

    return con


def verificarUsuarioExistente(email):
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute(f"select count(*) from usuarios where email = '{email}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False


def verificarContatoExistente(email):
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute(f"select count(*) from contato where email = '{email}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False


def cadastrarusuario(nome, idade, email, senha):
    if not verificarUsuarioExistente(email):
        conexao = conectarDB()
        cur = conexao.cursor()
        try:
            sql = f"INSERT INTO usuarios (nome, idade, email, senha) VALUES ('{nome}', '{idade}', '{email}', '{senha}' )"
            cur.execute(sql)
        except psycopg2.IntegrityError:
            conexao.rollback()
            exito = False
        else:
            conexao.commit()
            exito = True

        conexao.close()
        return exito
    else:
        return False


def checarlogin(email, senha):
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute(f"select count(*) from usuarios where email = '{email}' and senha ='{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False


def cadastrarusuario_antigo(users: list, nome, idade, email, senha):
    novousuario = {'nome': nome, 'idade': idade, 'email': email, 'senha': senha}
    if not usuarioexiste(users, email):
        users.append(novousuario)
        return True  # deu certo inserir o novo usuario no banco
    else:
        return False  # deu ruim pq ja tinha um user com este email


def usuarioexiste(users: list, email):
    for user in users:
        if user['email'] == email:
            return True  # já existe um usuario com este login
    return False  # nao existe ninguem com este login


def registrar_contato(nome, email, comentario, cep):
    conexao = conectarDB()
    cur = conexao.cursor()

    endereco = requests.get(f'https://api.brasilaberto.com/v1/zipcode/{cep}').json()
    rua = endereco['result']['street']
    cidade = endereco['result']['city']
    estado = endereco['result']['state']

    if not verificarContatoExistente(email):
        conexao = conectarDB()
        cur = conexao.cursor()
        try:
            sql = f"INSERT INTO contato (nome, email, cep, mensagem) VALUES ('{nome}', '{email}', '{cep}', '{comentario}')"
            cur.execute(sql)
        except psycopg2.IntegrityError:
            conexao.rollback()
            exito = False
        else:
            conexao.commit()
            exito = True

        conexao.close()
        return exito
    else:
        return False

    print(f'{rua}')
    print(f'Cidade: {cidade}')
    print(f'Cidade: {estado}')

    return True


def listar_contatos():
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute("SELECT * FROM contato")
    contatos = cur.fetchall()
    conexao.close()
    return contatos


def listar_cep(ceps):
    if not ceps or ceps == ['']:
        return listar_contatos()
    else:
        conexao = conectarDB()
        cur = conexao.cursor()
        ceps_str = '-'.join([f"'{cep.strip()}'" for cep in ceps])
        cur.execute(f"SELECT * FROM contato WHERE cep IN ({ceps_str})")
        contatos = cur.fetchall()
        conexao.close()
        return contatos
