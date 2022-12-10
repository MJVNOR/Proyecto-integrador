import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

st.set_page_config(
    page_title="Proyecto Integrador",
    page_icon="🤘",
    layout="wide",
)

st.title("Proyecto Integrador")
st.subheader(
    "Relación entre el presupuesto en educación de Sonora vs la cantidad de estudiantes matriculados en educación superior en los municipios de Sonora"
)
col1, col2 = st.columns(2)
municipios_son = json.load(open("./son-municipal.geojson", "r"))

# Data a un DataFrame
df_presupuesto = pd.read_csv("./PresupuestoEduSonora.csv")
df_estudiantes_matriculados = pd.read_csv("./CantidadEstudiantesEduSuperior.csv")
# Hacemos una copia para no modificar la data original
df_presupuesto_tidy = df_presupuesto.copy()
df_estudiantes_matriculados_tidy = df_estudiantes_matriculados.copy()

# Creamos una columna con la informacion de la inflacion para poder sacar el presupuesto basado en la inflación.
df_presupuesto_tidy["Amount Executed whit inflation 2021"] = [
    4927965126.63,
    5620885256.43,
    5882068944.27,
    6414849338.70,
    6779900503.00,
]


# Seleccionamos la informacion requerida del dataset df_presupuesto_tidy
df_presupuesto_tidy = df_presupuesto_tidy[
    ["Year", "Amount Executed whit inflation 2021"]
]
df_presupuesto_tidy["Year"] = pd.to_datetime(df_presupuesto_tidy["Year"], format="%Y")
df_presupuesto_tidy.head()

# Seleccionamos la informacion requerida del dataset df_estudiantes_matriculados_tidy
df_estudiantes_matriculados_tidy["Year"] = pd.to_datetime(
    df_estudiantes_matriculados_tidy["Year"], format="%Y"
)
df_estudiantes_matriculados_tidy.head()

# Convinamos nuestros dos df's y convertidos la columna Year a type period
tidyDf = pd.merge(
    df_presupuesto_tidy.assign(grouper=df_presupuesto_tidy["Year"].dt.to_period("2Y")),
    df_estudiantes_matriculados_tidy.assign(
        grouper=df_estudiantes_matriculados_tidy["Year"].dt.to_period("2Y")
    ),
    how="left",
    on="grouper",
)
tidyDf = tidyDf.drop(columns=["Year_x", "Year_y", "State", "State ID"])

tidyDf["Municipality"].value_counts().reset_index().to_csv("df.csv")
ciudades = pd.read_csv("./df.csv")
ciudades = ciudades["index"]
ciudades = ciudades.to_numpy()

with col1:
    option = st.selectbox("Seleccione la ciudad", ciudades)

    st.write("You selected:", option)
    sonora_city = tidyDf[tidyDf.Municipality == option]
    fig = px.bar(
        sonora_city,
        x=sonora_city.grouper.astype(str),
        y="Students",
        color="Students",
        color_continuous_scale=px.colors.sequential.Blues,
    )
    fig.update_layout(
        title="Cantidad de estudiantes matriculados por año en {}".format(option),
        xaxis_title="Años",
        yaxis_title="Cantidad de estudiantes matriculados",
    )
    st.plotly_chart(fig, use_container_width=True)

    sonora_city = tidyDf[tidyDf.Municipality == option]
    sonora_city["grouper"] = sonora_city["grouper"].astype(str).copy()
    cormat = sonora_city.corr()
    fig = px.imshow(cormat, color_continuous_scale=px.colors.sequential.Blues)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.text("  ")
    st.text("  ")
    st.text("  ")
    st.text("  ")
    st.text("  ")
    st.text("  ")
    st.text("  ")
    st.text("  ")

    fig = px.bar(
        df_presupuesto_tidy,
        x="Year",
        y="Amount Executed whit inflation 2021",
        title="Presupuesto Anual",
        color="Amount Executed whit inflation 2021",
        color_continuous_scale=px.colors.sequential.Blues,
    )
    st.plotly_chart(fig, use_container_width=True)


st.subheader(
    "En el municipio de {} hay una correlación del {}% entre el presupuesto del estado y la cantidad de alumnos de educación superior matriculados".format(
        option, str(cormat.iloc[0, -1])
    )
)
