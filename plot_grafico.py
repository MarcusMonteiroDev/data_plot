# Importa o módulo de plot de gráficos
import matplotlib.pyplot as plt

# Define a função que plota o gráfico na tela
def plot_grafico (x, y, 
                  cores_das_series,
                  legenda_serie,
                  titulo_grafico, 
                  titulo_eixo_x, 
                  titulo_eixo_y,
                  tipo_grafico,
                  mostrar_grid,
                  intervalo_x1,
                  intervalo_x2):
    
    # Cria a figura e os subplots
    fig, ax = plt.subplots()

    # Armazena as cores na linguagem do Matplotlib
    cor_selecionada = []

    # Percorre as cores de cada série e converte para a linguagem do Matplotlib
    for item in cores_das_series:
        # Sekeciona a cor de cada serie
        if item == 'Azul': item = 'blue'
        elif item == 'Vermelho': item = 'red'
        elif item == 'Verde': item = 'green'
        elif item == 'Amarelo': item = 'yellow'
        elif item == 'Preto': item = 'black'
        elif item == 'Roxo': item = 'purple'
        elif item == 'Laranja': item = 'orange'
        # Armazena cada cor convertida na lista de cores que será usada no plot do gráfico
        cor_selecionada.append (item)

    # Seleciona o tipo do gráfico
    # Tipo 0 gráfico de dispersão
    if tipo_grafico == 0: 
        # Percorre todas as listas presentes dentro dos dados fornecidos
        # Para cada lista plota os dados no gráfico
        for i in range (0, len (x)):
            ax.scatter (x[i],                           # Plota dados do eixo x
                        y[i],                           # Plota dados do eixo y
                        label = legenda_serie[i],       # Define a legenda da série
                        color = cor_selecionada[i]      # Define a cor da série
                        )

    # Tipo 1 gráfico de linha
    elif tipo_grafico == 1: 
        # Percorre todas as listas presentes dentro dos dados fornecidos
        # Para cada lista plota os dados no gráfico
        for i in range (0, len (x)):
            ax.plot (x[i],                           # Plota dados do eixo x
                     y[i],                           # Plota dados do eixo y
                     label = legenda_serie[i],       # Define a legenda da série
                     color = cor_selecionada[i]      # Define a cor da série
                     )

    # Insere título e outros aspectos visuais do gráfico
    # Verifica se haverá legenda no gráfico
    for i in legenda_serie:
        if i != '': 
            ax.legend()
            break        
    
    # Verifica se haverá limites de exibição no gráfico
    if intervalo_x1 != '' or intervalo_x2 != '':
        ax.set_xlim (intervalo_x1, intervalo_x2)
        
    ax.set_title (titulo_grafico)       # Título do gráfico
    ax.set_xlabel (titulo_eixo_x)       # Título do eixo x
    ax.set_ylabel (titulo_eixo_y)       # Título do eixo y
    ax.grid (mostrar_grid)              # Mostrar grid

    # Exibe o gráfio na tela
    plt.show()