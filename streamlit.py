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
st.title("📊 Étude des indices boursiers sous les présidences françaises 🇫🇷")
st.markdown("""
Bienvenue dans cette étude interactive des **performances d'indices boursiers** sous différents présidents français.
Explore la performance, la volatilité et la distribution des rendements mensuels.
""")

# 🧑‍💼 Paramètres
presidents = {
    'Jacques Chirac': {'start': '1995-01-01', 'end': '2006-12-31', 'color': 'blue'},
    'Nicolas Sarkozy': {'start': '2007-01-01', 'end': '2011-12-31', 'color': 'green'},
    'François Hollande': {'start': '2012-01-01', 'end': '2016-12-31', 'color': 'orange'},
    'Emmanuel Macron': {'start': '2017-01-01', 'end': '2024-12-31', 'color': 'red'}
}

# Sidebar
st.sidebar.header("⚙️ Paramètres de l’étude")
ticker_options = {
    "CAC40 (^FCHI)": "^FCHI",
    "S&P500 (^GSPC)": "^GSPC",
    "Nasdaq (^IXIC)": "^IXIC",
    "DAX (^GDAXI)": "^GDAXI"
}
selected_index = st.sidebar.selectbox("Choisir l'indice boursier :", list(ticker_options.keys()))
ticker = ticker_options[selected_index]

interval = st.sidebar.selectbox("Fréquence :", ["1mo", "1wk", "1d"], index=0)
st.sidebar.markdown("---")
st.sidebar.info("💡 Conseil : sélectionne un indice pour analyser ses performances selon les présidences.")

# 📦 Téléchargement et analyses
assets = {}
summary_stats = []

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
f_stat = float(anova.statistic) if hasattr(anova.statistic, "__len__") else anova.statistic
p_val = float(anova.pvalue) if hasattr(anova.pvalue, "__len__") else anova.pvalue

st.write(f"**F-statistic:** {f_stat:.3f} | **p-value:** {p_val:.3f}")
if anova.pvalue <= 0.05:
    st.success("✅ Différence significative de rendement moyen entre au moins deux présidents.")
else:
    st.warning("⚠️ Aucune différence significative de rendement moyen entre les présidences.")

# 📊 Visualisation synthétique des rendements moyens
st.header("📉 Moyenne des rendements mensuels par président")
fig_bar = px.bar(
    df_summary,
    x='President',
    y='Mean Return',
    color='President',
    title=f'📊 Rendement mensuel moyen par président ({selected_index})'
)
fig_bar.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_bar.update_layout(yaxis_tickformat=".2%", xaxis_title=None, yaxis_title="Rendement moyen")
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

    # Interactive distribution
    fig_dist = ff.create_distplot([returns.tolist()], [selected_president], show_hist=False, show_rug=False)
    fig_dist.update_layout(title=f'🌍 Distribution interactive - {selected_president}', xaxis_title='Rendement mensuel')
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    st.markdown(f"### 📉 Volatilité glissante sur 12 mois ({selected_president})")
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(returns.rolling(window=12).std(), color=info['color'])
    ax.set_title(f'Volatilité rolling 12 mois - {selected_president}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volatilité')
    st.pyplot(fig)

    # Interactive rolling volatility
    rolling_vol = returns.rolling(window=12).std()
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol, mode='lines', name=selected_president, line=dict(color=info['color'])))
    fig_vol.update_layout(title=f'📉 Volatilité interactive - {selected_president}', xaxis_title='Date', yaxis_title='Volatilité')
    st.plotly_chart(fig_vol, use_container_width=True)

# 📊 Distribution interactive globale
returns_list = [list(assets[p]) for p in presidents]
labels = list(presidents.keys())
filtered_returns_list = []
filtered_labels = []
for r, label in zip(returns_list, labels):
    if len(r) >= 2:
        filtered_returns_list.append(r)
        filtered_labels.append(label)
if filtered_returns_list:
    fig_dist_global = ff.create_distplot(filtered_returns_list, filtered_labels, show_hist=False, show_rug=False)
    fig_dist_global.update_layout(title=f'🌍 Distribution interactive globale ({selected_index})', xaxis_title='Rendement mensuel')
    st.plotly_chart(fig_dist_global, use_container_width=True)

# 📊 Volatilité glissante interactive
st.header("📉 Volatilité glissante (12 mois) - Comparaison globale")
fig_vol_global = go.Figure()
for name, info in presidents.items():
    rolling_vol = assets[name].rolling(window=12).std()
    fig_vol_global.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol, mode='lines', name=name, line=dict(color=info['color'])))
fig_vol_global.update_layout(title=f'Volatilité glissante globale ({selected_index})', xaxis_title='Date', yaxis_title='Volatilité')
st.plotly_chart(fig_vol_global, use_container_width=True)

# Analyse détaillée et conclusion
best_president = df_summary.loc[df_summary['Total Performance'].idxmax(), 'President']
best_perf = df_summary['Total Performance'].max()

st.header("📖 Analyse et conclusion")
analyse_text = f"""
### Analyse détaillée par président

#### Jacques Chirac (1995-2006, bleu)
- Croissance globalement stable.
- La bulle internet provoque des pics de volatilité et rendements négatifs ponctuels.

#### Nicolas Sarkozy (2007-2011, vert)
- Rendements plus faibles et volatilité élevée.
- Crise financière de 2008 visible : chute brutale du CAC40.

#### François Hollande (2012-2016, orange)
- Rendements moyens légèrement positifs, fluctuations modérées.

#### Emmanuel Macron (2017-2024, rouge)
- Début de mandat en forte hausse.
- Crises ponctuelles : Covid-19 et crise énergétique, pics de volatilité.

---

### Conclusion générale
- Les rendements moyens ne montrent pas toujours de différences significatives, mais les graphiques révèlent la dynamique réelle.
- Les périodes de crise (dotcom, 2008, Covid-19, énergie) sont les principaux facteurs de volatilité.
- **Le président ayant le mieux performé est {best_president} avec une performance totale de {best_perf:.2%}.**
- L’étude montre que l’analyse visuelle et interactive complète les statistiques classiques, permettant de comprendre le contexte macroéconomique et son impact sur le marché.

📚 *Source des données : Yahoo Finance. Visualisations interactives réalisées avec Plotly.*
"""
st.markdown(analyse_text)
