# Importa os módulos de Interface Gráfica de Usuário (GUI, em inglês) do Python
import tkinter as tk                # Módulo GUI built in do python
import ttkbootstrap as ttk          # Módulo de estilização
from tkinter import filedialog      # Módulo de caixas de diálogo
from tkinter import messagebox      # Módulo de caixas de mensagem
from PIL import Image, ImageTk      # Módulo de tratamento e exibição de imagens
# Importa o módulo que permite abrir links np navegador web
import webbrowser
# Importa a função que lê os dados selecionados
from ler_dados import ler_dados
# Importa a função que gera o gráfico
from plot_grafico import plot_grafico
# Importa a função que realiza as operações numéricas do programa
import operacoes

#-----------------------------------------------------------------------------------------------------------------------------------
# Declaração de variáveis globais que controlam a leituda de dados
caminho_arquivo = []        # Armazena o caminho dos arquivos a serem lidos pelo programa
eixo_x = []                 # Armazena dados referentes ao eixo x do gráfico de cada leitura de arquivo
eixo_y = []                 # Armazena dados referentes ao eixo y do gráfico de cada leitura de arquivo
obj_arquivos_selec = []     # Armazena os frames correspondentes a cada leitura de arquivo
identificador = 0           # Identifica cada frame de leitura por um número inteito
cores = ['Azul', 'Vermelho', 
         'Verde', 'Amarelo', 
         'Laranja', 'Roxo', 
         'Preto']           # Lista de cores que podem ser selecionadas

#-----------------------------------------------------------------------------------------------------------------------------------
# Função responsável por incrementar o valor do identificador
def adicionar ():
    global identificador
    identificador += 1

# Função que verifica se todos os elementos da lista são nulos ou vazios
def verificar_lista_nula (lista):
    # Variável índice usada para fazer a verificação
    j = 0

    # Percorre a lista passada como parâmetro
    for i in lista:
        # Verifica se o item em questão é nulo ou vazio
        if i == None or i == '': 
            # Adiciona um ao valor do índice sempre que o item da lista for nulo ou vazio
            j += 1

    # Caso o valor do índice seja igual o tamanho da lista, isso implica que todos os elementos
    # da lista são nulos e a função retorna um valor True
    if j == len (lista): 
        return True
    # Caso hajam elementos não nulos ou vazios da lista, retorna o valor False
    else: 
        return False

# Função que verifica a quantidade de itens válidos da lista
def verificar_tamanho_lista (lista):
    # Variável  usada para fazer a verificação
    j = 0
    # Lista que armazena todos os índices dos elementos não nulos da lista
    indices_validos = []
    # Variável que acompanha a mudança de índice
    indice = -1

    # Percorre a lista passada como parâmetro
    for i in lista:
        indice += 1
        # Verifica se o item em questão é nulo
        if i != None: 
            # Adiciona um ao valor à variável sempre que o item da lista não for nulo
            j += 1
            # Armazena na lista de índices válidos
            indices_validos.append (indice)
            
    # Retorna o número de itens válidos da lista bem como uma lista contedo a posição destes itens válidos
    return j, indices_validos

# Função que retorna o nome do arquivo selecionado para leitura
def vizualizar_nome_arquivo_selecionado (caminho):
    return caminho [len(caminho) - caminho[::-1].index('/') :: ]

