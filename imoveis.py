import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image


img=Image.open('venda-de-imoveis-usados-cai-em-dezembro-zappro.jpg')
st.image(img,width=600)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Analytics São Paulo Real Estate Sale & Rent \n')
df = pd.read_csv('sao-paulo-properties-april-2019.csv')
st.markdown('''
Este conjunto de dados contém cerca de 13.000 apartamentos para venda e aluguel na cidade de São Paulo, Brasil. Os dados vêm de várias fontes, especialmente sites de classificados imobiliários.:  
Base de dados: [Kaggle](https://www.kaggle.com/datasets/argonalyst/sao-paulo-real-estate-sale-rent-april-2019)
''')

# Data clean
# Excluindo os caracteres / e a palavra São Paulo da base

df['District'] = df['District'].apply(lambda x: x[:-10])
#st.dataframe(df)

# Criando novas colunas
# Criando uma classificação por preço
df["Classification"]= df["Price"].apply(lambda x: "low_standard" if x <= 200000 else "medium_standard" if (x>200000) & (x<=400000) else "high_standard")
#st.dataframe(df)

# Filtro com os imovéis que estão a venda
df_sale = df[df["Negotiation Type"] == "sale"]

# Criando nova coluna price_m2
df_sale["price_m2"] = df["Price"] / df["Size"]
st.dataframe(df_sale)

st.title('Motivação para o estudo')
st.markdown('''
Gerar insights para a área de negócio tomar as melhores decisões em relação ao valor do aluguel. ''')


st.title('4 hipotéses que serão validadas com os dados')
st.markdown('''H1 - Imóveis com piscina são, em média, 25% mais caros ''')
h1 = df_sale[['Price', 'Swimming Pool']].groupby('Swimming Pool').mean().reset_index()
st.bar_chart(x='Swimming Pool', y='Price', data = h1)
h1_percentual = (h1.loc[1,'Price'] / h1.loc[0,'Price'] -1) * 100
st.write(f'Falso, Imóveis com piscina são, em média, {h1_percentual:.2f}% mais caros.')



st.markdown('''H2 - Imóveis do bairro Vila Madalena, são em média, 30% mais baratos que o bairro de Moema ''')
bairro= df_sale.loc[(df['District'] == "Vila Madalena") |(df_sale['District'] =="Moema")]
h2 = bairro[['Price', 'District']].groupby('District').mean().reset_index()
st.bar_chart(x='District', y='Price', data = h2)

h2_percentual = (h2.loc[0,'Price'] / h2.loc[1,'Price'] -1) * 100

st.write(f'Falso,Imóveis na Vila Madalena são, em média, {h2_percentual:.2f}% mais baratos.')

st.markdown('''H3 - Apartamentos de 100m no bairro do Brooklin, são em média, 50% mais baratos que na Vila Olimpia ''')
df1 = df_sale[(df_sale['District'] == 'Brooklin') & (df_sale['Size'] >= 100)]
df2 = df_sale[(df_sale['District'] == 'Vila Olimpia') & (df_sale['Size'] >= 100)]
df3 = pd.concat([df1,df2])
h3 = df3[['Price', 'District']].groupby('District').mean().reset_index()
st.bar_chart(x='District', y='Price', data = h3)

h3_percentual = (h3.loc[1,'Price'] / h3.loc[0,'Price'] -1) * 100

st.write(f' Falso,Imóveis de mais de 100m2 no bairro do Brooklin são, em média, {h3_percentual:.2f}% mais baratos.')


st.markdown('''H4 - Apartamentos de 3 quartos no bairro de pinheiros, são em média, 25% mais caros que no bairro do morumbi.''')
df_filter = df[(df['District'] == 'Pinheiros') & (df['Rooms'] == 3)  & (df['Negotiation Type'] == 'sale') & (df['Property Type'] == 'apartment') | (df['District'] == 'Morumbi') &  (df['Rooms'] == 3)  & (df['Negotiation Type'] == 'sale') & (df['Property Type'] == 'apartment') ]
h4 = df_filter[['Price', 'District']].groupby('District').mean().reset_index()
st.bar_chart(x='District', y='Price', data = h4)

h4_percentual = (h4.loc[1,'Price'] / h4.loc[0,'Price'] -1) * 100

st.write(f'Falso, Apartamentos de 3 quartos em Pinheiros são, em média, {h4_percentual:.2f}% mais caros.')


# Gráficos
st.title('''Relação bairro vs preço por m2''')
df_district = df_sale.groupby("District")[["price_m2"]].mean().reset_index().sort_values(by="price_m2", ascending=False)
fig = px.line(df_district, x="District", y="price_m2")
st.plotly_chart(fig)

# Gráfico mapa
st.title('''Distribuição dos imóveis no mapa''')

fig = px.scatter_mapbox(df_sale, lat="Latitude", lon="Longitude", hover_name="District",hover_data=["Price", "price_m2"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

st.title('''Conclusão dos insights ''')
st.markdown('''H1 - Imóveis com piscina são, em média 56,72 mais caros''')
st.markdown('''H2 - Imóveis na Vila Madalena são, em média, 31.59% mais baratos..''')
st.markdown('''H3 - Imóveis de mais de 100m2 no bairro do Brooklin são, em média, 63.31% mais baratos...''')
st.markdown('''H4 - Apartamentos de 3 quartos em Pinheiros são, em média, 135.04% mais caros....''')

