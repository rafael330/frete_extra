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

# Widget de entrada para números de pedidos
pedido_input = st.text_input('Digite os números dos pedidos separados por vírgula:', '')

# Processamento da entrada de pedidos para criar uma lista
lista_pedidos = [pedido.strip() for pedido in pedido_input.split(',') if pedido.strip()]

# Função para verificar se algum pedido informado está na célula
def pedido_esta_na_celula(celula):
    pedidos_celula = [p.strip() for p in str(celula).split(',')]
    return any(pedido in pedidos_celula for pedido in lista_pedidos)

# Inicializa df_exibicao para evitar referência antes da atribuição
df_exibicao = pd.DataFrame()

# Filtragem do DataFrame com base nos pedidos informados
if lista_pedidos:
    df_filtrado = df[df['PEDIDOS'].apply(pedido_esta_na_celula)].reset_index(drop=True)
    # Selecionando apenas as colunas desejadas para exibição
    df_exibicao = df_filtrado[['ID', 'TRANSPORTADORA SOLICITANTE', 'PEDIDOS', 'Rota', 'VALOR APROVADO']]
    # Exibindo a tabela se houver dados filtrados
    if not df_exibicao.empty:
        # Adicionando estilo CSS para definir as dimensões da tabela
        st.markdown("""
        <style>
            .dataframe {
                width: 1200px !important;
                height: 300px !important;
                overflow: auto;
            }
        </style>
        """, unsafe_allow_html=True)
        # Convertendo o DataFrame filtrado para HTML e escondendo o índice
        html = df_exibicao.to_html(index=False)
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.write("Nenhum pedido encontrado com os números informados.")
else:
    st.write("Por favor, digite os números dos pedidos para buscar.")
