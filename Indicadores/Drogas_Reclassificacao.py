import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import unidecode

#Lendo dados
drogas_final = pd.read_csv('Dados/GESEG_SBX_DROGA_EXPORT.csv', encoding = 'latin-1', sep = ';', index_col=0)

#Pivotando valor "QUANTIDADE" da coluna "ATRIBUTOS" com o mesmo "NRO_INT_OBJETO"
drogas_final_pivot = drogas_final.pivot(index="NRO_INT_OBJETO", columns="ATRIBUTO", values="QUANTIDADE")

#Agrupando dados com o mesmo "K93_NRO_INT_OBJETO"
#Foi preciso utilizar "agg('min')" pois apenas groupby()...
#retorna um objeto iterável 
dg2_final = drogas_final[['NRO_INT_OBJETO','ANO_OCOR', 'NRO_OCOR','NRO_INT_TIPO_OBJETO','TIPO_OBJETO','ATRIBUTO']].groupby(["NRO_INT_OBJETO"]).min()

#Ordenando por "NRO_INT_OBJETO"
dg2_final_sorted = dg2_final.sort_values(by=['NRO_INT_OBJETO'])
drogas_pivot_final_sorted = drogas_final_pivot.sort_values(by=['NRO_INT_OBJETO'])

#Concatenando as duas tabelas
try_1_final = pd.concat([dg2_final_sorted, drogas_pivot_final_sorted],axis=1)

#Atribuindo a tabela resultado "try_1" com um index numérico
resultado = try_1_final.reset_index()

#Renomeando Coluans
resultado = resultado.rename(columns={"NRO_INT_OBJETO": "CHAVE_OBJETO", "TIPO_OBJETO": "TXT_TIPO_OBJETO"})

#Mudando o float do padrão brasileiro para o americano
resultado['Peso Unitário'] = pd.to_numeric(resultado['Peso Unitário'], errors='coerce')
resultado['Peso Total'] = pd.to_numeric(resultado['Peso Total'], errors='coerce')

#Trocando dados NaN por 0
resultado['Peso Unitário'] = resultado['Peso Unitário'].fillna(0)
resultado['Peso Total'] = resultado['Peso Total'].fillna(0)

#Trocando o tipo de dado para float
resultado['Peso Total']  = resultado['Peso Total'].astype(float)
resultado['Peso Unitário']  = resultado['Peso Unitário'].astype(float)




#Criando um DataFrame da quantidade de cores em "Cir Predominante"
cores = resultado['Cor Predominante'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
#Inverteu indices por colunas
cores = cores.T
#Definindo nome das colunas
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0],4:cores[4][0]
                             ,5:cores[5][0],6:cores[6][0],7:cores[7][0],8:cores[8][0],9:cores[9][0]
                             ,10:cores[10][0], 11:cores[11][0],12:cores[12][0]})
#Excluiu a linha index que repetia o nome das colunas
cores = cores.iloc[1:]

#Criando outro DataFrame de cores mas ao invés da quantidade, com as frequências de ocorrencia por cor
cores1 = resultado['Cor Predominante'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0],4:cores1[4][0]
                             ,5:cores1[5][0],6:cores1[6][0],7:cores1[7][0],8:cores1[8][0],9:cores1[9][0]
                             ,10:cores1[10][0], 11:cores1[11][0],12:cores1[12][0]})

#Criando uma lista com ambos DataFrames
lista = [cores,cores1]
#Concatenando os DataFrames
cores2 = pd.concat(lista)
#Criando um novo index numérico
cores2 = cores2.reset_index(drop=True)
#Removendo a linha repetida com o nome das cores
cores2 = cores2.drop([1], axis = 0)

#Mudando o nome dos index
#(Giuliano) mudei de % para frequência
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequencia"})
cores2

#Mudanças:
#Linhas comentadas e setx irrelevantes excluídas
#Criando um novo DataFrame a partir de "resultado"
stores_df = resultado

#Criando um plot e outros subplots
f, (ax1) = plt.subplots(1, 1, figsize=(12, 6))
sns.countplot(x="Cor Predominante", data=stores_df, ax=ax1)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=70)
ax1.set_ylabel("Quantidade",fontsize=20)
plt.tight_layout()
plt.grid(axis='x')
plt.title('Cor Predominante')

#Criando DataFrame cores a partir da quantidade de "Tipo de Embalagem"
cores = resultado['Tipo de Embalagem'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
cores = cores.T
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0],4:cores[4][0]
                             ,5:cores[5][0],6:cores[6][0],7:cores[7][0],8:cores[8][0],9:cores[9][0]
                             ,10:cores[10][0], 11:cores[11][0],12:cores[12][0]})
