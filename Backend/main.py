import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.datastructures import ContentRange, Range
from Usuario import User
from image import Image
from videos import Video
from werkzeug.utils import secure_filename
import json

app= Flask(__name__)
app.config['UPLOAD_FOLDER']="./backend"
CORS(app)

#Se crea la lista de usuarios
Usuario=[]
Usuario.append(User('Abner Cardona','M',"admin","admin@ipc1.com","admin@ipc1"))
Photos=[]
Videos=[]
Photos2=[]
Videos2=[]
Publicaciones=[]
Publicaciones2=[]


#Agregar nuevo usuario 
@app.route('/registros', methods=['POST'])

def addUser():

    contador=0
    verificador=0
    global Usuario

    nombre= request.json['name']
    genero = request.json['gender']
    username= request.json['username']
    email = request.json['email']
    contra= request.json['password']


    #Verificación de usuario y contraseña 
    for i in Usuario:

        if(username == User.getUsername(i)):
            verificador+=1
            return jsonify({"message": "Usuario ya existente"})
        
        elif(contador==len(Usuario)-1 and  verificador==0):
            if(username != User.getUsername(i) and len(contra)<8):
                return jsonify({"message": "Contraseña es menor a 8 dígitos"})
            else:
                newUser=User(nombre,genero,username,email,contra)
                Usuario.append(newUser)
            return jsonify({"message": "The user was created succesfully"})
        contador+=1     
### Fin del nuevo usuario ###
 
#Login usuario 
@app.route('/login', methods=['POST'])

def logUser():

    contador=0
    global Usuario

    username= request.json['username']
    contra= request.json['password']
    #Verificación de usuario y contraseña 
    for i in Usuario:

        if(username == User.getUsername(i) and contra== User.getPassword(i)):
            if(username=="admin"):
                return jsonify({"message": "admin"})
            else:
                return jsonify({"message": "Ingresaste!"})
        elif(username=="" or contra ==""):
            return jsonify({"message": "No dejes espacios vacíos"})
        elif(username == User.getUsername(i) and contra!= User.getPassword(i)):
            return jsonify({"message": "Contraseña incorrecta"})
        elif(contador==len(Usuario)-1 and username != User.getUsername(i) ):
            return jsonify({"message": "No existe el usuario"})
        contador+=1
### Fin del nuevo usuario ###

#Mostrar el registro
@app.route('/registro/<string:name>', methods=['GET'])
def getUser(name):
    global Usuario
    Datos = []
    for i in Usuario:
        if(name== User.getUsername(i)):
             objeto = {
                'name': User.getName(i),
                'gender': User.getGender(i),
                'username': User.getUsername(i),
                'email': User.getEmail(i),
                'password': User.getPassword(i)
            }
             Datos.append(objeto)  
    return(jsonify(Datos))

        
#Fin de mostrar los registros

@app.route('/registro', methods=['GET'])
def getUsers():
    global Usuario
    Datos = []
    for i in Usuario:

             objeto = {
                'name':User.getName(i),
                'gender':User.getGender(i),
                'username':User.getUsername(i),
                'email':User.getEmail(i),
                'password':User.getPassword(i)
            }
             Datos.append(objeto)  
    return(jsonify(Datos))

#Editar información
@app.route('/editar/<string:name>', methods=['PUT'])
def editUsers(name):
    contador=0
    verificador=0
    auxiliar=""

    nombre= request.json['name']
    genero = request.json['gender']
    username= request.json['username']
    email = request.json['email']

    contra= request.json['password']
    for i in Usuario:
        if(name==User.getUsername(i)):
            auxiliar = User.getUsername(i)
            
        
 #Verificación de usuario y contraseña 
    for i in Usuario:

        if(username == User.getUsername(i) and auxiliar != username):
            print(User.getUsername(i))  
            print(name)
            verificador+=1
            return jsonify({"message": "Username is in use"})
        
        elif(contador==len(Usuario)-1 and  verificador==0):
            if(username != User.getUsername(i) and len(contra)<=8):
                return jsonify({"message": "Password below 8 digits"})
            else:
                User.setName(i,nombre)
                User.setGender(i,genero)
                User.setUsername(i,username)
                User.setEmail(i,email)
                User.setPassword(i,contra)

                return jsonify({"message": "The user was edited succesfully"})
    contador+=1   
###Fin editar usuario

#Crear una publicación tipo: foto
@app.route('/newPhoto', methods=['POST'])
def newPhoto():
    global Photos
    url=request.json['url']
    date=request.json['date']
    category=request.json['category']
    author=request.json['author']
    Publicaciones.append(Image(url,date,category,author))
    return(jsonify({"message":"Entre"}))
#Fin crear una publicación tipo: foto



