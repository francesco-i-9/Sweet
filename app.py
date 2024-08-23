
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, request, redirect, url_for, render_template
from sqlalchemy import text
import os
import pandas as pd
from sqlalchemy import  Table

app = Flask(__name__)
app.secret_key="sessione"
host = "localhost"
username = "root"
password = ""



#---------------------------------------------------------------------------------------------------------

# ogni volta che "interroghiamo il db fuori richeste http c'è bisogno del contesto"
#non basta bisogna mettere la classe nel codice
#per usarla in altri contesti e riferimenti

# Creiamo la variabile preferenze_table all'interno del contesto applicativo


#--------------------------------------------------------------------------------------------------
try:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{host}/sito"
    print("Connesso")
except:
    print("Non connesso")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#--------------------------------------------------------------------------------------------------
class preferenza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preferenza = db.Column(db.String(120), nullable=False)

# Crea le tabelle nel database
with app.app_context():
    db.create_all()

with app.app_context():
    try:
        # tabella 'user'
        user_table = Table('user', db.metadata, autoload_with=db.engine)
        print("Tabella user riflessa con successo!")

        #classe riflessa
        class user(db.Model):
            __table__ = user_table

    except Exception as e:
        print(f"Errore nella riflessione della tabella: {e}")
        user = None 

if user is not None:
    print("Classe user definita con successo.")
else:
    print("Errore: Impossibile riflettere la tabella 'user'. Verificare la connessione al database.")
#-------------------------------------------------------------------------------------------------------

def sessione_nome(name):
     session["name"]=name
     a=session["name"]=name
     return a

def funzione__preferenze_sessione(lista):
     session["preferenze"]=lista
     a=session["preferenze"]=lista
     return a

#----------------------------------------------------------------------------------------
@app.route("/Login", methods=["GET", "POST"])
def Login():
 if request.method == "POST":
      name = request.form.get('name')
      password = request.form.get('password')
      #if di controllo dati nel db
      user_record = db.session.execute(
            db.select(user).filter_by(name=name)
            ).scalar_one_or_none()
      if user_record :
            sessione_nome(name)
            #session["login"]=True
            #session["user_id"] = user_record.id
            return redirect(url_for("profile"))          #vedere url for                    #{name:"name"}
                                                         #vedere meglio codice login

        #aggiungere id alla sessione
      else: return "Utente inesistente"

 return render_template("Login.html" )



#----------------------------------------------------------------------------------------

torta_al_cioccolato="static/chocolate_cake" #percorsi
cup_cake="static/cup_cakes"
cannoli="static/cannoli"
torta_di_carote="static/carrot_cake"
cheesecake="static/cheesecake"
torta_di_mele="static/apple_pie"


torta_al_cioccolato = os.listdir(torta_al_cioccolato)     #liste immagini
cup_cake = os.listdir(cup_cake)
cannoli = os.listdir(cannoli)
torta_di_carote = os.listdir(torta_di_carote)
cheesecake = os.listdir(cheesecake)
torta_di_mele = os.listdir(torta_di_mele)

L=[torta_al_cioccolato,torta_di_carote, torta_di_mele, cup_cake, cheesecake, cannoli]


#-----------------------------------------------------------------------------------------------


@app.route("/profile", methods=["GET", "POST"])
def profile():
    
    
     ricerca=request.form.get("ricerca")               #dato ricerca
     print(ricerca)
     immagini=[]
     numero_like=[]
     
     
     global cup_cake
     global torta_di_carote
     global torta_al_cioccolato
     global torta_di_mele
     global cheesecake
     global cannoli

     immagini_lista=[]                       #effettivamente non può ridare un valore obbligatoriamente se si trova nella condizione (si verfica solo a determinate condizioni)
     numero_like_lista=[]
     
     if ricerca == "ciambelle":
            immagini=text("SELECT path FROM donuts_post")              #prendi dal database le immagini più il numero di like e le passi alla pagina html
            numero_like=text("SELECT numero_like FROM donuts_post")    #lista tuple
            immagini=db.session.execute(immagini)
            numnero_like=db.session.execute(numero_like)
            for i in immagini:
             immagini_lista.append(i[0]) 
                                   #vengono restituiti come tupla
            for j in numnero_like:
             numero_like_lista.append(j[0])                #se fuori dall'if itera su qualcosa senza valore
          

     elif ricerca == "cup cakes":
            a = cup_cake
            preferenza="cup_cakes"
     elif ricerca == "torta di carote":
            preferenza="carrot_cake"
            a = torta_di_carote
     elif ricerca == "torta al cioccolato":
            a = torta_al_cioccolato
            preferenza="chocolate_cake"
     elif ricerca == "torta di mele":
            preferenza="apple_pie"
            a = torta_di_mele
     elif ricerca == "cheesecake":
            preferenza="cheesecake"
            a = cheesecake
     elif ricerca == "cannoli":
            preferenza="cannoli"
            a = cannoli
    
     print("Immagini:", immagini_lista)
     print("Numero di Like:", numero_like_lista)
         
     return render_template("Profile.html", name=session["name"], immagini_lista=immagini_lista, numnero_like_lista=numero_like_lista) 


