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

for name, info in presidents.items():
    with st.spinner(f"Chargement des données pour {name}..."):
        data = yf.download(ticker, start=info['start'], end=info['end'], interval=interval)['Close']
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
anova = stats.f_oneway(*[assets[p] for p in presidents])
st.subheader("📊 Test ANOVA entre les présidences")
st.write(f"**F-statistic:** {anova.statistic:.3f} | **p-value:** {anova.pvalue:.3f}")
if anova.pvalue <= 0.05:
    st.success("✅ Différence significative de rendement moyen entre au moins deux présidents.")
else:
    st.warning("⚠️ Aucune différence significative de rendement moyen entre les présidences.")

# 📊 Visualisation synthétique des rendements moyens
st.header("📉 Moyenne des rendements mensuels par président")
fig_bar = px.bar(df_summary, x='President', y='Mean Return',
                 color='President', title="Rendement mensuel moyen par président 🇫🇷",
                 text_auto='.2%')
st.plotly_chart(fig_bar, use_container_width=True)

# 🔍 Détails par président
st.header("🔎 Détails par président")
selected_president = st.selectbox("Choisir un président :", list(presidents.keys()))

info = presidents[selected_president]
returns = assets[selected_president]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 📦 Distribution des rendements mensuels ({selected_president})")
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.hist(returns, bins=20, color=info['color'], alpha=0.7)
    ax.set_title(f'Distribution des rendements mensuels - {selected_president}')
    ax.set_xlabel('Rendement mensuel')
    ax.set_ylabel('Fréquence')
    st.pyplot(fig)

with col2:
    st.markdown(f"### 📉 Volatilité glissante sur 12 mois ({selected_president})")
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(returns.rolling(window=12).std(), color=info['color'])
    ax.set_title(f'Volatilité rolling 12 mois - {selected_president}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volatilité')
    st.pyplot(fig)

# 📈 Distribution interactive globale
st.header("🌍 Distribution interactive des rendements")
returns_list = [assets[p] for p in presidents]
labels = list(presidents.keys())

fig_dist = ff.create_distplot(returns_list, labels, show_hist=False, show_rug=False)
fig_dist.update_layout(title='Distribution des rendements mensuels par président')
st.plotly_chart(fig_dist, use_container_width=True)

# 📊 Volatilité glissante interactive
st.header("📉 Volatilité glissante (12 mois)")
fig_vol = go.Figure()
for name, info in presidents.items():
    returns = assets[name]
    rolling_volatility = returns.rolling(window=12).std()
    fig_vol.add_trace(go.Scatter(x=rolling_volatility.index, y=rolling_volatility, mode='lines', name=name, line=dict(color=info['color'])))

fig_vol.update_layout(
    title='Volatilité glissante sur 12 mois - Comparaison par président',
    xaxis_title='Date',
    yaxis_title='Volatilité'
)
st.plotly_chart(fig_vol, use_container_width=True)

# ✍️ Conclusion
st.markdown("""
---
### 🧠 Conclusion
Cette étude met en lumière les différences de performance et de volatilité du **CAC40** selon les présidences françaises 🇫🇷.  
Même si certaines périodes présentent des variations marquées, **les différences statistiques ne sont pas toujours significatives**.  

📚 *Source des données : Yahoo Finance*
""")
