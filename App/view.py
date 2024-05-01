"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*100)

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    return controller.load_data(control)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    fecha_inicial = input("Ingrese la fecha inicial: ")
    fecha_final = input("Ingrese la fecha final: ")
    rq1 = controller.req_1(control, fecha_inicial, fecha_final)
    print("El total de ofertas publicadas entre ", fecha_inicial, " y ", fecha_final, " es ", rq1[0][0])

    lista = rq1[0][1]
    titulos = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "skills"]
    lista = tabular_sublista(lista, "skills", ["name", "level"])
    lista = filtrar_titulos(lista, titulos)
    print(tabulate(lt.iterator(lista),headers= "keys", tablefmt="grid"))

    tiempo = f"{rq1[1]:.3f}"
    print("Tiempo: ", tiempo, "ms")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    numero_ofertas = int(input("Ingrese el número de ofertas a consultar: "))
    codigo_pais = input("Ingrese el codigo del pais a consultar: ")
    experticia = input("Ingrese el nivel de experticia a consultar: ")
    rq3 = controller.req_3(control, numero_ofertas, codigo_pais, experticia)
    print("El número total de ofertas laborales publicadas para ", codigo_pais, " que requieren un nivel de experiencia ", experticia, " es ", rq3[0][0])

    lista = rq3[0][1]
    titulos = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skills"]
    lista = tabular_sublista(lista, "skills", ["name", "level"])
    lista = filtrar_titulos(lista, titulos)
    print(tabulate(lt.iterator(lista),headers= "keys", tablefmt="grid"))

    tiempo = f"{rq3[1]:.3f}"
    print("Tiempo: ", tiempo, "ms")


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    numero_ofertas = int(input("Ingrese el número de ofertas a consultar: "))
    ciudad = input("Ingrese la ciudad a consultar: ")
    ubicacion = input("Ingrese la ubicacion a consultar: ")
    rq4 = controller.req_4(control, numero_ofertas, ciudad, ubicacion)
    lista = rq4[0][1]
    titulos = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skills"]
    lista = tabular_sublista(lista,"skills", ["name","level"])
    lista = filtrar_titulos(lista, titulos)
    print(tabulate(lt.iterator(lista),headers= "keys", tablefmt="grid"))
    print("El total de ofertas fue",rq4[0][0])

    tiempo = f"{rq4[1]:.3f}"
    print("Tiempo: ", tiempo, "ms")
    

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    numero_ciudades = int(input("Ingrese el numero de ciudades a consultar: "))
    fecha_inicial = input("Ingrese la fecha inicial: ")
    fecha_final = input("Ingrese la fecha final: ")
    salario_min_inicial = float(input("Ingrese el límite inferior del salario mínimo ofertado: "))
    salario_min_final = float(input("Ingrese el límite superior del salario mínimo ofertado: "))
    rq6 = controller.req_6(control, numero_ciudades, fecha_inicial, fecha_final, salario_min_inicial, salario_min_final)
    print("El número total de ofertas laborales publicadas entre ", fecha_inicial, " y ", fecha_final, " y que su salario mínimo ofertado esté entre ", salario_min_final, " y ", salario_min_final, " es ", rq6[0][0])
    print("El número total de ciudades que cumplan con las especificaciones es ", rq6[0][1])
    print("Las ", numero_ciudades, " ciudades que cumplen las condiciones especificadas ordenadas alfabéticamente son ")
    for ciudad in lt.iterator(rq6[0][2]): 
        print(ciudad)
    
    lista = rq6[0][3]
    titulos = ["published_at", "title", "company_name", "experience_level", "country_code", "city", "company_size", "workplace_type", "salary_from", "skills"]
    lista = tabular_sublista(lista, "skills", ["name", "level"])
    lista = filtrar_titulos(lista, titulos)
    print(tabulate(lt.iterator(lista),headers= "keys", tablefmt="grid"))

    tiempo = f"{rq6[1]:.3f}"
    print("Tiempo: ", tiempo, "ms")


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    anio = int(input("Ingrese el año: "))
    codigo_pais = input("Ingrese el código del pais: ")
    propiedad = input("Ingrese la propiedad de conteo (experticia, ubicacion, o habilidad): ")
    rq7 = controller.req_7(control, anio, codigo_pais, propiedad)
    print("El número de ofertas laborales publicadas en ", anio, " es ", rq7[0][0])
    print("El número de ofertas laborales publicadas utilizados para crear el gráfico de barras de la propiedad es ", rq7[0][1])
    print("Valor mínimo de la propiedad consultada en el gráfico de barras es ", rq7[0][2][0], " y el valor máximo es ", rq7[0][2][1])

    lista = rq7[0][3]
    titulos = ["published_at", "title", "company_name", "country_code", "city", "company_size", "salary_from"]
    if propiedad == "experticia": 
        titulos.append("experience_level")
    elif propiedad == "ubicacion": 
        titulos.append("workplace_type")
    else: 
        titulos.append("skills")
        lista = tabular_sublista(lista, "skills", ["name", "level"])

    lista = filtrar_titulos(lista, titulos)
    print(tabulate(lt.iterator(lista),headers= "keys", tablefmt="grid"))

    tiempo = f"{rq7[1]:.3f}"
    print("Tiempo: ", tiempo, "ms")


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


#Función que crea un diccionario copia con solo los títulos necesarios
def filtrar_titulos(lista, titulos): 
    lista_auxiliar = lt.newList()
    for data in lt.iterator(lista): 
        diccionario_copia = {}
        for titulo in titulos:
            diccionario_copia[titulo] = data[titulo]
        lt.addLast(lista_auxiliar, diccionario_copia)
    return lista_auxiliar

#Función que permite hacer una tabla que irá dentro de otra
def tabular_sublista(lista, llave, titulos):
    lista_auxiliar = lt.newList()
    for data in lt.iterator(lista): 
        diccionario_copia = data.copy()
        diccionario_copia[llave] = tabulate(lt.iterator(filtrar_titulos(diccionario_copia[llave], titulos)), headers= "keys", tablefmt="grid")
        lt.addLast(lista_auxiliar, diccionario_copia)
    return lista_auxiliar


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            print("Se han cargado",data[0], "trabajos")            
            titulos = ["published_at", "title", "company_name", "experience_level", "country_code", "city"]
            lista = filtrar_titulos(data[1], titulos)
            print(tabulate(lt.iterator(lista),headers="keys", tablefmt = "grid"))
            tiempo = f"{data[2]:.3f}"
            print("Tiempo: ", tiempo, "ms")
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print("1- Ejecutar Requerimiento 1")
            print("3- Ejecutar Requerimiento 3")
            print("6- Ejecutar Requerimiento 6")
            print("7- Ejecutar Requerimiento 7")
            opcion = int(input("Seleccione una opción para continuar: "))

            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)