#-----------------------------------------------------------------------------------------------------------------------------------
# Cria a classe App que contém a janela principal do programa
# Esta classe herda ttk.Window
class App (ttk.Window):
    # Define o método __init__
    def __init__ (self):
        # Herda os atributos da classe mãe 
        super().__init__()

        # Define o título da janela
        self.title ('Data Plot')
        # Define o tamanho inicial da janela
        self.geometry ('400x800')
        # Define o tamanho mínimo da janela
        self.minsize (400, 800)

        # Cria um frame de fundo onde o Canvas será posicionado, a presença deste frame é importante
        # para que não ocorram distorções visuais ao atualizar a janela tk.Tk
        self.frame_fundo = ttk.Frame (self)
        self.frame_fundo.pack (expand = True, fill = 'both')

        # Cria uma janela rolável utilizando o Canvas
        self.janela_de_rolagem = tk.Canvas (self.frame_fundo, 
                                            # Define em qual região o canvas pode ser rolado na página
                                            # Na tupla temos (esquerda, cima, direita, baixo) que recebem
                                            # valores numéricos que determina em quantos pixels a região será
                                            # rolável em determinada direção
                                            scrollregion = (0, 0, self.winfo_width(), 5000)
                                            )
        self.janela_de_rolagem.pack (expand = True, fill = 'both')
        
        # Crie o frame que será posicionado na janela de rolagem e será a base para os outros frames do programa
        self.frame_base = ttk.Frame (self.frame_fundo, )

        # Atribui um evento ao Canvas que permite a rolagem utilizando a roda do mouse
        self.janela_de_rolagem.bind_all ('<MouseWheel>',
                                         # Chama a função específica que fará a rolagem de forma vertical
                                         # O primeiro parâmetro representa a quantidade de pixels a serem deslocados
                                         # a cada rolagem e o segundo argumento representa a unidade padrão do Tkinter 
                                         lambda event: self.janela_de_rolagem.yview_scroll (-int(event.delta/60), 'units'))
        
        # Atribui um evento ao frame de fundo que irá atualizá-lo constantemente de forma a desenhar no Canvas
        # o frame base e atualiza-lo sempre que uma nova ação do usuário no programa for realizada
        self.frame_fundo.bind ('<Configure>', self.atualizar_janela)

        # Define o estilo de widgets específicos
        estilo_label = ttk.Style()
        estilo_label.configure ('TLabel',
                                background = '#FCFCFC')

        estilo_botao = ttk.Style()
        estilo_botao.configure ('TButton', 
                                font = ('Roboto', 10))              # Estilo dos botões

        estilo_radio = ttk.Style()
        estilo_radio.configure ('TRadiobutton', 
                                font = ('Roboto', 10), 
                                background = '#FCFCFC')             # Estilio dos botões radio

        estilo_grid = ttk.Style()
        estilo_grid.configure ('TCheckbutton', 
                               font = ('Roboto', 10), 
                               background = '#FCFCFC')              # Estilo dos botões check

        estilo_frame = ttk.Style()
        estilo_frame.configure ('TFrame', 
                                background = '#FCFCFC')             # Estilo dos frames

        # Exibe a imagem de logo do programa
        #imagem = Image.open ('img/logo.png').resize ((180, 200))
        #imagem_final = ImageTk.PhotoImage (imagem)
        #ttk.Label (self.frame_base, image = imagem_final, borderwidth = 0).pack()

        # Cria e posiciona a label que exibe a versão do programa
        ttk.Label (self.frame_base, text = 'Versão 2.0', font = ('Roboto', 9)).pack()

        # Chama o frame principal que contém as principais funcionalidades do programa
        self.frame_principal = FramePrincipal (self.frame_base)

        # Chama o método que cria o menu da janela principal
        self.criar_menu()

        # Executa a janela
        self.mainloop()

    # Método responsável por atualizar a janela constantemente
    def atualizar_janela (self, event):
        # Posiciona no Canvas o frame base
        self.janela_de_rolagem.create_window ((0,0),                        # Posição de início
                                              window = self.frame_base,     # Janela a ser posicionada no Canvas
                                              anchor = 'nw',                # âncora da janela
                                              height = 5000,                # Altura da janela
                                              width = self.winfo_width()    # Largura da janela
                                              )

    # Método que cria o menu do programa
    def criar_menu (self):
        # Declara o menu que será a base dos outros menus
        menu_base = ttk.Menu (self)

        # Declara o menu que contém informações do programa
        menu_informacoes = ttk.Menu (self)
        menu_base.add_cascade (label = 'Informações', menu = menu_informacoes)

        # Declara os submenus dentro do menu de informações
        menu_informacoes.add_command (label = 'Código fonte',
                                      command = lambda: webbrowser.open ('https://github.com/marcusmonteiro12/Data_plot'))
        
        menu_informacoes.add_command (label = 'Manual de instruções',
                                      command = lambda: webbrowser.open ('https://docs.google.com/document/d/1QVlfnA9x-g7hXnVuG8BKAmcX45YMzRe9/edit?usp=sharing&ouid=114170842824316500229&rtpof=true&sd=true'))

        # Declara o menu de operações e posiciona no menu base
        menu_operacoes = ttk.Menu (menu_base, tearoff=False)
        menu_base.add_cascade (label = 'Operações', menu = menu_operacoes)

        # Declara os submenus dentro do mnu de operações
        menu_operacoes.add_command (label = 'Integração',               # Abre a janela de integração
                                    command = self.janela_integral_numerica)
        
        menu_operacoes.add_command (label = 'Encontrar máximos e mínimos',                # Abre a janela de derivação
                                    command = self.derivada_numerica)
        
        menu_operacoes.add_command (label = 'Ajuste de curva',          # Abre a janela de ajuste de curva
                                    command = self.ajuste_curva)

        # Exibe o menu base
        self.configure (menu = menu_base)

    # Método que abre a janela onde pode ser feita a integração numérica
    def janela_integral_numerica (self):
        # Declaração de classe do método
        # Define o botão de seleção de arquivos para realizar a operação
        class BotaoSelecao (ttk.Button):
            # Este objeto recebe como parâmetros o master, nome do arquivo e identificador do arquivo
            def __init__ (self, master, nome ,id):
                super().__init__ (master = master, 
                                  text = nome,
                                  # Usa o identificador do botão criado para realizar a operação
                                  command = lambda: substituir_janela (self.id)
                                  )
                # Objeto recebe o atributo de identificação
                self.id = id
                # Exibe o botão na tela
                self.pack()

        #----------------------------------------------------------------------------------------------------------------------------
        # Declaração de funções do método
        # Define a função interna ao método que será usada para exibir os widgets responsáveis pela
        # seleção do intervalo de integração. Realiza a operação de acordo com o id do conjunto de dados
        def widgets_integracao (master, id):
            # Declara as variáveis de controle correspondentes aos limites inicial e final de integração
            valor_inicial = tk.StringVar()
            valor_final = tk.StringVar()
            
            # Cria os widgets de seleção de intervalo de integração
            frame_widgets_integração = ttk.Frame (master = master)
            frame_widgets_integração.pack (expand = True, fill = 'both')

            label_selec_intervalo = ttk.Label (frame_widgets_integração, 
                                               text = 'Escolha o intervalo de integração', 
                                               font = ('Rodonto', 11),
                                               borderwidth = 0)
            label_selec_intervalo.pack(pady = 3)

            frame_valor_inicial = ttk.Frame (frame_widgets_integração, borderwidth = 0)
            frame_valor_inicial.pack(pady = 3)

            label_valor_inicial = ttk.Label (frame_valor_inicial, 
                                             text = 'Valor inicial ', 
                                             font = ('Rodonto', 11),
                                             borderwidth = 0)
            label_valor_inicial.pack(side = 'left', pady = 3)

            entry_valor_inicial = ttk.Entry (frame_valor_inicial, textvariable = valor_inicial)
            entry_valor_inicial.pack(side = 'right', pady = 3)

            frame_valor_final = ttk.Frame (frame_widgets_integração, borderwidth = 0)
            frame_valor_final.pack(pady = 3)

            label_valor_final = ttk.Label (frame_valor_final, 
                                           text = 'Valor final ', 
                                           font = ('Rodonto', 11),
                                           borderwidth = 0)
            label_valor_final.pack(side = 'left', pady = 3)

            entry_valor_final = ttk.Entry (frame_valor_final, textvariable = valor_final)
            entry_valor_final.pack(side = 'right', pady = 3)

            botao_calcular = ttk.Button (frame_widgets_integração,
                                         text = 'Calcular',
                                         command = lambda: resultado (frame_widgets_integração, 
                                                                      id,
                                                                      valor_inicial.get(),
                                                                      valor_final.get()
                                                                      )
                                        )
            botao_calcular.pack(pady = 3)

        # Função que substitúi a janela atual para outra onde pode ser selecionado o intervalo de integração
        def substituir_janela (id):
            # Destrói a janela atual
            janela.destroy()

            # Abre uma nova janela onde poderá ser realizada a integração
            nova_janela = ttk.Toplevel()          # Cria e exibe a janela na tela
            nova_janela.geometry ('300x400')     # Define o tamanho inicial da janela
            nova_janela.title ('Integração')     # Define o título da janela

            # Posiciona na nova janela os widgets de integação e passa o id do arquivo a se realizar a operação
            widgets_integracao (nova_janela, id)

        # Função que exibe o resultado da operação de integração na tela
        def resultado (master, id, valor_inicial, valor_final):
            # Verifica se o intervalo de integração inserido pelo usuário é válido
            try:
                if valor_inicial != '':
                    valor_inicial = float (valor_inicial)

                if valor_final != '':
                    valor_final = float (valor_final)

            except:
                messagebox.showerror (title = 'Erro', message = 'O intervalo de integração não é válido')
                return

            # Chama a função que retorna o valor da integração
            # O conjunto de dados usado no cálculo é determinado pelo id do arquivo escolhido pelo usuário
            resultado = operacoes.integral_regra_trapezio (eixo_x[id], eixo_y[id], valor_inicial, valor_final)
            # Exibe o resultado em uma label
            ttk.Label (master = master ,text = f'Resultado: {resultado}', font = ('Rodonto', 11)).pack()

        #--------------------------------------------------------------------------------------------------------------------------
        # Verifica se há dados selecionados para fazer a integração chamando a função verificar_lista_nula
        if verificar_lista_nula (obj_arquivos_selec):
            # Exibe uma mensagem de aviso informando que não á dados para realizar a integração
            messagebox.showwarning (title = 'Aviso', message = 'Não há dados para realizar a integração')
        else:
            # Abre a janela onde poderá ser realizada a integração
            janela = ttk.Toplevel()          # Cria e exibe a janela na tela
            janela.geometry ('300x400')     # Define o tamanho inicial da janela
            janela.title ('Integração')     # Define o título da janela

            # Se houver apenas um arquivo selecionado pelo usuário, cria na janela os widgets para o tratamento deste conjunto
            # de dados único
            if verificar_tamanho_lista (obj_arquivos_selec) [0] == 1:
                # Chama a função que exibe os widgets de seleção de intervalo de integração na tela
                widgets_integracao (janela,
                                    verificar_tamanho_lista (obj_arquivos_selec) [1] [0]    # Retorna o índice do primeiro 
                                                                                            # elemento não nulo
                                    )

            # Caso haja mais de um arquivo selecionado pelo usuário, pede primeiro para o usuário escolher em qual
            # conjunto de dados ele quer realizar a operação
            else:
                label_selec_arquivo = ttk.Label (janela, text = 'Selecione o conjunto de dados', font = ('Rodonto', 11))
                label_selec_arquivo.pack(pady = 3)

                # Exibe na tela os botões de seleção do arquivo a ser realizada a operação
                for i in obj_arquivos_selec:
                    if i != None:
                        # Cria os botões de seleção de arquivo para se realizar a operação
                        BotaoSelecao (janela,
                                      nome = i.nome_arquivo,
                                      id = i.id
                                      ).pack(pady = 3)

    # Método que abre a janela onde pode ser feita a derivação numérica
    def derivada_numerica (self):
        pass
    
    # Método que abre a janela de ajuste de curva
    def ajuste_curva (self):
        pass

