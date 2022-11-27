from flask import Flask, redirect, request, jsonify, url_for, session, flash, render_template
import json, requests
from werkzeug.exceptions import abort

app = Flask(__name__)


# criar a primeira pagina do site
# route -- meu dominio /contatos
# funcao -- o que vc quer exibir naquela pagina
# template
# @ decorator -- atribuir uma nova funcionalidade, on   de essa funcao será exibida dentro dessa pagina
@app.route('/index', methods=['POST'])
def index():
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('index.html', userlogin=userlogin)


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def return_login():
    return render_template('login.html')


# CALL
@app.route('/list_call', methods=['POST'])
def list_call():
    try:
        param = request.form.get('pcall')
        if param == "":
            data = requests.get('http://127.0.0.1:5000/list_call').json()
            if 'userlogin' in session:
                userlogin = session['userlogin']
                return render_template('search_call_.html', userlogin=userlogin, data=data)
        else:
            data = requests.post('http://127.0.0.1:5000/find_call/'+param+'/').json()
            if data:
                print("register found!")
            else:
                flash('register not found!')
                return redirect(url_for('search_call_'))
            if 'userlogin' in session:
                userlogin = session['userlogin']
            return render_template('search_call_.html', userlogin=userlogin, data=data, pcall=param)
    except:
        flash('register not found!')
        print("An exception occurred")


@app.route('/search_call_', methods=['POST'])
def search_call_():
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('search_call_.html', userlogin=userlogin)


@app.route('/search_call_')
def return_search_call_():
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('search_call_.html', userlogin=userlogin)


@app.route('/new_call_', methods=['GET', 'POST'])
def new_call_():
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/create_call_'
        my_json = {'id_user': 1, 'id_kind': request.form['id_kind'], 'id_status': 1, 'description': request.form['description']}
        requests.post(url, json=my_json)
        flash('call created!')
        return redirect(url_for('search_call_'))
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('new_call_.html', userlogin=userlogin)


# DELETE CALL
@app.route('/delete_call_/<int:id>')
def delete_call_(id):
    url = 'http://127.0.0.1:5000/delete_call_'
    my_json = {'id': id}
    requests.delete(url, json=my_json)
    flash('call deleted!')
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('search_call_.html', userlogin=userlogin)


@app.route('/update_call_/<int:id>', methods=['POST'])
def update_call_put_(id):
    # PEGAR INFORMAÇÃO NA PAGINA
    if request.method == 'POST':
        id_string = str(id)
        description_ = request.form['description']
        id_status_ = request.form['id_status']
        my_json = {'id': id, 'id_status': id_status_, 'description': description_, 'id_kind': 1, 'id_user': 1}
        url = 'http://127.0.0.1:5000/update_call_/'+(id_string)
        requests.put(url, json=my_json)
        flash('call updated!')
        return redirect(url_for('search_call_'))
    else:
        print('update_call_- não é post')
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('update_call_.html')


@app.route('/update_call_/<int:id>', methods=['GET'])
def update_call_(id):
    # 1 buscar pelo id o objeto
    id_string = str(id)
    url = 'http://127.0.0.1:5000/find_call_id/'+(id_string)
    result = requests.post(url).json()
    # 2 preencher a pagina com o objeto consultado
    id = result.get("id")
    description = result.get("description")
    id_kind = result.get("id_kind")
    id_user = result.get("id_user")
    id_status = result.get("id_status")
    if id_status == 1:
        is_open = True
    else:
        is_open = False
    my_json = {'id': id, 'id_status': id_status, 'description': description, 'id_kind': id_kind, 'id_user': id_user}
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('update_call_.html', userlogin=userlogin, data=my_json, is_open=is_open)


# USER  - ok
@app.route('/list_user', methods=['POST'])
def list_user():
    try:
        param = request.form.get('puser')
        if param == "":
            data = requests.get('http://127.0.0.1:5000/list_user').json()
            if 'userlogin' in session:
                userlogin = session['userlogin']
                return render_template('search_user_.html', userlogin=userlogin, data=data)
        else:
            data = requests.post('http://127.0.0.1:5000/find_user/'+param+'/').json()
            if data:
                print("register found!")
            else:
                flash('register not found!')
                return redirect(url_for('search_user_'))
            if 'userlogin' in session:
                userlogin = session['userlogin']
            return render_template('search_user_.html', userlogin=userlogin, data=data, puser=param)
    except:
        flash('register not found!')
        print("An exception occurred")


@app.route('/search_user_', methods=['POST'])
def search_user_():
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('search_user_.html', userlogin=userlogin)


@app.route('/search_user_')
def return_search_user_():
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('search_user_.html', userlogin=userlogin)


# NEW USER
@app.route('/new_user_', methods=['GET', 'POST'])
def new_user_():
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/create_user_'
        my_json = {'name': request.form['name'], 'login': request.form['login'], 'email': request.form['email'], 'password': request.form['password'],
                   'repeat_password': request.form['repeat_password'], 'id_admin': request.form['id_admin']}
        p = request.form['password']
        rp = request.form['repeat_password']
        if p != rp:
            flash('Password is different!')
        else:
            reques = requests.post(url, json=my_json)
            if reques:
                flash('user created!')
            else:
                flash('created failed!')
        return redirect(url_for('search_user_'))
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('new_user_.html', userlogin=userlogin)


