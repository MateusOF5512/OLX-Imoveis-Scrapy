import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from PIL import Image

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium.plugins import MarkerCluster
from folium import plugins

@st.experimental_memo
def get_data(path):
    df = pd.read_csv(path, thousands='.', decimal=',')
    return df

def get_data_float(path):
    df = pd.read_csv(path)
    return df

@st.experimental_memo
def tratamento_dados(df):

    df['IMOVEIS'] = np.where(df['NOME'] == 2, 0, 1)


    DATA = df['TIPO'].str.split(' ', 1, expand=True)
    df['CATEGORIA'] = DATA[0]

    DATA = df['DATA_ANUNCIO'].str.split(' às ', 1, expand=True)
    df['DATA'] = DATA[0]
    df['HORARIO'] = DATA[1]

    HORA = df['HORARIO'].str.split(':', 1, expand=True)
    df['HORA'] = HORA[0]

    df['DATA'] = df['DATA'].replace(['Hoje'], '27 de mar')
    df['DATA'] = df['DATA'].replace(['Ontem'], '26 de mar')

    df['LOCALIZACAO'] = df.apply(lambda row: row['MUNICIPIO'] + ', ' + row['BAIRRO'], axis=1)

    df = df[['NOME','VALOR[R$]','TIPO','AREA[M2]','QUARTOS','BANHEIROS','VAGAS GARAGEM','CONDOMINIO[R$]',
             'IPTU[R$]','GASTOS_ANO[R$]','LINK','MUNICIPIO','BAIRRO','LOGRADOURO','CEP','LATITUDE','LONGITUDE','LOCALIZACAO',
             'Academia','Ar condicionado','Armários na cozinha','Armários no quarto',
             'Churrasqueira','Condomínio fechado','Elevador','Mobiliado','Permitido animais','Piscina','Portaria','Porteiro 24h',
             'Portão eletrônico','Quarto de serviço','Salão de festas','Segurança 24h','Varanda','Área de serviço','Área murada',
             'IMAGENS','CODIGO','CATEGORIA','DATA_ANUNCIO','DATA','HORARIO','HORA','IMOVEIS']]


    return df


def rodape():
    html_rodape = """
    <hr style= "display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;">
      <p style="color:#b0b0b0; text-align: center;">Desenvolvedor: Mateus Ortiz</p>
    """
    st.markdown(html_rodape, unsafe_allow_html=True)
    return None



path = 'data/imoveis2.csv'
df = get_data(path)



config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['zoom2d', 'toggleSpikelines',
                                   'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian']}


def agg_tabela(df, use_checkbox):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=False)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_selection(use_checkbox=use_checkbox, selection_mode='multiple')
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=300, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows


def plot_bolha(df, tipo, varx, vary, varz):

    fig = go.Figure()
    if tipo == "Total":
        df_gp = df.groupby(varz).agg('sum').reset_index()
        fig.add_trace(go.Scatter(x=df_gp[varx], y=df_gp[vary], customdata=df_gp[varz],
                                 mode='markers', name='',
                                 hovertemplate="</br><b>"+varz+"</b> %{customdata}" +
                                               "</br><b>"+varx+":</b> %{x:,.0f}" +
                                               "</br><b>"+vary+":</b> %{y:,.0f}",
                                 marker=dict(
                                     size=50,
                                     color=(df_gp[vary] + df_gp[varx] / 2),
                                     colorscale='Portland',
                                     showscale=True)
                                 ))
    elif tipo == "Média":
        df_gp = df.groupby(varz).agg('mean').reset_index()
        imoveis  = df_gp['IMOVEIS']
        fig.add_trace(go.Scatter(x=df_gp[varx], y=df_gp[vary], customdata=df_gp[varz],
                                 mode='markers', name='',
                                 hovertemplate="</br><b>" + varz + "</b> %{customdata}" +
                                               "</br><b>" + varx + ":</b> %{x:,.0f}" +
                                               "</br><b>" + vary + ":</b> %{y:,.0f}",
                                 marker=dict(
                                     size=50,
                                     color=(df_gp[vary] + df_gp[varx] / 2),
                                     colorscale='Portland',
                                     showscale=True)
                                 ))


    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=20, r=20, b=20, t=20))
    fig.update_xaxes(
        title_text="Eixo X: "+varx, title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')
    fig.update_yaxes(
        title_text="Eixo Y: "+vary, title_font=dict(family='Sans-serif', size=18), zeroline=False,
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.8, gridcolor='#D3D3D3')

    return fig





def bar_plot(df, var1, var2, tipo):


    if tipo == 'Total dos Valores':
        df = df.groupby(var1).agg('sum').reset_index()

    elif tipo == 'Média dos Valores':
        df = df.groupby(var1).agg('mean').reset_index()

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, name=tipo,
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y:,.0f}",
        textposition='none', marker_color='#F18000'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=20, r=20, b=20, t=20), autosize=False, hovermode="x")
    fig.update_yaxes(
        title_text="Eixo Y: "+var2, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        title_text="Eixo X: "+var1, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=20, showgrid=False)

    return fig




