from flask import Flask, render_template \
    , url_for, request, redirect

from flask_login import LoginManager \
    , login_required, login_user, logout_user, current_user

from models import User, obter_conexao

from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)

# quando precisar saber qual o usuario conectado
# temos como consultar ele no banco

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['pass']
        
        user = User.get_by_matricula(matricula)
        
        if user:

            aux = check_password_hash(user.senha,senha)

            if user and aux == True:
                
                login_user(user)

                return render_template('dash.html')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        
        #Gerar hash de uma string:
        #generate_password_hash('string')

        #Comparar hash e string:
        #check_password_hash(hash, 'string')

        matricula = request.form['matricula']

        email = request.form['email']
        email = generate_password_hash(email)

        senha = request.form['pass']
        senha = generate_password_hash(senha)

        conexao = obter_conexao()
        INSERT = 'INSERT INTO usuarios(matricula,email,senha) VALUES (?,?,?)'
        conexao.execute(INSERT, (matricula,email,senha))
        conexao.commit()
        conexao.close()

        user = User.get_by_email(email)
        
        if user and user.senha == senha:
            
            login_user(user)

            return render_template('dash.html')

    return render_template('register.html')

@app.route('/dash', methods=['POST'])
@login_required
def dash():

    if request.method == 'POST':

        #user = User.get_by_matricula(matricula)

        matricula = current_user.id
        exercicio = request.form['exercicio']
        descricao = request.form['descricao']

        conexao = obter_conexao()
        INSERT = 'INSERT INTO exercicios(matricula, exercicio, descricao) VALUES (?,?,?)'
        conexao.execute(INSERT, (matricula, exercicio, descricao))
        conexao.commit()
        conexao.close()


    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/listarexercicios', methods=['POST'])
def listar():

    if request.method == 'POST':

        return redirect(url_for('listar'))
    
    return render_template('listar')
