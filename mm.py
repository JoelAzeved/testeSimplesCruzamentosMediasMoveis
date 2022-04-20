from cProfile import label
from curses import window
from math import floor
from tkinter import Label
import pandas as pd
import numpy as np
import datetime as datetime
import yfinance as yf
import matplotlib.pyplot as plt


df = yf.download("PETR4.SA", "2018-01-01", "2022-04-15")

print(df) 

plt.figure(figsize=(12.5, 4.5))
plt.plot(df["Adj Close"],label= "PETR4", linewidth=2,color="blue")
plt.show()

mm1 = 8
mm2 = 25

ma1 = pd.DataFrame()
ma1["media curta"] = df["Adj Close"].rolling(window = mm1).mean()

ma2 = pd.DataFrame()
ma2["media de 20"] = df["Adj Close"].rolling(window = mm2).mean()

plt.figure(figsize=(16,10))
plt.plot(ma1["media curta"], label= "media curta", linewidth= 1, color = "green")
plt.plot(ma2["media de 20"], label= "media curta", linewidth= 1, color = "blue")

plt.title("fechamento")
plt.show()

df_r = pd.DataFrame()
df_r["Ativo"] = df["Adj Close"]
df_r["Media curta"] = ma1["media curta"]
df_r["media de 20"] = ma2["media de 20"]
df_r

def regra(base):
    preco_compra = []
    preco_venda = []
    aux = 1 

    for i in range(len(base)):
        if base["Media curta"][i] > base["media de 20"][i]:
            if aux !=1 :
                preco_compra.append(base["Ativo"][i])
                preco_venda.append(np.nan)
                aux = 1
            else:
                preco_compra.append(np.nan)
                preco_venda.append(np.nan)
        elif base["Media curta"][i] < base["media de 20"][i]:
            if aux != 0 :
                preco_compra.append(np.nan)
                preco_venda.append(base["Ativo"][i])
                aux = 0
            else:
                preco_compra.append(np.nan)
                preco_venda.append(np.nan)
        else:
            preco_compra.append(np.nan) 
            preco_venda.append(np.nan)    
    return(preco_compra,preco_venda)  

compra, venda = regra(df_r)
sinal = pd.DataFrame()
sinal["Compra"] = compra
sinal["Venda"] = venda
df_r["Compra"] = compra
df_r["Venda"] = venda

df_compra = df_r[~ df_r["Compra"].isna()]
df_compra

np.array(df_compra["Compra"])

df_venda = df_r[~ df_r["Venda"].isna()]
df_venda

np.array(df_venda["Venda"])[-1]
np.array(df_compra["Compra"])[-1]


np.array(df_venda["Venda"])[:-1] - np.array(df_compra["Compra"])[-1]

resultado = round(sum(np.array(df_venda["Venda"])[:-1]-np.array(df_compra["Compra"])[-1]), 2)

print("resultado por ação : R$ " + str(resultado))