def barra_empilada(df, var, tipo):
    df_q = df.groupby('QUARTOS').agg(tipo).reset_index().sort_values(by='QUARTOS', ascending=True)
    df_b = df.groupby('BANHEIROS').agg(tipo).reset_index().sort_values(by='BANHEIROS', ascending=True)
    df_v = df.groupby('VAGAS GARAGEM').agg(tipo).reset_index().sort_values(by='VAGAS GARAGEM', ascending=True)

    x = df_q['QUARTOS'].unique()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='QUARTOS', x=x, y=df_q[var],
        hovertemplate="</br><b>Quartos:</b> %{x}" +
                      "</br><b>"+tipo+":</b> %{y}",
        textposition='none', marker_color='#6D09D5',
        marker_line_color = '#404040', marker_line_width = 1
    ))
    fig.add_trace(go.Bar(
        name='BANHEIROS', x=x, y=df_b[var],
        hovertemplate="</br><b>Banheiros:</b> %{x}" +
                      "</br><b>" + tipo + ":</b> %{y}",
        textposition='none', marker_color='#8BE462',
        marker_line_color = '#404040', marker_line_width = 1
    ))
    fig.add_trace(go.Bar(
        name='VAGAS GARAGEM', x=x, y=df_v[var],
        hovertemplate="</br><b>Vagas Garagem:</b> %{x}" +
                      "</br><b>" + tipo + ":</b> %{y}",
        textposition='none', marker_color='#F18000',
        marker_line_color = '#404040', marker_line_width = 1
    ))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=11, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=320, barmode='stack', margin=dict(l=1, r=10, b=25, t=10), autosize=True, hovermode="x",
    )
    fig.update_yaxes(
        title_text=var, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=9), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        tickfont=dict(family='Sans-serif', size=9), nticks=20, showgrid=False)

    return fig





def pizza(df, var1, var2, tipo):

    df = df.groupby(var1).agg(tipo).sort_values(by=var2, ascending=False).reset_index()
    df = df[[var1, var2]]
    colors = ['#8BE462', '6D09D5']

    fig = go.Figure(data=[go.Pie(labels=df[var1],
                                    values=df[var2], name='',
                                    hovertemplate="</br><b>" + var1 + ":</b> %{label}" +
                                                  "</br><b>" + var2 + ":</b> %{value:,.0f}" +
                                                  "</br><b>Proporção:</b> %{percent}",
                                    textinfo='percent',
                                    showlegend=False,
                                    marker=dict(colors=colors,
                                                line=dict(color='#000010', width=2)))])
    fig.update_traces(hole=.4, )
    fig.update_layout(autosize=False,
                         height=150, margin=dict(l=10, r=10, b=10, t=10),
                         paper_bgcolor="#F8F8FF", font={'size': 20})

    return fig


def barra(df, var1, var2, tipo, marker_color):

    df = df.groupby(var1).agg(tipo).sort_values(by=var2, ascending=False).reset_index()

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, name='',
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y:.0f}",
        textposition='none', marker_color=marker_color,
        marker_line_color = '#404040', marker_line_width = 1))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=10, r=10, b=10, t=10), autosize=False, hovermode="x")
    fig.update_yaxes(
        title_text=var2, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        title_text=var1, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=11), showgrid=False)

    return fig


def funil(df, var1, var2, colors, tipo):

    df = df.groupby(var1).agg(tipo).sort_values(by=var2, ascending=False).reset_index()

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=values, x=y, name='',
        textposition="inside", textinfo="percent total + value",
        marker={"color": colors,
                "line": {"width": [2, 2, 2, 2, 2, 2],
                         "color": ["black", "black", "black", "black", "black"]}},
        connector={"line": {"color": "black", "dash": "solid", "width": 2}}))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=200, margin=dict(l=1, r=1, b=1, t=1))


    return fig



def wordcoud(df, var1):
    words = ' '.join(df[var1])
    stop_words = STOPWORDS.update(["da", "do", "a", "e", "o", "em", "para", "um",
                                   "que", "por", "como", "uma", "de", "onde", "são",
                                   "sim", "não", "mas", "mais", "então", "das", "dos", "nas", "nos",
                                   "bio", "link", "isso", "tem", "até"])

    fig, ax = plt.subplots()
    wordcloud = WordCloud(
        height=150,
        min_font_size=8,
        scale=2.5,
        background_color='#F8F8FF',
        max_words=100,
        stopwords=stop_words,
        min_word_length=3).generate(words)
    plt.imshow(wordcloud)
    plt.axis('off')  # to off the axis of x and

    return fig



def barra2(df, var1, var2, tipo, marker_color):

    df = df.groupby(var1).agg(tipo).sort_values(by=var2, ascending=False).reset_index()[:10]

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, name='',
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y:,.0f}",
        textposition='none', marker_color=marker_color,
        marker_line_color = '#404040', marker_line_width = 1))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=10, r=10, b=10, t=10), autosize=False, hovermode="x")
    fig.update_yaxes(
        title_text=var2, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        title_text=var1, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=11), showgrid=False)

    return fig




def barra3(df, var1, var2, tipo, marker_color):

    df = df.groupby(var1).agg(tipo).sort_values(by=var1, ascending=True).reset_index()

    values = df[var1].unique()
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, name='',
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y:,.0f}",
        textposition='none', marker_color=marker_color,
        marker_line_color = '#404040', marker_line_width = 1))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=10, r=10, b=10, t=10), autosize=False, hovermode="x")
    fig.update_yaxes(
        title_text=var2, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')

    fig.update_xaxes(
        title_text=var1, title_font=dict(family='Sans-serif', size=16),
        tickfont=dict(family='Sans-serif', size=11), showgrid=False)

    return fig







