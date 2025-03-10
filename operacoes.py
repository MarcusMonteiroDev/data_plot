import numpy as np
from tkinter import messagebox

# Usa a regra do trapézio generalizada para calcular a integral numérica
def integral_regra_trapezio (eixo_x, eixo_y, a, b):
    # Transforma as listas em ndarrays para ganhar desempenho no cálculo
    eixo_x = np.array (eixo_x)
    eixo_y = np.array (eixo_y)

    # Realiza a integração com base no intervalo a e b fornecidos
    # Caso a e b não sejam fornecidos, realiza a integração em todo o intervalo
    if a == '' and b == '':
        integral = (eixo_x[-1] - eixo_x[0]) * (2 * np.sum (eixo_y) - eixo_y[-1] - eixo_y[0]) / (2 * (np.size (eixo_x) - 1))
        # Retorna o resultado da integral
        return integral

    # Caso a e b sejam fornecidos, realiza a integração no intervalo formado entre a e b
    elif (a != '' and b != '') and (a < b):
        # Verifica se a e b estão contidos nos dados lidos
        try:
            # Encontra os índices dos intervalos de integração (a e b) existentes nos dados do eixo_x
            b_indice = np.where (eixo_x == b) [0][0]
            a_indice = np.where (eixo_x == a) [0][0]

            # Fórmula da aplicação múltipla da regra do trapézio para calcular a integral numérica
            # É necessário fatiar os arrays (array[a_indice:b_indice+1]) para efetuar o cálculo no intervalo especificado
            integral = (b - a) * (2 * np.sum (eixo_y[a_indice : b_indice+1]) - eixo_y[b_indice] - eixo_y[a_indice]) / (2 * (np.size (eixo_x[a_indice : b_indice+1]) - 1))
            
            # Retorna o resultado da integral
            return integral
        # Caso a ou b não esteja contido no arquivo de leitura de dados, exibe um aviso alertando o usuário
        except IndexError or UnboundLocalError: 
            messagebox.showwarning (title = "Atenção", message = "O valor inicial ou final não está contido no arquivo de eitura de dados")

    # Caso somente o valor inicial não seja especificado, realiza a integração desde o início dos dados até o valor final do intervalo
    elif a == '' and b != '':
        try:
            # Encontra o índice de b existente nos dados do eixo_x
            b_indice = np.where (eixo_x == b) [0][0]

            # Fórmula da aplicação múltipla da regra do trapézio para calcular a integral numérica
            # É necessário fatiar os arrays (array[:b_indice+1]) para efetuar o cálculo no intervalo especificado
            integral = (b - eixo_x[0]) * (2 * np.sum (eixo_y[:b_indice+1]) - eixo_y[b_indice] - eixo_y[0]) / (2 * (np.size (eixo_x[:b_indice+1]) - 1))
            
            # Retorna o resultado da integral
            return integral
        
        # Caso a ou b não esteja contido no arquivo de leitura de dados, exibe um aviso alertando o usuário
        except IndexError or UnboundLocalError: 
            messagebox.showwarning (title = "Atenção", message = "O valor inicial ou final não está contido no arquivo de eitura de dados")

    # Caso somente o valor final não seja especificado, realiza a integração desde o valor inicial até o fim do intervalo dos dados
    elif a != '' and b == '':
        try:
            # Encontra o índice de a existente nos dados do eixo_x
            a_indice = np.where (eixo_x == a) [0][0]

            # Fórmula da aplicação múltipla da regra do trapézio para calcular a integral numérica
            # É necessário fatiar os arrays (array[a_indice:]) para efetuar o cálculo no intervalo especificado
            integral = (eixo_x[-1] - a) * (2 * np.sum (eixo_y[a_indice:]) - eixo_y[-1] - eixo_y[a_indice]) / (2 * (np.size (eixo_x[a_indice:]) - 1))
            
            # Retorna o resultado da integral
            return integral
        
        # Caso a ou b não esteja contido no arquivo de leitura de dados, exibe um aviso alertando o usuário
        except IndexError or UnboundLocalError: 
            messagebox.showwarning (title = "Atenção", message = "O valor inicial ou final não está contido no arquivo de eitura de dados")

    # Caso o valor inicial seja maior do que o valor final, exibe uma mensagem de alerta
    elif a >= b: messagebox.showwarning (title = "Atenção", message = "O valor inicial não pode ser maior ou igual ao valor final")

