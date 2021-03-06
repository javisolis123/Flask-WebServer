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
import csv
from datetime import date
import time
import datetime


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

class juno(db.Model):
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

def ConvertirHora(hora,minuntos,segundos):
    resultado1 = hora * 3600
    resultado2 = minuntos * 60
    respuesta = resultado1 + resultado2 + segundos
    return respuesta

def promedios(datos, anio):
    tempe = [0,0,0,0,0,0,0,0,0,0,0,0]
    hume = [0,0,0,0,0,0,0,0,0,0,0,0]
    trans = [0,0,0,0,0,0,0,0,0,0,0,0]
    gab = [0,0,0,0,0,0,0,0,0,0,0,0]
    cont = [0,0,0,0,0,0,0,0,0,0,0,0]
    temperatura = [0,0,0,0,0,0,0,0,0,0,0,0]
    humedad = [0,0,0,0,0,0,0,0,0,0,0,0]
    Tx = [0,0,0,0,0,0,0,0,0,0,0,0]
    TempGab = [0,0,0,0,0,0,0,0,0,0,0,0]
    for dato in datos:
        if ((dato.fecha >= date(year=anio, month=1, day =1)) and (dato.fecha <= date(year=anio, month=1, day =31))):  #Enero
            tempe[0] = tempe[0] + dato.temperatura
            hume[0] = hume[0] + dato.humedad
            trans[0] = trans[0] + dato.canal1
            gab[0] = gab[0] + dato.tempGabinete
            cont[0] = cont[0] + 1
        if ((dato.fecha >= date(year=anio, month=2, day =1)) and (dato.fecha <= date(year=anio, month=2, day =28))):  #Febrero
            tempe[1] = tempe[1] + dato.temperatura
            hume[1] = hume[1] + dato.humedad
            trans[1] = trans[1] + dato.canal1
            gab[1] = gab[1] + dato.tempGabinete
            cont[1] = cont[1] + 1
        if ((dato.fecha >= date(year=anio, month=3, day =1)) and (dato.fecha <= date(year=anio, month=3, day =31))):  #Marzo
            tempe[2] = tempe[2] + dato.temperatura
            hume[2] = hume[2] + dato.humedad
            trans[2] = trans[2] + dato.canal1
            gab[2] = gab[2] + dato.tempGabinete
            cont[2] = cont[2] + 1
        if ((dato.fecha >= date(year=anio, month=4, day =1)) and (dato.fecha <= date(year=anio, month=4, day =30))):  #Abril
            tempe[3] = tempe[3] + dato.temperatura
            hume[3] = hume[3] + dato.humedad
            trans[3] = trans[3] + dato.canal1
            gab[3] = gab[3] + dato.tempGabinete
            cont[3] = cont[3] + 1
        if ((dato.fecha >= date(year=anio, month=5, day =1)) and (dato.fecha <= date(year=anio, month=5, day =31))):  #Mayo
            tempe[4] = tempe[4] + dato.temperatura
            hume[4] = hume[4] + dato.humedad
            trans[4] = trans[4] + dato.canal1
            gab[4] = gab[4] + dato.tempGabinete
            cont[4] = cont[4] + 1
        if ((dato.fecha >= date(year=anio, month=6, day =1)) and (dato.fecha <= date(year=anio, month=6, day =30))):   #Junio
            tempe[5] = tempe[5] + dato.temperatura
            hume[5] = hume[5] + dato.humedad
            trans[5] = trans[5] + dato.canal1
            gab[5] = gab[5] + dato.tempGabinete
            cont[5] = cont[5] + 1
        if ((dato.fecha >= date(year=anio, month=7, day =1)) and (dato.fecha <= date(year=anio, month=7, day =31))):  #Julio
            tempe[6] = tempe[6] + dato.temperatura
            hume[6] = hume[6] + dato.humedad
            trans[6] = trans[6] + dato.canal1
            gab[6] = gab[6] + dato.tempGabinete
            cont[6] = cont[6] + 1
        if ((dato.fecha >= date(year=anio, month=8, day =1)) and (dato.fecha <= date(year=anio, month=8, day =31))):  #Agosto
            tempe[7] = tempe[7] + dato.temperatura
            hume[7] = hume[7] + dato.humedad
            trans[7] = trans[7] + dato.canal1
            gab[7] = gab[7] + dato.tempGabinete
            cont[7] = cont[7] + 1
        if ((dato.fecha >= date(year=anio, month=9, day =1)) and (dato.fecha <= date(year=anio, month=9, day =30))):  #Septiembre
            tempe[8] = tempe[8] + dato.temperatura
            hume[8] = hume[8] + dato.humedad
            trans[8] = trans[8] + dato.canal1
            gab[8] = gab[8] + dato.tempGabinete
            cont[8] = cont[8] + 1
        if ((dato.fecha >= date(year=anio, month=10, day =1)) and (dato.fecha <= date(year=anio, month=10, day =31))):  #Octubre
            tempe[9] = tempe[9] + dato.temperatura
            hume[9] = hume[9] + dato.humedad
            trans[9] = trans[9] + dato.canal1
            gab[9] = gab[9] + dato.tempGabinete
            cont[9] = cont[9] + 1
        if ((dato.fecha >= date(year=anio, month=11, day =1)) and (dato.fecha <= date(year=anio, month=11, day =30))):  #Noviembre
            tempe[10] = tempe[10] + dato.temperatura
            hume[10] = hume[10] + dato.humedad
            trans[10] = trans[10] + dato.canal1
            gab[10] = gab[10] + dato.tempGabinete
            cont[10] = cont[10] + 1
        if ((dato.fecha >= date(year=anio, month=12, day =1)) and (dato.fecha <= date(year=anio, month=12, day =31))):  #Diciembre
            tempe[11] = tempe[11] + dato.temperatura
            hume[11] = hume[11] + dato.humedad
            trans[11] = trans[11] + dato.canal1
            gab[11] = gab[11] + dato.tempGabinete
            cont[11] = cont[11] + 1
    for x in range(11):
        if (tempe[x] > 0):
            temperatura[x] = tempe[x] / cont[x]
        else:
            temperatura[x] = 0
        if(hume[x] > 0):
            humedad[x] = hume[x] / cont[x]
        else:
            humedad[x] = 0
        if(trans[x] > 0):
            Tx[x] = trans[x] / cont[x]
        else:
            Tx[x] = 0
        if(gab[x] > 0):
            TempGab[x] = gab[x] / cont[x]
        else:
            TempGab[x] = 0
    return temperatura,humedad,Tx, TempGab


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
    Txultimas = []
    tempUltima = []
    humUltima = []
    tG = []
    datos = todo.query.all()
    anio = int(time.strftime("%Y"))
    PromTemp,PromHum,PromTx,tempGab = promedios(datos,anio)
    ultimas_24hrs = (datetime.date.today()) - datetime.timedelta(days=1)
    ahoras = todo.query.filter_by(fecha = str(ultimas_24hrs))
    for x in ahoras:
        tempUltima.append(x.temperatura)
        humUltima.append(x.humedad)
        Txultimas.append(x.canal1)
        tG.append(x.tempGabinete)
    #return render_template('index.html', name = current_user.nombre, notificaciones = 0, titulo = "DASHBOARD TUTI")
    return render_template(
        'index.html', 
        name = current_user.nombre, 
        temp = PromTemp, 
        hum = PromHum, 
        Tx = PromTx, 
        TempGab = tempGab, 
        ultimasTx = Txultimas, 
        ultimasTemp = tempUltima, 
        ultimasHum = humUltima,
        ultimasGab = tG,
        notificaciones = 0,
        titulo = "DASHBOARD TUTI")

