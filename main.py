import yfinance as yf
import pandas as pd
import time

accion = input("Introduzca la accion que desea monitorear: ")

token = yf.Ticker(accion)

info_token = token.info
try:
    current_price = info_token.get("currentPrice")
except Exception as e:
    print(f"Error obteniendo el precio: {e}")
    exit()


print(f"El precio actual de la accion es {current_price}")


precio_objetivo = float(input(
    "Introduzca el precio al cual desea que se le mande un aviso: ")
)
if (precio_objetivo > current_price):
    while (precio_objetivo > current_price):
        token = yf.Ticker(accion)
        info_token = token.info
        current_price = info_token.get("currentPrice")
        print(f"El precio actual de la accion es {current_price}")
        time.sleep(2)
elif (precio_objetivo < current_price):
    while (precio_objetivo < current_price):
        token = yf.Ticker(accion)
        info_token = token.info
        current_price = info_token.get("currentPrice")
        print(f"El precio actual de la accion es {current_price}")
        time.sleep(2)
else:
    print("Valor no valido")

print(f"La accion {accion} ha llegado al valor deseado {precio_objetivo}")
