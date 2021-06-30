import pandas as pd
import numpy as np

## Função para criar tabela com dados dos livros coletados
def criar_tabela_livros(df):
    
    df_total = df.copy()
    # df_total = df_books.copy()
    df_livros = pd.DataFrame()
    
    # Informacoes dos Livros
    df_livros['Google_ID'] = df_total['id']
    df_livros['Titulo'] = df_total['volumeInfo.title'].str.title()
    df_livros['Sub_Titulo'] = df_total['volumeInfo.subtitle'].str.title()
    
    for i, row in df_livros.iterrows():
        if (type(row['Sub_Titulo']) == float):
           continue
        else:
            df_livros['Titulo'][i] = row.Titulo + ': ' + row.Sub_Titulo
    df_livros.drop(columns=['Sub_Titulo'], inplace=True)
    
    
    for i, row in df_total.iterrows():
        if (type(row['volumeInfo.industryIdentifiers']) == float):
           continue
        else:
            #x=df_total.loc[i,'volumeInfo.industryIdentifiers']
            isbn = str(row['volumeInfo.industryIdentifiers']).split()
            isbn = isbn[-1].strip("'}]'")
            df_livros.loc[i,'ISBN_13'] = isbn
 
 
    df_livros['Autores'] = df_total['volumeInfo.authors'].astype(str).str.strip("[]")
    df_livros['Autores'] = df_livros['Autores'].str.replace("'","")
    df_livros['Autores'] = df_livros['Autores'].str.title()
    
    df_livros['Editora'] = df_total['volumeInfo.publisher']
    
    df_livros['Data_Publicacao'] = df_total['volumeInfo.publishedDate']
    df_livros['Data_Publicacao'] = pd.to_datetime(df_livros['Data_Publicacao'])
    df_livros['Ano_Publicacao'] = df_livros['Data_Publicacao'].dt.year.astype('Int64')
    
    idiomas = {'pt-BR':'Português', 'en':'Inglês', 'ar':'Espanhol', 'de':'Alemão', 'pt':'Português', 'pt-PT':'Português Portugal'}
    for i, row in df_total.iterrows():
        for key, value in idiomas.items():
            if (row['volumeInfo.language'] == key):
                df_livros.loc[i,'Idioma'] = value
            else:
                continue
    
    df_livros['Paginas'] = df_total['volumeInfo.pageCount'].astype('Int64')

    df_livros['Categoria'] = df_total['volumeInfo.categories']
    df_livros['Categoria'] = df_total['volumeInfo.categories'].astype(str).str.strip("[]")
    df_livros['Categoria'] = df_livros['Categoria'].str.replace("'","")
    df_livros['Categoria'] = df_livros['Categoria'].str.replace(" / ", ", ")

    df_livros['Thumbnail'] = df_total['volumeInfo.imageLinks.smallThumbnail']
        
    # Informacoes de Venda dos Livros
    df_livros['Disponivel_Venda'] = df_total['saleInfo.saleability']
    df_livros.loc[df_livros.Disponivel_Venda == 'FOR_SALE', 'Disponivel_Venda'] = True
    df_livros.loc[df_livros.Disponivel_Venda == 'NOT_FOR_SALE', 'Disponivel_Venda'] = False
    
    df_livros['Preco_R$'] = df_total['saleInfo.listPrice.amount'].astype(float)
    df_livros['Link_Compra'] = df_total['saleInfo.buyLink']
    
    df_livros['Link_Google_Books'] = df_total['volumeInfo.canonicalVolumeLink']
    
    df_livros['Epub_Disponivel'] = df_total['accessInfo.epub.isAvailable']
    df_livros['Epub_Link'] = df_total['accessInfo.epub.acsTokenLink']
    
    df_livros['PDF_Disponivel'] = df_total['accessInfo.pdf.isAvailable']
    df_livros['PDF_Link'] = df_total['accessInfo.pdf.acsTokenLink']
    df_livros['PDF_WEB_Reader'] = df_total['accessInfo.webReaderLink']    
    
    return(df_livros)
