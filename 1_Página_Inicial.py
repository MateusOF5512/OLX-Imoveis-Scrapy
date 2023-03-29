# BIBLIOTECAS USADAS

import streamlit as st
from PIL import Image

im = Image.open("imagens/olx_.png")
st.set_page_config(page_title="Imóveis OLX Analytics", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)


from plots.plots_olx import *
from layout.layout_olx import *

path1 = 'data/2703_venda_tratado.csv'
path2 = 'data/2703_aluguel_tratado.csv'
path3 = 'data/local.csv'
df_local = get_data_float(path3)


col2, col3, col4 = st.columns([300, 1000, 300])

with col2:
    st.image(im)
with col3:
    st.markdown("<h1 style='font-size:300%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Imóveis OLX Analytics</h1>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:180%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Anúncios de Imóveis da Grande Florianópolis</h2>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:130%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Atualização: 27/03/2023</h3>",
                unsafe_allow_html=True)

with col4:
    st.text('')
    basedados = st.radio("Base de Dados dos Imóveis:",
                    options=["Venda", "Aluguel"], index=0, horizontal=False)
st.markdown('---')


if basedados == 'Venda':
    df1 = get_data(path1)
elif basedados == 'Aluguel':
    df1 = get_data(path2)
    df1['VALOR[R$]'] = df1.apply(lambda row: row['VALOR[R$]'] / 10, axis= 1)

df =  tratamento_dados(df1)

with st.expander("⚙️ Configurar Dados"):
    col1, col2, col3 = st.columns([10, 1, 10])
    with col1:
        valor_max = int(df['VALOR[R$]'].max())
        valor_min = int(df['VALOR[R$]'].min())
        valor_min_input = st.number_input('Adicione o Valor [R$] Mínimo:',
                                          min_value=valor_min, max_value=valor_max, value=valor_min, step=100)
    with col2:
        st.text('')

    with col3:
        valor_max_input = st.number_input('Adicione o Valor [R$] Máximo:',
                                          min_value=valor_min, max_value=valor_max, value=valor_max, step=100)
        mask_valor = (df['VALOR[R$]'] >= valor_min_input) & (df['VALOR[R$]'] <= valor_max_input)


    col1, col2, col3 = st.columns([10, 1, 10])
    with col1:
        area_max = int(df['AREA[M2]'].max())
        area_min = int(df['AREA[M2]'].min())
        area_min_input = st.number_input('Adicione a Area [M2] Mínima:',
                                         min_value=area_min, max_value=area_max, value=area_min, step=10)
    with col2:
        st.text('')

    with col3:
        area_max_input = st.number_input('Adicione a Area [M2] Máxima:',
                                         min_value=area_min, max_value=area_max, value=area_max, step=10)
        mask_area = (df['AREA[M2]'] >= area_min_input) & (df['AREA[M2]'] <= area_max_input)


    categoria = df['TIPO'].unique().tolist()
    selected_categoria = st.multiselect("Filtre por Categoria de Imóvel:",
                                   options=categoria, default=categoria)

    quartos = df['QUARTOS'].unique().tolist()
    selected_quartos = st.multiselect("Filtre a Quantidade de Quartos:",
                                     options=quartos, default=quartos)
    banheiros = df['BANHEIROS'].unique().tolist()
    selected_banheiros = st.multiselect("Filtre a Quantidade de Banheiros:",
                                      options=banheiros, default=banheiros)
    vagas = df['VAGAS GARAGEM'].unique().tolist()
    selected_vagas = st.multiselect("Filtre a Quantidade de Vagas de Garagem:",
                                      options=vagas, default=vagas)

    cidade = df['MUNICIPIO'].unique().tolist()
    selected_cidade = st.multiselect("Filtre por Cidades:",
                                   options=cidade, default=cidade)

    bairro = df['BAIRRO'].unique().tolist()
    selected_bairro = st.multiselect("Filtre por Bairros:",
                                     options=bairro, default=bairro)


df = df[df['TIPO'].isin(selected_categoria)]
df = df[df['QUARTOS'].isin(selected_quartos)]
df = df[df['BANHEIROS'].isin(selected_banheiros)]
df = df[df['VAGAS GARAGEM'].isin(selected_vagas)]
df = df[df['MUNICIPIO'].isin(selected_cidade)]
df = df[df['BAIRRO'].isin(selected_bairro)]
df = df.loc[mask_valor]
df = df.loc[mask_area]

st.markdown("<h3 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
            ">Base de Dados Completa - "+basedados+" de Imóveis</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
            ">Número de Imóveis: "+str(df.shape[0])+"</h4>", unsafe_allow_html=True)
st.text("")

selected_rows = agg_tabela(df, use_checkbox=True)
st.markdown('---')


tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 DASHBOARD","🌎 MAPAS",  "‍🔬 LABORATÓRIO", "🔎 ANALISE EXPLORATÓRIA", '👶 PRIMEIRA VEZ AQUI?'])

with tab1:
    if len(selected_rows) == 0:
        dashboard(df, df_local)
    elif len(selected_rows) != 0:
        dashboard(selected_rows, df_local)

with tab2:
    if len(selected_rows) == 0:
        mapa(df, df_local)
    elif len(selected_rows) != 0:
        mapa(selected_rows, df_local)
with tab3:
    if len(selected_rows) == 0:
        olxlab(df)
    elif len(selected_rows) != 0:
        olxlab(selected_rows)
with tab4:
    if len(selected_rows) == 0:
        relatorio(df)
    elif len(selected_rows) != 0:
        relatorio(selected_rows)
with tab5:
   introducao(df)

st.text("")

rodape()