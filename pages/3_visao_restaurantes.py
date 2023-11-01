from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go  
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np
import streamlit as st

st.set_page_config (page_title ='Visão Restaurantes', page_icon='🥘', layout='wide')


#_______________________FUNCÕES___________________________________
# ================================================================

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
    df1 = df.copy()

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


   # Distância Média 
def distancia (df1):
                
           cols = ['Restaurant_latitude', 'Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
           df1['distance'] = df1.loc[:,cols].apply( lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
           avg_distance = np.round(df1['distance'].mean(),2)

           return avg_distance

# MÉDIA DE TEMPO
def avg_delivery(df1):

              order_media_std = df1.loc[:,['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean','std']})
              order_media_std.columns = ['avg_time','std_time']
              order_media_std = order_media_std.reset_index()
              order_media = np.round(order_media_std.loc[order_media_std['Festival']== 'Yes','avg_time'],2)
                  
              return order_media
# DESVIO PADRÃO
def std_delivery(df1):
        order_media_std = df1.loc[:,['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean','std']})
        order_media_std.columns = ['avg_time','std_time']
        order_media_std = order_media_std.reset_index()
        order_std = np.round(order_media_std.loc[order_media_std['Festival']== 'Yes','std_time'],2)

        return order_std


def time_media_avg(df1, festival, op):

        order_media_std = df1.loc[:,['Time_taken(min)','Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean','std']})
        order_media_std.columns = ['avg_time','std_time']
        order_media_std = order_media_std.reset_index()
        order_media_std = np.round(order_media_std.loc[order_media_std['Festival']== festival, op],2)
            
        return order_media_std

def time_avg_std(df1):

        time_media_std = df1.loc[:,['Time_taken(min)','City']].groupby('City').agg({'Time_taken(min)': ['mean','std']})
        time_media_std.columns = ['avg_time','std_time']
        time_media_std = time_media_std.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar (name='Control',x=time_media_std['City'],y=time_media_std['avg_time'],error_y=dict(type='data', array=time_media_std['std_time'])))
        fig.update_layout(barmode='group')
        
        return fig

def distance_share(df1):
                 
        order_media_std = (df1.loc[:,['Time_taken(min)','Type_of_order','City']]
                    .groupby(['Type_of_order','City'])
                    .agg({'Time_taken(min)': ['mean','std']}))
    
        order_media_std.columns=['avg_time','std_time']
        order_media_std = order_media_std.reset_index()
        
        return order_media_std


def distance_fig(df1):
                
        cols = ['Restaurant_latitude', 'Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:,cols].apply( lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df1.groupby('City')['distance'].mean()
        fig = go.Figure(data=[go.Pie(labels=avg_distance.index, values=avg_distance.values, pull=[0, 0.1, 0])])

        return fig

def traffic_media(df1):
        
    traffic_media_std = (df1.loc[:,['Time_taken(min)','Road_traffic_density','City']]
                        .groupby(['Road_traffic_density','City'])
                        .agg({'Time_taken(min)': ['mean','std']}))

    traffic_media_std.columns=['avg_time', 'std_time']
    traffic_media_std = traffic_media_std.reset_index()
    fig = px.sunburst(traffic_media_std, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='Cividis',
                    color_continuous_midpoint=np.average(traffic_media_std['std_time']))
    
    return fig


#------------------------------------------------------------------------------------------
df = pd.read_csv('train.csv')

df1 = clean_code(df)
#------------------------------------------------------------------------------------------

#=======================================================================================
                                #VISAO RESTAURANTES
# ======================================================================================

# BARRA LATERAL NO STREAMLIT


import streamlit as st
from datetime import datetime
from PIL import Image

st.header('Marketplace - Visão Restaurantes ')
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

conditions_wheather= st.sidebar.multiselect(
    'Quais as condições do Clima:',
    ['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy','conditions Sunny','conditions Windy'],
    default=['conditions Cloudy','conditions Fog','conditions Sandstorms','conditions Stormy','conditions Sunny','conditions Windy'])
    
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

# FILTROS DE CLIMA NO STREAMLIT
#________________________________________
linhas_selecionadas = df1['Weatherconditions'].isin(conditions_wheather) 
df1= df1.loc[linhas_selecionadas,:]



# ==========================================================
#  LAYOUT STREAMLIT
# ==========================================================


tab1, tab2,tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')

        col1, col2, col3, col4, col5, col6 = st.columns(6, gap='small')
        with col1:
            #Entregadores Unicos
            unicos = len(df.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Entregadores', unicos)

        with col2:
            avg_distance = distancia(df1)
            col2.metric('Média', avg_distance)                           
                               
        with col3:
            order_media = avg_delivery(df1)
            col3.metric('Tempo c/ Festival',order_media)
                  
        with col4:
            order_std = std_delivery(df1)
            col4.metric('Desvio Padrão c/ Festival',order_std)
              
        with col5:
            order_media_std = time_media_avg(df1,'No','avg_time')
            col5.metric('Tempo s/ Festival',order_media_std)

        with col6:
            order_media_std = time_media_avg(df1,'No','std_time')
            col6.metric('Desvio Padrão s/ Festival',order_media_std)

    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:    
            st.title('Tempo Médio de entrega por Cidade')
            fig = time_avg_std(df1)
            st.plotly_chart(fig,use_container_width=True)
     

        with col2:
            st.title('Distribuição da Distância')      
            order_media_std = distance_share(df1)
            st.dataframe(order_media_std)
           
    with st.container():
        st.title('Distribuição do Tempo')
        col1, col2 = st.columns(2)
        
        with col1:

            fig = distance_fig(df1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = traffic_media(df1)
            st.plotly_chart(fig, use_container_width=True)

            

   
