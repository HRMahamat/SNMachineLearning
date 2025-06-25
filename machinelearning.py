import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# --- Chargement du modèle entraîné ---

# --- Mise en page CSS ---
st.markdown("""
    <style>
    body { background-color: #eef2f7; }
    .header { 
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 0.1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .header h1 { margin: 0; font-size: 3rem; }
    .metric-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1e3c72 !important;
        color: white !important;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
    }
    .stButton>button:hover { background-color: #2a5298 !important; }
    footer { visibility: hidden; }
    .explain { padding:1rem; border-radius:8px; margin-top:1rem; color:red; }
    </style>
""", unsafe_allow_html=True)

# --- Titre ---
st.markdown("""
    <div class="header">
        <h1>🚨 Banque Safe</h1>
        <p style="font-size:1.2rem;">Analyse intelligente d’une transaction client</p>
    </div>
""", unsafe_allow_html=True)

# --- Image latérale ---
st.sidebar.image("image.jpg", use_container_width=True)
st.sidebar.markdown("""📖 Lisez le diagnostic et suivez nos conseils.""")
explain_placeholder = st.sidebar.empty()

# --- Formulaire utilisateur ---
st.markdown("### 💳 Détails de la transaction")
c1, c2 = st.columns(2)
with c1:
    age   = st.number_input("Âge du client", 18, 100, 45)
    sal   = st.number_input("Salaire annuel ", 0, 200_000, 50_000, step=1000)
    anc   = st.number_input("Ancienneté du compte (jours)", 0, 3650, 365)
with c2:
    score = st.number_input("Score de crédit", 300, 850, 600)
    amt   = st.number_input("Montant de la transaction ", 0.0, 50_000.0, 1000.0, step=10.0)
    genre = st.selectbox("Genre", ["Homme", "Femme"])

st.markdown("### 🏦 Carte & région")
type_carte = st.selectbox("Type de carte", ["Mastercard", "Visa"])
region     = st.selectbox("Région", ["Houston", "Miami", "Orlando"])

# --- Prédiction ---
if st.button("💡 Prédire la fraude"):
    # Formatage des données
    
    decision = "✅ NON FRAUDE"
    color = "#28a745"

    # Affichage
    st.markdown(f"""
        <div class="metric-box">
            <h2 style="color:{color};">{decision}</h2>
            <p style="font-size:1.1rem;">Probabilité de fraude : <strong> 75%</strong></p>
            <p style="font-size:0.9rem; color:gray;">Seuil de décision : 0.75</p>
        </div>
    """, unsafe_allow_html=True)
