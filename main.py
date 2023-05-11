
from typing import Union
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
import re
from pandas import Timestamp
from datetime import datetime


def read_data_file():
    try:
        df = pd.read_csv('archivos_fuentes/data.csv',sep=';')
        # Eliminar filas con valores NaN
        df = df.dropna()
        # Arreglando formato de la data
        #df['fecha'] = pd.to_datetime(df['fecha'])
        df['valor'] = df['valor'].str.replace('.', '')
        df['valor'] = df['valor'].str.replace(',', '.')
        df['valor'] = df['valor'].astype(float)
    except:
        print('--Error leyendo el archivo de UF--')
    
    return df


app = FastAPI()


class Data(BaseModel):
    fecha: str
    valor: float

# Leyendo archivo de UFs
df = read_data_file()

# Definiendo la ruta de la API para obtener todos los datos
@app.get('/valor_uf')
def obtener_datos():
    print('Obteniendo todos los datos históricos de la UF')
    datos = []
    for _, row in df.iterrows():
        datos.append(Data(fecha=row['fecha'], valor=row['valor']))
    print('Entregando todos los datos históricos de la UF')
    return datos


# Definiendo la ruta de la API para obtener un dato por fecha
@app.get('/valor_uf/{fecha}')
def obtener_dato_por_fecha(fecha: str):
    print(f'Obteniendo los datos de la fecha : {fecha}')
    print(df['fecha'])
    if int(fecha[:4]) < 2013:
        return {'mensaje': 'Lo siento, esta API solo tiene información del 2013 en adelante'}
    dato = df.loc[df['fecha'] == fecha].to_dict(orient='records')
    if dato:
        print(f'Entregando los datos de la fecha: {fecha}')
        return dato[0]
    else:
        return {'mensaje': 'Dato no encontrado'}

# Ejecutar el servidor de desarrollo
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
