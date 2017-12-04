"""
Importando los paquetes necesarios para nuestro programa o lo pueden ver en el archivo requirements.txt
"""

from flask import Flask,render_template,redirect,request, url_for
from translate_api.translate_api import api
import requests, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
"""
Creando la base de datos donde guardaremos las targetas introducidas
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarj.sqlite3'
app.config['SECRET_KEY'] = 'GBBB3V-Q9WWUS-GF4FHN-40WBI0'
db = SQLAlchemy(app)

"""Base de Datos"""
class Tarjetas(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    tarjetas = db.Column('tarjetas',db.String(10))
    saldo = db.Column('saldo',db.String(5))

    """Metodos"""
    def __init__(self,tarjetas, saldo):
        self.tarjetas = tarjetas
        self.saldo = saldo

"""Primera ruta y unica, donde se haran todos los procedimientos de los llamdos que hagamos"""
@app.route('/',methods=['GET'])
def index():
    """
    Validamos que lo que recargamos sea GET
    """
    if request.method == 'GET':
        """
        Como primera llamada o la primera recarga de la pagina el texto va vacio
        ponemos una condicion que si va vacio la deje pasar, para asi dejar terminar cargar la pagina
        y poder enviarle valor mas adelante.
        :return: 
        """
        if request.args.get('text') is None:
            pass
        else:
            """
            Los valores que recogemos de la pagina
            :var text Es la que esta recibiendo el texto que se va a traducir
            :var siglas Es la sigla que obtenemos del idioma de la primera lista del html esta nos dice en que idioma estamos introduciendo el texto que vamos a traducir
            :var siglas1 Es la sigla que obtenemos del idioma al cual vamos a traducir...
            :var traductor Es el resultado de la traduccion
            :param api(textoAtraducir,siglaDelIdiomaIntroducido,siglaDelIdiomaAtraducir)
            :return Estamos enviandole los valores necesarios o el resultado de la traduccion
            """
            text = request.args.get('text')
            siglas = request.args.get('siglas')
            siglas1 = request.args.get('siglas1')
            traductor = api(text,siglas,siglas1)
            print(api(text,siglas,siglas1))
            return render_template('translate.html', traductor=traductor, text=text)
        """
        Como el es primer llamado de la pagina el valor va vacio le ponemos la condicion para que no reviente
        """
        if request.args.get('numero') is None:
            pass
        else:
            """
            :var numero Esta obteniendo el numero introducido del html
            :var url es la que esta conteniendo la api y el --> .format(numero) <-- es la agregacion del numero recibido del html a la api
            :var response Estamos haciendo una consulta a la api para ver si tiene algun valor
            """
            numero = request.args.get('numero')
            url = 'http://panamenio.herokuapp.com/api/com/metrobus/{}'.format(numero)
            response = requests.get(url)
            """
            El if response.ok: nos dira si status de la api es True si es asi prosigue si no vuelve a cargar el html
            """
            if response.ok:
                """
                response.text quiere decir que de lo obtenido del llamado de la api estamos extrayendo especificamente el texto
                :var consulta es el resultado de la api(response.text) cargada en un json para mejor manipulacion
                :var tarjeta esta obteniendo de la api el numero de la tarjeta y eso lo hace con el valor que tiene la api 'cardId'.  
                :var status esta obteniendo de la api si esta activa o en funcionamiento la tarjeta y eso lo hace con el valor que tiene la api 'status'.
                :var balance esta obteniendo de la api el saldo de la tarjeta y eso lo hace con el valor que tiene la api 'balance'.
                :var ult_trans esta obteniendo de la api la ultima ves utilizada la tarjeta y eso lo hace con el valor que tiene la api 'lastTransactionAt'.
                """
                consulta = json.loads(response.text)
                tarjeta = consulta['cardId']
                status = consulta['status']
                balance = consulta['balance']
                ult_trans = consulta['lastTransactionAt']
                print(response.ok)
                print(consulta)
                """
                Esta condicion es por si meten un numero de tarjeta invalido o algun numero de tarjeta erroneo
                en la tabla nos saldra el mensaje de abajo error de tarjeta
                """
                if consulta['balance'] is '':
                    balance = 'Error'
                    status = 'de'
                    ult_trans = 'Tarjeta'
                try:
                    """
                    Se guarda la tarjeta y su balance, si en el numero de tarjeta hay un error
                    en la base de datos en el lado de balance se guardara el string error
                    """
                    guardar = Tarjetas(tarjeta, balance)
                    db.session.add(guardar)
                    db.session.commit()
                except Exception as e:
                    """Imprimiendo la exception si nos causa error"""
                    print(e)
                """
                :return Estamos enviandole los valores necesarios de la consulta de saldo.
                """
                return render_template('translate.html', consulta=consulta, tarjeta=tarjeta, status=status,
                                       balance=balance, ult_trans=ult_trans)
            """:return 'translate.html'"""
            return render_template('translate.html')
        return render_template('translate.html')

if __name__ == '__main__':
    """
    Iniciando base de datos
    Corriendo pagina
    """
    db.create_all()
    app.run()