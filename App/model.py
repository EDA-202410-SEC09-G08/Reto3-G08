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
        "lista_jobs": None,
        "mapa_jobs": None,
        "multilocations": None,
        "skills": None, 
        "employments_types": None, 
        "map_req1": None,
        "map_req3": None, 
        "map_req4": None,
        "map_req5": None, 
        "map_req6": None,
        "map_req7": None, 
        "map_req8": None
    }
    catalog["lista_jobs"] = lt.newList(datastructure="SINGLE_LINKED")
    catalog["mapa_jobs"] = om.newMap(omaptype="BST")
    catalog["skills"] = mp.newMap(numelements=250000,
                                  prime=109345121,
                                  maptype="CHAINING",
                                  loadfactor=0.5)
    catalog["employments_types"] =  mp.newMap(numelements=250000,
                                              prime=109345121,
                                              maptype="CHAINING",
                                              loadfactor=0.5)
    catalog["multilocations"] =  mp.newMap(numelements=250000,
                                          prime=109345121,
                                          maptype="CHAINING",
                                          loadfactor=0.5)
    catalog["map_req1"] = om.newMap(omaptype="RBT")
    catalog["map_req3"] = mp.newMap(numelements= 100,
                                    prime= 109345121,
                                    maptype="CHAINING")
    return catalog


# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass

