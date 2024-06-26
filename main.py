import os  # Solo para debug y comprobacion de PATH
import time
import tkinter as tk
from tkinter import ttk

import pandas as pd
from PIL import Image, ImageTk

import constants
import csv_manager
import functions

global imagen_tk

realtime = []


# Funcion para añadir compra
def aniadir_compra():
    try:
        compra = csv_manager.Stock(stock=realtime[control_opcion.get()]['Stock'],
                                   buyprice=control_price.get(),
                                   qty=control_qty.get(),
                                   expense=control_expense.get(),
                                   index=control_index.get(),
                                   tobin=opcion_tobin.get())

        if opcion_tobin.get():
            compra.calcular_tobin()

        constants.WALLET_TOTAL.append(compra)
        mostrar_pop_up_compra()

    except tk.TclError:
        mostrar_popup_error()


def aniadir_venta():
    try:
        delete_wallet = control_opcion.get()
        constants.WALLET_TOTAL.pop(delete_wallet)
        mostrar_pop_up_venta()
    except IndexError:
        mostrar_popup_error()


'''def debug():
    indice = entry_stock.get()
    print(type(indice)'''


# Funcion para reloj en pantalla
def actualizar_hora():
    reloj.config(text=time.strftime('\t%H:%M:%S'), font=('Terminal', 25))
    window.after(1000, actualizar_hora)


# Popup para gestionar las excepciones de los entry.
def mostrar_popup_error():
    popup_error_entry = tk.Toplevel(window)
    popup_error_entry.title('Error')
    popup_error_entry.geometry('600x450')

    if os.path.exists(constants.PATH_ERROR_IMG):
        imagen = Image.open(constants.PATH_ERROR_IMG)
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


def mostrar_pop_up_venta():
    pop_up_venta = tk.Toplevel(window)
    pop_up_venta.title('Venta')
    pop_up_venta.geometry('250x80')

    label_venta = tk.Label(pop_up_venta, text='Venta producida con exito\n')
    boton_cerrar = tk.Button(pop_up_venta, text='Cerrar', command=pop_up_venta.destroy)

    label_venta.pack()
    boton_cerrar.pack()


def mostrar_pop_up_compra():
    pop_up_compra = tk.Toplevel(window)
    pop_up_compra.title('Compra')
    pop_up_compra.geometry('250x80')

    label_compra = tk.Label(pop_up_compra, text='Compra producida con exito\n')
    boton_cerrar = tk.Button(pop_up_compra, text='Cerrar', command=pop_up_compra.destroy)

    label_compra.pack()
    boton_cerrar.pack()


# Funcion para cambiar color boton y habilitar o deshabilitar la entrada de los entry y configurar en boton
# con el command de venta o de compra
def color_boton():
    if opcion.get() == 'venta':
        boton_ejecutar.config(bg='green', command=aniadir_venta)
        entry_qty.config(state='disabled')
        entry_price.config(state='disabled')
        entry_expense.config(state='disabled')
        opcion_radio_tobin.config(state='disabled')
        # print(realtime)
    elif opcion.get() == 'compra':
        boton_ejecutar.config(bg='red', command=aniadir_compra)
        entry_qty.config(state='normal')
        entry_price.config(state='normal')
        entry_expense.config(state='normal')
        opcion_radio_tobin.config(state='normal')


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
    print('Actualizando tiempo real cada {} segundos'.format(freq_actualizacion_var_control.get()))
    window.after(freq_actualizacion_var_control.get() * 1000, mostrar_datos_tabulares)


