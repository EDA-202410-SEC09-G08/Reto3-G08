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
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    catalog = control['model']
    start_time = get_time()

    file = cf.data_dir + '10-por-jobs.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'),delimiter=";")
    for jobs in input_file:
        model.add_data_jobs(catalog, jobs)

    file2 = cf.data_dir + "10-por-employments_types.csv"
    input_file2 = csv.DictReader(open(file2, encoding="utf-8"),delimiter=";")
    for employments_types in input_file2:
        model.add_data_employments_types(catalog,employments_types)

    file3 = cf.data_dir + "10-por-multilocations.csv"
    input_file3 = csv.DictReader(open(file3, encoding="utf-8"),delimiter=";")
    for multilocations in input_file3:
        model.add_data_multilocations(catalog,multilocations)
 
    file4 = cf.data_dir + "10-por-skills.csv"
    input_file4 = csv.DictReader(open(file4, encoding="utf-8"),delimiter=";")
    for multilocations in input_file4:
        model.add_data_skills(catalog,multilocations)
    
    end_time = get_time()
    tiempo = delta_time(start_time, end_time)
    
    return model.data_size_jobs(catalog), model.first_last_mapa(catalog["mapa_jobs"], 3), tiempo


# Funciones de ordenamiento

def sort(lista, funcion_sort):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    model.sort(lista, funcion_sort)

def remove_data(oferta, columnas):
    for i in columnas: 
        model.delete_data(oferta, i)


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    rq1 = model.req_1(control["model"], fecha_inicial, fecha_final)
    end_time = get_time()
    tiempo = delta_time(start_time, end_time)
    return rq1, tiempo


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control, numero_ofertas, codigo_pais, experticia):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    rq3 = model.req_3(control["model"], numero_ofertas, codigo_pais, experticia)
    end_time = get_time()
    tiempo = delta_time(start_time, end_time)
    return rq3, tiempo


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