cores = cores.iloc[1:]

#Criando outro DataFrame de cores mas ao invés da quantidade, com as frequências de Tipos de embalagem
cores1 = resultado['Tipo de Embalagem'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0],4:cores1[4][0]
                             ,5:cores1[5][0],6:cores1[6][0],7:cores1[7][0],8:cores1[8][0],9:cores1[9][0]
                             ,10:cores1[10][0], 11:cores1[11][0],12:cores1[12][0]})

#Concatenando o DF com os dois iniciais
lista = [cores,cores1]
cores2 = pd.concat(lista)
cores2 = cores2.reset_index(drop=True)
cores2 = cores2.drop([1], axis = 0)
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequencia"})
#PROBLEMA
cores2 = cores2.rename(columns={13:'Maço(s)', 14:'Kit(s)'})
#Lote == maço?
cores2

#Plotando os gráficos
#Mudanças: Linhas palettes irrelevantes para o código excluídas
#          ax2.set(xlabel)irrelevante

stores_df = resultado

f, (ax2) = plt.subplots(1, 1, figsize=(12, 6))
sns.countplot(x="Tipo de Embalagem", data=stores_df, ax=ax2)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=70)
ax2.set_ylabel("Quantidade",fontsize=20)
plt.tight_layout()
plt.grid(axis='x')
plt.title('Embalagem')

#Criando DataFrame a partir de "Unidade de Peso"
cores = resultado['Unidade de Peso'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
cores = cores.T
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0],4:cores[4][0],5:cores[5][0]})
cores = cores.iloc[1:]

#Criando outro DataFrame para as frequências de "Unidade de Peso"
cores1 = resultado['Unidade de Peso'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0],4:cores1[4][0],5:cores1[5][0]
                             })
#Concatenando tabelas
lista = [cores,cores1]
cores2 = pd.concat(lista)
cores2 = cores2.reset_index(drop=True)
cores2 = cores2.drop([1], axis = 0)
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequência"})
cores2

#Mudanças: Linhas palettes irrelevantes para o código excluídas
#          ax2.set(xlabel)irrelevante
stores_df = resultado

f, (ax2) = plt.subplots(1, 1, figsize=(12, 6))
palette ={"Verde": "green", "Marrom": "brown", "Branco": "white", "Amarelo": "yellow","Cinza":'grey',"Dourado":'gold',"Laranja":"orange","Azul":"Blue","Vermelho":"Red",'Bege':'beige',"Preto":"black", "Incolor":"blue", "Rosa":"pink"}

sns.countplot(x="Unidade de Peso", data=stores_df, ax=ax2)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=70)
ax2.set_ylabel("Quantidade",fontsize=20)
plt.grid(axis='x')
plt.tight_layout()
plt.title('Unidade de Peso')

sem_info = resultado.loc[resultado['Unidade de Peso'] == 'Não soube informar']
sem_info

#Criando um DataFrame com "Unidade de Peso" == "Não soube informar"
sem_info = resultado.loc[resultado['Unidade de Peso'] == 'Não soube informar']
sem_info = sem_info.reset_index(drop=True)

#Criando um DataFrame com "Unidade de Peso" diferente de "Não soube informar"
com_info = resultado.loc[resultado['Unidade de Peso'] != 'Não soube informar']
com_info = com_info.reset_index(drop= True)

#Criando um DataFrame porcao com "Tipo de Embalagem" sendo "Porção(es)" 
#"Unidade de Peso" sendo "Grama"
#"Peso Unitário" não nulo
porcao = com_info.loc[com_info['Tipo de Embalagem'] == 'Porção(es)']
porcao = porcao.loc[porcao['Unidade de Peso'] == 'Grama']
porcao = porcao.loc[porcao['Peso Unitário'].notna()]
porcao = porcao.reset_index(drop=True)

#Substituindo "-" por 0
x = 0
#Enquanto x < 10495
while x < len(porcao):
    if porcao['Peso Unitário'][x] == '-':
        porcao['Peso Unitário'][x] = 0
    x += 1

#Mudando o tipo de dado da Coluna "Peso Unitário" do DataFrame porcao, para o tipo float
porcao['Peso Unitário'] = porcao['Peso Unitário'].astype(float)

