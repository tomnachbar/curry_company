from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go  
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st

st.set_page_config (page_title ='Visão Empresa', page_icon='📋', layout='wide')

#_______________________FUNCÕES___________________________________
# ================================================================

def country_maps(df1):
    #6A localização central de cada cidade por tipo de tráfego.

    columns = [
    'City',
    'Road_traffic_density',
    'Delivery_location_latitude',
    'Delivery_location_longitude']

    columns_groupby = ['City', 'Road_traffic_density']

    data_plot = (df1.loc[:, columns]
                   .groupby(columns_groupby)
                   .median()
                   .reset_index())
    data_plot = data_plot[data_plot['City'] != 'NaN']
    data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']

    map = folium.Map()

    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
         
    folium_static(map,width=920,height=600)

def order_share_by_week(df1):    
    #5 A quantidade de pedidos por entregador por semana.
    # Quantas entregas na semana / Quantos entregadores únicos por semana
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    aux = pd.merge(df_aux1,df_aux2, how='inner', on='week_of_year')
    aux['order_by_delivery'] = aux['ID'] / aux['Delivery_person_ID']
    # gráfico
    fig= px.line( aux, x='week_of_year', y='order_by_delivery' )
           
    return fig


def order_by_week(df1):
             
    #2 Quantidade de pedidos por semana.
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df1_aux = (df1.loc[:, ['ID', 'week_of_year']]
               .groupby( 'week_of_year' )
               .count()
               .reset_index())
    fig = px.line(df1_aux, x='week_of_year', y='ID')

    return fig

def traffic_order_city(df1):
    columns = ['ID', 'City', 'Road_traffic_density']
    linhas_vazias = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df_aux = (df1.loc[:, columns]
        .groupby( ['City', 'Road_traffic_density'] )
        .count()
        .reset_index())
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    # gráfico
    fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def traffic_order_share(df1):
    #3 Distribuição dos pedidos por tipo de tráfego.
    df1_aux = (df1[['ID', 'Road_traffic_density']]
               .groupby('Road_traffic_density')
               .count().reset_index())
    df1_aux['perc_ID'] = 100 * ( df1_aux['ID'] / df1_aux['ID'].sum() )
    fig = px.pie(df1_aux, values='perc_ID', names='Road_traffic_density')
                    
    return fig

def order_metric(df1):
    cols = ['ID','Order_Date']
            
    #Selecao de linhas
    df_aux = df1.loc[:,cols].groupby('Order_Date').count().reset_index()
           
    #Desenhar o grafico de linhas
    fig = px.bar(df_aux, x='Order_Date', y='ID')
                      
    return fig    

def clean_code(df1):
    """Esta função serve para limpar o dataframe
    
        Tipos de limpeza:
        1. Remoção dos dados NAN
        2. Mudança do tipo de coluna 
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da Data
        5. Limpeza Coluna Tempo(min) variável númerica
    """ 
#LIMPEZA DOS DADOS
    linhas_vazias = df1['ID'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Delivery_person_ID'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Order_Date'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Weatherconditions'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Type_of_vehicle'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Type_of_order'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    #LIMPEZA DOS ESPAÇOS EM BRANCO
    df1['City'] = df1['City'].apply(lambda x: x.strip())
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.strip())
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Delivery_person_ID'] = df1['Delivery_person_ID'].apply(lambda x: x.strip())
    df1['Order_Date'] = df1['Order_Date'].apply(lambda x: x.strip())
    df1['Weatherconditions'] = df1['Weatherconditions'].apply(lambda x: x.strip())
    df1['Road_traffic_density'] = df1['Road_traffic_density'].apply(lambda x: x.strip())
    df1['multiple_deliveries'] = df1['multiple_deliveries'].apply(lambda x: x.strip())
    df1['Festival'] = df1['Festival'].apply(lambda x: x.strip())
    df1['City'] = df1['City'].apply(lambda x: x.strip())
    df1['Type_of_vehicle'] = df1['Type_of_vehicle'].apply(lambda x: x.strip())
    df1['Type_of_order'] = df1['Type_of_order'].apply(lambda x: x.strip())

    ## CONVERSÃO DE TIPOS DE COLUNA
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# _______________________________Inicio Estrutura Código _________________________
# IMPORTAR DATASET
df = pd.read_csv('train.csv')

# LIMPANDO DADOS
df1 = clean_code(df)

# VISAO EMPRESA
# ======================================================================================

# BARRA LATERAL NO STREAMLIT
#=======================================================================================

import streamlit as st
from datetime import datetime
from PIL import Image

st.header('Marketplace - Visão Cliente ')
#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=160)

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """____""" )


st.sidebar.markdown('## Selecione uma data limite')
date_slider= st.sidebar.slider(
    'Até qual valor?', 
    value=pd.Timestamp('2022-04-13').to_pydatetime(),
    min_value=pd.Timestamp('2022-02-11').to_pydatetime(),
    max_value=pd.Timestamp('2022-04-06').to_pydatetime(),
    format='DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown( """____""" )

traffic_options= st.sidebar.multiselect(
    'Quais as condições do trânsito:',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'])

st.sidebar.markdown("""____""")
st.sidebar.markdown('### Powered by Eliton Nachbar')


# FILTROS DE DATA NO STREAMLIT
#________________________________________

linhas_selecionadas =df1['Order_Date'] < date_slider
df1= df1.loc[linhas_selecionadas,:]


# FILTROS DE TRANSITO NO STREAMLIT
#________________________________________
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options) 
df1= df1.loc[linhas_selecionadas,:]

# ==========================================================
#  LAYOUT STREAMLIT
# ==========================================================

tab1, tab2,tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1: 
    with st.container():
         #Order Metric
         fig = order_metric(df1)
         st.markdown('# Orders by Day')
         st.plotly_chart(fig, use_container_width=True)
             
    with st.container():       
        col1, col2 = st.columns(2)
        
        with col1:
                fig = traffic_order_share(df1)
                st.header(' Traffic Order Share')
                st.plotly_chart(fig, use_container_width=True)
                             
        with col2:
                #4. Comparação do volume de pedidos por cidade e tipo de tráfego.
                fig = traffic_order_city(df1)
                st.header(' Traffic Order City')
                st.plotly_chart(fig, use_container_width=True)
               
with tab2:
    with st.container():
        st.markdown('# Order by Week')
        st.plotly_chart(fig,use_container_width=True)
        fig = order_by_week(df1)
       
    with st.container(): 
        st.markdown('# Order Share by Week')
        st.plotly_chart(fig,use_container_width=True)
        fig = order_share_by_week(df1)

with tab3:
    st.markdown('# Country Maps')
    country_maps(df1)
    
        