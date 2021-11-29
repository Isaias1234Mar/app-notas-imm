from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
 
app = Flask(__name__)
# Habilitando el uso del ORM en la app flask mediante el objeto "db"
db = SQLAlchemy(app)
# postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config ['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5433/notas'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

class Notas(db.Model):
    '''Clases Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self,tituloNota, cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    objeto = {"Nombre": "Isaias", 
              "Apellido": "Martinez"
            }
    nombre = "Isaias"
    Lista_nombres = ["Isaias", "Cristian", "Brenda"]
    return render_template("index.html",variable = Lista_nombres)

@app.route("/crearnota",methods=['POST'])
def crearnota():
     campotitulo = request.form ["campotitulo"]
     campocuerpo = request.form ["campocuerpo"]
     print (campotitulo)
     print (campocuerpo)
     notaNueva = Notas(tituloNota=campotitulo,cuerpoNota=campocuerpo)
     db.session.add(notaNueva)
     db.session.commit()
     return render_template("layout.html", titulo = campotitulo, cuerpo = campocuerpo)


@app.route("/leernotas")
def leernotas():
     consulta_notas = Notas.query.all()
     print(consulta_notas)
     for nota in consulta_notas:
         print(nota.tituloNota)
         print(nota.cuerpoNota)
     return "Notas consultadas"

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota = int(id)).delete()
    print(nota)
    db.session.commit()
    return redirect("/leernotas")

if __name__== "__main__":
    db.create_all()
    app.run()
    