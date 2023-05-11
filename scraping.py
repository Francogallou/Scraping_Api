from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import datetime
import os
import time

#Funcion para generar la lista de urls que vamos a realizar la solicitud
def getLink():
    print("Obteniendo lista de urls a utilizar")
    año_actual = datetime.datetime.now().year
    lista_años = list(range(2013, año_actual + 1))
    print(f'Lista de años:{lista_años}')

    lista_url = []
    for a in lista_años:         
        url = f'https://www.sii.cl/valores_y_fechas/uf/uf{str(a)}.htm'
        lista_url.append(url)

    print(f'Retornando lista de urls: {lista_url}')
    return lista_url


# Sacando tabla de la pagina SII iterando por la lista de url obtenida anteriormente
def getTable():

    lista_url = getLink()
    dfs = []

    for url in lista_url: 
        try:
            print(f'Haciendo scraping de la siguiente url: {url}') 
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            tabla = soup.find('table', id="table_export")
            print('\tTrayendo tabla con los datos')
            data = []
            rows = tabla.find_all("tr")

            for row in rows[1:]:
                months = row.find_all("td")
                days = row.find("th").get_text().strip()
                row_data = []

                for month in months:
                    row_data.append(month.text.strip())

                # Agregamos los días a la lista de valores de cada mes
                row_data.insert(0, days)
                data.append(row_data)

            print('\tTabla obtenida correctamente')
            print('\tArreglando formatos de dataframe')
            df = pd.DataFrame(data)
            df.columns = ['dia','01','02','03','04','05','06','07','08','09','10','11','12']

            # Derretimos las columnas de mes en una sola columna
            df = df.melt(id_vars='dia', var_name='Mes', value_vars=['01','02','03','04','05','06','07','08','09','10','11','12'], value_name='valor')

            # Creamos una columna "fecha" a partir de las columnas "dia" y "mes"
            df['fecha'] = pd.to_datetime(df['dia'].astype(str) + '-' + df['Mes'] + f'-{url[41:45]}', format='%d-%m-%Y', errors='coerce')
            df = df[['fecha', 'valor']]
            df.dropna(inplace=True)
            dfs.append(df)
        except:
            print(f'--Error en url -- {url}')

    df_combinado = pd.concat(dfs)
    df_combinado.to_csv(os.getcwd() + '/archivos_fuentes/data.csv', index=False, sep=';')
    print('\tInformación guardada correctamente')

if __name__ == '__main__':
    getTable()