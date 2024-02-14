from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

url = "https://www.productoscotizados.com/mercado/ibex-35"
HEADER = "Wellcome to wallettraker v1.0 by elhorDev"

def borrado_dep_so():
    borrado = None
    if os.name == "posix":
        borrado = "clear"
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        borrado = "cls"
    return borrado


def urlcontent(url):
    result = requests.get(url)
    return result


def scrapurl(result,realtime):
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")
    
    acciones = []
    precio_acciones = []
    tiempo_acciones = []
    var_acciones = []
    close_acciones = []
    more_or_less_acciones = []

    for acc in acc_scrap:
        acc = acc.text.replace("\t","").replace("\r","").replace("\n","")
        acciones.append(acc)
    for price in price_scrap:
        if "\nPrecio\n" not in price.text:
            price = price.text.replace("\n","").replace(",",".")
            precio_acciones.append(float(price))
    for time in time_scrap:
        if "\nÚLTIMA ACTUALIZACIÓN\n" not in time.text:
            time = time.text.replace("\n","")
            tiempo_acciones.append(time)
    for var in var_scrap:
        if "\n%\n" not in var.text:
            var = var.text.replace("\n","")
            var_acciones.append(var) 
    for close in close_scrap:
        if "\nPRECIO DE CIERRE\n" not in close.text:
            close = close.text.replace("\n","").replace("\t","").replace("\r","")
            close_acciones.append(close)
    for more_or_less in more_or_less_scrap:
        if "\n+/-" not in more_or_less.text:
            more_or_less = more_or_less.text.replace("\n","")
            more_or_less_acciones.append(more_or_less)
    for Stock, Price, Time, Var, Close, VarinPercent in zip(acciones, precio_acciones, tiempo_acciones, var_acciones, 
                                                            close_acciones, more_or_less_acciones):
        value = {"Stock":Stock, "Price":Price, "Time":Time, "%":Var, "Close":Close, "+/-":VarinPercent}
        realtime.append(value) 

def ad_to_wallet(realtime,wallet_total,borrado):
    
    df_acciones = pd.DataFrame(realtime)
    print(df_acciones)
    try:
        opcion = int(input("Qué valor del Ibex 35 has comprado?\n"))
                
               

        Stock = realtime[opcion]["Stock"]
        Buyprice = float(input(f"A que precio has comprado las acciones de {Stock} ?\n"))
        Qty = int(input(f"Cuantas acciones de {Stock} has comrpado a {Buyprice}?\n"))
        Expense = float(input("Cuanto te han cobrado de gastos de compra?\n"))
        Index = opcion
        wallet = dict(
                        Stock = Stock,
                        Buyprice = Buyprice,
                        Qty = Qty,
                        Expense = Expense,
                        Index = Index,
                        AccountCharge = (Buyprice * Qty) + Expense,
                        Balance = 0
                    )
        os.system(borrado)
        print(f"Añadida la compra de {Qty} acciones de {Stock} por un cargo en cuenta de {wallet['AccountCharge']} euros.")
        wallet_total.append(wallet)
    except ValueError:
            os.system(borrado)
            print("Valor introducido incorrecto, solo valor numerico.")
            sleep(5)
            os.system(borrado)
            ad_to_wallet(realtime,wallet_total,borrado)
    except IndexError:
            os.system(borrado)
            print(f"El Indice introducido se ha salido del rango, por favor , elije del 0 al {len(realtime)-1}.")
            sleep(5)
            os.system(borrado)
            ad_to_wallet(realtime,wallet_total,borrado)
    sleep(5)
    os.system(borrado)
    menu_principal(realtime,wallet_total,borrado)

