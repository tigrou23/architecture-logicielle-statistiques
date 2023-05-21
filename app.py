import pandas as pd
import streamlit as st
import mysql.connector
import warnings
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

st.title("Statistiques sur la bibliothèque \U0001F4D6")

tab_titles = [
    "Réservations",
    "Emprunts"
]

tabs = st.tabs(tab_titles)

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

cursor = conn.cursor()

warnings.filterwarnings('ignore', category=UserWarning)

# Récupérer les données
df_document = pd.read_sql("SELECT * FROM document", conn)
df_emprunt = pd.read_sql("SELECT * FROM emprunter_histo", conn)
df_abonne = pd.read_sql("SELECT * FROM abonne", conn)
df_reservation = pd.read_sql("SELECT * FROM reserver_histo", conn)

df_emprunt = df_emprunt.merge(df_document, left_on='ID_document', right_on='ID_document')
df_reservation = df_reservation.merge(df_document, left_on='ID_document', right_on='ID_document')
df_emprunt = df_emprunt.merge(df_abonne, left_on='ID_abonne', right_on='ID_abonne')
df_reservation = df_reservation.merge(df_abonne, left_on='ID_abonne', right_on='ID_abonne')

warnings.filterwarnings('default')

conn.close()

with tabs[0]:
    
    st.markdown("## Données générales")
    documentLePlusUtilise = df_reservation['titre'].mode()[0]
    col1, col2 = st.columns(2)
    col1.metric("Nombre de réservations effectuées : ", str(df_reservation.size), '4%')
    col2.metric("Document le plus réservé : ", documentLePlusUtilise)

    st.markdown("## Histogramme des réservations")
    st.markdown('- axe x : Titre des documents')
    st.markdown("- axe y : Nombre de réservations")
    st.bar_chart(df_reservation['titre'].value_counts())


    st.markdown("## Répartition des des âges")
    aujourdhui = pd.Timestamp.today().normalize()  # Récupérer la date d'aujourd'hui
    df_reservation['DateNais'] = pd.to_datetime(df_reservation['DateNais'])
    df_reservation['Age'] = ((aujourdhui - df_reservation['DateNais']) / pd.Timedelta(days=365)).astype(int)
    nombre_adultes = df_reservation[df_reservation['Age'] >= 18].shape[0]
    nombre_enfants = df_reservation[df_reservation['Age'] < 18].shape[0]
    labels = ['Adultes', 'Enfants']
    sizes = [nombre_adultes, nombre_enfants]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

with tabs[1]:
        
    st.markdown("## Données générales")
    documentLePlusUtilise = df_emprunt['titre'].mode()[0]
    col1, col2 = st.columns(2)
    col1.metric("Nombre d'emprunts effectuées : ", str(df_emprunt.size), '-10%')
    col2.metric("Document le plus emprunté : ", documentLePlusUtilise)

    st.markdown("## Histogramme des emprunts")
    st.markdown('- axe x : Titre des documents')
    st.markdown("- axe y : Nombre d'emprunts")
    st.bar_chart(df_emprunt['titre'].value_counts())

    st.markdown("## Répartition des âges")
    aujourdhui = pd.Timestamp.today().normalize()  # Récupérer la date d'aujourd'hui
    df_emprunt['DateNais'] = pd.to_datetime(df_emprunt['DateNais'])
    df_emprunt['Age'] = ((aujourdhui - df_emprunt['DateNais']) / pd.Timedelta(days=365)).astype(int)
    nombre_adultes = df_emprunt[df_emprunt['Age'] >= 18].shape[0]
    nombre_enfants = df_emprunt[df_emprunt['Age'] < 18].shape[0]
    labels = ['Adultes', 'Enfants']
    sizes = [nombre_adultes, nombre_enfants]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)