@app.route('/postPhoto', methods=['GET'])
def getThePost():
    Publicaciones2=[]

    Datos = []

    for i in Publicaciones:
        try:
            objeto = {
                    'url':Image.getUrl(i),
                    'date':Image.getDate(i),
                    'category':Image.getCategory(i),
                    'author':Image.getAuthor(i),
                    'like':Image.getLike(i),
                    'tipo': Image.getTipo(i)
                }
            Datos.append(objeto)
        except:
            objeto = {
                'url': Video.getUrl(i),
                'date':Video.getDate(i),
                'category':Video.getCategory(i),
                'author':Video.getAuthor(i),
                'like':Video.getLike(i),
                'tipo': Video.getTipo(i)
                }
            Datos.append(objeto)  
    return(jsonify(Datos))

#Guardamos el json
@app.route('/loadUser', methods=['POST'])
def loadUser():
    if request.method=="POST":
        f=request.files['archivos']
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f)
        cargarUsuario()
    return(jsonify({"message":"Entre"}))
    
#Fin de guardar json


#Crear una publicación tipo: foto
@app.route('/newVideo', methods=['POST'])
def newVideo():
    url=request.json['url']
    date=request.json['date']
    category=request.json['category']
    author=request.json['author']
    Publicaciones.append(Video(url,date,category,author))
    return(jsonify({"message":"Entre"}))
#Fin crear una publicación tipo: foto


#Nuevo like
@app.route('/newLike', methods=['POST'])
def newLike():
    user=request.json['user']
    post=request.json['post']

    global Publicaciones
    for i in Publicaciones:
        try:
            if(post== Image.getUrl(i)):
                Image.like(i,user)
                return(jsonify({'like': Image.getLike(i)}))
        except:
            if(post== Video.getUrl(i)):
                Video.like(i,user)
                return(jsonify({'like': Video.getLike(i)}))

#Nuevo like
@app.route('/newLikeVideo', methods=['POST'])
def newVideoLike():
    
    user=request.json['user']
    post=request.json['post']

    global Videos
    for i in Videos:
        if(post== Video.getUrl(i)):
            Video.like(i,user)
            return(jsonify({'like': Video.getLike(i)}))

@app.route('/sortedLike', methods=['GET'])
def getsortedLikes():
    Publicaciones2.extend(Publicaciones)
    Datos = []
    newList=[]
    if(len(Publicaciones2)>1):
        for i in range(1,len(Publicaciones2)):
            for j in range(len(Publicaciones2)-i):
                newList.append(Publicaciones2[j])
                if(int(Publicaciones2[j].getLike())<int(Publicaciones2[j+1].getLike())):
                    Publicaciones2[j]=Publicaciones2[j+1] 
                    Publicaciones2[j+1]=newList[0]

    for i in Publicaciones2:
        try:
            objeto = {
                    'url':Image.getUrl(i),
                    'date':Image.getDate(i),
                    'category':Image.getCategory(i),
                    'author':Image.getAuthor(i),
                    'like':Image.getLike(i),
                    'tipo': Image.getTipo(i)
                }
            Datos.append(objeto)
        except:
            objeto = {
                'url': Video.getUrl(i),
                'date':Video.getDate(i),
                'category':Video.getCategory(i),
                'author':Video.getAuthor(i),
                'like':Video.getLike(i),
                'tipo': Video.getTipo(i)
                }
            Datos.append(objeto)  
    return(jsonify(Datos))

#Mostrar el registro
@app.route('/myPosts/<string:name>', methods=['GET'])
def getMyPosts(name):
    global Usuario
    global Videos
    Datos=[]

    for i in Publicaciones:
        try:
            if(Image.getAuthor(i)==name):
                objeto = {
                    'url':Image.getUrl(i),
                    'date':Image.getDate(i),
                    'category':Image.getCategory(i),
                    'author':Image.getAuthor(i),
                    'like':Image.getLike(i),
                    'tipo': Image.getTipo(i)
                    }
                Datos.append(objeto)
        except:
            if(Video.getAuthor(i)==name):
                objeto = {
                'url': Video.getUrl(i),
                'date':Video.getDate(i),
                'category':Video.getCategory(i),
                'author':Video.getAuthor(i),
                'like':Video.getLike(i),
                'tipo': Video.getTipo(i)
                }
                Datos.append(objeto)  
    return(jsonify(Datos))

#Eliminar usuarios
@app.route('/delete/<string:name>', methods=['DELETE'])
def delete(name):
    global Usuario
    for i in range(len(Usuario)):
        if(name== Usuario[i].getUsername()):
             del Usuario[i]
             return jsonify({"message": "The user was deleted succesfully"})
    return jsonify({"message": "No existe el usuario"})

             
def cargarUsuario():
    f= open("./backend/users.json") 
    c= f.read()
    
    
    




if __name__ == '__main__':
    app.run(debug =True, port=3000)