import streamlit as st
import pymongo
import random as r
import pandas as pd
#import os
from decouple import config 

#mongo_uri = os.environ.get('MONGO_URI')
cluster = pymongo.MongoClient(config('MONGO_URI'))
db = cluster["BASE_DE_DATOS"]
collection = db["test"]


#crear una funcion para insertar datos en la base de datos con streamlit al ejecutar el boton
def insertar_datos():
    #insertar datos en la base de datos con streamlit 
    st.title("Insertar datos en la base de datos")
    st.write("Inserte los datos que desea ingresar en la base de datos")
    name = st.text_input("Nombre")
    score = st.text_input("Puntaje")
    #Crear un _id aleatorio para cada dato ingresado en la base de datos
    _id = r.randint(1000,9999)
    #consultar si el _id ya existe en la base de datos
    results = collection.find({})
    for result in results:
        if _id == result["_id"]:
            _id = r.randint(1,1000)
    post = {"_id": _id, "name": name, "score": score}
        
    botton = st.button("Insertar datos en la base de datos")
    
    if botton:
        collection.insert_one(post)
        st.write("Done")

#crear funcion para mostrar los datos en forma de tabla al ejecutar el boton
def mostrar_datos_tabla():
    #mostrar datos de la base de datos
    st.title("Mostrar datos de la base de datos")
    botton3 = st.button("mostrar datos de la base de datos",key=16)
    if botton3:
        results = collection.find({})
        #crear una tabla para mostrar los datos
        st.table(results)

def descargar_datos_tabla():
    #descargar datos de la base de datos
    st.title("Descargar datos de la base de datos")
    results = collection.find({})
    df1 = pd.DataFrame.from_records(results)
    df1.to_csv("nombre_del_archivo.csv",index=False)
    
    
    with open('nombre_del_archivo.csv') as f:
       st.download_button('Download CSV', f)



        

#crear funcion para eliminar y editar datos en la base de datos
def eliminar_datos():
    #eliminar datos de la base de datos
    st.title("Eliminar datos de la base de datos")
    st.write("Inserte el _id del dato que desea eliminar")
    _id = st.text_input("_id")
    botton4 = st.button("Eliminar datos de la base de datos",key=4)
    if botton4:
        collection.delete_one({"_id": int(_id)})
        st.write("Done")

#create a function to update data in the database
def actualizar_datos():
    #actualizar datos de la base de datos name y score
    st.title("Actualizar datos de la base de datos")
    st.write("Inserte el _id del dato que desea actualizar")
    _id = st.text_input("_id",key=12)
    st.write("Inserte el nuevo nombre")
    name = st.text_input("Nombre",key=13)
    st.write("Inserte el nuevo puntaje")
    score = st.text_input("Puntaje",key=14)
    botton5 = st.button("Actualizar datos de la base de datos",key=5)
    if botton5:
        collection.update_one({"_id": int(_id)}, {"$set": {"name": name, "score": score}})
        st.write("Done")

with st.sidebar:
    eliminar_datos()
    actualizar_datos()

if __name__ == "__main__":
    insertar_datos()
    mostrar_datos_tabla()
    descargar_datos_tabla()


    