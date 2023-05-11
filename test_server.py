import requests
import pandas as pd


#print(requests.get("http://127.0.0.1:8000/valor_uf").json())


print(requests.get("http://127.0.0.1:8000/valor_uf/2014-01-07").json())




