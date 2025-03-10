import pandas as pd
import os
from tkinter import messagebox

def ler_dados (caminho_arquivo):

    # Cria listas que irão armazenar as coordenadas x e y do arquivo
    x = []
    y = []

    # Verifica o tipo do arquivo e realiza uma leitura específica para ele
    if os.path.splitext (caminho_arquivo) [1] == '.txt' or os.path.splitext (caminho_arquivo) [1] == '.dpt':
        df = pd.read_csv (caminho_arquivo, sep = '\t', names = ['x', 'y'])
        tipo = 'txt'

    elif os.path.splitext (caminho_arquivo) [1] == '.csv':
        df = pd.read_csv (caminho_arquivo, sep = ',', names = ['x', 'y'])
        tipo = 'csv'
    try:
        # Percorre cada linha do DataFrame transformando ela em uma Series
        # O método .iterows() retorna o index da linha e uma Series contendo os elementos daquela linha
        for indice, serie in df.iterrows():

            # Percorre os elementos de cada linha
            for i in [0]:

                # Verifica se o elemento da linha é uma string e possui uma vírgula que deve ser substituída por um ponto
                if tipo == 'txt' and type (serie.iloc[i]) is str:
                    serie.iloc[i] = float(serie.iloc[i].replace(',','.'))
                if tipo=='txt' and type (serie.iloc[i+1]) is str:
                    serie.iloc[i+1] = float(serie.iloc[i+1].replace(',','.'))
            
                # Armazena o valor nas listas que contém as coordenadas
                x.append (serie.iloc[i])
                y.append (serie.iloc[i+1]) 

        return x, y
    except:
        messagebox.showerror (title = 'Erro de leitura',
                              message = 'O arquivo selecionado não pode ser lido.'+
                              ' Verifique se o arquivo segue a seguinte formatação:\n'+
                              '- O formato do arquivo é algum destes: .txt, .dpt ou .csv\n'+
                              '- Há apenas números no arquivo contendo os dados\n'+
                              '- O arquivo possui apenas duas colunas\n'+
                              '- A linha inicial do arquivo não está vazia')
        return False