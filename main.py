import tkinter as tk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tkinter import ttk
import csv_manager

TITLE = "Wellcome to wallettraker v.berza by elhorDev"
url = "https://www.productoscotizados.com/mercado/ibex-35"
wallet_total = []
TITLE_POPUP = ['Venta de acciones', 'Compra de acciones']

# Configuracion de la ventana Root.
window = tk.Tk()
window.title('WallettrakerUI by elhor')
window.geometry('1920x1080')
window.resizable(False, False)

# Creamos frame para el label y el reloj
frame_superior = tk.Frame(window)

# Creamos el label.
cabecera = tk.Label(frame_superior, text=TITLE)
cabecera.config(font=('Terminal', 20))
cabecera.grid(row=0, column=0)

# Creamos el label para el reloj.
reloj = tk.Label(frame_superior, text='')
reloj.grid(row=0, column=1, columnspan=1)

frame_superior.grid(row=0, column=0)

# Creamos un frame para contener los dos botones
frame_botones = tk.Frame(window)


# Funcion e instancia de objetos entry para abrir popup y creamos Toplevel para compra y venta


def abrir_popup_venta():
    popup = tk.Toplevel(window)
    popup.geometry('400x300')
    popup.title(TITLE_POPUP[0])
    titulo_popup = tk.Label(popup, text='Venta de valores')
    titulo_popup.config(font=('Terminal', 20))
    label_indice_valor = tk.Label(popup, text='Introduce el indice del valor')
    label_cantidad_valor = tk.Label(popup, text='Introduce la cantidad de acciones')
    label_gastos_venta_valor = tk.Label(popup, text='Introduce la cantidad de gastos de venta')
    boton_efectuar_venta = tk.Button(popup, text='Confirmar Venta')

    entry_indice_valor = tk.Entry(popup)
    entry_cantidad_venta = tk.Entry(popup)
    entry_cantidad_gastos = tk.Entry(popup)

    titulo_popup.pack()

    label_indice_valor.pack()
    entry_indice_valor.pack()

    label_cantidad_valor.pack()
    entry_cantidad_gastos.pack()

    label_gastos_venta_valor.pack()
    entry_cantidad_venta.pack()

    boton_efectuar_venta.pack()


def abrir_popup_compra():
    result = urlcontent(url)
    realtime = scrapurl(result)

    popup = tk.Toplevel(window)
    popup.geometry('400x300')
    popup.title(TITLE_POPUP[1])
    titulo_popup = tk.Label(popup, text='Compra de valores')
    titulo_popup.config(font=('Terminal', 20))
    label_indice_valor = tk.Label(popup, text='Introduce el indice del valor')
    label_precio_compra = tk.Label(popup, text='Introduce el precio de compra')
    label_cantidad_valor = tk.Label(popup, text='Introduce la cantidad de acciones')
    label_gastos_compra_valor = tk.Label(popup, text='Introduce la cantidad de gastos de compra')

    entry_indice_valor = tk.Entry(popup)
    entry_precio_compra = tk.Entry(popup)
    entry_cantidad_compra = tk.Entry(popup)
    entry_cantidad_gastos = tk.Entry(popup)

    titulo_popup.pack()

    label_indice_valor.pack()
    entry_indice_valor.pack()

    label_precio_compra.pack()
    entry_precio_compra.pack()

    label_cantidad_valor.pack()
    entry_cantidad_gastos.pack()

    label_gastos_compra_valor.pack()
    entry_cantidad_compra.pack()

    def efectuar_compra(realtime):
        realtime = scrapurl(result)
        compra = csv_manager.Stock(
            realtime[entry_indice_valor.get()]['Stock'],
            float(entry_precio_compra.get()),
            int(entry_cantidad_compra.get()),
            float(entry_cantidad_gastos.get()),
            int(entry_indice_valor.get())
        )

        wallet_total.append(compra)

    boton_efectuar_compra = tk.Button(popup, text='Confirmar compra', command=efectuar_compra)
    boton_efectuar_compra.pack()


# Creamos los botones de Compra y Venta

boton_compra = tk.Button(frame_botones, text='Añadir compra', command=abrir_popup_compra)
boton_compra.config(bg='red', font=('Terminal', 12))
boton_venta = tk.Button(frame_botones, text='Vender Acciones', command=abrir_popup_venta)
boton_venta.config(bg='green', font=('Terminal', 12))

boton_compra.pack()
boton_venta.pack()
frame_botones.grid(row=1, column=1)

# Creamos tabla.

realtime_tabular = ttk.Treeview(window, height=35)

realtime_tabular.grid(row=1, column=0)


# Funcion para reloj en pantalla
def actualizar_hora():
    reloj.config(text=time.strftime('%H:%M:%S'), font=('Terminal', 20))
    window.after(1000, actualizar_hora)


actualizar_hora()


# Creamos funcion para descarga de pagina a scrapear.
def urlcontent(url):
    result = requests.get(url)
    return result


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


# Creamos funcion para mostrar el tiempo real.

def show_tiempo_real():
    result = urlcontent(url)
    realtime = scrapurl(result)
    df = pd.DataFrame(realtime)

    if wallet_total:
        print('\n' * 2)
        for x in wallet_total:
            for y in x:
                if y == "Balance":
                    for price in realtime:
                        if price["Stock"] == x["Stock"]:
                            x["Balance"] = "{} €".format((price["Price"] * x["Qty"]) - x["AccountCharge"])

            df1 = pd.DataFrame(wallet_total)
    return df


def mostrar_datos_tabulares():
    df = show_tiempo_real()
    for item in realtime_tabular.get_children():
        realtime_tabular.delete(item)
    columnas = list(df.columns)
    realtime_tabular['columns'] = columnas
    print(columnas)
    # realtime_tabular.delete('#0')

    for col in columnas:
        realtime_tabular.column(col, anchor="center")
        realtime_tabular.heading(col, text=col)
    for i, row in df.iterrows():
        realtime_tabular.insert('', i, values=list(row))

    window.after(30000, mostrar_datos_tabulares)


mostrar_datos_tabulares()

window.mainloop()