#Mostrando Média, mediana e quartil
print('Média')
print(porcao['Peso Unitário'].mean())
print('Mediana')
print(porcao['Peso Unitário'].median())
print('Quartil')
print(porcao['Peso Unitário'].quantile(0.25))

#Criando o Data_Frame porcao_sem
#Partindo do DataFrame sem_info
#Apenas quando "Tipo de Embalagem" for "Porção(es)"
porcao_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Porção(es)']
#Aletrando "Unidade de Peso" de:
#Não soube informar -> Grama
porcao_sem['Unidade de Peso'] = 'Grama'
#Tornando a coluna "Peso Unitário" como a sua mediana
porcao_sem['Peso Unitário'] = porcao['Peso Unitário'].median()

#Criando o DF cigarro_com
#A partir do DF com_info
cigarro_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Cigarro(s)']
cigarro_com = cigarro_com.loc[cigarro_com['Unidade de Peso'] == 'Grama']
cigarro_com = cigarro_com.loc[cigarro_com['Peso Unitário'].notna()]
cigarro_com = cigarro_com.reset_index(drop=True)
cigarro_com['Peso Unitário'] = cigarro_com['Peso Unitário'].astype(float)

#Printando estatisticas
print('Média')
print(cigarro_com['Peso Unitário'].mean())
print('Mediana')
print(cigarro_com['Peso Unitário'].median())
print('Quartil')
print(cigarro_com['Peso Unitário'].quantile(0.25))

#Criando o DF cigarro_sem
cigarro_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Cigarro(s)']
cigarro_sem['Unidade de Peso'] = 'Grama'
cigarro_sem['Peso Unitário'] = cigarro_com['Peso Unitário'].median()

unidade_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Unidade(s)']
unidade_com = unidade_com.loc[unidade_com['Unidade de Peso'] == 'Grama']
unidade_com = unidade_com.loc[unidade_com['Peso Unitário'].notna()]
unidade_com = unidade_com.reset_index(drop=True)
unidade_com['Peso Unitário'] = unidade_com['Peso Unitário'].astype(float) 
print('Média')
print(unidade_com['Peso Unitário'].mean())
print('Mediana')
print(unidade_com['Peso Unitário'].median())
print('Quartil')
print(unidade_com['Peso Unitário'].quantile(0.25))

unidade_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Unidade(s)']
unidade_sem['Unidade de Peso'] = 'Grama'
unidade_sem['Peso Unitário'] = unidade_com['Peso Unitário'].median()

tijolo_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Tijolo(s)']
tijolo_com = tijolo_com.loc[tijolo_com['Unidade de Peso'] == 'Grama']
tijolo_com = tijolo_com.loc[tijolo_com['Peso Unitário'].notna()]
tijolo_com = tijolo_com.reset_index(drop=True)
tijolo_com['Peso Unitário'] = tijolo_com['Peso Unitário'].astype(float) 
print('Média')
print(tijolo_com['Peso Unitário'].mean())
print('Mediana')
print(tijolo_com['Peso Unitário'].median())
print('Quartil')
print(tijolo_com['Peso Unitário'].quantile(0.25))

tijolo_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Tijolo(s)']
tijolo_sem['Unidade de Peso'] = 'Grama'
tijolo_sem['Peso Unitário'] = tijolo_com['Peso Unitário'].median()

frasco_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Frasco(s)']
frasco_com = frasco_com.loc[frasco_com['Unidade de Peso'] == 'Grama']
frasco_com = frasco_com.loc[frasco_com['Peso Unitário'].notna()]
frasco_com = frasco_com.reset_index(drop=True)
frasco_com['Peso Unitário'] = frasco_com['Peso Unitário'].astype(float) 
print('Média')
print(frasco_com['Peso Unitário'].mean())
print('Mediana')
print(frasco_com['Peso Unitário'].median())
print('Quartil')
print(frasco_com['Peso Unitário'].quantile(0.25))

frasco_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Frasco(s)']
frasco_sem['Unidade de Peso'] = 'Grama'
frasco_sem['Peso Unitário'] = frasco_com['Peso Unitário'].median()

pacote_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Pacote(s)']
pacote_com = pacote_com.loc[pacote_com['Unidade de Peso'] == 'Grama']
pacote_com = pacote_com.loc[pacote_com['Peso Unitário'].notna()]
pacote_com = pacote_com.reset_index(drop=True)
pacote_com['Peso Unitário'] = pacote_com['Peso Unitário'].astype(float) 
print('Média')
print(pacote_com['Peso Unitário'].mean())
print('Mediana')
print(pacote_com['Peso Unitário'].median())
print('Quartil')
print(pacote_com['Peso Unitário'].quantile(0.25))