# Cria a classe FramePrincipal que contém as principais funcionalidades do programma
class FramePrincipal (ttk.Frame): 
    # Define o método __init__
    def __init__ (self, master):
        # Cria e posiciona o frame na janela principal
        super().__init__ (master = master)
        self.pack()

        # Declaração dos atributos da classe
        self.titulo_grafico = tk.StringVar()      # Armazena o título do gráfico
        self.titulo_eixo_x = tk.StringVar()       # Armazena o título do eixo x
        self.titulo_eixo_y = tk.StringVar()       # Armazena o título do eixo y
        self.tipo_grafico = tk.IntVar()           # Armazena qual o tipo de gráfico foi selecionado pelo usuário
        self.mostrar_grid = tk.BooleanVar()       # Armazena o indicador caso o usuário selecionou o grid 
        self.intervalo_x1 = tk.StringVar()        # Armazena o valor inicial do intervalo a ser exibido
        self.intervalo_x2 = tk.StringVar()        # Armazena o valor final do intervalo a ser exibido

        # Cria e posiciona o espaço para a seleção de arquivo
        self.widgets_selecao_arquivo()
        # Cria e posiciona os widgets para a configuração do gráfico gerado
        self.widgets_config_grafico()

    # Método que cria e posiciona o espaço para a seleção de arquivo
    def widgets_selecao_arquivo (self):
        # Cria e posiciona a label que pede para o usuário selecionar o arquivo a ser lido
        label_selecao_arquivo = ttk.Label (self, text = 'Selecione o arquivo a ser lido', font = ('Roboto', 11))
        label_selecao_arquivo.pack()

        # Cria e posiciona o botão de seleção de arquivo
        botao_selecao_arquivo = ttk.Button (self, 
                                            text = 'Selecionar arquivo',
                                            command = self.selecionar_caminho_arquivo
                                            )
        botao_selecao_arquivo.pack(pady = 5)

    # Método que abre uma caixa de seleção de arquivo e lê o arquivo selecionado
    def selecionar_caminho_arquivo (self):
        # Abre uma caixa para o usuário selecionar um arquivo e armazena o caminho
        # desse arquivo na última posição listado na variável global caminho_arquivo
        caminho_arquivo.append (filedialog.askopenfilename())

        # Caso o usuário cancele a operação de selecionar o arquivo, nenhum erro será gerado
        # e a string vazia será deletada da última posição da variável global caminho_arquivo
        if caminho_arquivo [-1] == '': 
            del caminho_arquivo [-1]
        # Caso o usuário selecione um arquivo
        else:
            # Verifica se o arquivo selecionado pode ser lido
            if ler_dados (caminho_arquivo[-1]) != False:
            # Chama o método que lê o arquivo selecionado no momento e armazena os dados
            # coletados na última posição das listas eixo_x e eixo_y 
                tmp_x, tmp_y = ler_dados (caminho_arquivo[-1])      # Variáveis temporárias para armazenar os dados 
                                                                    # retornados pela função
                # Cria labels que permitem o usuário selecionar quais arquivos ele quer que o programa leia
                self.ver_arquivos_selecionados (caminho_arquivo[-1])

                eixo_x.append (tmp_x)
                eixo_y.append (tmp_y)
            # Caso o arquivo seja inválido para leitura, o programa não realiza nenhuma ação
            else:
                pass

    # Método que lê o arquivo selecionado e cria labels que permitem o usuário selecionar quais arquivos ele quer ler
    def ver_arquivos_selecionados (self, nome_arquivo):

        # Chama a função que retorna o nome do arquivo selecionado pelo usuário
        # O nome do arquivo será exibido na label do frame de leitura
        nome_arquivo = vizualizar_nome_arquivo_selecionado (nome_arquivo)

        # Armazena o frame de leitura na lista de objetos
        obj_arquivos_selec.append (FrameDeLeitura (self, nome_arquivo))

        # Chama a função que incrementa a variável global de identificação de frmes de leitura
        # para que o próximo a ser criado tenha um identificador sucessor a este
        adicionar()

    # Método que cria os widgets referentes à configuração geral do gráfico
    def widgets_config_grafico (self):
        # Cria e posiciona a label que pede para o usuário inserir o título do gráfico
        label_titulo_grafico = ttk.Label (self, text = 'Título do gráfico', font = ('Roboto', 11))
        label_titulo_grafico.pack(pady = 3)

        # Cria e posiciona a entrada de título
        entry_titulo_grafico = ttk.Entry (self,
                                          textvariable = self.titulo_grafico    # Variável de controle
                                          )
        entry_titulo_grafico.pack(pady = 3)

        # Cria e posiciona a label que pede para o usuário inserir o título do eixo x
        label_titulo_eixo_x = ttk.Label (self, text = 'Título do eixo horizontal', font = ('Roboto', 11))
        label_titulo_eixo_x.pack(pady = 3)

        # Cria e posiciona a entrada de título do eixo x
        entry_titulo_eixo_x = ttk.Entry (self,
                                         textvariable = self.titulo_eixo_x
                                         )
        entry_titulo_eixo_x.pack(pady = 3)

        # Cria e posiciona a label que pede para o usuário inserir o título do eixo y
        label_titulo_eixo_y = ttk.Label (self, text = 'Título do eixo vertical', font = ('Roboto', 11))
        label_titulo_eixo_y.pack(pady = 3)

        # Cria e posiciona a entrada de título do eixo y
        entry_titulo_eixo_y = ttk.Entry (self,
                                         textvariable = self.titulo_eixo_y
                                         )
        entry_titulo_eixo_y.pack(pady = 3)

        # Cria e pocisiona o frame que permite a seleção de um intervalo de leitura de dados pelo usuário
        label_selecao_intervalo_x = ttk.Label (self, text = 'Intervalo de visualização dos dados', font = ('Roboto', 11))
        label_selecao_intervalo_x.pack(pady = 3)

        frame_x1 = ttk.Frame (self)
        frame_x1.pack()

        label_x1 = ttk.Label (frame_x1, text = 'Inicial:', font = ('Roboto', 11))
        label_x1.pack (side = 'left', pady = 3)

        entry_intervalo_x1 = ttk.Entry (frame_x1,
                                       textvariable = self.intervalo_x1
                                       )
        entry_intervalo_x1.pack (side = 'right', pady = 3)

        frame_x2 = ttk.Frame (self)
        frame_x2.pack()

        label_x2 = ttk.Label (frame_x2, text = 'Final:', font = ('Roboto', 11))
        label_x2.pack (side = 'left', pady = 3)

        entry_intervalo_x2 = ttk.Entry (frame_x2,
                                       textvariable = self.intervalo_x2
                                       )
        entry_intervalo_x2.pack (side = 'right', pady = 3)

        # Cria e posiciona a label que pede para o usuário escolher o tipo de gráfico (linhas o dispersão)
        label_tipo_grafico = ttk.Label (self, text = 'Tipo de gráfico', font = ('Roboto', 11))
        label_tipo_grafico.pack(pady = 3)

        # Cria e posiciona os radio buttons que selecionam se o gráfico gerado será de dispersão ou de linha
        radio_tipo_dispersao = ttk.Radiobutton (self, 
                                                text = 'Gráfico de dispersão',
                                                value = 0,
                                                variable = self.tipo_grafico
                                                )
        radio_tipo_dispersao.pack(pady = 3)

        radio_tipo_linha = ttk.Radiobutton (self, 
                                            text = 'Gráfico de linha', 
                                            value = 1,
                                            variable = self.tipo_grafico
                                            )
        radio_tipo_linha.pack(pady = 3)

        # Cria e posiciona 0 check button de inserir grid ao gráfico
        check_grid_grafico = ttk.Checkbutton (self, 
                                              text = 'Adicionar linhas de grade',
                                              variable = self.mostrar_grid,
                                              )
        check_grid_grafico.pack(pady = 3)

        # Cria e posiciona o botão que irá gerar o gráfico de acordo com as configurações feitas pelo usuário
        botao_gerar_grafico = ttk.Button (self, 
                                          text = 'Gerar gráfico',
                                          command = self.tratar_dados   # Chama o método que trata os dados antes de gerar o gráfico
                                          )
        botao_gerar_grafico.pack(pady = 3)

    # Método que garante que apenas os arquivos selecionados pelo usuário sejam plotados no gráfico gerado
    def tratar_dados (self):
        # Cria variáveis temporárias que serão passadas como argumentos para a função plot_grafico
        tmp_x = []                  # Armazena os dados do eixo x válidos
        tmp_y = []                  # Armazena os dados do eixo y válidos
        tmp_cores = []              # Armazena as cores escolhidas para cada série de dados
        tmp_legenda_serie = []      # Armazena a legenda de cada série de dados
        tmp_intervalo_x1 = None     # Valor inicial do intervalo
        tmp_intervalo_x2 = None     # Valor final do intervalo

        # Caso não haja dados selecionados, exibe uma mensagem de aviso ao usuário
        if verificar_lista_nula (obj_arquivos_selec) == True:
            messagebox.showwarning (title = 'Aviso', message = 'Não há dados para gerar o gráfico')
            return
        
        # Filtra o conjunto de dados para aqueles que não são nulos e armazena nas variáveis temporárias
        for i in eixo_x:
            if i != None:
                tmp_x.append (i)
        for i in eixo_y:
            if i != None:
                tmp_y.append (i)
        # Percorre todos os frames de leitura
        for i in obj_arquivos_selec:
            if i != None:
                tmp_cores.append (i.cor.get())                      # Armazena a cor de cada série
                tmp_legenda_serie.append (i.legenda_serie.get())    # Armazena a legenda da série

        # Verifica se o usuário selecionou algum intervalo de exibição do gráfico
        # Verifica se a entrada do usuário é válida
        try:
            # Condicionais que verificam se as entradas de seleção de entervalo estão preenchidas
            if self.intervalo_x1.get() != '':
                tmp_intervalo_x1 = float (self.intervalo_x1.get())

            if self.intervalo_x2.get() != '':
                tmp_intervalo_x2 = float (self.intervalo_x2.get())
        # Caso a entrada do usuário seja inválida, exibe uma mensagem de erro
        except:
            # Exibe uma mensagem de erro na tela
            messagebox.showerror (message = 'O intervalo inserido não é válido',
                                  title = 'Erro')
            return

        # Chama a função que plota gráfico com as características definidas pelo usuário
        plot_grafico (tmp_x, 
                        tmp_y, 
                        tmp_cores,
                        tmp_legenda_serie,
                        self.titulo_grafico.get(),
                        self.titulo_eixo_x.get(),
                        self.titulo_eixo_y.get(),
                        self.tipo_grafico.get(),
                        self.mostrar_grid.get(),
                        tmp_intervalo_x1,
                        tmp_intervalo_x2
                        )
 
