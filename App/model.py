"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from datetime import datetime
from matplotlib import pyplot as plt
import folium


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    catalog = {
        "jobs": None,
        "mapa_id": None,
        "skills": None, 
        "employments_types": None, 
        "map_req1": None,
        "map_req3": None,
        "map_req4": None,
        "map_req6": None,
        "map_req7": None, 
    }
    catalog["jobs"] = om.newMap(omaptype="BST",
                                cmpfunction=cmpdate)
    catalog["mapa_id"] = mp.newMap(numelements=203564,
                                   prime=109345121,
                                   maptype="CHAINING",
                                   loadfactor=1)
    catalog["skills"] = mp.newMap(numelements=250000,
                                  prime=109345121,
                                  maptype="CHAINING",
                                  loadfactor=0.5)
    catalog["employments_types"] =  mp.newMap(numelements=250000,
                                              prime=109345121,
                                              maptype="CHAINING",
                                              loadfactor=0.5)
    catalog["map_req1"] = om.newMap(omaptype="RBT",
                                    cmpfunction=cmpdate)
    catalog["map_req3"] = mp.newMap(numelements= 100,
                                    prime= 109345121,
                                    maptype="CHAINING")
    catalog["map_req4"] = mp.newMap(numelements=150)
    catalog["map_req6"] = om.newMap(omaptype="RBT")
    catalog["map_req7"] = mp.newMap(numelements=4)
    return catalog

# Funciones para agregar informacion al modelo

