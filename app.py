# =====================================
# IMPORTACIÓN DE LIBRERÍAS
# =====================================

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================
# SESSION STATE
# =====================================

if "data" not in st.session_state:
    st.session_state.data = None

if "nombre_archivo" not in st.session_state:
    st.session_state.nombre_archivo = None

# =====================================
# CONFIGURACIÓN GENERAL
# =====================================

st.title("Proyecto Final Diploma BI")

st.sidebar.title("Parámetros")

st.image("python.png", width=500)

st.sidebar.image("dmc.png", width=100)

st.write("Elaborado por: Yaneri Martínez")

# =====================================
# MENÚ PRINCIPAL
# =====================================

modulos = st.sidebar.selectbox(
    "Seleccione un módulo",
    [
        "Home",
        "Carga y perfil del dataset",
        "Procesamiento de datos",
        "Análisis visual"
    ]
)

# =====================================
# HOME
# =====================================

if modulos == "Home":

    st.header("Bienvenido a la aplicación")

    st.write("""
    Esta aplicación permite cargar, procesar y analizar
    datasets utilizando Streamlit y Python.
    """)

    if st.session_state.data is not None:
        st.success(
            f"Dataset cargado: {st.session_state.nombre_archivo}"
        )
    else:
        st.info(
            "Aún no se ha cargado ningún dataset."
        )

# =====================================
# CARGA Y PERFIL DEL DATASET
# =====================================

elif modulos == "Carga y perfil del dataset":

    st.subheader("Carga y perfil del dataset")

    archivo = st.file_uploader(
        "Cargue el archivo Excel o CSV",
        type=["csv", "xlsx"]
    )

    if archivo is not None:

        st.session_state.nombre_archivo = archivo.name

        if archivo.name.endswith(".csv"):

            st.session_state.data = pd.read_csv(archivo)

        elif archivo.name.endswith(".xlsx"):

            st.session_state.data = pd.read_excel(archivo)

        else:

            st.error("Formato no válido")

        st.success("Archivo cargado correctamente")

    if st.session_state.data is not None:

        data = st.session_state.data

        st.write(
            f"Archivo actual: **{st.session_state.nombre_archivo}**"
        )

        st.subheader("Vista previa")

        st.dataframe(data.head())

        st.subheader("Perfil básico")

        st.write("Filas:", data.shape[0])

        st.write("Columnas:", data.shape[1])

        st.write("Columnas del dataset:")

        st.write(data.columns.tolist())

        st.write("Tipos de datos:")

        st.write(data.dtypes)

        st.write("Valores nulos:")

        st.write(data.isnull().sum())

        st.write("Estadística descriptiva:")

        st.write(data.describe(include="all"))

        if st.button("Eliminar dataset cargado"):

            st.session_state.data = None

            st.session_state.nombre_archivo = None

            st.rerun()

    else:

        st.info("Por favor cargue un archivo.")

# =====================================
# PROCESAMIENTO DE DATOS
# =====================================

elif modulos == "Procesamiento de datos":

    st.subheader("Procesamiento de datos")

    if st.session_state.data is not None:

        data = st.session_state.data

        st.write("Dataset disponible")

        st.dataframe(data.head())

        st.subheader("Valores nulos")

        st.write(data.isnull().sum())

        st.subheader("Duplicados")

        st.write(data.duplicated().sum())

        st.subheader("Tipos de datos")

        st.write(data.dtypes)

    else:

        st.warning(
            "Primero debe cargar un dataset."
        )

# =====================================
# ANÁLISIS VISUAL
# =====================================

elif modulos == "Análisis visual":

    st.subheader("Análisis visual")

    if st.session_state.data is not None:

        data = st.session_state.data

        st.write("Dataset disponible para análisis")

        st.dataframe(data.head())

        lista_columna_numerica = data.select_dtypes(
            include="number"
        ).columns.tolist()

        lista_columna_categorica = data.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if len(lista_columna_numerica) == 0:

            st.warning("No existen columnas numéricas.")

        else:

            variable_numerica = st.selectbox(
                "Seleccione la columna numérica",
                lista_columna_numerica
            )

            if len(lista_columna_categorica) > 0:

                variable_categorica = st.selectbox(
                    "Seleccione la columna categórica",
                    lista_columna_categorica
                )

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Distribución",
                    "Comparación",
                    "Correlación",
                    "Conclusiones"
                ]
            )

            with tab1:

                st.subheader("Histograma")

                fig = px.histogram(
                    data,
                    x=variable_numerica
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("Boxplot")

                fig2 = px.box(
                    data,
                    y=variable_numerica
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            with tab2:

                if len(lista_columna_categorica) > 0:

                    fig3 = px.box(
                        data,
                        x=variable_categorica,
                        y=variable_numerica
                    )

                    st.plotly_chart(
                        fig3,
                        use_container_width=True
                    )

            with tab3:

                if len(lista_columna_numerica) > 1:

                    corr = data[
                        lista_columna_numerica
                    ].corr()

                    fig4, ax = plt.subplots(
                        figsize=(8,5)
                    )

                    sns.heatmap(
                        corr,
                        annot=True,
                        cmap="coolwarm",
                        ax=ax
                    )

                    st.pyplot(fig4)

            with tab4:

                st.subheader("Conclusiones")

                st.write(
                    f"La variable analizada es {variable_numerica}."
                )

                st.write(
                    "El histograma muestra la distribución de los datos."
                )

                st.write(
                    "El boxplot permite identificar posibles valores atípicos."
                )

                st.write(
                    "El mapa de calor muestra la relación entre variables numéricas."
                )

    else:

        st.warning(
            "Primero debe cargar un dataset en el módulo "
            "'Carga y perfil del dataset'."
        )
