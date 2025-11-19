import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Data Science - Mario Project",
    page_icon="🍄",
    layout="wide"
)

# CSS personnalisé pour reproduire le style Mario
st.markdown("""
<style>
    /* Variables de couleurs Mario */
    :root {
        --color-mario: #E52521;
        --color-luigi: #00A651;
        --color-yoshi: #6DBE47;
        --color-peach: #FF8FAB;
        --color-toad: #0066B3;
    }
    
    /* Style général */
    .main {
        background-color: #FCF9F3;
    }
    
    /* Cartes personnalisées */
    .mario-card {
        background-color: white;
        border: 3px solid var(--color-mario);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    
    .luigi-card {
        background-color: white;
        border: 3px solid var(--color-luigi);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .yoshi-card {
        background-color: white;
        border: 3px solid var(--color-yoshi);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .peach-card {
        background-color: white;
        border: 3px solid var(--color-peach);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .toad-card {
        background-color: white;
        border: 3px solid var(--color-toad);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .card-icon {
        font-size: 48px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .placeholder-box {
        background-color: rgba(94, 82, 64, 0.05);
        border: 2px dashed rgba(94, 82, 64, 0.3);
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .placeholder-icon {
        font-size: 40px;
        opacity: 0.3;
        margin-bottom: 10px;
    }
    
    .placeholder-text {
        font-size: 14px;
        opacity: 0.5;
        font-weight: 500;
    }
    
    /* Style pour les expanders */
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Data Science – Projet Mario Group</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8; margin-bottom: 40px;'>Sélectionne une section pour explorer les modules. Chaque carte représente une partie du projet.</p>", unsafe_allow_html=True)

# Création des colonnes pour la disposition en grille (2 cartes par ligne sur desktop)
col1, col2 = st.columns(2)

# PARTIE 1: Prévision financière - Mario
with col1:
    st.markdown("""
    <div class="mario-card">
        <div class="card-icon">🍄</div>
        <h3 style="margin: 0;">Partie 1: Prévision financière</h3>
        <p style="font-size: 12px; opacity: 0.6; margin: 5px 0 15px 0;">Mario</p>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
            Module de prévision des tendances financières et analyse prédictive des marchés.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Voir les détails et intégrer le code"):
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">📈</div>
            <div class="placeholder-text">Section à compléter par le membre du groupe</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📝 Zone de code à intégrer :")
        st.info("""
        **Ici, tu pourras ajouter :**
        - 📈 Les graphiques interactifs (Plotly, Matplotlib)
        - 🤖 Les modèles de prévision
        - 📊 Les métriques de performance
        - 💾 Les exports de données
        
        **Exemple de structure :**
        ```
        import plotly.express as px
        # Ton code ici
        fig = px.line(...)
        st.plotly_chart(fig)
        ```
        """)

# PARTIE 2: Optimisation de portefeuille - Luigi
with col2:
    st.markdown("""
    <div class="luigi-card">
        <div class="card-icon">⭐</div>
        <h3 style="margin: 0;">Partie 2: Optimisation de portefeuille</h3>
        <p style="font-size: 12px; opacity: 0.6; margin: 5px 0 15px 0;">Luigi</p>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
            Algorithmes d'optimisation pour maximiser les rendements et minimiser les risques.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Voir les détails et intégrer le code"):
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">💰</div>
            <div class="placeholder-text">Section à compléter par le membre du groupe</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📝 Zone de code à intégrer :")
        st.info("""
        **Ici, tu pourras ajouter :**
        - 📉 Les frontières efficientes
        - 🎯 Les allocations optimales
        - 🔗 Les matrices de corrélation
        - 🎲 Les simulations Monte Carlo
        """)

# Ligne 2
col3, col4 = st.columns(2)

# PARTIE 3: Trading algorithmique - Yoshi
with col3:
    st.markdown("""
    <div class="yoshi-card">
        <div class="card-icon">🥚</div>
        <h3 style="margin: 0;">Partie 3: Trading algorithmique</h3>
        <p style="font-size: 12px; opacity: 0.6; margin: 5px 0 15px 0;">Yoshi</p>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
            Stratégies de trading automatisées et backtesting de signaux de marché.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Voir les détails et intégrer le code"):
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">🤖</div>
            <div class="placeholder-text">Section à compléter par le membre du groupe</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📝 Zone de code à intégrer :")
        st.info("""
        **Ici, tu pourras ajouter :**
        - 📡 Les signaux de trading
        - 📊 Les performances historiques
        - 📐 Les indicateurs techniques
        - 🔄 Les backtests interactifs
        """)

# PARTIE 4: Pricing d'options - Peach
with col4:
    st.markdown("""
    <div class="peach-card">
        <div class="card-icon">👑</div>
        <h3 style="margin: 0;">Partie 4: Pricing d'options</h3>
        <p style="font-size: 12px; opacity: 0.6; margin: 5px 0 15px 0;">Peach</p>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
            Modélisation et valorisation d'instruments dérivés et options financières.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Voir les détails et intégrer le code"):
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">📊</div>
            <div class="placeholder-text">Section à compléter par le membre du groupe</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📝 Zone de code à intégrer :")
        st.info("""
        **Ici, tu pourras ajouter :**
        - 🧮 Les calculateurs d'options
        - ⚫ Les modèles Black-Scholes
        - 🌊 Les surfaces de volatilité
        - 🔤 Les Greeks interactifs (Delta, Gamma, Theta, Vega)
        """)

# Ligne 3 - Centrée
col5, col6, col7 = st.columns([1, 2, 1])

# PARTIE 5: Gestion des risques - Toad
with col6:
    st.markdown("""
    <div class="toad-card">
        <div class="card-icon">🛡️</div>
        <h3 style="margin: 0;">Partie 5: Gestion des risques</h3>
        <p style="font-size: 12px; opacity: 0.6; margin: 5px 0 15px 0;">Toad</p>
        <p style="font-size: 14px; opacity: 0.8; margin-bottom: 20px;">
            Évaluation et mitigation des risques financiers, VaR et stress testing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Voir les détails et intégrer le code"):
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">⚠️</div>
            <div class="placeholder-text">Section à compléter par le membre du groupe</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📝 Zone de code à intégrer :")
        st.info("""
        **Ici, tu pourras ajouter :**
        - 📉 Les calculs de VaR (Value at Risk)
        - 🧪 Les stress tests
        - 🔍 Les analyses de sensibilité
        - 📋 Les tableaux de risques
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; opacity: 0.7; margin-top: 50px;'>
    <p>🎮 Projet Python collaboratif – Interface Mario Dashboard</p>
    <p>Prêt à accueillir le code des 5 membres du groupe</p>
</div>
""", unsafe_allow_html=True)

# Sidebar optionnelle pour navigation future
with st.sidebar:
    st.markdown("### 🎮 Navigation Mario")
    st.markdown("Sélectionne une partie :")
    if st.button("🍄 Partie 1 - Mario"):
        st.info("Prévision financière")
    if st.button("⭐ Partie 2 - Luigi"):
        st.info("Optimisation de portefeuille")
    if st.button("🥚 Partie 3 - Yoshi"):
        st.info("Trading algorithmique")
    if st.button("👑 Partie 4 - Peach"):
        st.info("Pricing d'options")
    if st.button("🛡️ Partie 5 - Toad"):
        st.info("Gestion des risques")
    
    st.markdown("---")
    st.markdown("**💡 Astuce :**")
    st.markdown("Clique sur 'Voir les détails' pour déplier chaque section et voir où intégrer le code !")
