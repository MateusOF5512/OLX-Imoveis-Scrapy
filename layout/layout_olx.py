
from plots.plots_olx import *

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report




def olxlab(df):
    st.markdown('---')
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Análise Comparativa -  Gráfico de Barra</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Dados em Análise: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        df_x = df[['NOME', 'TIPO', 'QUARTOS', 'BANHEIROS',
                   'VAGAS GARAGEM', 'IMAGENS', 'DATA', 'HORARIO', 'LOCALIZACAO',
                   'LINK']]
        var1 = st.selectbox('coluna pro Eixo X:', df_x.columns.unique(), index=2, key=78)
    with col2:
        df_y = df[['VALOR[R$]', 'AREA[M2]',
                   'CONDOMINIO[R$]', 'IPTU[R$]', 'GASTOS_ANO[R$]', 'IMOVEIS']]
        var2 = st.selectbox('Coluna paro Eixo Y:', df_y.columns.unique(), index=0, key=79)

    with col3:
        tipo = st.radio("Formato do Eixo Y:",
                        options=["Total dos Valores", "Média dos Valores"], index=1, horizontal=True)

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

    st.text("")
    st.markdown('---')
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px 0px 0px;'" +
                ">Análise de Disperção -  Gráfico de Bolha</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Dados em Análise: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        varz = st.selectbox("Agrupamento dos dados:",
                            options=["TIPO", 'QUARTOS', 'BANHEIROS', "VAGAS", 'MUNICIPIO', 'BAIRRO'
                                                                                           'HORA', 'DATA', 'LINK'],
                            index=1)
    with col2:
        df_x_bolha = df[['VALOR[R$]', 'AREA[M2]', 'GASTOS_ANO[R$]', 'CONDOMINIO[R$]', 'IPTU[R$]']]
        varx = st.selectbox('Coluna pro Eixo X:',
                            df_x_bolha.columns.unique(), index=0, key=71)
    with col3:
        df_y_bolha = df[['VALOR[R$]', 'AREA[M2]', 'GASTOS_ANO[R$]', 'CONDOMINIO[R$]', 'IPTU[R$]']]
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
    st.text("")

    return None



def relatorio(df):

    st.markdown('---')
    st.markdown("<h3 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px 0px 0px;'" +
                ">Análise Exploratória dos Dados</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Dados em Análise: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')

    text = """Para gerar os Relatórios utilizamos o pandas-profiling, que entrega todas as ferramentas necessárias para 
                    uma análise profunda, rápida e simples dos dados. Gerando automaticamente relatórios personalizados para 
                    cada variável no conjunto de dados, com estatística, gráficos, alertas, correlações e mais. 
                    Para gerar esses Relatórios pode demorar uns segundos, dependendo da Tabela até minutos."""

    st.info(text)



    report = st.checkbox("Carregar Relatório dos Dados 🔎", key=76)

    if report:
        profile = ProfileReport(df, title="Relatório dos Dados", explorative=True)
        st_profile_report(profile)

    return None


def dashboard(df, df_local):
    st.text('')
    st.markdown("<h2 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Características dos Imóveis</h2>",unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                ">Número de Imóveis: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        fig = pizza(df, 'CATEGORIA', 'IMOVEIS', 'sum')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Imóveis por Categorias</h4>",unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config=config)
    with col2:
        st.text('')
    with col3:
        fig1 = pizza(df, 'CATEGORIA', 'VALOR[R$]', 'mean')
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Categorias</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config=config)
    st.text('')


    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Quartos</h4>",
                    unsafe_allow_html=True)

        colors = ["#410f70", "#761cca", "#8f35e3", "#c18ff0", "#e6d2f9"]
        fig4 = funil(df, 'QUARTOS', 'IMOVEIS', colors, 'sum')
        st.plotly_chart(fig4, use_container_width=True, config=config)

    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Quartos</h4>",
                    unsafe_allow_html=True)
        colors = ["#410f70", "#761cca", "#8f35e3", "#c18ff0", "#e6d2f9"]
        fig5 = funil(df, 'QUARTOS', 'VALOR[R$]', colors, 'mean')
        st.plotly_chart(fig5, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Banheiros</h4>",
                    unsafe_allow_html=True)
        colors = ["#008000", "#00cc00", "#1aff1a", "#66ff66", "#b3ffb3"]
        fig6 = funil(df, 'BANHEIROS', 'IMOVEIS', colors, 'sum')
        st.plotly_chart(fig6, use_container_width=True, config=config)
    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Banheiros</h4>",
                    unsafe_allow_html=True)
        colors = ["#008000", "#00cc00", "#1aff1a", "#66ff66", "#b3ffb3"]
        fig7 = funil(df, 'BANHEIROS', 'VALOR[R$]', colors, 'mean')
        st.plotly_chart(fig7, use_container_width=True, config=config)
    st.text('')

    col1, col2, col3 = st.columns([520, 60, 520])
    with col1:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Número de Vagas Garagem</h4>",
                    unsafe_allow_html=True)
        colors = ["#cc7000", "#ff8c00", "#ffa333", "#ffba66", "#ffd199", "#fff"]
        fig5 = funil(df, 'VAGAS GARAGEM', 'IMOVEIS', colors, 'sum')
        st.plotly_chart(fig5, use_container_width=True, config=config)
    with col2:
        st.text("")
    with col3:
        st.markdown("<h4 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Média dos Valores por Vagas Garagem</h4>",
                    unsafe_allow_html=True)
        colors = ["#cc7000", "#ff8c00", "#ffa333", "#ffba66", "#ffd199", "#fff"]
        fig5 = funil(df, 'VAGAS GARAGEM', 'VALOR[R$]', colors, 'mean')
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
        fig = barra_empilada(df, 'GASTOS_ANO[R$]', 'mean')
        st.plotly_chart(fig, use_container_width=True, config=config)
    with col2A:
        st.text("")
    with col3A:
        df_des = df.describe()
        df_des = df_des[['VALOR[R$]', 'GASTOS_ANO[R$]', 'CONDOMINIO[R$]', 'IPTU[R$]', 'AREA[M2]', 'IMOVEIS']]
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Estatísticas dos Gastos</h3>",
                    unsafe_allow_html=True)
        st.dataframe(df_des)

    col1A, col2A, col3A = st.columns([520, 60, 520])
    with col1A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Média do Gasto Ano por Categoria de Imóvel</h3>",
                    unsafe_allow_html=True)
        fig = barra(df, 'TIPO', 'GASTOS_ANO[R$]', 'mean', '#6D09D5')
        st.plotly_chart(fig, use_container_width=True, config=config)

    with col2A:
        st.text("")
    with col3A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Tipo do Imóvel por Média de Gastos Ano & Valor</h3>",
                    unsafe_allow_html=True)
        fig = plot_bolha(df, 'Média','VALOR[R$]', 'GASTOS_ANO[R$]',  'TIPO', )
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
        fig = wordcoud(df, 'NOME')
        st.pyplot(fig)

    with col2A:
        st.text("")
    with col3A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">10 Municípios com mais Anúncios</h3>",
                    unsafe_allow_html=True)

        fig = barra2(df, 'MUNICIPIO', 'IMOVEIS', 'sum', '#6D09D5')
        st.plotly_chart(fig, use_container_width=True, config=config)

    col1A, col2A, col3A = st.columns([520, 60, 520])
    with col1A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Total de Anúncios Publicados por Dia</h3>",
                    unsafe_allow_html=True)

        fig = barra(df, 'DATA', 'IMOVEIS', 'sum', '#8BE462')
        st.plotly_chart(fig, use_container_width=True, config=config)

    with col2A:
        st.text("")
    with col3A:
        st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 0px;'" +
                    ">Total de Anúncios Publicados por Hora</h3>",
                    unsafe_allow_html=True)
        fig = barra3(df, 'HORA', 'IMOVEIS', 'sum', '#F18000')
        st.plotly_chart(fig, use_container_width=True, config=config)


    return None


