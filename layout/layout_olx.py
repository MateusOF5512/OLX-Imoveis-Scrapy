import struct

import streamlit

from plots.plots_olx import *

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report



def sidebar(df):
    with st.sidebar:
        with st.expander("⚙️ Configurar Dados"):
            st.text("ainda nada")

        with st.expander("⚙️ Configurar Dashbords"):
            st.text("ainda nada")

    return None


def olxlab(df, selected_rows):

    if len(selected_rows) == 0:
        # GRÁFICO DE BOLHO - ANÁLSIE DE DISPERÇÃO - PARTE 1 ----------------------------------------
        st.markdown("<h3 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px 0px 0px;'" +
                    ">Análise de Disperção -  Gráfico de Bolha</h3>",
                    unsafe_allow_html=True)
        st.text("")
        st.text("")

        # CONFIGURAÇÃO PARA ANÁLISE E EXPLORAÇÃO
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            varz = st.selectbox("Agrupamento dos dados:",
                                options=["CATEGORIA", 'TIPO', 'QUARTOS', 'BANHEIROS',
                                         "VAGAS", 'CEP'], index=1)
        with col2:
            df_x_bolha = df[['VALOR [R$]', 'AREA [M2]', 'FINANCIAMENTO ENTRADA [R$]',
                             'CONDOMINIO [R$]', 'IPTU [R$]', 'GASTOS POR ANO [R$]']]
            varx = st.selectbox('Coluna pro Eixo X:',
                                df_x_bolha.columns.unique(), index=0, key=71)
        with col3:
            df_y_bolha = df[['VALOR [R$]', 'AREA [M2]', 'FINANCIAMENTO ENTRADA [R$]',
                             'CONDOMINIO [R$]', 'IPTU [R$]', 'GASTOS POR ANO [R$]']]
            vary = st.selectbox('Coluna pro Eixo Y:',
                                df_y_bolha.columns.unique(), index=1, key=72)
        with col4:
            tipo = st.radio("Formato do Eixo Y:",
                            options=["Total", "Média"], key=73, horizontal=True, index=1)

        fig2 = plot_bolha(df, tipo, varx, vary, varz)
        st.plotly_chart(fig2, use_container_width=True, config=config)

        # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
        with st.expander("🔎️   Dados - Análise de Disperção"):
            if tipo == "Total":
                df_bolha = df.groupby([varx])[vary].agg('sum').reset_index().sort_values(varx, ascending=True)
                df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)
            elif tipo == "Média":
                df_bolha = df.groupby([varx])[vary].agg('mean').reset_index().sort_values(varx, ascending=True)
                df_bolha.loc[:, vary] = df_bolha[vary].map('{:,.0f}'.format)

            checkdf = st.checkbox('Visualizar Dados', key=70)
            if checkdf:
                df_bolha = df_bolha[[varx, vary]]

                st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB;'" +
                            "><i>" + tipo + "</i> de <i>" + vary + "</i> por <i>" + varx + "</i> - TABELA RESUMIDA</h3>",
                            unsafe_allow_html=True)
                agg_tabela(df_bolha, use_checkbox=True)

            df_bolha = df_bolha.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_bolha,
                               file_name="DataApp.csv", mime='text/csv')
        st.markdown('---')
        st.text('')
        # GRÁFICO DE BARRA ´ANÁLISE COMPARATIVA - PARTE 2 ------------------------------------------------
        st.markdown("<h3 style='font-size:200%; text-align: center; color: #6709CB;'" +
                    ">Análise Comparativa -  Gráfico de Barra</h3>",
                    unsafe_allow_html=True)
        st.text("")
        st.text("")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            df_x = df[['NOME ANUNCIO', 'CATEGORIA', 'TIPO', 'QUARTOS', 'BANHEIROS',
                       'VAGAS GARAGEM', 'DETALHES DO IMOVEL', 'DETALHES DO CONDOMINIO',
                       'IMAGENS ANUNCIO', 'DATA ANUNCIO', 'CIDADE', 'CEP', 'LINK ANUNCIO']]
            var1 = st.selectbox('coluna pro Eixo X:', df_x.columns.unique(), index=2, key=78)
        with col2:
            df_y = df[['VALOR [R$]', 'AREA [M2]', 'FINANCIAMENTO ENTRADA [R$]',
                             'CONDOMINIO [R$]', 'IPTU [R$]', 'GASTOS POR ANO [R$]', 'UNIDADE']]
            var2 = st.selectbox('Coluna paro Eixo Y:', df_y.columns.unique(), index=0, key=79)

        with col3:
            tipo = st.radio("Formato do Eixo Y:",
                            options=["Total dos Valores", "Média dos Valores"], horizontal=True)

        fig1 = bar_plot(df, var1, var2, tipo)
        st.plotly_chart(fig1, use_container_width=True, config=config)

        # DOWNLOAD E VISUALIZAÇÃO DOS DADOS SELECIONADOS ------------------------------------------------
        with st.expander("🔎️   Dados - Análise Comparativa"):
            if tipo == "Total dos Valores":
                df_barra = df.groupby([var1])[var2].agg('sum').reset_index().sort_values(var1, ascending=True)
                df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)
            elif tipo == "Média dos Valores":
                df_barra = df.groupby([var1])[var2].agg('mean').reset_index().sort_values(var1, ascending=True)
                df_barra.loc[:, var2] = df_barra[var2].map('{:,.0f}'.format)

            checkdf = st.checkbox('Visualizar Dados', key=58)
            if checkdf:
                df_barra = df_barra[[var1, var2]]

                st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB;'" +
                            "><i>" + tipo + "</i> de <i>" + var2 + "</i> por <i>" + var1 + "</i> - TABELA RESUMIDA</h3>",
                            unsafe_allow_html=True)
                agg_tabela(df_barra, use_checkbox=True)

            df_barra = df_barra.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_barra,
                               file_name="DataApp.csv", mime='text/csv')


    return None