@app.route("/post")
def post():
 

 return render_template("post_creation.html")


@app.route("/register", methods=["GET", "POST"])           # traffico dati dal form a @app route
def register():
    if request.method == 'POST':
        
        name = request.form.get('name')
        e_mail = request.form.get('e_mail')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f"{name} {e_mail} {password}")

        
        if password != confirm_password:
            return "Le password non coincidono. Riprova."

       
        existing_user = user.query.filter_by(name=name).first()   #cerca name nel db
        if existing_user:                                        # se il valore c'è
            return "Nome utente già esistente. Riprova."
        else: 
            new_user = user(name=name, e_mail=e_mail, password=password)   #altrimenti crea l'utente
        
        
        db.session.add(new_user)
        db.session.commit()
        
        
        

    return render_template("register.html" )

@app.route("/")
def home():
    
         return render_template('index.html')


#funzione aggiunta preferenze database
def inserisci_preferenze(name, preferenze_selezionate):
    try:
        for preferenza in preferenze_selezionate:
            # Controlla se la preferenza esiste già
            query_controllo = text(
                "SELECT COUNT(*) FROM preferenze WHERE preferenze = :i AND name = :name"
            )
            result = db.session.execute(query_controllo, {'i': preferenza, 'name': name})
            count = result.scalar() 

            if count == 0:
                query_inserimento = text(
                    "INSERT INTO preferenze (name, preferenze) VALUES (:name, :i)"
                )
                db.session.execute(query_inserimento, {'name': name, 'i': preferenza})

        db.session.commit()
        a = "Preferenze aggiunte"
        return "Preferenze aggiunte", a

    except Exception as e:
       
        db.session.rollback()
        print(f"Errore durante l'inserimento: {e}")
        return "Preferenze non aggiunte", None

        
    #se abbiamo il modello orm db.session.add altrimenti usiamo db.session.execute, perchè non stiamo interagendo con un modello ma con il database direttamente
#funzione per mostrarla in profilo
def mostra_preferenze(name):
     K=[]                                                                                                   #messa prima perchè se in request si attiva solo quando prende i dati
     result = db.session.execute(text("SELECT preferenze FROM preferenze WHERE name = :name"), {'name': session["name"]})
     for i in result:
          i=i[0]
          K.append(i)
          print(i)
     return K

@app.route("/info", methods=["GET", "POST"])
def info():

    mostra_preferenze(session["name"])
    if request.method == "POST": #riceve dati
        # Raccogli le preferenze selezionate
        preferenze_selezionate = request.form.getlist('preferenze')  #fa una lista
                                                                     #li aggiunge al dizionario di sessione 
        print(preferenze_selezionate)
        inserisci_preferenze(session["name"], preferenze_selezionate)
        
             


        
            
 
        return redirect(url_for("info"))  # Puoi anche reindirizzare a un'altra pagina

    return render_template("Profile_info.html", K=mostra_preferenze(session["name"]))


@app.route('/post_s')
def post_s():
    img_url = request.args.get('img_url')                                       #args prende i parametri della query string from quelli del form
    print(f'Immagine selezionata: {img_url}')
    

    
    if img_url:
       numero_like=db.session.execute(text("SELECT numero_like FROM donuts_post WHERE path = :img_url"), {"img_url":img_url})        #le query restituiscono un oggetto cursor non il risultato effettivo
       numero_like=numero_like.scalar()
    
    print("numero like:", numero_like)

    
    return render_template("post_s.html", img_url=img_url, numero_like=numero_like)





if __name__=="__main__":
    app.run(debug=True)














#quando si inviano dati tramite modulo all'endpoint si viene reinderizzati a una pagina perchè il server risponde con l'endpoint stesso renderizzando il
#richieste get args, richieste post form, perchè le richieste from i dati sono inclusi nel corpo form non in query string come con post
#il corpo della richiesta (http request body ) è separato dall'url
#get non ha un corpo della richiesta i dati vengono passati nella query string (che è parte dell'url)