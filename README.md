
# Data Plot - Leitura de arquivos e construção de gráficos

Data Plot é um programa escrito em python para a construção de gráficos a partir da leitura de arquivos que contém duas colunas de dados, uma referente ao eixo x e outra referente ao eixo y.

  

![Description](Imagens%5Cimage1.png)

  

## Seleção de arquivos

  

Ao clicar no botão “Selecionar arquivo”, uma janela de diálogo será aberta de forma que o usuário pode escolher o arquivo a ser lido pelo programa. São reconhecidos os seguintes formatos de arquivo:

  

- .txt

- .csv

- .dpt

  

Caso o arquivo selecionado não possa ser lido pelo programa, uma mensagem de erro será exibida:

![Erro na leitura do arquivo](Imagens%5Cimage3.png)

  

Para que os dados sejam lidos, é necessário que o arquivo possua apenas números (caso haja letras ou outros símbolos um erro será gerado) e que eles se iniciem na primeira linha. Alguns exemplos de arquivos compatíveis e incompatíveis são mostrados abaixo.

  

*Arquivo incompatível pois não há apenas números*

![enter image description here](Imagens%5Cimage2.png)

  

*Arquivo incompatível pois os dados se iniciam na segunda linha e não na primeira*

![enter image description here](Imagens%5Cimage5.png)

  

*Arquivo compatível pois há apenas números e eles se iniciam na primeira linha*

![enter image description here](Imagens%5Cimage4.png)

  

## **Configuração do gráfico**

Ao selecionar um arquivo válido para leitura, uma caixa de configuração irá aparecer na parte inferior da janela como mostra a figura.

  

![enter image description here](Imagens%5Cimage7.png)

  

Na parte superior da janela é mostrado o nome do arquivo selecionado (neste caso, “teste_1.txt”). No campo **Legenda da série** pode ser escrito a legenda que a série terá no gráfico, enquanto no campo **Cor da série** pode ser definida a cor que a série terá no gráfico. Vários arquivos podem ser lidos ao mesmo tempo e, ao gerar o gráfico, todas as séries aparecerão na mesma figura, cada uma com sua respectiva legenda e cor definidas pelo usuário.

  

![enter image description here](Imagens%5Cimage6.png)

  

As seguintes características gerais do gráfico podem ser configuradas pelo usuário:

  

- Título principal: o título que aparece no topo do gráfico.

- Título dos eixos horizontal e vertical: título que aparece nos eixos do gráfico.

- Intervalo de visualização dos dados: intervalo no qual os dados serão visualizados.

- Tipo de gráfico: pode ser escolhido entre dispersão e linha.

- Linhas de grade: pode-se adicionar ou não linhas de grade ao gráfico.

  

![enter image description here](Imagens%5Cimage9.png)

  

Ao clicar no botão Gerar gráfico, o gráfico com as características escolhidas será exibido na tela.

![enter image description here](Imagens%5Cgrafico1.png)

![enter image description here](Imagens%5Cgrafico2.png)

![enter image description here](Imagens%5Cgrafico3.png)