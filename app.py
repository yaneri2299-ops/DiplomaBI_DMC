import streamlit as st

st.title("Proyecto Final Diploma BI")

st.sidebar.title("Parámetros")

st.image("python.png",width=500)
st.sidebar.image("dmc.png",width=300)

st.write("Elaborado por Yaneri Martinez")

archivo = st.file_uploader("Cargue el archivo excel o csv")

if archivo is not None :
    
    if archivo.name.endswith(".csv"):
        data = pd.read_csv(archivo)
      st.write(data)

    elif archivo.name.endswith(".xlsx")
        data =pd.read_excel(archivo)
      st.write(data)
    else:
      st.write("Formato no válido")



else :
    st.write ("Por favor cargue su archivo")
  
