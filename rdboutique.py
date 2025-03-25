from flask import Flask, render_template, url_for,request,redirect,flash
from config import config
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash 
from datetime import datetime

rdboutique = Flask(__name__)
db         = MySQL(rdboutique)
adminSesion = LoginManager(rdboutique)

@adminSesion.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(db,id)

@rdboutique.route('/')
def home():
    return render_template('home.html')

@rdboutique.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        telefono = request.form['telefono']
        fechareg = datetime.now()
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario(nombre,correo,clave,telefono,fechareg) VALUES (%s,%s,%s,%s,%s)",(nombre,correo,claveCifrada,telefono,fechareg))
        db.connection.commit()
        regUsuario.close()
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

@rdboutique.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        usuario = User(0,None,request.form['correo'], request.form['clave'], None, None, None)
        usuarioAutenticado = ModelUser.signin(db,usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                flash('Contraseña Incorrecta')
                return redirect(request.url)
        else:
            flash('Correo inexistente')
            return redirect(request.url)
    else:
        
        return render_template('signin.html')

@rdboutique.route('/signout',methods=['GET','POST'])
def signout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    rdboutique.config.from_object(config['development'])
    rdboutique.run(port=3300)