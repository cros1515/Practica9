# data_handler.py

import os
import pandas as pd
from config import COLUMNS, CSV_FILE

def cargar_datos(csv_file=CSV_FILE):
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        df = pd.read_csv(csv_file)
        df['ISBN'] = df['ISBN'].astype(str)  # Asegurarse de que ISBN sea una cadena
        return df
    else:
        return pd.DataFrame(columns=COLUMNS)

def guardar_datos(df, csv_file=CSV_FILE):
    df.to_csv(csv_file, index=False)

def agregar_libro(df, titulo, autor, anio, genero, isbn):
    nuevo_libro = pd.DataFrame([[titulo, autor, anio, genero, isbn]], columns=COLUMNS)
    df = pd.concat([df, nuevo_libro], ignore_index=True)
    guardar_datos(df, csv_file)
    return df

def eliminar_libro(df, isbn):
    df = df[df['ISBN'] != isbn]
    guardar_datos(df, csv_file)
    return df

def buscar_libro(df, campo, valor):
    return df[df[campo].str.contains(valor, case=False, na=False)]

def listar_libros(df):
    return df
