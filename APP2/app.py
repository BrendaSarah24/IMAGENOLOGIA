# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import numpy as np
import cv2
import random
import skfuzzy as fuzz
import skimage
from skimage import data,color,filters,morphology,exposure,io

 
app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/bsros/Desktop/PAGINAPYTHON/APP2/static/uploads1/' #almacenaremos los archivos subidos
app.secret_key = "secret key"   #Bueno, se almacena dentro de una cookie y se usa para vincular al usuario para especificar datos en el lado del servidor, como información sobre el usuario en la base de datos.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # aqui se limita el tamaño del archivo subido
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  # tipos de archivos aceptados para subir
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    #las funciones que verifican si una extensión es válida y que carga el archivo y redirige al usuario a la URL del archivo cargado
def HEfun(Ruta):
    RUTA=str(Ruta)
    gris=cv2.imread(RUTA,0)
    histo=np.zeros(256)
    filas=gris.shape[0] #
    columnas=gris.shape[1]
    salida=np.zeros((filas,columnas))
    for i in range(filas):
        for j in range(columnas):
            pixel = int(gris[i,j])
            histo[pixel]  +=1   #ocurrencia en el univero
    pro = histo/(filas*columnas)  
    ecualiza=np.zeros(256)
    acumulado = 0
    for k in range(256):
        acumulado = pro[k] + acumulado
        ecualiza[k]=acumulado * 255.0           
    for i in range(filas):
        for j in range(columnas):
            entrada = int(gris[i,j])
            salida[i,j]=ecualiza[entrada]
    return salida

def Unsharpfun(Ruta):
    RUTA=str(Ruta)    
    kernel = np.array([
      [-1, -1, -1],
      [-1, 9, -1],
      [-1, -1, -1]
    ])
    imagen=cv2.imread(RUTA,0)
    img3=cv2.filter2D(imagen, -1, kernel)
    return img3

def MEJORAPROPUESTO(Ruta):
    RUTA=str(Ruta)
    rgb=io.imread(RUTA)
    gamma= exposure.adjust_gamma(rgb, 2.2)
    filt2=exposure.equalize_adapthist(gamma[:,:,2])
    filt3=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    gris=np.uint8(filt3)
    kernel = np.ones((3,3), np.uint8) 
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.erode(gris, kernel, iterations=1)
    gris= cv2.dilate(gris, kernel, iterations=1)
    bordes=cv2.Canny(gris,25,26)
    return bordes

def Gamma(Ruta):
    RUTA=str(Ruta)
    gris2=cv2.imread(RUTA)
    gamma= exposure.adjust_gamma(gris2,20)
    return gamma

def Original(Ruta):
    RUTA=str(Ruta)
    gris=cv2.imread(RUTA,0)

    filas=gris.shape[0] 
    columnas=gris.shape[1]
    matriz=np.zeros((filas,columnas))
    nueva=np.zeros((filas,columnas))

    for i in range(filas):
        for j in range(columnas):
            matriz= gris[i,j]
            nueva[i,j]=matriz
    return nueva


@app.route('/')
def home():
    return render_template('index.html')
 
   
@app.route('/', methods=['POST'])
def upload_image1(): #esta es para cargar la imagen
    if 'Archivo' not in request.files: 
        flash('No file part')
        return redirect(request.url)
    file = request.files['Archivo'] 
    if file.filename == '':
        flash('No se seleccionó ninguna imagen para subir')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        if request.form.get('v1') == 'HE': #Información recibida en el cuerpo de la petición cuando se utiliza el método POST, 
            #normalmente se utiliza un formulario HTML para enviar esta información.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            RUTA=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #########################
            salida=HEfun(RUTA)
            filenameo=filename
            filename2='processHE'+filename
            cv2.imwrite(os.path.join(UPLOAD_FOLDER,filename2),salida)        
            #flash('Imagen procesada de manera exitosa HE: ')
            return render_template('index.html', filename=filename2, filenameo=filenameo)
        elif  request.form.get('v4') == 'Unsharp':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            RUTA=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #########################
            salida=Unsharpfun(RUTA)
            filenameo=filename
            filename6='processUNSHARPI'+filename
            cv2.imwrite(os.path.join(UPLOAD_FOLDER,filename6),salida)        
            #flash('Imagen procesada de manera exitosa por Unsharp: ')
            return render_template('index.html', filename=filename6, filenameo=filenameo)
        elif  request.form.get('v5') == 'M':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            RUTA=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #########################
            salida=MEJORAPROPUESTO(RUTA)
            filenameo=filename
            filename6='processM'+filename
            cv2.imwrite(os.path.join(UPLOAD_FOLDER,filename6),salida)        
            #flash('Imagen procesada de manera exitosa por Unsharp: ')
            return render_template('index.html', filename=filename6, filenameo=filenameo)
        elif  request.form.get('v6') == 'Gamma':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            RUTA=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #########################
            salida=Gamma(RUTA)
            filenameo=filename
            filename6='processM'+filename
            cv2.imwrite(os.path.join(UPLOAD_FOLDER,filename6),salida)        
            #flash('Imagen procesada de manera exitosa por Unsharp: ')
            return render_template('index.html', filename=filename6, filenameo=filenameo)

        else:
            pass 
        
    else:
        flash('Solo imagenes con extensión: png, jpg, jpeg, gif')
        return redirect(request.url)
    

 
@app.route('/display/<filename>')
def display_image1(filename): 
    return redirect(url_for('static', filename='uploads1/' + filename), code=301)

@app.route('/display/<filenameo>')
def display_image2(filenameo): 
    return redirect(url_for('static', filenameo='uploads1/' + filenameo), code=301)

if __name__ == "__main__":
    app.run()