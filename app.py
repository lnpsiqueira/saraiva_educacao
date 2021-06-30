import pandas as pd
import streamlit as st

## Carrega o dataset dos livros da Saraiva Educação
df_saraiva_edu = pd.read_csv('./data/livros_saraiva_edu.csv', sep=';')

df_saraiva_edu['Ano_Publicacao'] = df_saraiva_edu['Ano_Publicacao'].astype('Int64')
df_saraiva_edu['Categoria'].fillna('Não Informado', inplace=True)

## Filtra as opções para escolha
categorias = df_saraiva_edu['Categoria'].unique()
idiomas = df_saraiva_edu['Idioma'].unique()
ano_publlicacoes = df_saraiva_edu['Ano_Publicacao'].unique()

## Cria opções para o usuário escolher
st.sidebar.markdown('Escolha as opções para sua pesquisa:')
idioma = st.sidebar.selectbox('Escolha o Idioma do Livro:', idiomas,1)
categoria = st.sidebar.selectbox('Escolha a Categoria:', categorias,0)
ano = st.sidebar.selectbox('Escolha o Ano de Publicação:', ano_publlicacoes,0)

## Realiza tratativas para apresentar dataset
df_saraiva_pesquisa = df_saraiva_edu.loc[df_saraiva_edu['Idioma']==idioma]
df_saraiva_pesquisa = df_saraiva_pesquisa.loc[df_saraiva_pesquisa['Categoria']==categoria]
df_saraiva_pesquisa = df_saraiva_pesquisa.loc[df_saraiva_pesquisa['Ano_Publicacao']==ano]
df_saraiva_pesquisa.reset_index(drop = True, inplace = True)
df_saraiva_pesquisa['Preco_R$'].fillna(0)
df_saraiva_pesquisa['Paginas'].fillna(0)
size = len(df_saraiva_pesquisa)

#st.dataframe(df_saraiva_pesquisa.style.set_precision(2))

markdown_list = []
image_list = []

if size > 0:
    
    st.title(f'Foram encontrados um total de {size} livros:')
    max_livros = st.slider('Escolha a Quantidade de Livros para Mostrar', 1, size, value = 4, step=1)
    
    for index, row in df_saraiva_pesquisa.iloc[0:max_livros, :].iterrows():
        livro = row['Titulo']
        autor = row['Autores']
        paginas = row['Paginas']
        editora = row['Editora']
        ano = row['Ano_Publicacao']
        preco = round(float(row['Preco_R$']),2)
        google_id = row['Google_ID']
        figura = row['Thumbnail']    
        isbn_13 = int(row['ISBN_13'])
        disponivel = int(row['Disponivel_Venda'])
        url_compra = row['Link_Compra']
    
        column1, column2 = st.beta_columns((1, 4))
    
        with column1:  # coluna para figuras dos livros
            # try:
            st.text("")
            st.image(f'{figura}', use_column_width=True)
            image_list.append(f'{figura}')
            markdown_list.append(
                f"""
                <br>
                <div>
                    <img
                        src="cid:image{len(image_list)}"
                        alt="Logo"
                        style="width:200px;height:200px;">
                </div>
                """
            )
    
            # except FileNotFoundError:
            #     st.text("")
            #     st.image('fig/placeholder-image.jpg', use_column_width=False)
            #     image_list.append('fig/placeholder-image.jpg')
            #     markdown_list.append(
            #         f"""
            #         <br>
            #         <div>
            #             <img
            #                 src="cid:image{len(image_list)}"
            #                 alt="Logo"
            #                 style="width:200px;height:200px;">
            #         </div>
            #         """
            #     )
    
        with column2:  # Caracteristicas dos livros
    
                preco_ = f'R$ {float(preco)}0' if disponivel == 1 else 'Indisponvel'
                # discount_phrase = f'(Cupom de desconto: {discount_coupon})' if discount_coupon else ''
                paginas_ = f'{int(paginas)}' if paginas > 1 else 'Indisponvel'
                compra = f'<b><a href="{url_compra}" target="_blank">Comprar!</a></b>' if disponivel == 1 else f'<br>Indisponível!</br>'
                livro_markdown = f"""
                <div>
                    <h3>{livro}</h3>
                    <h4>{autor}</h3>
                    <p> 
                        Páginas: {(paginas_)}<br>
                        Preço: {preco_}<br>
                        <b>Editora</b>: {editora}<br>
                        <b>Ano Publicação</b>: {int(ano)}<br>
                        <b>ISBN13</b>: {isbn_13} <br>
                        <b>Google ID</b>: {google_id}<br>
                        {compra}
                    </p>
                </div>
                """
                st.markdown(livro_markdown, unsafe_allow_html=True)
                markdown_list.append(livro_markdown)

else:
    st.title('Sua pesquisa não encontrou nenhum livro, tente novamente!')
    

