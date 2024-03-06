global imagen_tk

import tkinter as tk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tkinter import ttk
import csv_manager
from PIL import Image, ImageTk
import os  # Solo para debug y comprobacion de PATH

realtime = []

TITLE = "Wellcome to wallettraker v.0.1 by elhorDev"
url = "https://www.productoscotizados.com/mercado/ibex-35"
wallet_total = []
TITLE_POPUP = ['Venta de acciones', 'Compra de acciones']
path_error_img = 'peligro.png'

# Configuracion de la ventana Root.
window = tk.Tk()
window.title('WallettrakerUI by elhor')
window.geometry('1920x1080')
window.resizable(False, False)


# Popup para gestionar las excepciones de los entry.
def mostrar_popup_error():
    popup_error_entry = tk.Toplevel(window)
    popup_error_entry.title('Error')
    popup_error_entry.geometry('600x450')

    if os.path.exists(path_error_img):
        imagen = Image.open(path_error_img)
        global imagen_tk
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(popup_error_entry, image=imagen_tk, anchor=tk.CENTER)
        label_imagen.pack()
    else:
        print("Error: Image file 'imagen.png' not found.")
    label_error = tk.Label(popup_error_entry,
                           text='\n\nError al Introducir datos, recuerda que:\n\n-Valor son enteros.\n\n- Cantidad son '
                                'enteros.\n\n- Gastos pueden ser decimales, usando el punto.\n\n- Precio igual que '
                                'gastos.\n\n')
    label_error.config(font=('Terminal', 15))
    label_error.pack()

    boton_cerrar = tk.Button(popup_error_entry, text='Entendido', command=popup_error_entry.destroy)
    boton_cerrar.pack()


# Creamos frame para el label y el reloj
frame_superior = tk.Frame(window)

# Creamos el label.
cabecera = tk.Label(frame_superior, text=TITLE)
cabecera.config(font=('Terminal', 25))
cabecera.grid(row=0, column=0)

# Creamos el label para el reloj.
reloj = tk.Label(frame_superior, text='')
reloj.grid(row=0, column=1, columnspan=1)

frame_superior.grid(row=0, column=0)

# Creamos frame para opciones de compra y venta.

frame_opciones = tk.Frame(window)
frame_opciones.grid(row=1, column=1)

# Variable de control para los Radiobutton de las opciones.

opcion = tk.StringVar()
opcion_tobin = tk.BooleanVar()

# Variables de control

control_opcion = tk.IntVar()
control_qty = tk.IntVar()
control_expense = tk.DoubleVar()
control_price = tk.DoubleVar()
control_index = tk.IntVar()


# Funcion para añadir compra
def aniadir_compra():
    try:
        compra = csv_manager.Stock(stock=realtime[control_opcion.get()]['Stock'],
                                   buyprice=control_price.get(),
                                   qty=control_qty.get(),
                                   expense=control_expense.get(),
                                   index=control_index.get(),
                                   tobin =opcion_tobin.get())

        if opcion_tobin.get():
            compra.calcular_tobin()

        wallet_total.append(compra)
        print(wallet_total[0].stock)
    except tk.TclError:
        mostrar_popup_error()


'''def debug():
    indice = entry_stock.get()
    print(type(indice)'''


# Funcion para cambiar color boton
def color_boton():
    if opcion.get() == 'compra':
        boton_ejecutar.config(bg='red')
        # print(realtime)
    elif opcion.get() == 'venta':
        boton_ejecutar.config(bg='green')


# Creamos opciones dentro de frame.
opcion_radio_tobin = tk.Checkbutton(frame_opciones, text='Tobin', font=('Terminal', 16), variable=opcion_tobin)
opcion_venta = tk.Radiobutton(frame_opciones, text='Venta ', font=('Terminal', 16), variable=opcion, value='venta'
                              , command=color_boton)
opcion_venta.pack()

opcion_compra = tk.Radiobutton(frame_opciones, text='Compra ', font=('Terminal', 16), variable=opcion, value='compra'
                               , command=color_boton)