# NEW USER
# @app.route('/new_user_')
# def new_user_():
    #     if 'userlogin' in session:
    #         userlogin = session['userlogin']
    # return render_template('new_user_.html', userlogin=userlogin)


# @app.route("/1")
# def homepage1():
# return "ESTE É MEU PRIMEIRO SITE"


# @app.route("/contatos1")
# def contatos1():
# return "<p>nome: ricardo</p> <p>email:barcelos.java@gmail.com</p> <p>fone: 91447639</p>"


# @app.route("/")
# def homepage():
#    return render_template("homepage.html")


# @app.route("/contatos")
# def contatos():
    # return render_template("contatos.html")


# @app.route("/usuarios1/<nome_usuario>")
# def usuarios1(nome_usuario):
    # return nome_usuario


# @app.route("/usuarios/<nome_usuario>")
# def usuarios(nome_usuario):
    # return render_template("usuarios.html", nome_usuario=nome_usuario)


@app.route("/main", methods=['GET', 'POST'])
def main():
    return render_template("main.html")


@app.route('/layout', methods=['POST'])
def layout():
    # PESQUISAR USER
    usr = request.form.get('vname')
    pas = request.form.get('password')
    data = requests.post('http://127.0.0.1:5000/find_user_login_/'+usr+'/'+pas+'/').json()
    if data:
        usuario = request.form.get('vname')
        return render_template('layout.html', variavel=usuario)
    else:
        flash('Login and Password not found')
        return render_template('login.html')



@app.route('/layout_', methods=['POST'])
def layout_():
    # PESQUISAR USER
    usr = request.form.get('vname').upper()
    pas = request.form.get('password')
    data = requests.get('http://127.0.0.1:5000/find_user_login_/'+usr+'/'+pas+'/').json()

    if data == []:
        flash('Login and Password not found')
        return redirect(url_for('login'))
    else:
        session['userlogin'] = request.form['vname']
        return render_template('layout_.html', userlogin=session['userlogin'])

# @app.route('/teste')
# def teste():
    # if 'userlogin' in session:
        # userlogin = session['userlogin']
    # return render_template('teste.html', userlogin=userlogin)


@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


# UPDATE USER
@app.route('/update_user_/<int:id>', methods=['POST'])
def update_user_put_(id):
    # PEGAR INFORMAÇÃO NA PAGINA
    if request.method == 'POST':
        id_string = str(id)
        name_ = request.form['name']
        login_ = request.form['login']
        email_ = request.form['email']
        id_admin_ = request.form['id_admin']
        password_ = request.form['password']
        repeat_password_ = request.form['repeat_password']
        my_json = {'id': id, 'name': name_, 'login': login_, 'email': email_, 'password': password_, 'repeat_password': repeat_password_, 'id_admin': id_admin_}
        url = 'http://127.0.0.1:5000/update_user_/'+(id_string)
        print('UPDATE FEITO APP')
        if password_ != repeat_password_:
            flash('Password is different!')
        else:
            reques = requests.put(url, json=my_json)
            if reques:
                flash('user updated!')
            else:
                flash('updated failed!')
        return redirect(url_for('search_user_'))
    else:
        print('update_user_- não é post')
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('update_user_.html')


# UPDATE USER
@app.route('/update_user_/<int:id>', methods=['GET'])
def update_user_(id):
    print('ENTREI NO UPDATE')
    # 1 buscar pelo id o objeto
    id_string = str(id)
    url = 'http://127.0.0.1:5000/find_user_id/'+(id_string)
    result = requests.post(url).json()
    # 2 preencher a pagina com o objeto consultado
    id = result.get("id")
    name = result.get("name")
    login = result.get("login")
    email = result.get("email")
    id_admin = result.get("id_admin")
    if id_admin == 1:
        is_open = True
    else:
        is_open = False
    password = result.get("password")
    repeat_password = result.get("repeat_password")
    my_json = {'id': id, 'name': name, 'login': login, 'email': email, 'id_admin': id_admin, 'password': password, 'repeat_password': repeat_password}
    if 'userlogin' in session:
        userlogin = session['userlogin']
    return render_template('update_user_.html', userlogin=userlogin, data=my_json, is_open=is_open)


# DELETE USER
@app.route('/delete_user_/<int:id>')
def delete_user_(id):
        url = 'http://127.0.0.1:5000/delete_user_'
        my_json = {'id': id}
        reques = requests.delete(url, json=my_json)
        if reques:
            flash('user deleted!')
        else:
            flash('delete failed!')
        if 'userlogin' in session:
            userlogin = session['userlogin']
            return render_template('search_user_.html', userlogin=userlogin)


#  colocar o site no ar
if __name__ == "__main__":
    # CONFIGURATION TO USER SESSION
    app.secret_key = 'super secret key'
    app.run(port=8085, debug=True, threaded=True)
    # Executa a aplicação na porta 8085, vc poderá mudar tb para outro valor dentro o espectro permitido.
    # app.run(debug=True)