def add_data_jobs(data_structs, data):
    #Lleno el mapa de id
    mp.put(data_structs["mapa_id"], data["id"], data)

    #Lleno el mapa de jobs 
    data["published_at"] = datetime.strptime(data["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")
    lista = cargar_mapa(om, data_structs["jobs"], data["published_at"], lt.newList())
    lt.addLast(lista, data)

    #Lleno el mapa del req 1
    data["published_at"] = datetime.strptime(datetime.strftime(data["published_at"],"%Y-%m-%d"), "%Y-%m-%d")
    lista = cargar_mapa(om, data_structs["map_req1"], data["published_at"], lt.newList())
    lt.addLast(lista, data)

    #Lleno mapa req 3
    mapa_paises = data_structs["map_req3"]
    pais = data["country_code"]
    experticia = data["experience_level"]
    mapa_experticia = cargar_mapa(mp, mapa_paises, pais, mp.newMap(numelements=4,
                                                                   maptype="PROBING"))
    arbol_ofertas = cargar_mapa(mp, mapa_experticia, experticia, om.newMap(omaptype="RBT"))
    lista = cargar_mapa(om, arbol_ofertas, data["published_at"], lt.newList())
    lt.addLast(lista, data)

    #Lleno mapa req 7
    mapa_anios = data_structs["map_req7"]
    anio = int(data["published_at"].year)
    valor = {"mapa_paises": mp.newMap(numelements=100),
             "total_ofertas": 0}
    diccionario_anio = cargar_mapa(mp, mapa_anios, anio, valor)
    mapa_paises = diccionario_anio["mapa_paises"]
    diccionario_anio["total_ofertas"] += 1
    diccionario_mapas = cargar_mapa(mp, mapa_paises, data["country_code"], newDict_req7())
    lista_jobs_experticia = cargar_mapa(mp, diccionario_mapas["experticia"], data["experience_level"], lt.newList("ARRAY_LIST"))
    lt.addLast(lista_jobs_experticia, data)
    lista_jobs_ubicacion = cargar_mapa(mp, diccionario_mapas["ubicacion"], data["workplace_type"], lt.newList("ARRAY_LIST"))
    lt.addLast(lista_jobs_ubicacion, data)

    #Lleno mapa req 4 
    mapa_ciudades = data_structs["map_req4"]
    mapa_ubicacion =  cargar_mapa(mp,mapa_ciudades,data["city"],mp.newMap(numelements=4))
    lista_jobs = cargar_mapa(mp,mapa_ubicacion,data["workplace_type"],lt.newList(datastructure="ARRAY_LIST"))
    lt.addLast(lista_jobs,data)

def newDict_req7(): 
    diccionario = {}
    diccionario["experticia"] = mp.newMap(numelements=3)
    diccionario["ubicacion"] = mp.newMap(numelements=4)
    diccionario["habilidad"] = mp.newMap(numelements=100)
    return diccionario


def add_data_skills(data_structs, data):
    #Calculo el salario mínimo de cada una de las ofertas y las agrego a la información de cada una de las ofertas.
    job = me.getValue(mp.get(data_structs["mapa_id"], data["id"]))

    if "skills" not in job.keys(): 
        job["skills"] = lt.newList(datastructure="ARRAY_LIST")
    else: 
        job["skills"] = job["skills"]
    lt.addLast(job["skills"], data)

    #Lleno mapa req 7
    mapa_anios = data_structs["map_req7"]
    anio = int(job["published_at"].year)
    diccionario_anio = me.getValue(mp.get(mapa_anios, anio))
    mapa_paises = diccionario_anio["mapa_paises"]
    diccionario_mapas = me.getValue(mp.get(mapa_paises, job["country_code"]))
    lista_jobs_habilidades = cargar_mapa(mp, diccionario_mapas["habilidad"], data["name"], lt.newList("ARRAY_LIST"))
    lt.addLast(lista_jobs_habilidades, job)


def add_data_employments_types(data_structs, data):
    #Calculo las skills de cada una de las ofertas y las agrego a la información de cada una de las ofertas.
    job = me.getValue(mp.get(data_structs["mapa_id"], data["id"]))
    salario_min = data["salary_from"]
    if salario_min != "":
        salario_min = convertir_salario(float(salario_min), data["currency_salary"])
        if "salary_from" not in job.keys(): 
            job["salary_from"] = float("inf")
        if salario_min < job["salary_from"]: 
            job["salary_from"] = salario_min
    else: 
        salario_min = 0
        job["salary_from"] = salario_min

    #Lleno mapa req 6
    arbol_fechas6 = data_structs["map_req6"]
    arbol_salarios_minimos = cargar_mapa(om, arbol_fechas6, job["published_at"], om.newMap(omaptype="RBT"))
    lista_jobs = cargar_mapa(om, arbol_salarios_minimos, salario_min, lt.newList("ARRAY_LIST"))
    lt.addLast(lista_jobs, job)

#Función para convertir monedas
def convertir_salario(salario, currency): 
    if currency == "usd": 
        return salario
    elif currency == "eur": 
        return salario*1.07
    elif currency == "pln": 
        return salario*0.25 
    elif currency == "chf":
        return salario*1.1
    elif currency == "gbp": 
        return salario*1.24
    else: 
        return 0

#Función para llenar un mapa de tipo mp u om.
def cargar_mapa(tipo_mapa, mapa, llave, valor): 
    if not tipo_mapa.contains(mapa, llave): 
        tipo_mapa.put(mapa, llave, valor)
    else: 
        valor = me.getValue(tipo_mapa.get(mapa, llave))
    return valor

#Función para calcular el total de ofertas en un arbol.
def total_ofertas_mapa(mapa): 
    lista_valores = om.valueSet(mapa)
    lista = convertir_lista_de_listas(lista_valores)
    return lt.size(lista)

#Función que retorna en una lista los primeros y últimos n elementos de una lista ingresada por parámetro
def first_last(lista, n): 
    first = lt.subList(lista, 1, n)
    last = lt.subList(lista, lt.size(lista)-n+1, n)
    rta = lt.newList(datastructure="ARRAY_LIST")
    for element in lt.iterator(first):
        lt.addLast(rta, element)
    for element in lt.iterator(last):
        lt.addLast(rta, element)
    return rta

#Función que retorna una lista con los primeros n elementos de una lista ingresada por parámetro
def first(lista, n): 
    return lt.subList(lista, 1, n)

#Función que retorna una lista con los últimos n elementos de una lista ingresada por parámetro
def last(lista, n):
    return lt.subList(lista, lt.size(lista)-n+1, n)

#Función que retorna en una lista los primeros y últimos n elementos de un mapa
def first_last_mapa(mapa, n): 
    valores = om.valueSet(mapa)
    lista = convertir_lista_de_listas(valores)
    respuesta = first_last(lista, n)
    return respuesta


#Funciones pararesolver los requerimientos.

def req_1(data_structs, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    mapa_fechas = data_structs["map_req1"]
    fecha_inicial = datetime.strptime(fecha_inicial,"%Y-%m-%d")
    fecha_final = datetime.strptime(fecha_final,"%Y-%m-%d")

    lista_valores = om.values(mapa_fechas, fecha_final, fecha_inicial)
    lista = convertir_lista_de_listas(lista_valores)

    total_ofertas = lt.size(lista)
    if total_ofertas > 10: 
        lista = first_last(lista, 5)

    return total_ofertas, lista



def req_3(data_structs, numero_ofertas, codigo_pais, experticia):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    mapa_paises = data_structs["map_req3"]

    mapa_pais_exp = me.getValue(mp.get(mapa_paises, codigo_pais))
    arbol_ofertas_pais_exp = me.getValue(mp.get(mapa_pais_exp, experticia))

    lista_valores = om.valueSet(arbol_ofertas_pais_exp)    
    lista_final = convertir_lista_de_listas(lista_valores)
    total_ofertas = lt.size(lista_final)

    merg.sort(lista_final, sort_date_salario)
    if total_ofertas > numero_ofertas:
        lista_final = first(lista_final, numero_ofertas)

    return total_ofertas, lista_final


def req_4(data_structs, numero_ofertas, ciudad, ubicacion):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    mapa_ciudades = data_structs["map_req4"]
    mapa_ubicacion = me.getValue(mp.get(mapa_ciudades, ciudad))
    lista_jobs = me.getValue(mp.get(mapa_ubicacion, ubicacion))
    merg.sort(lista_jobs,sort_date_salario)
    total_ofertas = lt.size(lista_jobs)
    if total_ofertas>numero_ofertas:
        lista_jobs= lt.subList(lista_jobs,1,numero_ofertas)
    return total_ofertas, lista_jobs


def req_6(data_structs, numero_ciudades, fecha_inicial, fecha_final, salario_min_inicial, salario_min_final):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    arbol_fechas = data_structs["map_req6"]
    fecha_inicial = datetime.strptime(fecha_inicial,"%Y-%m-%d")
    fecha_final = datetime.strptime(fecha_final,"%Y-%m-%d")

    lista_fecha_salario = lt.newList(datastructure="ARRAY_LIST")
    mapa_ciudades = mp.newMap(numelements=1000,
                              prime = 109345121,
                              maptype="CHAINING",
                              loadfactor=1)
    lista_arboles_salarios = om.values(arbol_fechas, fecha_inicial, fecha_final)
    ciudad_mayor = None
    max_ofertas = 0
    for arbol_salarios in lt.iterator(lista_arboles_salarios): 
        lista_valores = om.values(arbol_salarios, salario_min_inicial, salario_min_final)
        lista_jobs = convertir_lista_de_listas(lista_valores)
        for job in lt.iterator(lista_jobs): 
            lt.addLast(lista_fecha_salario, job)
            lista_ofertas_ciudad = cargar_mapa(mp, mapa_ciudades, job["city"], lt.newList(datastructure="ARRAY_LIST"))
            lt.addLast(lista_ofertas_ciudad, job)
            if lt.size(lista_ofertas_ciudad) > max_ofertas: 
                max_ofertas = lt.size(lista_ofertas_ciudad)
                ciudad_mayor = job["city"]

    total_ofertas = lt.size(lista_fecha_salario)
    lista_ciudades = mp.keySet(mapa_ciudades)
    total_ciudades = lt.size(lista_ciudades)
    merg.sort(lista_ciudades, sort_city)
    if lt.size(lista_ciudades) > numero_ciudades: 
        lista_ciudades = first(lista_ciudades, numero_ciudades)

    lista_jobs_mayor = me.getValue(mp.get(mapa_ciudades, ciudad_mayor))
    merg.sort(lista_jobs_mayor, sort_date_salario)
    if lt.size(lista_jobs_mayor) > 10: 
        lista_jobs_mayor = first_last(lista_jobs_mayor, 5)

    return total_ofertas, total_ciudades, lista_ciudades, lista_jobs_mayor


def req_7(data_structs, anio, codigo_pais, propiedad):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    mapa_anios = data_structs["map_req7"]
    diccionario_anio = me.getValue(mp.get(mapa_anios, anio))
    mapa_paises = diccionario_anio["mapa_paises"]
    diccionario_mapas = me.getValue(mp.get(mapa_paises, codigo_pais))
    mapa_propiedad = diccionario_mapas[propiedad]

    total_ofertas_anio = diccionario_anio["total_ofertas"]
    total_ofertas_propiedad = 0
    x = []
    y = []
    valor_min = float("inf")
    valor_max = 0
    lista_final = lt.newList("ARRAY_LIST")
    for llave in lt.iterator(mp.keySet(mapa_propiedad)):
        lista_jobs_propiedad = me.getValue(mp.get(mapa_propiedad, llave))
        total_ofertas_propiedad += lt.size(lista_jobs_propiedad)
        x.append(llave)
        y.append(lt.size(lista_jobs_propiedad))
        if lt.size(lista_jobs_propiedad) > valor_max: 
            valor_max = lt.size(lista_jobs_propiedad)
        if lt.size(lista_jobs_propiedad) < valor_min: 
            valor_min = lt.size(lista_jobs_propiedad)
        lt.addLast(lista_final, lista_jobs_propiedad)
    fig,ax = plt.subplots()
    ax.barh(x, y)
    plt.show()
    lista_final = convertir_lista_de_listas(lista_final)

    if lt.size(lista_final) > 10: 
        lista_final = first_last(lista_final, 5)

    return total_ofertas_anio, total_ofertas_propiedad, (valor_min, valor_max), lista_final


def req_8(data_structs, requerimiento, fecha_inicial, fecha_final, numero_ofertas, codigo_pais, experticia, numero_ciudades, salario_min_inicial, salario_min_final, anio, propiedad):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    if requerimiento == 1: 
        tupla = req_1(data_structs, fecha_inicial, fecha_final)
        lista_final = tupla[1]
    elif requerimiento == 3:
        tupla = req_3(data_structs, numero_ofertas, codigo_pais, experticia)
        lista_final = tupla[1]
    elif requerimiento == 6: 
        tupla = req_6(data_structs, numero_ciudades, fecha_inicial, fecha_final, salario_min_inicial, salario_min_final)
        lista_final = tupla[3]
    elif requerimiento == 7:
        tupla = req_7(data_structs, anio, codigo_pais, propiedad)
        lista_final = tupla[3]

    m = folium.Map([23, 25], zoom_start=2)

    for oferta in lt.iterator(lista_final): 
        info = "published at: " + datetime.strftime(oferta["published_at"],"%Y-%m-%d") + " - title: " + oferta["title"] + " - company name: " + oferta["company_name"] + " - country code: " + oferta["country_code"] + " - city: " + oferta["city"] + " - company size: " + oferta["company_size"] + " - experience level: " + oferta["experience_level"]
        popup = folium.Popup(info, min_width=150, max_width=150)
        folium.Marker(location=[oferta["latitude"], oferta["longitude"]],
                      tooltip="Click me!",
                      popup= popup,
                      icon=folium.Icon(color="red")).add_to(m)
    m.save("map.html")
    return m
    

#Función que transforma una lista de listas en una lista completa que contiene todos los elementos de las sublistas [[], [], [], []] ---> []
def convertir_lista_de_listas(lista_mayor): 
    lista_final = lt.newList(datastructure="ARRAY_LIST")
    for lista in lt.iterator(lista_mayor): 
        for data in lt.iterator(lista): 
            lt.addLast(lista_final, data)
    return lista_final

#Cmp function para ordenar los mapas de mayor a menor
def cmpdate(key1, key2):
    if key1 == key2: 
        return 0
    elif key1 > key2: 
        return -1
    else: 
        return 1

#Función para oredenar una lista por fechas y salarios mínimos
def sort_date_salario(data_1, data_2): 
    if data_1["published_at"] > data_2["published_at"]: 
        return True
    elif data_1["published_at"] == data_2["published_at"]: 
        return data_1["salary_from"] > data_2["salary_from"]
    else: 
        return False
    
#Función para ordenar las ciudades en orden alfabético
def sort_city(data_1, data_2): 
    return data_1 < data_2
