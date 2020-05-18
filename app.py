from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import json
from time import time
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Frida123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://javi:javiersolis12@localhost:3306/tuti'

#Configuracion del objeto mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ccmcomteco@gmail.com'  #Cambiar por algun usuario valido
app.config['MAIL_PASSWORD'] = 'javiersolis12'                  #Cambiar por el password correcto
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


mail = Mail(app)

class tecnicos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80))
    apellido = db.Column(db.String(80))
    num_carnet = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(50), unique = True)
    num_cel = db.Column(db.String(8), unique = True)

class administradores(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80))
    apellido = db.Column(db.String(80))
    num_carnet = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(50), unique = True)
    num_cel = db.Column(db.String(8), unique = True)
    password = db.Column(db.String(200))

class ahora(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    temperatura = db.Column(db.Float())
    humedad = db.Column(db.Float())
    canal1 = db.Column(db.Float())
    canal2 = db.Column(db.Float())
    canal3 = db.Column(db.Float())
    canal4 = db.Column(db.Float())
    tempGabinete = db.Column(db.Float())
    hora = db.Column(db.Time())

class alarmas(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codigo = db.Column(db.String(10))
    descripcion = db.Column(db.String(200))
    hora_inicial = db.Column(db.Time())
    fec_inicial = db.Column(db.Date())
    estado = db.Column(db.String(10))
    estado_email = db.Column(db.String(20))

class todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    temperatura = db.Column(db.Float())
    humedad = db.Column(db.Float())
    canal1 = db.Column(db.Float())
    canal2 = db.Column(db.Float())
    canal3 = db.Column(db.Float())
    canal4 = db.Column(db.Float())
    tempGabinete = db.Column(db.Float())
    hora = db.Column(db.Time())
    fecha = db.Column(db.Date())

class regresion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    x1 = db.Column(db.Float())
    x2 = db.Column(db.Float())
    y = db.Column(db.Float())
    xx = db.Column(db.Float())
    x1y = db.Column(db.Float())
    x2y = db.Column(db.Float())
    x1x2 = db.Column(db.Float())
    x2x2 = db.Column(db.Float())
    yy = db.Column(db.Float())

@login_manager.user_loader
def load_user(user_id):
    return administradores.query.get(int(user_id))

class LoginForm(FlaskForm):
    email =     StringField('email',        validators=[InputRequired(), Length(min=4, max=15)])
    password =  PasswordField('password',   validators=[InputRequired(), Length(min=2, max=80)])

class RegisterForm(FlaskForm):
    nombre =    StringField('Nombre',                   validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    apellido =  StringField('Apellido',                 validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    ci =        StringField('Carnet de Identidad',      validators =    [InputRequired(),                                       Length(min = 4, max = 20)])
    email =     StringField('email',                    validators =    [InputRequired(), Email(message='Email Invalido'),      Length(max=50)])
    cel =       StringField('Numero de Celular',        validators =    [InputRequired()])
    password =  PasswordField('password',               validators =    [InputRequired(),                                       Length(min=8, max=80)])

@app.route('/')
@login_required
def index():
    return render_template('index.html', name = current_user.nombre, notificaciones = 0, titulo = "DASHBOARD TUTI")

@app.route('/datos', methods=["GET", "POST"])
def data1():
    datos = ahora.query.first()
    Alarmas = alarmas.query.filter_by(estado='activo').all()
    contador = 0
    for alarma in Alarmas:
        contador += 1
    data = [datos.temperatura,
            datos.humedad,
            datos.canal1,
            datos.canal2,
            datos.canal3,
            datos.canal4,
            datos.tempGabinete,
            contador,
            (time() - 14400) * 1000]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/datosJSON/<fec>/', methods=['GET', 'POST'])
def ValoresJson(fec):
    xData = []
    data0 = []
    data1 = []
    data2 = []
    SalidaDatos = {}
    Datos = todo.query.filter_by(fecha=fec).all()
    for dato in Datos:
        aux = dato.hora
        NumeroHoras = int(aux.hour) + (int(aux.minute) / 100)
        xData.append(NumeroHoras)
        data0.append(dato.canal1)
        data1.append(dato.temperatura)
        data2.append(dato.humedad)
    SalidaDatos = {
        "xData": xData,
        "datasets": [{
            "name": "Potencia Recepción",
            "data": data0,
            "unit": "[V]",
            "type": "line",
            "valueDecimals": 1
        }, {
            "name": "Temperatura",
            "data": data1,
            "unit": "°C",
            "type": "line",
            "valueDecimals": 0
        }, {
            "name": "Humedad",
            "data": data2,
            "unit": "%",
            "type": "line",
            "valueDecimals": 0
        }]
    }
    return jsonify(SalidaDatos)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = administradores.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', mensaje = 'Email o password incorrecto', titulo = "Iniciar Sesión")            
    else:
        return render_template('login.html', titulo = "Iniciar Sesión")

@app.route('/RegAdmin', methods=['GET', 'POST'])

def Registrar_Administradores():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = administradores(
                                    nombre = form.nombre.data, 
                                    apellido = form.apellido.data, 
                                    num_carnet = form.ci.data, 
                                    email = form.email.data, 
                                    num_cel = form.cel.data, 
                                    password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('registrar.html', form = form, mensaje = 'Se creo exitosamente el Administrador', titulo = "Registrar Administrador")
    else:
        return render_template('registrar.html', form = form, titulo = "Registrar Administrador")

@app.route('/VistaEmails', methods = ['GET', 'POST'])
@login_required
def VistaEmails():
    if request.method == 'GET':
        Tecnicos = tecnicos.query.all()
        return render_template('VistaEmails.html', tecnicos = Tecnicos, name = current_user.nombre, titulo = "Enviar Email")
    else:
        msg = Message(request.form['asunto'], sender = 'ccmcomteco@gmail.com', recipients = request.form.getlist('emails'))
        msg.html = request.form['mensaje']
        mail.send(msg)
        Tecnicos = tecnicos.query.all()
        return render_template('VistaEmails.html', mensaje = 'Se envio satisfactoriamente el email', name = current_user.nombre, tecnicos = Tecnicos, titulo = 'Enviar Emails')

@app.route('/prueba')
def prueba():
    return render_template('template_email.html')

@app.route('/RegTec', methods = ['GET','POST'])
@login_required
def RegistroTecnicos():
    if request.method == 'GET':
        Todos_Tecnicos = tecnicos.query.all()
        return render_template('VistaRegistro.html', tecnicos = Todos_Tecnicos, name = current_user.nombre, titulo = "Registrar Técnicos")
    else:
        Nombre = request.form['nombre']
        Apellido = request.form['apellido']
        Num_carnet = request.form['carnet']
        Email = request.form['email']
        Num_cel = request.form['celular']
        Todos_Tecnicos = tecnicos.query.all()
        if Todos_Tecnicos:
            for tech in Todos_Tecnicos:
                if tech.nombre == Nombre or tech.apellido == Apellido or tech.num_carnet == Num_carnet or tech.email == Email or tech.num_cel == Num_cel:
                    return render_template('VistaRegistro.html', msg = 'No se pudo registrar, Datos ya utilizados', name = current_user.nombre, titulo = "Registrar Técnicos", tecnicos = Todos_Tecnicos)
                else:
                    nuevo_Tecnico = tecnicos(
                                                nombre = request.form['nombre'],
                                                apellido = request.form['apellido'],
                                                num_carnet = request.form['carnet'],
                                                email = request.form['email'],
                                                num_cel = request.form['celular'])
                    db.session.add(nuevo_Tecnico)
                    db.session.commit()
                    todos_Tecnicos = tecnicos.query.all()
                    return render_template('VistaRegistro.html', mensaje = 'Se agrego satisfactoriamente el Técnico', name = current_user.nombre, titulo = "Registrar Técnicos", tecnicos = todos_Tecnicos)
        else:
            nuevo_Tecnico = tecnicos(
                                                nombre = request.form['nombre'],
                                                apellido = request.form['apellido'],
                                                num_carnet = request.form['carnet'],
                                                email = request.form['email'],
                                                num_cel = request.form['celular'])
            db.session.add(nuevo_Tecnico)
            db.session.commit()
            Todos_Tecnicos = tecnicos.query.all()
            return render_template('VistaRegistro.html', mensaje = 'Se agrego satisfactoriamente el Técnico', name = current_user.nombre, tecnicos = Todos_Tecnicos, titulo = "Registrar Técnicos")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete/<id>')
@login_required
def delete(id):
    tecnicos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('RegistroTecnicos'))

@app.route('/alarmas')
@login_required
def Alarmas():
    Alarmas = alarmas.query.filter_by(estado='activo').all()
    return render_template('alarmas.html', alm = Alarmas, titulo = "Alarmas", name = current_user.nombre)

@app.route('/graf/diarios')
@login_required
def GraDiarios():
    return render_template('diarios.html', titulo = "Gráficos Díarios", name = current_user.nombre)

@app.route('/graf/regresion', methods = ['GET','POST'])
@login_required
def Regresion():
    regresion.query.delete()
    sumatorias = [0,0,0,0,0,0,0,0,0,0]
    cont = 0
    DatosTemp = []
    DatosHum = []
    #Seleccionamos todos los datos de la tabla todo
    DatosTodo = todo.query.all()
    #Hacemos la insercion de los datos para la regrion en dicha tabla
    for dato in DatosTodo:
        #Creamos dos listas DatosTemp y DatosHum para devolver a la vista
        DatosTemp.append([dato.temperatura, dato.canal1]) 
        DatosHum.append([dato.canal1, dato.humedad])
    #Metodo GET
    if request.method == 'GET':
        return render_template('regresion.html', titulo = "Regresion Lineal", name = current_user.nombre, temp = DatosTemp, hum = DatosHum, aux = 0)
    #Metodo POST
    else:
        cantidad = 0
        #Recolectamos los datos de temperatura y humedad de la vista
        temp = request.form['temperatura']
        hum = request.form['humedad']
        #Hacemos la insercion de los datos para la regrion en dicha tabla
        for dato in DatosTodo:
            nuevaRegresion = regresion(
                                        x1 = dato.temperatura,
                                        x2 = dato.humedad,
                                        y = dato.canal1,
                                        xx = (dato.temperatura * dato.temperatura),
                                        x1y = (dato.temperatura * dato.canal1),
                                        x2y = (dato.humedad * dato.canal1),
                                        x1x2 = (dato.temperatura * dato.humedad),
                                        x2x2 = (dato.humedad * dato.humedad),
                                        yy = (dato.canal1 * dato.canal1)
            )
            db.session.add(nuevaRegresion)
        #Confirmamos la insercion de los datos
        db.session.commit()
        #Seleccionamos todas las filas de la tabla regresion que fueron llenadas previamente
        DatosRegresion = regresion.query.all() 
        #Hacemos la Sumatoria de todas las columnas en una lista llamada sumatorias
        for i in DatosRegresion:
            sumatorias = [
                            sumatorias[0] + i.x1, 
                            sumatorias[1] + i.x2,
                            sumatorias[2] + i.y,
                            sumatorias[3] + i.xx,
                            sumatorias[4] + i.x1y,
                            sumatorias[5] + i.x2y,
                            sumatorias[6] + i.x1x2,
                            sumatorias[7] + i.x2x2,
                            sumatorias[8] + i.yy
                        ]
            cont += 1
        #Creamos la matriz A donde estan las incognitas
        A = np.array([
            [cont,sumatorias[0],sumatorias[1]],
            [sumatorias[0],sumatorias[3],sumatorias[6]],
            [sumatorias[1],sumatorias[6],sumatorias[7]]
        ])
        #Creamos la matriz resultado
        R = np.array([
            [sumatorias[2]],
            [sumatorias[4]],
            [sumatorias[5]]
        ])
        A_determinante = np.linalg.det(A)
        #Si el determinante de A es diferente de cero el sistema de ecuaciones tiene solución
        if A_determinante != 0:
            #Calculamos la matriz inversa
            A_inversa = np.linalg.inv(A)
            #Multiplicamos la matriz inversa de A con la matriz resultados
            Matriz_Resultado = np.dot(A_inversa,R)
            resp_aprox = round(Matriz_Resultado[0][0] + (Matriz_Resultado[1][0] * float(temp)) + (Matriz_Resultado[2][0] * float(hum)), 3)
        else:
            #Si la determinante es cero el sistema no tiene Solución
            A_inversa = 0
            Matriz_Resultado = 0
        FiltroDatos = todo.query.filter_by(temperatura = float(temp), humedad = float(hum)).all()
        aux1 = 0
        for x in FiltroDatos:
            if round(x.canal1,2) == round(resp_aprox,2):
                aux1 += 1    
            cantidad += 1
        if cantidad == 0:
            porcentaje = 0
        else:
            porcentaje = (aux1 / cantidad) * 100
        return render_template(
            'regresion.html',
            titulo = "Regresion Lineal",
            name = current_user.nombre,
            temp = DatosTemp,
            hum = DatosHum,
            sumas = sumatorias,
            resp = Matriz_Resultado,
            x1_prom = round((sumatorias[0] / cont), 3),
            x2_prom = round((sumatorias[1] / cont), 3),
            y_prom = round((sumatorias[2]),3),
            tempe = temp,
            hume = hum,
            determinante = A_determinante,
            aux = 1,
            result_aproximado = resp_aprox,
            porcentaje = porcentaje
            )


@app.errorhandler(404)
def not_found(e):
    Alarmas = alarmas.query.filter_by(estado='activo').all()
    return render_template("404.html", titulo = "Error 404 No encontrado", name = current_user.nombre)   
    

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')