@app.route('/datos', methods=["GET", "POST"])
def data1():
    datos = ahora.query.first()
    Alarmas = alarmas.query.filter_by(estado='activo').all()
    contador = 0
    for alarma in Alarmas:
        contador += 1
    tiempo = ConvertirHora(int(time.strftime("%H")),int(time.strftime("%M")),int(time.strftime("%S")))
    data = [datos.temperatura,
            datos.humedad,
            datos.canal1,
            datos.canal2,
            datos.canal3,
            datos.canal4,
            datos.tempGabinete,
            contador,
            (tiempo * 1000)]
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
    else:
        #Si la determinante es cero el sistema no tiene Solución
        A_inversa = 0
        Matriz_Resultado = 0
    #Metodo GET
    if request.method == 'GET':
        return render_template('regresion.html', titulo = "Regresion Lineal", name = current_user.nombre, Respuesta = Matriz_Resultado, determinante = A_determinante, metodo = "get")
    #Metodo POST
    else:
        cantidad = 0
        #Recolectamos los datos de temperatura y humedad de la vista
        temp = request.form['temperatura']
        hum = request.form['humedad']
        y = float(Matriz_Resultado[0]) + (float(temp) * float(Matriz_Resultado[1])) + (float(hum) * float(Matriz_Resultado[2]))
        return render_template(
            'regresion.html',
            titulo = "Regresion Lineal Juno",
            name = current_user.nombre,
            determinante = A_determinante,
            Respuesta = Matriz_Resultado,
            resultado_regresion = y,
            metodo = "post"
            )


@app.errorhandler(404)
def not_found(e):
    #Alarmas = alarmas.query.filter_by(estado='activo').all()
    return render_template("404.html", titulo = "Error 404 No encontrado", name = current_user.nombre)   
    
@app.route('/cargardatos')
def uploadcsv():
    return render_template("VcargaJuno.html", titulo = "Cargar datos de Juno", name = current_user.nombre)

