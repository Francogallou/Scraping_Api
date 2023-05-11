# API de información de UF Chile
Esta API considera los valores sobre el año 2013 en adelante extraidos del Servicio de impuestos internos (SII).


## Paquetes
Usa el gestor instalador [pip](https://pip.pypa.io/en/stable/) junto al archivo requirements.txt para instalar los paquetes necesarios.

```bash
pip install -r requirements.txt
```

### Ejecutar Scrapping
Este programa debe ejecutarse diariamente para actualizar la base de datos local de los valores de UF.

```bash
python scraping.py
```

### Levantar servicio de API
esto levanta el servidor a nivel local

```bash
uvicorn main:app --reload
```

## API 
A través de un request para una API hecha con FastAPI, retorna los valores correspondiente a cada función.

### Extraer todos los valores UF desde el 2013 en adelante

```python
"http://127.0.0.1:8000/valor_uf"
```

### Extraer valor UF de cierta fecha
El formato de fecha debe ser: 
`<YYYY>-<MM>-<DD>`, por ejemplo: `2013-01-01`

```python
"http://127.0.0.1:8000/valor_uf/{fecha}"
```
