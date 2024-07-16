# main.py

import streamlit as st
import pandas as pd
from data_handler import cargar_datos, guardar_datos, agregar_libro, eliminar_libro, buscar_libro, listar_libros
from utils import add_bg_from_local
from config import COLUMNS, CSV_FILE

# Inicializar un DataFrame con los datos del archivo CSV
df = cargar_datos(CSV_FILE)

# Inyectar CSS para la imagen de fondo
add_bg_from_local()

# Título de la aplicación
st.markdown('<h1 style="color: blue;">Inventario de Libros</h1>', unsafe_allow_html=True)
# Menú de opciones
menu = ['Agregar libro', 'Eliminar libro', 'Buscar libro', 'Listar libros']
choice = st.sidebar.selectbox('Menú', menu)

# Botón para descargar el archivo CSV
csv = df.to_csv(index=False).encode()
st.sidebar.download_button(
    label="Descargar archivo",
    data=csv,
    file_name='inventario_libros.csv',
    mime='text/csv'
)

# Cargar un archivo CSV
uploaded_file = st.sidebar.file_uploader("Subir un archivo CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['ISBN'] = df['ISBN'].astype(str)  # Asegurarse de que ISBN sea una cadena
    guardar_datos(df, CSV_FILE)
    st.success("Archivo subido y datos cargados correctamente.")

if choice == 'Agregar libro':
    st.subheader('Agregar un nuevo libro')
    with st.form(key='form_agregar'):
        titulo = st.text_input('<label style="color: #FFFDD0;">Título</label>')
        autor = st.text_input('Autor')
        anio = st.number_input('Año', min_value=0, step=1)
        genero = st.text_input('Género')
        isbn = st.text_input('ISBN')
        submit_button = st.form_submit_button(label='Agregar libro')
        
        if submit_button:
            if titulo and autor and genero and isbn:  # Validación de entradas
                df = agregar_libro(df, titulo, autor, anio, genero, isbn)
                st.success(f"Libro '{titulo}' agregado al inventario.")
                st.dataframe(df)
            else:
                st.error("Todos los campos son obligatorios para agregar un libro.")

elif choice == 'Eliminar libro':
    st.subheader('Eliminar un libro')
    with st.form(key='form_eliminar'):
        isbn = st.text_input('ISBN del libro a eliminar')
        submit_button = st.form_submit_button(label='Eliminar libro')
        
        if submit_button:
            if isbn:  # Validación de entrada
                df = eliminar_libro(df, isbn)
                st.success(f"Libro con ISBN '{isbn}' eliminado del inventario.")
                st.dataframe(df)
            else:
                st.error("El ISBN es obligatorio para eliminar un libro.")

elif choice == 'Buscar libro':
    st.subheader('Buscar un libro')
    with st.form(key='form_buscar'):
        opciones_busqueda = ['Título', 'Autor', 'ISBN']
        campo = st.selectbox('Buscar por', opciones_busqueda)
        valor = st.text_input(f'Ingrese {campo.lower()} del libro a buscar')
        submit_button = st.form_submit_button(label='Buscar libro')
        
        if submit_button:
            if valor:  # Validación de entrada
                resultado = buscar_libro(df, campo, valor)
                if not resultado.empty:
                    st.write("Libro(s) encontrado(s):")
                    st.dataframe(resultado)
                else:
                    st.warning(f"No se encontraron libros con {campo.lower()} '{valor}'.")
            else:
                st.error(f"El {campo.lower()} es obligatorio para buscar un libro.")

elif choice == 'Listar libros':
    st.subheader('Listado de libros en el inventario')
    if df.empty:
        st.warning("No hay libros en el inventario.")
    else:
        st.dataframe(df)