@app.route('/upload',methods = ['POST'])
def upload_route_summary():
    if request.method == 'POST':
        data =[]
        # Crear variable donde subira el contenido del archivo
        f = request.files['fileupload']  
        #Guardar informacion en un string
        fstring = f.read()
        #Codificar el texto en UTF-8
        text = fstring.decode("UTF-8")
        for row in csv.DictReader(text.splitlines(), fieldnames=['id', 'temperatura', 'humedad', 'ch1', 'ch2', 'ch3', 'ch4', 'tempGabinete', 'hora', 'fecha']):
            data.append([item[1] for item in row.items()])
        if data:
            DatosJuno = juno.query.all()
            if DatosJuno:
                juno.query.delete()
                db.session.commit()
                for aux in data:
                    nuevoRegistro = juno(
                        id = aux[0],
                        temperatura = aux[1],
                        humedad = aux[2],
                        canal1 = aux[3],
                        canal2 = aux[4],
                        canal3 = aux[5],
                        canal4 = aux[6],
                        tempGabinete = aux[7],
                        hora = aux[8],
                        fecha = aux[9]
                    )
                    db.session.add(nuevoRegistro)
                db.session.commit()
            else:
                for x in data:
                    nuevoRegistro = juno(
                        id = x[0],
                        temperatura = x[1],
                        humedad = x[2],
                        canal1 = x[3],
                        canal2 = x[4],
                        canal3 = x[5],
                        canal4 = x[6],
                        tempGabinete = x[7],
                        hora = x[8],
                        fecha = x[9]
                    )
                    db.session.add(nuevoRegistro)
                db.session.commit()
        else:
            return render_template('VcargaJuno.html', mensaje = 'El archivo .csv esta vacio', name = current_user.nombre, titulo = "Cargar datos de Juno")
    return render_template('VcargaJuno.html', mensaje = 'Se guardaron todos los datos correctamente', name = current_user.nombre, titulo = "Cargar datos de Juno")

@app.route('/dashjuno')
def dashjuno():
    Txultimas = []
    tempUltima = []
    humUltima = []
    tG = []
    datos = juno.query.all()
    anio = int(time.strftime("%Y"))
    PromTemp,PromHum,PromTx,tempGab = promedios(datos,anio)
    ultimas_24hrs = (datetime.date.today()) - datetime.timedelta(days=1)
    ahoras = juno.query.filter_by(fecha = str(ultimas_24hrs))
    for x in ahoras:
        tempUltima.append(x.temperatura)
        humUltima.append(x.humedad)
        Txultimas.append(x.canal1)
        tG.append(x.tempGabinete)
    return render_template(
        'Vdashboardjuno.html', 
        name = current_user.nombre, 
        titulo = 'DASHBOARD JUNO', 
        temp = PromTemp, 
        hum = PromHum, 
        Tx = PromTx, 
        TempGab = tempGab, 
        ultimasTx = Txultimas, 
        ultimasTemp = tempUltima, 
        ultimasHum = humUltima,
        ultimasGab = tG)

@app.route('/graf/juno')
def grafJuno():
    return render_template('VgrafJuno.html', titulo = 'Graficos Juno', name = current_user)

@app.route('/juno/datosJSON/<fec>/', methods=['GET', 'POST'])
def ValoresJsonJuno(fec):
    xData = []
    data0 = []
    data1 = []
    data2 = []
    SalidaDatos = {}
    Datos = juno.query.filter_by(fecha=fec).all()
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

@app.route('/graf/regresionjuno', methods = ['GET','POST'])
def regresionJuno():
    regresion.query.delete()
    sumatorias = [0,0,0,0,0,0,0,0,0,0]
    cont = 0
    cont_aux = 0
    DatosTemp = []
    DatosHum = []
    #Seleccionamos todos los datos de la tabla todo
    DatosTodo = juno.query.all()
    #Hacemos la insercion de los datos para la regrion en dicha tabla
    for dato in DatosTodo:
        cont_aux += 1
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
    else:
        #Si la determinante es cero el sistema no tiene Solución
        A_inversa = 0
        Matriz_Resultado = 0
    #Metodo GET
    if request.method == 'GET':
        return render_template('regresion_juno.html', 
        titulo = "Regresion Lineal", 
        name = current_user.nombre, 
        Respuesta = Matriz_Resultado, 
        determinante = A_determinante, 
        metodo = "get", 
        TamJuno = cont_aux)
    #Metodo POST
    else:
        cantidad = 0
        #Recolectamos los datos de temperatura y humedad de la vista
        temp = request.form['temperatura']
        hum = request.form['humedad']
        if cont_aux > 0:
            y = float(Matriz_Resultado[0]) + (float(temp) * float(Matriz_Resultado[1])) + (float(hum) * float(Matriz_Resultado[2]))
        else:
            y = 0
        return render_template(
            'regresion_juno.html',
            titulo = "Regresion Lineal Juno",
            name = current_user.nombre,
            determinante = A_determinante,
            Respuesta = Matriz_Resultado,
            resultado_regresion = y,
            metodo = "post",
            TamJuno = cont_aux
            )
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 6001)
