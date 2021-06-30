import pandas as pd

from functions import carregar_livros_google as clg
from functions import criar_tabela_livros as livros_saraiva

## funcao para carregar livros conforme editora (esta definida como saraiva educacao)
df_lista = clg.carregar_livros_google_editora('Saraiva Educação')
df_lista.to_csv('./data/lista_saraiva.csv', sep=';', index=False)

## funcao para tratar carregar dados individuais dos livros
## utiliza o id do google para carregar os dados
df_livros = clg.gerar_lista_completa_saraiva(df_lista)
df_livros.to_csv('./data/livros_saraiva_completo.csv', sep=';', index=False)

## função para criar um dataframe com todas editoras que tenham Saraiva
df_livros_saraiva = livros_saraiva.criar_tabela_livros(df_livros)

## criar .csv com os dados completos
df_livros_saraiva.to_csv('./data/livros_saraiva.csv', sep=';', index=False)

## filtra livros que sejam da Editora Saraiva Educação
df_livros_saraiva_edu = df_livros_saraiva.loc[df_livros_saraiva.Editora == 'Saraiva Educação S.A.']

## criar .csv com os livros da Saraiva Educação
df_livros_saraiva_edu.to_csv('./data/livros_saraiva_edu.csv', sep=';', index=False)
df_livros_saraiva_edu = pd.read_csv('./data/livros_saraiva_edu.csv', sep=';')



