import time

import requests
from bs4 import BeautifulSoup
import constants


# Creamos funcion para descarga de pagina a scrapear.
def urlcontent():
    conexion = None

    while not conexion:
        try:
            result = requests.get(constants.URL)
            return result

        except requests.exceptions.ConnectionError:
            conexion = False
            print('No hay conexión, revisa tu conexión a internet.', '\nReintentando en 5 segundos...')

            time.sleep(5)


# Creamos funcion para filtrar, listar y crear los DataFrames del contenido de la pagina descargada.
def scrapurl(result):
    realtime = []
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_="ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")

    index_number = -1
    index = []
    acciones = []
    precio_acciones = []
    tiempo_acciones = []
    var_acciones = []
    close_acciones = []
    more_or_less_acciones = []

    for acc in acc_scrap:
        acc = acc.text.replace("\t", "").replace("\r", "").replace("\n", "")
        acciones.append(acc)
        index_number += 1
        index.append(index_number)

    for price in price_scrap:
        if "\nPrecio\n" not in price.text:
            price = price.text.replace("\n", "").replace(",", ".")
            precio_acciones.append(float(price))

    for time in time_scrap:
        if "\nÚLTIMA ACTUALIZACIÓN\n" not in time.text:
            time = time.text.replace("\n", "")
            tiempo_acciones.append(time)

    for var in var_scrap:
        if "\n%\n" not in var.text:
            var = var.text.replace("\n", "")
            var_acciones.append(var)

    for close in close_scrap:
        if "\nPRECIO DE CIERRE\n" not in close.text:
            close = close.text.replace("\n", "").replace("\t", "").replace("\r", "")
            close_acciones.append(close)

    for more_or_less in more_or_less_scrap:
        if "\n+/-" not in more_or_less.text:
            more_or_less = more_or_less.text.replace("\n", "")
            more_or_less_acciones.append(more_or_less)

    for Index, Stock, Price, Time, Var, Close, VarinPercent in zip(index, acciones, precio_acciones, tiempo_acciones,
                                                                   var_acciones,
                                                                   close_acciones, more_or_less_acciones):
        value = {"Index": Index, "Stock": Stock, "Price": Price, "Time": Time, "%": Var, "Close": Close,
                 "+/-": VarinPercent}

        realtime.append(value)
    return realtime