def mostrar_datos_tabulares_wallet():
    index_wallet = -1

    for item in wallet_tabular.get_children():
        wallet_tabular.delete(item)
    if constants.WALLET_TOTAL:
        columns = ['Index', 'Stock', 'QTY', 'Expense', 'AccCharge', 'Balance', 'Tobin']
        wallet_tabular['columns'] = columns
        for col in columns:
            wallet_tabular.column(col, anchor='center')
            wallet_tabular.heading(col, text=col)

        for compra in constants.WALLET_TOTAL:
            index_wallet += 1
            compra.index = index_wallet
            for accion in realtime:
                if accion['Stock'] == compra.stock:
                    compra.balance = '{}€'.format(round((accion['Price'] * compra.qty) - compra.accountcharge), 2)

            wallet_tabular.insert('', 'end', values=(compra.index, compra.stock, compra.qty,
                                                     compra.expense, compra.accountcharge, compra.balance,
                                                     compra.tobin))
            print('Actualizando wallet cada {} segundos'.format(freq_actualizacion_var_control.get()))
    window.after(freq_actualizacion_var_control.get() * 1000, mostrar_datos_tabulares_wallet)


# Creamos funcion para mostrar el tiempo real.
def show_tiempo_real():
    global realtime

    result = functions.urlcontent()
    realtime = functions.scrapurl(result)
    df = pd.DataFrame(realtime)

    return df


def control_freq_actualizacion(nuevo_valor):
    freq_actualizacion_var_control.set(nuevo_valor)
    print(freq_actualizacion_var_control.get())


# Configuracion de la ventana Root.
window = tk.Tk()
window.title('WallettrakerUI by elhor')
window.geometry('1920x1080')
window.resizable(False, False)
# window.iconbitmap(constants.PATH_ICON_WINDOW)

# Crear la barra de menu
barra_menu = tk.Menu(window)

# Creamos menu archivo
archivo_menu = tk.Menu(barra_menu, tearoff=False)
archivo_menu.add_command(label='Cargar cartera')
archivo_menu.add_command(label='Guardar cartera')
archivo_menu.add_separator()
archivo_menu.add_command(label='Salir', command=window.quit)

# Agregar el menu archivo a la barra_menu
barra_menu.add_cascade(label='Archivo', menu=archivo_menu)
window.config(menu=barra_menu)

# Creamos frame para el label y el reloj
frame_superior = tk.Frame(window)

# Creamos el label.
cabecera = tk.Label(frame_superior, text=constants.TITLE)
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

opcion = tk.StringVar(value='venta')
opcion_tobin = tk.BooleanVar()

# Variables de control

control_opcion = tk.IntVar()
control_qty = tk.IntVar()
control_expense = tk.DoubleVar()
control_price = tk.DoubleVar()
control_index = tk.IntVar()

# Creamos un tk.scale para controlar la actualizacion.

freq_actualizacion_var_control = tk.IntVar(value=10)

label_slide = tk.Label(frame_opciones, text='\n\nFrecuencia de actualizacion', font=('Terminal', 10))
label_bajo_slide = tk.Label(frame_opciones, text='Segundos', font=('Terminal', 8))
slide = tk.Scale(frame_opciones, from_=3, to=20, orient='horizontal', resolution=1,
                 variable=freq_actualizacion_var_control, command=control_freq_actualizacion, sliderlength=10)

# Creamos opciones dentro de frame.
opcion_radio_tobin = tk.Checkbutton(frame_opciones, text='Tobin', font=('Terminal', 16), variable=opcion_tobin)
opcion_venta = tk.Radiobutton(frame_opciones, text='Venta ', font=('Terminal', 16), variable=opcion, value='venta',
                              command=color_boton)
opcion_venta.pack()

opcion_compra = tk.Radiobutton(frame_opciones, text='Compra ', font=('Terminal', 16), variable=opcion, value='compra',
                               command=color_boton)
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

label_slide.pack()
slide.pack()
label_bajo_slide.pack()

# Creamos tabla.

realtime_tabular = ttk.Treeview(window, height=35)

realtime_tabular.grid(row=1, column=0)

# Creamos tabla de wallet.

wallet_tabular = ttk.Treeview(window, height=35)

wallet_tabular.grid(row=3, column=0)

# Label wallet
label_wallet = tk.Label(text='Wallet Personal', font=('Terminal', 20))

label_wallet.grid(row=2, column=0)


def main():
    actualizar_hora()
    color_boton()
    mostrar_datos_tabulares()
    mostrar_datos_tabulares_wallet()
    window.mainloop()


if __name__ == "__main__":
    main()