def show_tiempo_real(wallet_total,realtime,borrado):
    
    while True:
        realtime = []
        os.system(borrado)
        result = urlcontent(url)          
        scrapurl(result,realtime)
        df = pd.DataFrame(realtime)
        print(df)
        if wallet_total:
            print('\n'*2)
            for x in wallet_total:
                 for y in x:   
                    if y == "Balance":
                        for price in realtime:
                            if price["Stock"] == x["Stock"]:
                                x["Balance"] = "{} €".format((price["Price"] * x["Qty"]) - x["AccountCharge"])


            df1 = pd.DataFrame(wallet_total)
            print(df1)
        sleep(5)

def wellcome_menu(borrado):
    print ("\n" + HEADER + "\n" + "-" *len(HEADER) + "\n")
    type_wallet = input("Como deseas trabajar?\n"
                            "[A]Importar Wallet.\n"
                            "[B]Wallet Temporal.\n"
                            "[Q]Para Salir\n\n")
    os.system(borrado)
    while type_wallet != "Q" and type_wallet != "q":
        
        if type_wallet == "A" or type_wallet == "a":
            wallet_total = upload_wallet()
            return wallet_total
        if type_wallet == "b" or type_wallet == "B":
            wallet_total = []
            return wallet_total
           
    print("Hasta la proxima!")
    exit()   
    
def menu_principal(realtime,wallet_total,borrado):
    os.system(borrado)
    opcion = input("Elije la opción:\n"
                   "[A]Añadir a tu cartera.\n"
                   "[B]Eliminar de tu cartera.\n"
                   "[C]Tiempo Real.\n"
                   "[D]Guardar Wallet\n"
                   )
    os.system(borrado)
    if opcion == "A" or opcion == "a":
        ad_to_wallet(realtime,wallet_total,borrado)
    if opcion == "B" or opcion == "b":
        delete_to_wallet(realtime,wallet_total,borrado)
    if opcion == "C" or opcion == "c":
        show_tiempo_real(wallet_total,realtime,borrado)    
    if opcion == "D" or opcion == "d":
        save_wallet(wallet_total)  
    
    return opcion

def delete_to_wallet(realtime,wallet_total,borrado):
    try:
        if wallet_total:
            walletdf = pd.DataFrame(wallet_total)
            print(walletdf)
            opcion = int(input("Que movimiento quieres eliminar?\n"))
            wallet_total.pop(opcion)
            os.system(borrado)
            print("Movimiento Eliminado")
            sleep(5)
            menu_principal(realtime,wallet_total,borrado)
        else:
            print("Tu wallet esta Vacia")
            sleep(5)
            menu_principal(realtime,wallet_total,borrado)
    except ValueError:
            os.system(borrado)
            print("Valor introducido incorrecto, solo valor numerico.")
            sleep(5)
            os.system(borrado)
            delete_to_wallet(realtime,wallet_total,borrado)
    except IndexError:
            os.system(borrado)
            print(f"El Indice introducido se ha salido del rango, por favor , elije del 0 al {len(wallet_total)-1}.")
            sleep(5)
            os.system(borrado)
            delete_to_wallet(realtime,wallet_total,borrado)    

def save_wallet(wallet_total):
    if wallet_total:
        df1 = pd.DataFrame(wallet_total)
        df1.to_csv("wallet.csv")
        print("Cartera guardada con exito!")
    else:
        print("Wallet temporal vacia, imposible generar.")

def upload_wallet():
    try:
        
        saved_wallet = pd.read_csv("wallet.csv",index_col=0)
        wallet_total = saved_wallet.to_dict("records")
        print("Cartera cargada correctamente!")
        sleep(5)
        return wallet_total
        
    except:
        print("No existe un Wallet guardado actualmente.")
        wallet_total = []
        sleep(5)
        return wallet_total
    
def main():   
        borrado = borrado_dep_so()
        wallet_total = wellcome_menu(borrado)
        while True:
            realtime = []
            result = urlcontent(url)
            scrapurl(result,realtime)
            opcion = menu_principal(realtime,wallet_total,borrado)

    

if __name__ == "__main__":
    main()
