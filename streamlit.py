# app.py 🚀
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

# 🎨 Configuration de la page
st.set_page_config(page_title="Analyse du CAC40 par Président 🇫🇷", layout="wide", page_icon="📈")

# 🧭 Titre principal
st.title("📊 Étude du CAC40 sous les présidences françaises 🇫🇷")
st.markdown("""
Bienvenue dans cette étude interactive des **performances du CAC40** sous différents présidents français.
Nous allons explorer la performance, la volatilité et la distribution des rendements mensuels sur la période 1995-2024.
""")

# 🧑‍💼 Paramètres
presidents = {
    'Jacques Chirac': {'start': '1995-01-01', 'end': '2006-12-31', 'color': 'blue'},
    'Nicolas Sarkozy': {'start': '2007-01-01', 'end': '2011-12-31', 'color': 'green'},
    'François Hollande': {'start': '2012-01-01', 'end': '2016-12-31', 'color': 'orange'},
    'Emmanuel Macron': {'start': '2017-01-01', 'end': '2024-12-31', 'color': 'red'}
}

# 📦 Téléchargement et analyses
assets = {}
summary_stats = []

st.sidebar.header("⚙️ Paramètres de l’étude")
ticker = st.sidebar.text_input("Indice boursier :", "^FCHI", help="Par défaut : CAC40 (^FCHI)")
interval = st.sidebar.selectbox("Fréquence :", ["1mo", "1wk", "1d"], index=0)

st.sidebar.markdown("---")
st.sidebar.info("💡 Conseil : tu peux modifier le ticker pour analyser un autre indice (ex: ^GSPC pour le S&P 500).")

# 🔄 Téléchargement et calcul des rendements
for name, info in presidents.items():
    with st.spinner(f"Chargement des données pour {name}..."):
        data = yf.download(ticker, start=info['start'], end=info['end'], interval=interval)['Close']

        # Assurer que data est une Series
        if isinstance(data, pd.DataFrame):
            data = data.squeeze()
        
        returns = data.pct_change().dropna()
        vol = returns.std()
        mean = returns.mean()
        perf = ((data.iloc[-1] / data.iloc[0]) - 1)
        sharpe = mean / vol
        skew = returns.skew()
        kurt = returns.kurt()
        normal = stats.shapiro(returns)

        summary_stats.append({
            'President': name,
            'Mean Return': mean,
            'Volatility': vol,
            'Total Performance': perf,
            'Sharpe Ratio': sharpe,
            'Skewness': skew,
            'Kurtosis': kurt,
            'Normality p-value': normal.pvalue
        })

        assets[name] = returns

# 🧾 Résumé statistique
df_summary = pd.DataFrame(summary_stats)
st.header("📈 Résumé statistique global")
st.dataframe(df_summary.round(4), use_container_width=True)

# 🧪 Comparaisons statistiques
anova = stats.f_oneway(*[assets[p] for p in presidents if not assets[p].empty])

f_stat = float(anova.statistic)
p_val = float(anova.pvalue)

st.write(f"**F-statistic:** {f_stat:.3f} | **p-value:** {p_val:.3f}")
if p_val <= 0.05:
    st.success("✅ Différence significative de rendement moyen entre au moins deux présidents.")
else:
    st.warning("⚠️ Aucune différence significative de rendement moyen entre les présidences.")

# 📊 Graphique moyenne des rendements
st.header("📉 Moyenne des rendements mensuels par président")

# Créer colonne 'Mean Return Value' pour Plotly
df_summary['Mean Return Value'] = df_summary['Mean Return']

fig_bar = px.bar(
    df_summary,
    x='President',
    y='Mean Return Value',
    color='President',
    title='📊 Rendement mensuel moyen par président 🇫🇷'
)
fig_bar.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_bar.update_layout(yaxis_tickformat=".2%", xaxis_title=None, yaxis_title="Rendement moyen")
st.plotly_chart(fig_bar, use_container_width=True)

# 🔍 Détails par président (avec graphiques interactifs)
st.header("🔎 Détails par président interactifs")
selected_president = st.selectbox("Choisir un président :", list(presidents.keys()))

returns = assets[selected_president]
color = presidents[selected_president]['color']

# Histogramme interactif
fig_hist = px.histogram(
    returns,
    nbins=20,
    title=f'📦 Distribution des rendements mensuels - {selected_president}',
    labels={'value': 'Rendement mensuel'},
    color_discrete_sequence=[color]
)
fig_hist.update_layout(yaxis_title='Fréquence', xaxis_title='Rendement mensuel')
st.plotly_chart(fig_hist, use_container_width=True)

# Volatilité rolling 12 mois interactive
rolling_vol = returns.rolling(window=12).std()
fig_vol_pres = go.Figure()
fig_vol_pres.add_trace(go.Scatter(
    x=rolling_vol.index,
    y=rolling_vol.values,
    mode='lines+markers',
    name=f'Volatilité {selected_president}',
    line=dict(color=color)
))
fig_vol_pres.update_layout(
    title=f'📉 Volatilité glissante 12 mois - {selected_president}',
    xaxis_title='Date',
    yaxis_title='Volatilité'
)
st.plotly_chart(fig_vol_pres, use_container_width=True)

# 📊 Distribution interactive globale
returns_list = [assets[p].values.tolist() for p in presidents if not assets[p].empty]
labels = [p for p in presidents if not assets[p].empty]

if returns_list:
    fig_dist = ff.create_distplot(returns_list, labels, show_hist=False, show_rug=False)
    fig_dist.update_layout(title='🌍 Distribution des rendements mensuels par président', xaxis_title='Rendement mensuel')
    st.plotly_chart(fig_dist, use_container_width=True)
else:
    st.warning("⚠️ Pas assez de données pour créer le graphique de distribution.")

# 📊 Volatilité glissante interactive
st.header("📉 Volatilité glissante (12 mois)")
fig_vol = go.Figure()
for name in presidents:
    if not assets[name].empty:
        rolling_vol = assets[name].rolling(window=12).std()
        fig_vol.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol.values, mode='lines', name=name, line=dict(color=presidents[name]['color'])))

fig_vol.update_layout(title='Volatilité glissante sur 12 mois - Comparaison par président', xaxis_title='Date', yaxis_title='Volatilité')
st.plotly_chart(fig_vol, use_container_width=True)

# ✍️ Conclusion
st.markdown("""
---
### 🧠 Conclusion
Cette étude met en lumière les différences de performance et de volatilité du **CAC40** selon les présidences françaises 🇫🇷.  
Même si certaines périodes présentent des variations marquées, **les différences statistiques ne sont pas toujours significatives**.  

📚 *Source des données : Yahoo Finance*
""")
