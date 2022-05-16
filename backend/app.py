#Importamos nuestras bilbiotecas necesarias para ejecutar nuestro script en python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

#se inicializa el entorno de flask y lo alojamos en la variable app
app = Flask(__name__)

#Configuración necesaria para conectar con nuestra base de datos
#En el siguiente enlace podrá obtener la configuración que necesita
#para conectar con la base de datos que usted prefiera
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
                                       #basededatos://nombredeusuario:contraseña@servidor/basededatos
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@localhost/flask'
#Ahora para que la anterior linea de codigo funcione correctamente
#Necesitamos la siguiente linea de codigo. 
#A continuación se explicará su uso

#Si se establece en True, Flask-SQLAlchemy rastreará las modificaciones 
#de los objetos y emitirá señales. El valor predeterminado es None, 
#lo que habilita el seguimiento pero emite una advertencia de que se 
#desactivará de forma predeterminada en el futuro.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#La conexión a la base de datos la guardamos en una variable llamada "db"
db = SQLAlchemy(app)
#Inicializamos flask-Marshmallow para poder manipular datos en nuestras tablas creadas 
ma = Marshmallow(app)

#Creamos la clase Article que será una tabla en nuestra base de datos
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100))
    body=db.Column(db.Text())
    date=db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, title,body):
        self.title=title
        self.body=body
#Creamos el esquema para nuestra clase article, lo que nos permitirá manipular 
#los datos
class ArticleSchema(ma.Schema):
    class Meta:
        fields=('id','title','body','date')
#Nos ayudará con la manipulación de un articulo
article_schema=ArticleSchema()
#Nos ayudará con la manipulación de varios articulos
articles_schema=ArticleSchema(many=True)


#Creamos el end-point que nos permitirá mostrar varios articulos
@app.route("/get", methods = ['GET'])
def get_articles():
    all_articles= Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

#Creamos el end-point que nos permitirá mostrar un articulo por ID
@app.route("/get/<id>/", methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

#Creamos el end-point que nos permitirá añadir un articulo
@app.route("/add", methods = ['POST'])
def add_articles():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

#Creamos el end-point que nos permitirá actualizar un articulo
@app.route("/update/<id>/", methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)

#Creamos el end-point que nos permitirá eliminar un articulo por id
@app.route("/delete/<id>/", methods = ['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)

#Esta función ejecutará nuestro programa
if __name__=="__main__":
    app.run(debug=True)