opcion_compra.pack()

label_stock = tk.Label(frame_opciones, text='Valor: ', font=('Terminal', 16))
label_info_stock = tk.Label(frame_opciones,
                            text='*Recuerda que para una venta,\n tienes que poner el indice de tu wallet.',
                            font=('Terminal', 7))
label_qty = tk.Label(frame_opciones, text='Cantidad: ', font=('Terminal', 16))
label_expense = tk.Label(frame_opciones, text='Gastos operacion: ', font=('Terminal', 16))
label_price = tk.Label(frame_opciones, text='Precio valor: ', font=('Terminal', 16))

entry_stock = tk.Entry(frame_opciones, textvariable=control_opcion)
entry_qty = tk.Entry(frame_opciones, textvariable=control_qty)
entry_expense = tk.Entry(frame_opciones, textvariable=control_expense)
entry_price = tk.Entry(frame_opciones, textvariable=control_price)

boton_ejecutar = tk.Button(frame_opciones, text='Ejecutar', font=('Terminal', 14), bg='green',
                           command=aniadir_compra)

label_stock.pack(padx=10, pady=5)
entry_stock.pack(padx=10, pady=5)
label_info_stock.pack()

label_price.pack(padx=10, pady=5)
entry_price.pack(padx=10, pady=5)

label_qty.pack(padx=10, pady=5)
entry_qty.pack(padx=10, pady=5)

label_expense.pack(padx=10, pady=5)
entry_expense.pack(padx=10, pady=5)

opcion_radio_tobin.pack(padx=10, pady=5)

boton_ejecutar.pack(padx=10, pady=5)

# Creamos tabla.

realtime_tabular = ttk.Treeview(window, height=35)

realtime_tabular.grid(row=1, column=0)

# Creamos tabla de wallet.

wallet_tabular = ttk.Treeview(window, height=35)

wallet_tabular.configure(columns=('Stock', 'BuyPrice', 'QTY', 'Expense', 'AccCharge', 'Balance', 'Tobin'))
wallet_tabular.grid(row=3, column=0)

# Label wallet
label_wallet = tk.Label(text='Wallet Personal', font=('Terminal', 20))

label_wallet.grid(row=2, column=0)


# Funcion para reloj en pantalla
def actualizar_hora():
    reloj.config(text=time.strftime('%H:%M:%S'), font=('Terminal', 25))
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
    global realtime

    result = urlcontent(url)
    realtime = scrapurl(result)
    df = pd.DataFrame(realtime)

    '''if wallet_total:
        print('\n' * 2)
        for x in wallet_total:
            for y in x:
                if y == "Balance":
                    for price in realtime:
                        if price["Stock"] == x["Stock"]:
                            x["Balance"] = "{} €".format((price["Price"] * x["Qty"]) - x["AccountCharge"])

            df1 = pd.DataFrame(wallet_total)'''
    return df


def mostrar_datos_tabulares():
    df = show_tiempo_real()
    for item in realtime_tabular.get_children():
        realtime_tabular.delete(item)
    columnas = list(df.columns)
    realtime_tabular['columns'] = columnas

    for col in columnas:
        realtime_tabular.column(col, anchor="center")
        realtime_tabular.heading(col, text=col)
    for i, row in df.iterrows():
        realtime_tabular.insert('', i, values=list(row))

    window.after(30000, mostrar_datos_tabulares)


def mostrar_datos_tabulares_wallet():
    for item in wallet_tabular.get_children():
        wallet_tabular.delete(item)

    for item in wallet_total:
        
        if item.tobin:
            item.calcular_tobin()

        wallet_tabular.insert('', 'end', values=(item.stock, item.buyprice, item.qty, item.expense
                                                 , item.accountcharge, item.balance, item.tobin))
    window.after(30000, mostrar_datos_tabulares_wallet)


mostrar_datos_tabulares()

mostrar_datos_tabulares_wallet()
window.mainloop()