def relatorio(df):

    text = """Para gerar os Relatórios utilizamos o pandas-profiling, que entrega todas as ferramentas necessárias para 
                    uma análise profunda, rápida e simples dos dados. Gerando automaticamente relatórios personalizados para 
                    cada variável no conjunto de dados, com estatística, gráficos, alertas, correlações e mais. 
                    Para gerar esses Relatórios pode demorar uns segundos, dependendo da Tabela até minutos, 
                    mas a demora vale a pena pela riqueza de informações, enquanto espera leia sobre suas funcionalidades:"""

    st.info(text)

    report = st.checkbox("Carregar Relatório dos Dados 🔎", key=76)

    if report:
        profile = ProfileReport(df, title="Relatório dos Dados", explorative=True)
        st_profile_report(profile)

    return None



def dashboard(df):
    st.text('')
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Características dos Imóveis</h2>",unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Número de Imóveis: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        fig = pizza(df, 'CATEGORIA', 'UNIDADE')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Imóveis por Categorias</h4>",unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config=config)
    with col2:
        st.text('')
    with col3:
        fig1 = pizza(df, 'CATEGORIA', 'VALOR [R$]')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Categorias</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        fig2 = barra(df, 'TIPO', 'UNIDADE', 'sum', '#F18000')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Imóveis por Tipo de Venda</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config=config)
    with col2:
        st.text("")
    with col3:
        fig3 = barra(df, 'TIPO', 'VALOR [R$]', 'mean', '#F18000')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Tipo de Venda</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Quartos</h4>",
                    unsafe_allow_html=True)

        colors = ["#410f70", "#761cca", "#8f35e3", "#c18ff0", "#e6d2f9"]
        fig4 = funil(df, 'QUARTOS', 'UNIDADE', colors, 'sum')
        st.plotly_chart(fig4, use_container_width=True, config=config)

    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Quartos</h4>",
                    unsafe_allow_html=True)
        colors = ["#410f70", "#761cca", "#8f35e3", "#c18ff0", "#e6d2f9"]
        fig5 = funil(df, 'QUARTOS', 'VALOR [R$]', colors, 'mean')
        st.plotly_chart(fig5, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Banheiros</h4>",
                    unsafe_allow_html=True)
        colors = ["#008000", "#00cc00", "#1aff1a", "#66ff66", "#b3ffb3"]
        fig6 = funil(df, 'BANHEIROS', 'UNIDADE', colors, 'sum')
        st.plotly_chart(fig6, use_container_width=True, config=config)
    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Banheiros</h4>",
                    unsafe_allow_html=True)
        colors = ["#008000", "#00cc00", "#1aff1a", "#66ff66", "#b3ffb3"]
        fig7 = funil(df, 'BANHEIROS', 'VALOR [R$]', colors, 'mean')
        st.plotly_chart(fig7, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Vagas Garagem</h4>",
                    unsafe_allow_html=True)
        colors = ["#cc7000", "#ff8c00", "#ffa333", "#ffba66", "#ffd199"]
        fig5 = funil(df, 'VAGAS GARAGEM', 'UNIDADE', colors, 'sum')
        st.plotly_chart(fig5, use_container_width=True, config=config)
    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Vagas Garagem</h4>",
                    unsafe_allow_html=True)
        colors = ["#cc7000", "#ff8c00", "#ffa333", "#ffba66", "#ffd199"]
        fig5 = funil(df, 'VAGAS GARAGEM', 'VALOR [R$]', colors, 'mean')
        st.plotly_chart(fig5, use_container_width=True, config=config)
    st.text('')



    st.markdown('---')

    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Gastos com os Imóveis</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Número de Imóveis: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')
    st.text('')

    col1A, col2A, col3A = st.columns([520, 60, 520])
    with col1A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 5px 0px;'" +
                    ">Gastos Ano por Características do Imóvel</h3>",
                    unsafe_allow_html=True)
        fig = barra_empilada(df, 'GASTOS POR ANO [R$]', 'mean')
        st.plotly_chart(fig, use_container_width=True, config=config)
    with col2A:
        st.text("")
    with col3A:
        df_des = df.describe()
        df_des = df_des[['VALOR [R$]', 'AREA [M2]', 'VALOR M2 [R$]',
                         'GASTOS POR ANO [R$]', 'CONDOMINIO [R$]', 'IPTU [R$]',
                         'FINANCIAMENTO ENTRADA [R$]', 'FINANCIAMENTO 1PARCELA [R$]']]
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Estatísticas dos Gastos</h3>",
                    unsafe_allow_html=True)
        st.dataframe(df_des)

    col1A, col2A, col3A = st.columns([520, 60, 520])
    with col1A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Média do Gasto Ano por Categoria de Imóvel</h3>",
                    unsafe_allow_html=True)
        fig = barra(df, 'CATEGORIA', 'GASTOS POR ANO [R$]', 'mean', '#6D09D5')
        st.plotly_chart(fig, use_container_width=True, config=config)

    with col2A:
        st.text("")
    with col3A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Tipo de Imóvel por Gastos Ano X Valor da Compra</h3>",
                    unsafe_allow_html=True)
        fig = plot_bolha(df, 'Média','VALOR [R$]', 'GASTOS POR ANO [R$]',  'TIPO', )
        st.plotly_chart(fig, use_container_width=True, config=config)

    st.markdown('---')

    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Detalhes dos Anúncios</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Número de Anúncios: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')
    st.text('')

    col1A, col2A, col3A = st.columns([520, 60, 520])
    with col1A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Palavras mais Comuns nos Nomes de Anuncios</h3>",
                    unsafe_allow_html=True)
        fig = wordcoud(df, 'NOME ANUNCIO')
        st.pyplot(fig)

    with col2A:
        st.text("")
    with col3A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Total de Anúncios Publicados por Data</h3>",
                    unsafe_allow_html=True)
        fig = barra(df, 'DATA ANUNCIO', 'UNIDADE', 'sum', '#8BE462')
        st.plotly_chart(fig, use_container_width=True, config=config)


    return None