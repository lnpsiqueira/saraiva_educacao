import pandas as pd
import requests
import time
from unidecode import unidecode
import urllib

## Função para carregar lista completa por editora, neste exemplo esta apenas para
## livros da Saraiva Educação

def carregar_livros_google_editora(editora):

    df_lista = pd.DataFrame()
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=inpublisher:'
    editora = unidecode((urllib.parse.quote(editora, safe='')))
    pesquisa = '&maxResults=20&orderBy=newest&startIndex='
    start_index = 0
    url = base_url + editora + pesquisa + str(start_index)
    response = requests.get(url)
    data = response.json()
    df_lista= pd.json_normalize(data,'items')
    
    for index in range(20,479,20):
        url = base_url + editora + pesquisa + str(index)
        response = requests.get(url)
        data = response.json()

        df = pd.json_normalize(data,'items')
        df_lista = df_lista.append(df, ignore_index=True, sort=False)

    return(df_lista)

## Refina para entrar nas informações individuais de cada livro, garantindo assim que
## irá carregar todas as informações disponíveis de cada livro.
def gerar_lista_completa_saraiva(df):
    books_id = df['id']
    
    df_books = pd.DataFrame()
    for i in range(len(books_id)):
        base_url = 'https://www.googleapis.com/books/v1/volumes/'
        book_id = books_id[i]
        url = base_url + book_id
        response = requests.get(url)
        data = response.json()
        df = pd.json_normalize(data)
        df_books = df_books.append(df, ignore_index=True, sort=False)
        print('Livro {} de {} carregado.'.format(i+1,len(books_id)+1))
        time.sleep(1)
    return(df_books)
