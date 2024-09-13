from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

#Configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelo tabla logs

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.Text)
    
#Crear la tabla si no existe
with app.app_context():
    db.create_all()
    
    # Pruebas
    # prueba1 = Log(texto='Mensaje de Prueba1')
    # prueba2 = Log(texto='Mensaje de Prueba2')
    
    # db.session.add(prueba1)
    # db.session.add(prueba2)
    # db.session.commit()
    
#Funcion para ordenar los registros por fecha y hora

def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    #Obtener todos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)

mensajes_log=[]

#Funcion para agregar mensajes y guardar en la base de datos
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)
    
    #Guardar en la base de datos
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

#Creacion de token de verificacion
TOKEN_COD = "HUBCODEESLAONDA"

#webhook

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        response = recibir_mensajes(request)
        return response
        
def verificar_token(req):
    token= req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')
    
    if challenge and token == TOKEN_COD:
        return challenge
    else:
        return jsonify({'error':'Error de verificacion'}),401
    

def recibir_mensajes(req):
    return jsonify({'Message':'EVENT_RECEIVED'}),200

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80, debug=True) 
    