def add_data_jobs(data_structs, data): 
    data["published_at"] = datetime.strptime(data["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")
    lt.addLast(data_structs["lista_jobs"], data)
    cargar_mapa(om, data_structs["mapa_jobs"], data["published_at"], data)

    #Lleno el mapa del req 1
    data["published_at"] = datetime.strptime(datetime.strftime(data["published_at"],"%Y-%m-%d"), "%Y-%m-%d")
    cargar_mapa(om, data_structs["map_req1"], data["published_at"], data)

    #Lleno mapa req 3
    mapa_paises = data_structs["map_req3"]
    pais = data["country_code"]
    experticia = data["experience_level"]
    mapa_experticia = cargar_mapa(mp, mapa_paises, pais, mp.newMap(numelements=4,
                                                                   prime=109345121,
                                                                   maptype="PROBING",
                                                                   loadfactor=0.5))
    mapa_ofertas = cargar_mapa(mp, mapa_experticia, experticia, om.newMap(omaptype="RBT"))
    cargar_mapa(om, mapa_ofertas, data["published_at"], data)
    #print(mapa_ofertas)


def add_data_skills(data_structs, data):
    cargar_mapa(mp, data_structs["skills"], data["id"], data)

def add_data_employments_types(data_structs, data):
    cargar_mapa(mp, data_structs["employments_types"], data["id"], data)
    
def add_data_multilocations(data_structs, data):
    cargar_mapa(mp, data_structs["multilocations"], data["id"], data)


def cargar_mapa(tipo_mapa, mapa, llave, valor): 
    if not tipo_mapa.contains(mapa, llave): 
        lista_interna = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(lista_interna, valor)
        tipo_mapa.put(mapa, llave, lista_interna)
    else: 
        lista_interna = me.getValue(tipo_mapa.get(mapa, llave))
        lt.addLast(lista_interna, valor)
    return valor


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def data_size_jobs(data_structs):
    return lt.size(data_structs["lista_jobs"])

def first_last(lista, n): 
    first = lt.subList(lista, 1, n)
    last = lt.subList(lista, lt.size(lista)-n+1, n)
    rta = lt.newList(datastructure="ARRAY_LIST")
    for element in lt.iterator(first):
        lt.addLast(rta, element)
    for element in lt.iterator(last):
        lt.addLast(rta, element)
    return rta

def first(lista, n): 
    return lt.subList(lista, 1, n)

def first_last_mapa(mapa, n): 
    first = lt.newList(datastructure="ARRAY_LIST")
    last = lt.newList(datastructure="ARRAY_LIST")
    llave_minima = om.minKey(mapa)
    valor_minimo = me.getValue(om.get(mapa, llave_minima))
    if lt.size(valor_minimo) >= n: 
        first = lt.subList(valor_minimo, 1, n)
    else: 
        first = valor_minimo
        tamano = n-lt.size(first)
        while tamano != 0: 
            om.deleteMin(mapa)
            llave_minima = om.minKey(mapa)
            valor_minimo = me.getValue(om.get(mapa, llave_minima))
            if lt.size(valor_minimo) >= n: 
                sublista_minima = lt.subList(valor_minimo, 1, tamano)
                for element in lt.iterator(sublista_minima):
                    lt.addFirst(first, element)
                tamano = 0
            else: 
                for element in lt.iterator(valor_minimo): 
                    lt.addFirst(first, element)
                    tamano -= 1
    llave_maxima = om.maxKey(mapa)
    valor_maximo = me.getValue(om.get(mapa, llave_maxima))
    if lt.size(valor_maximo) >= n: 
        last = lt.subList(valor_maximo, 1, n)
    else: 
        last = valor_maximo
        n = n-lt.size(last)
        while n != 0: 
            om.deleteMax(mapa)
            llave_maxima = om.maxKey(mapa)
            valor_maximo = me.getValue(om.get(mapa, llave_maxima))
            if lt.size(valor_maximo) >= n: 
                sublista_maxima = lt.subList(valor_maximo, 1, n)
                for element in lt.iterator(sublista_maxima):
                    lt.addLast(last, element)
                n = 0
            else: 
                for element in lt.iterator(valor_maximo): 
                    lt.addLast(last, element)
                    n -= 1
    
    rta = lt.newList(datastructure="ARRAY_LIST")
    for element in lt.iterator(last):
        lt.addLast(rta, element)
    for element in lt.iterator(first):
        lt.addLast(rta, element)
    return rta


def req_1(data_structs, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    mapa_fechas = data_structs["map_req1"]
    mapa_salario = data_structs["employments_types"]
    mapa_habilidades = data_structs["skills"]
    fecha_inicial = datetime.strptime(fecha_inicial,"%Y-%m-%d")
    fecha_final = datetime.strptime(fecha_final,"%Y-%m-%d")

    lista_valores = om.values(mapa_fechas, fecha_inicial, fecha_final)
    rq1 = lt.newList(datastructure="ARRAY_LIST")
    for lista in lt.iterator(lista_valores): 
        for oferta in lt.iterator(lista):
            id = oferta["id"] #2 salarios diferentes dependiendo del type. Cual se toma? Para salario se toma el promedio de salarios?
            salario_from = lt.getElement(me.getValue(mp.get(mapa_salario, id)), 0)["salary_from"]
            salario_to = lt.getElement(me.getValue(mp.get(mapa_salario, id)), 0)["salary_to"]
            if salario_from != "" and salario_to != "":
                salario = (int(salario_from) + int(salario_to))/2
            elif salario_from == "" and salario_to != "": 
                salario = int(salario_to)
            elif salario_from != "" and salario_to == "": 
                salario = int(salario_from)
            else: 
                salario = 0 #Debo imprimir unknown?
            oferta["salary"] = salario
            oferta["skills"] =  ""
            lista_habilidades = me.getValue(mp.get(mapa_habilidades, id))
            numero_habilidades = lt.size(lista_habilidades)
            for i in range(0, numero_habilidades): 
                habilidad = lt.getElement(lista_habilidades, i)["name"]
                if habilidad == "": 
                    habilidad = "Unknown"
                if i != numero_habilidades-1:
                    oferta["skills"] += habilidad
                    oferta["skills"] += ", "
                else: 
                    oferta["skills"] += habilidad
            lt.addLast(rq1, oferta)
    merg.sort(rq1, sort_ofertas1)

    if lt.size(rq1) > 10: 
        rq1_first_last = first_last(rq1, 5)
    else: rq1_first_last = rq1

    return rq1, rq1_first_last


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


# def req_3(data_structs, numero_ofertas, codigo_pais, experticia):
#     """
#     Función que soluciona el requerimiento 3
#     """
#     # TODO: Realizar el requerimiento 3
#     mapa_paises = data_structs["map_req3"]
#     mapa_salario = data_structs["employments_types"]
#     mapa_habilidades = data_structs["skills"]

#     mapa_pais_exp = lt.getElement(me.getValue(mp.get(mapa_paises, codigo_pais)), 0) 
#     mapa_ofertas_pais_exp = lt.getElement(me.getValue(mp.get(mapa_pais_exp, experticia)), 0)

#     lista_valores = om.valueSet(mapa_ofertas_pais_exp)
#     rq3 = lt.newList(datastructure="SINGLE_LINKED")
#     for lista in lt.iterator(lista_valores): 
#         for oferta in lt.iterator(lista):
#             id = oferta["id"] #2 salarios diferentes dependiendo del type. Cual se toma?
#             salario_from = lt.getElement(me.getValue(mp.get(mapa_salario, id)), 0)["salary_from"]

#             if salario_from != "":
#                 oferta["salary_from"] = int(salario_from)
#             else: 
#                 oferta["salary_from"] = 0 #Debo imprimir unknown?
            
#             oferta["skills"] =  ""
#             lista_habilidades = me.getValue(mp.get(mapa_habilidades, id))
#             numero_habilidades = lt.size(lista_habilidades)
#             for i in range(0, numero_habilidades): 
#                 habilidad = lt.getElement(lista_habilidades, i)["name"]
#                 if habilidad == "": 
#                     habilidad = "Unknown"
#                 if i != numero_habilidades-1:
#                     oferta["skills"] += habilidad
#                     oferta["skills"] += ", "
#                 else: 
#                     oferta["skills"] += habilidad
#             lt.addLast(rq3, oferta)
#     merg.sort(rq3, sort_ofertas3)

#     # if lt.size(rq3) > numero_ofertas: 
#     #     rq3_first = first(rq3, numero_ofertas)
#     # else: 
#     #     rq3_first = rq3

#     return rq3 #, rq3_first


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(lista, funcion_sort):
    """
    Función encargada de ordenar la lista con los datos
    """
    merg.sort(lista, funcion_sort)


def sort_jobs(data_1, data_2): 
    return data_1["published_at"] > data_2["published_at"]
    
def sort_ofertas1(data_1, data_2): 
    if data_1["published_at"] > data_2["published_at"]: 
        return True
    elif data_1["published_at"] == data_2["published_at"]: 
        return data_1["salary"] > data_2["salary"]
    else: 
        return False
    
def sort_ofertas3(data_1, data_2): 
    if data_1["published_at"] > data_2["published_at"]: 
        return True
    elif data_1["published_at"] == data_2["published_at"]: 
        return data_1["salary_from"] > data_2["salary_from"]
    else: 
        return False
    


#Función para eliminar información de la oferta
def delete_data(oferta, columna):
    oferta.pop(columna)