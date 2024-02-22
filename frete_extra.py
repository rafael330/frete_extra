import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página do Streamlit
st.set_page_config(layout='wide')
st.header('SOLICITAÇÕES DE FRETE EXTRA')

# Definição do escopo e autenticação usando gspread
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('jsonkey_raf.json', scopes=scope)
client = gspread.authorize(credentials)

# Abrindo a planilha e selecionando a aba específica
spreadsheet = client.open_by_key('13q7wnIdGMtT1kVjzeX3TFdanktTLvhOpmj_cd1Czy2Y')
worksheet = spreadsheet.worksheet('Respostas ao formulário 2')

# Leitura dos dados e conversão para DataFrame
dados = worksheet.get_all_records()
df = pd.DataFrame(dados)
df['PEDIDOS'] = df['PEDIDOS'].astype(str)

# Widget de seleção da transportadora
#transportadora_selecionada = st.selectbox('Escolha a transportadora:', options=df['TRANSPORTADORA SOLICITANTE'].unique())

# Widget de entrada para números de pedidos
pedido_input = st.text_input('Digite os números dos pedidos separados por vírgula:', '')

# Processamento da entrada de pedidos para criar uma lista
lista_pedidos = [pedido.strip() for pedido in pedido_input]#.split(',') if pedido.strip()]

# Filtragem do DataFrame com base nos filtros selecionados
if lista_pedidos:
    df_filtrado = df[df['PEDIDOS'].isin(lista_pedidos)]# & (df['PEDIDOS'].isin(lista_pedidos))]
else:
    df_filtrado = df[df['PEDIDOS'] == '-']

# Selecionando apenas as colunas desejadas para exibição
df_exibicao = df_filtrado[['ID','TRANSPORTADORA SOLICITANTE', 'PEDIDOS', 'Rota', 'VALOR APROVADO']]

# Adicionando estilo CSS para definir as dimensões da tabela
st.markdown(f"""
<style>
    .dataframe {{
        width: 1200px !important;
        height: 300px !important;
        overflow: auto;
    }}
</style>
""", unsafe_allow_html=True)

# Convertendo o DataFrame filtrado para HTML e escondendo o índice
html = df_exibicao.to_html(index=False)
st.markdown(html, unsafe_allow_html=True)
