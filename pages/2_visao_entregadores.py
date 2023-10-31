from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go  
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st

st.set_page_config (page_title ='Visão Entregadores', page_icon='🚚', layout='wide')

df = pd.read_csv('train.csv')

print(df.head())

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


#Os 10 entregadores mais rápidos por cidade
def top_rapidos(df1):

        df2 = (df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
             .groupby( ['City','Delivery_person_ID'] )
             .mean().sort_values( ['City','Time_taken(min)'] )
             .reset_index())
            
        dfaux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
        dfaux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
        dfaux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
        dfaux4 = pd.concat([dfaux1, dfaux2, dfaux3]).reset_index(drop=True)
           
                
        return dfaux4


#Os 10 entregadores mais lentos por cidade
def top_lentos(df1):

                lentos = (df1[['Delivery_person_ID', 'City', 'Time_taken(min)']]
                        .groupby(['City','Delivery_person_ID'])
                        .mean().sort_values(['City','Delivery_person_ID'],ascending=False)
                        .reset_index())

                df2 = lentos.loc[lentos['City'] == 'Metropolitian', :].head(10)
                df3 = lentos.loc[lentos['City'] == 'Urban', :].head(10)
                df4 = lentos.loc[lentos['City'] == 'Semi-Urban', :].head(10)
                df5 = pd.concat([df2, df3, df4]).reset_index(drop=True)

                return df5


#_____________________________________________________________________________________________________________
# _______________________________Inicio Estrutura Código _________________________

# IMPORTAR DATASET
df = pd.read_csv('train.csv')

# LIMPANDO DADOS
df1 = clean_code(df)



#VISAO ENTREGADORES
# ======================================================================================

# BARRA LATERAL NO STREAMLIT


import streamlit as st
from datetime import datetime
from PIL import Image

st.header('Marketplace - Visão Entregadores ')
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
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
                      
            #A maior idade dos entregadores
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior de Idade', maior_idade)

        with col2:
                      
            # A menor idade dos entregadores
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor de Idade', menor_idade)   

        with col3:
          
            # A melhor condição de veículos
            melhor_condicao= df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_condicao)

        with col4:
        
            # A pior condição de veículos
            pior_condicao= df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_condicao)

                

    with st.container():
        st.markdown("""___""")
        st.title('Avaliações')        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Avaliação média por entregador")
            # Avaliação média por entregador
            avg_rating_deliver = (df1[['Delivery_person_ID','Delivery_person_Ratings']]
                                  .groupby('Delivery_person_ID')
                                  .mean()
                                  .reset_index())
            
            st.dataframe(avg_rating_deliver)

        with col2:
            st.markdown('##### Avaliação média por Trânsito')

            #Avaliação média e desvio padrao por tipo de trafego
            media__std_traffic_ratings = (df1[['Delivery_person_Ratings','Road_traffic_density']]
                                      .groupby('Road_traffic_density')
                                      .agg({'Delivery_person_Ratings': ['mean','std']}))

            #Mudança de nome da coluna
            media__std_traffic_ratings.columns = ['Traffic_Mean', 'Traffic_STD']

            #Reset de Index
            media__std_traffic_ratings.reset_index()
        
            st.dataframe(media__std_traffic_ratings)

            st.markdown('##### Avaliação média por Clima')

            #Avaliação média e desvio padrao por condições climaticas
            clima_traffic_ratings = (df1[['Delivery_person_Ratings','Weatherconditions']]
                                     .groupby('Weatherconditions')
                                     .agg({'Delivery_person_Ratings': ['mean', 'std']}))                                   
            
            #Mudança de nome da coluna                        
            clima_traffic_ratings.columns = ['Weather_Mean', 'Weather_Std']

            #Reset de Index
            clima_traffic_ratings.reset_index()
    
            st.dataframe(clima_traffic_ratings)

    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('###### Top Entregadores Mais Rápidos')
            dfaux4 = top_rapidos(df1)
            st.dataframe(dfaux4)
           

        with col2:
            st.markdown('###### Top Entregadores Mais Lentos')
            df5 = top_lentos(df1)
            st.dataframe(df5)
            

            