pacote_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Pacote(s)']
pacote_sem['Unidade de Peso'] = 'Grama'
pacote_sem['Peso Unitário'] = pacote_com['Peso Unitário'].median()

saco_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Saco(s)']
saco_com = saco_com.loc[saco_com['Unidade de Peso'] == 'Grama']
saco_com = saco_com.loc[saco_com['Peso Unitário'].notna()]
saco_com = saco_com.reset_index(drop=True)
saco_com['Peso Unitário'] = saco_com['Peso Unitário'].astype(float) 
print('Média')
print(saco_com['Peso Unitário'].mean())
print('Mediana')
print(saco_com['Peso Unitário'].median())
print('Quartil')
print(saco_com['Peso Unitário'].quantile(0.25))

saco_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Saco(s)']
saco_sem['Unidade de Peso'] = 'Grama'
saco_sem['Peso Unitário'] = saco_com['Peso Unitário'].median()

ponto_com = com_info.loc[com_info['Tipo de Embalagem'] == 'Ponto(s)']
ponto_com = ponto_com.loc[ponto_com['Unidade de Peso'] == 'Grama']
ponto_com = ponto_com.loc[ponto_com['Peso Unitário'].notna()]
ponto_com = ponto_com.reset_index(drop=True)
ponto_com['Peso Unitário'] = ponto_com['Peso Unitário'].astype(float) 
print('Média')
print(ponto_com['Peso Unitário'].mean())
print('Mediana')
print(ponto_com['Peso Unitário'].median())
print('Quartil')
print(ponto_com['Peso Unitário'].quantile(0.25))

ponto_sem = sem_info.loc[sem_info['Tipo de Embalagem'] == 'Ponto(s)']
ponto_sem['Unidade de Peso'] = 'Grama'
ponto_sem['Peso Unitário'] = ponto_com['Peso Unitário'].median()

#Definindo um DF com todos os tipos de embalagem sem informação de "Unidade de Peso"
lista = [ponto_sem, saco_sem, tijolo_sem, unidade_sem, cigarro_sem, pacote_sem, frasco_sem, porcao_sem]
sem_info2 = pd.concat(lista)

#Definindo um DF 
lista = [sem_info2, com_info]
resultado = pd.concat(lista)
resultado = resultado.reset_index(drop=True)

resultado['Unidade de Peso'].value_counts()

#DF cores recebe quantidade de valores 
#Presentes na coluna "Unidade de peso" 
#Do DF resultado
cores = resultado['Unidade de Peso'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
cores = cores.T
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0]})
cores = cores.iloc[1:]

#Construindo DF cores1 com a frequência
cores1 = resultado['Unidade de Peso'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0]})

#Concatenando ambos os DF
lista = [cores,cores1]
cores2 = pd.concat(lista)
cores2 = cores2.reset_index(drop=True)
cores2 = cores2.drop([1], axis = 0)
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequência"})
print(cores2)

stores_df = resultado

f, (ax2) = plt.subplots(1, 1, figsize=(12, 6))
sns.countplot(x="Unidade de Peso", data=stores_df, ax=ax2)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=70)
ax2.set_ylabel("Quantidade",fontsize=20)
plt.grid(axis='x')
plt.tight_layout()
plt.title('Unidade de Peso')



#Criando DF cores a partir de frequência do tipo do Objeto
cores = resultado['TXT_TIPO_OBJETO'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
cores = cores.T
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0]})
cores = cores.iloc[1:]

#Criando DF cores1 com as frequências
cores1 = resultado['TXT_TIPO_OBJETO'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0][0]
                             })
#Concatenado DF para cores2
lista = [cores,cores1]
cores2 = pd.concat(lista)
cores2 = cores2.reset_index(drop=True)
cores2 = cores2.drop([1], axis = 0)
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequencias"})
#Atribuindo a coluna Crack também as frequências de C
#Não foi atribuido também Quantidade pois retornava um valor NaN
cores2['Crack']['Frequencias'] = cores2['C']['Frequencias']
cores2 = cores2.drop(['C'], axis = 1)
print(cores2)

#Plotando gráficos
stores_df = resultado

palette ={"Maconha": "green", "Cocaína": "white", "Crack": "yellow", "Drogas": "blue"}
f, (ax3) = plt.subplots(1, 1, figsize=(14, 5))
sns.set(font_scale=1.5)