def mapa(df, df_local):

    try:
        merge = pd.merge(df, df_local, how='left', on='LOCALIZACAO')
        merge = merge[merge['LAT'].notna()]

        st.markdown('---')
        st.markdown("<h3 style='font-size:200%; text-align: center; color: #6709CB; padding: 0px 0px 0px 0px;'" +
                    ">Localização dos Imóveis</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size:120%; text-align: center; color: #6709CB; padding: 0px 0px;'" +
                    ">Imóveis em Análise: " + str(merge.shape[0]) + "</h4>", unsafe_allow_html=True)
        st.markdown('---')

        col1A, col2A, col3A = st.columns([520, 60, 520])
        with col1A:
            coordenadas = []
            for lat, long in zip(merge["LAT"], merge["LONG"]):
                coordenadas.append([lat, long])

            mapa = folium.Map(location=[merge["LAT"].mean(),
                                        merge["LONG"].mean()],
                              zoom_start=9, tiles='Stamen Terrain',
                              width=550, height=350, control_scale=True)

            mapa.add_child(plugins.HeatMap(coordenadas))

            st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 10px;'" +
                        ">Mapa de Calor dos Imóveis</h3>", unsafe_allow_html=True)
            folium_static(mapa)

        with col2A:
            st.text("")
        with col3A:
            colors = {
                'Biguaçu': 'red',
                'Laguga': 'red',
                'Governador Celso Ramos': 'purple',
                'Tijucas': 'red',
                'Garopaba': 'orange',
                'Criciúma': 'red',
                'Tubarão': 'red',
                'Florianópolis': 'green',
                'São José': 'blue',
                'Palhoça': 'red',
            }

            merge2 = merge.groupby(['LOCALIZACAO', 'MUNICIPIO', "LAT", "LONG", ]).count().reset_index()

            mapa2 = folium.Map(location=[merge2["LAT"].mean(),
                                         merge2["LONG"].mean()],
                               zoom_start=9,
                               tiles='Stamen Terrain',
                               width=550, height=350, control_scale=True)

            for name, row in merge2.iterrows():
                if row['MUNICIPIO'] in colors.keys():
                    folium.Marker(
                        location=[row["LAT"], row["LONG"]],
                        popup=f"Local: {row['LOCALIZACAO']} \n "
                              f"N°Imóveis: {row['IMOVEIS']}",
                        icon=folium.Icon(color=colors[row['MUNICIPIO']])
                    ).add_to(mapa2)

            st.markdown("<h3 style='font-size:150%; text-align: center; color: #6709CB; padding: 10px 10px;'" +
                        ">Concentração de Imóveis por Município</h3>", unsafe_allow_html=True)
            folium_static(mapa2)

        merge3 = merge.groupby(['LOCALIZACAO', 'MUNICIPIO', "LAT", "LONG"]).mean().reset_index()
        #merge3 = merge3[['LOCALIZACAO', 'CIDADE', "LAT", "LONG"]]
        #st.dataframe(merge3)
    except:
        st.error('Selecione um Bairro e Município cadastrado', icon='🚨')

    return None


def introducao(df):
    st.markdown('Em construção!')

    return None