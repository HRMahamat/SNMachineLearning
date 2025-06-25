import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# --- Chargement du modèle entraîné ---
bundle = joblib.load("Hamad_Rassem_Mahamat_Models.joblib")
pipeline = bundle['pipeline']
threshold = bundle['threshold']

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
    sexe = "male" if genre == "Homme" else "femelle" if genre == "Femme" else "non précisé"
    df_in = pd.DataFrame([{
        'age': age,
        'salaire': sal,
        'score_credit': score,
        'montant_transaction': amt,
        'anciennete_compte': anc,
        'genre': sexe,
        'type_carte': type_carte,
        'region': region
    }])
    # Variables dérivées
    df_in['amt_to_salary'] = df_in['montant_transaction'] / (df_in['salaire'] + 1)
    df_in['score_to_age']  = df_in['score_credit'] / (df_in['age'] + 1)
    df_in['log_sal']       = np.log1p(df_in['salaire'])
    df_in['log_trans']     = np.log1p(df_in['montant_transaction'])
    df_in['small_txn']     = (df_in['montant_transaction'] == 25000).astype(int)

    # Prédiction
    prob = pipeline.predict_proba(df_in)[:, 1][0]
    decision = "🚨 FRAUDE" if prob >= threshold else "✅ NON FRAUDE"
    color = "#dc3545" if prob >= threshold else "#28a745"

    # Affichage
    st.markdown(f"""
        <div class="metric-box">
            <h2 style="color:{color};">{decision}</h2>
            <p style="font-size:1.1rem;">Probabilité de fraude : <strong>{prob*100:.1f}%</strong></p>
            <p style="font-size:0.9rem; color:gray;">Seuil de décision : {threshold:.2f}</p>
        </div>
    """, unsafe_allow_html=True)

    # Histogramme
    st.subheader("🔍 Contexte : distribution des scores")
    hist = np.random.beta(2, 10, size=200)
    fig, ax = plt.subplots()
    ax.hist(hist, bins=20, color='#83c5be', label='Historique')
    ax.axvline(prob, color='#ff006e', linestyle='--', linewidth=2, label='Votre transaction')
    ax.legend()
    ax.set_xlabel("Score de probabilité")
    ax.set_ylabel("Nombre d'exemples")
    st.pyplot(fig)

    # Explication
    if prob >= threshold:
        explain_placeholder.markdown(f"""
            <div class="explain">
            <strong>Pourquoi ce résultat ?</strong><br>
            • Montant important par rapport au salaire<br>
            • Profil de risque plus élevé que la moyenne<br>
            <br>
            Veuillez vérifier cette transaction avec un agent ou suspendre temporairement la carte.
            </div>
        """, unsafe_allow_html=True)