sns.countplot(x="TXT_TIPO_OBJETO", data=stores_df, ax=ax3, palette= palette, alpha = 0.7, linewidth=2.5, edgecolor=".0")
ax3.set_facecolor('#ababab')
ax3.patch.set_alpha(0.3)
ax3.set_xlabel("Tipo de Objeto",fontsize=20)
ax3.set_ylabel("Quantidade",fontsize=20)
ax3.set_xticklabels(ax3.get_xmajorticklabels(), fontsize = 15)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=70)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=70)
plt.grid(axis='x')
plt.tight_layout()
plt.title('Tipo de Objeto')

#Definindo uma series Drogas
#Como resultado do tipo de objeto de resultado = Drogas
Drogas = resultado.loc[resultado['TXT_TIPO_OBJETO'] == 'Drogas']
#Pegando 5 linhas aleatórias da Series
Drogas.sample(5)

Drogas = resultado.loc[resultado['TXT_TIPO_OBJETO'] == 'Drogas']
Outras = resultado.loc[resultado['TXT_TIPO_OBJETO'] != 'Drogas']
Outras = Outras.reset_index(drop= True)

#DF com descrição nula
DrogasNA = Drogas.loc[Drogas['Descrição'].isnull()]
DrogasNA = DrogasNA.reset_index(drop=True)

#Excluindo descrição nula do DF Drogas
Drogas = Drogas.loc[Drogas['Descrição'].notna()]
Drogas = Drogas.reset_index(drop=True)

#Excluindo virgulas e pontos
x = 0
while x < len(Drogas):
    frase = Drogas['Descrição'][x]
    frase = frase.replace(',','')
    frase = frase.replace('.','')
    #frase = unidecode.unidecode(frase)
    Drogas['Descrição'][x] = frase
    x += 1
    
Drogas['Descrição'] = Drogas['Descrição'].str.lower()

#Tratando ajustes de drogas

def analizer(x):
    
    if 'maconha' in x:
        return 'Maconha'
    elif 'canabis' in x:
        return 'Maconha'
    elif 'cannabis' in x:
        return 'Maconha'
    elif 'crack' in x:
        return 'Crack'
    elif 'cocaina' in x:
        return 'Cocaína'
    else:
        return 'Drogas'
    
Drogas['RECLASSIFICAÇÃO'] = Drogas['Descrição'].apply(analizer)

stores_df = Drogas

palette ={"Maconha": "green", "Cocaína": "white", "Crack": "yellow", "Drogas": "blue"}
f, (ax3) = plt.subplots(1, 1, figsize=(14, 5))
sns.set(font_scale=1.5)

sns.countplot(x="RECLASSIFICAÇÃO", data=stores_df, ax=ax3, palette= palette, alpha = 0.7, linewidth=2.5, edgecolor=".0")
ax3.set_facecolor('#ababab')
ax3.patch.set_alpha(0.3)
ax3.set_xlabel("Tipo de Objeto",fontsize=20)
ax3.set_ylabel("Quantidade",fontsize=20)
ax3.set_xticklabels(ax3.get_xmajorticklabels(), fontsize = 15)

plt.setp(ax1.xaxis.get_majorticklabels(), rotation=70)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=70)
plt.grid(axis='x')
plt.tight_layout()
plt.title('Tipo de Objeto')

#DF cores com as drogas
cores = Drogas['RECLASSIFICAÇÃO'].value_counts()
cores = pd.DataFrame(cores)
cores = cores.reset_index()
cores = cores.T
cores = cores.rename(columns={0:cores[0][0],1:cores[1][0],2:cores[2][0],3:cores[3][0]})
cores = cores.iloc[1:]

#Frequência das drogas
cores1 = Drogas['RECLASSIFICAÇÃO'].value_counts(normalize=True)
cores1 = pd.DataFrame(cores1)
cores1 = cores1.reset_index()
cores1 = cores1.T
cores1 = cores1.rename(columns={0:cores1[0][0],1:cores1[1][0],2:cores1[2][0],3:cores1[3][0][0]
                             })
#Concatenando DF
lista = [cores,cores1]
cores2 = pd.concat(lista)
cores2 = cores2.reset_index(drop=True)
cores2 = cores2.drop([1], axis = 0)
cores2 = cores2.rename(index={0:'Quantidade', 2:"Frequencia"})
cores2['Drogas']['Frequencia'] = cores2['D']['Frequencia']
cores2 = cores2.drop(['D'], axis = 1)
print(cores2)