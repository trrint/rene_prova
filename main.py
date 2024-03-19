from flask import *
import dao

# isntancia o servidor flask
app = Flask(__name__)
app.secret_key = '3j45h3j2k4h5kj3h45h23JHGJHgh'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/inscricao')
def inscricao():
    return render_template('inscricao.html')


@app.route('/cadastrarusuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form.get('nomeusuario')
    idade = request.form.get('idadeusuario')
    email = request.form.get('emailusuario')
    senha = request.form.get('senhausuario')

    if dao.cadastrarusuario(nome, idade, email, senha):
        return render_template('home.html', msg='Usuário inserido com sucesso')
    else:
        return render_template('home.html', msg='Usuário já existe')


@app.route('/verificarlogin', methods=['POST'])
def verificar_login():
    user = request.form.get('emailusuario')
    senha = request.form.get('senhausuario')

    if dao.checarlogin(user, senha):
        session['idusuario'] = user
        return render_template('logado.html', email=user)
    else:
        return render_template('errologin.html')


@app.route('/entraremcontato')
def mostrarpaginacontato():
    if session.get('idusuario') != None:
        return render_template('contato.html', email=session['idusuario'])
    else:
        return render_template('home.html')


@app.route('/inserircontato', methods=['POST', 'GET'])
def inserircontato():
    if request.method == 'POST':
        nome = request.form.get('nome')  # POST
        email = request.form.get('email')
        texto = request.form.get('texto')
        cep = request.form.get('cep')
    else:
        nome = request.args.get('nome')  # GET
        email = request.args.get('email')
        texto = request.args.get('texto')
        cep = request.args.get('cep')

    cep = cep.replace('-', '')
    if dao.registrar_contato(nome, email, texto, cep):
        return render_template('logado.html', msg='Contato inserido com sucesso')
    else:
        # criar pagina de erro de contato
        return render_template('index.html')


@app.route('/listarContatos', methods=['GET', 'POST'])
def listar_contatos():
    if request.method == 'POST':
        ceps_selecionados = request.form.get('ceps')
        contatos = dao.listar_cep(ceps_selecionados.split(','))
    else:
        contatos = dao.listar_contatos()
    return render_template('listarContatos.html', contatos=contatos)


if __name__ == '__main__':
    app.run(debug=True)  # executa/roda/starta o servidor