# Frame de leitura correspondente que características do arquivo que foi lido pelo programa
class FrameDeLeitura (ttk.Frame):
    # Cria e posiciona o frame na janela principal
    def __init__ (self, master, nome_arquivo):
        super().__init__ (master = master, relief='groove', borderwidth=15)
        self.pack(pady = 5)

        # Declara os atributos da classe
        self.nome_arquivo = nome_arquivo            # Dá um nome para o objeto de acordo com o nome do arquivo
        self.id = identificador                     # Identifica o frame de leitura com base em um número inteiro
        self.cor = tk.StringVar (value = cores[0])  # Armazena a cor selecionada dentro do frame de leitura
        self.legenda_serie = tk.StringVar()         # Armazena a legenda da série de dados dentro do frame de leitura

        # Cria e posiciona uma label contém o nome do arquivo lido pelo programa
        label_nome_arquivo = ttk.Label (self, text = nome_arquivo, font = ('Roboto', 11))
        label_nome_arquivo.pack(pady = 3)

        # Cria e posiciona label que pede para o usuário informar a legenda da série
        label_legenda_serie = tk.Label (self, text = 'Legenda da série', font = ('Roboto', 11))
        label_legenda_serie.pack(pady = 3)

        # Cria e posiciona a entrada de legenda da série
        entry_legenda_serie = ttk.Entry (self, textvariable = self.legenda_serie)
        entry_legenda_serie.pack(pady = 3)

        # Cria e posiciona label que pede para o usuário escolher uma cor para a série
        label_selecionar_cor = ttk.Label (self, text = 'Cor da série', font = ('Roboto', 11))
        label_selecionar_cor.pack(pady = 3)

        # Cria e posiciona a combobox de seleção de cores
        selecao_cores = ttk.Combobox (self, values = cores, textvariable = self.cor, state = 'readonly')
        selecao_cores.pack(pady = 3)

        # Cria e pociion o botão que cancela a leitura do rquivo e desfaz o frma de leitura
        botao_deletar_frame = ttk.Button (self,
                                          text = 'Cancelar',
                                          command = self.deletar    # Chama o método responvável por cancelar a leitura do arquivo
                                                                    # e desfazer o frame de leitura
                                          )
        botao_deletar_frame.pack(pady = 5)

    # Método que cancela a leitura do rquivo pelo programa e desfaz o frame de leitura
    def deletar (self):
        # Retira o frame de leitura da janela principal
        self.pack_forget()
        # Coloca o valor nulo na posição referente ao identificador do frame de leitura nas variáveis globais
        caminho_arquivo [self.id] = None
        eixo_x [self.id] = None
        eixo_y [self.id] = None
        obj_arquivos_selec [self.id] = None

#-----------------------------------------------------------------------------------------------------------------------------------
# Chama a classe principal para executar o programa
App() 