# app.py 🚀
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
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

# 🧑‍💼 Paramètres des présidents
presidents = {
    'Jacques Chirac': {'start': '1995-01-01', 'end': '2006-12-31', 'color': 'blue'},
    'Nicolas Sarkozy': {'start': '2007-01-01', 'end': '2011-12-31', 'color': 'green'},
    'François Hollande': {'start': '2012-01-01', 'end': '2016-12-31', 'color': 'orange'},
    'Emmanuel Macron': {'start': '2017-01-01', 'end': '2024-12-31', 'color': 'red'}
}

# 📦 Téléchargement et analyses
assets = {}
summary_stats = []

# 🛠 Paramètres Streamlit
st.sidebar.header("⚙️ Paramètres de l’étude")
ticker = st.sidebar.text_input("Indice boursier :", "^FCHI", help="Par défaut : CAC40 (^FCHI)")
interval = st.sidebar.selectbox("Fréquence :", ["1mo", "1wk", "1d"], index=0)
st.sidebar.markdown("---")
st.sidebar.info("💡 Conseil : tu peux modifier le ticker pour analyser un autre indice (ex: ^GSPC pour le S&P 500).")

# 🔄 Téléchargement et calcul des rendements
for name, info in presidents.items():
    with st.spinner(f"Chargement des données pour {name}..."):
        data = yf.download(ticker, start=info['start'], end=info['end'], interval=interval)['Close']
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

# 🧾 Résumé statistique global
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

# 📊 Graphique moyenne des rendements interactif
df_summary['Mean Return Value'] = df_summary['Mean Return']
fig_bar = px.bar(
    df_summary,
    x='President',
    y='Mean Return Value',
    color='President',
    title='📊 Rendement mensuel moyen par président 🇫🇷'
)
fig_bar.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_bar.update_layout(
    yaxis_tickformat=".2%",
    xaxis_title="Président",
    yaxis_title="Rendement moyen"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 🔍 Détails par président
st.header("🔎 Détails par président")
selected_president = st.selectbox("Choisir un président :", list(presidents.keys()))
returns = assets[selected_president]
color = presidents[selected_president]['color']

# Distribution interactive par président
st.markdown(f"### 📦 Distribution des rendements mensuels ({selected_president})")
fig_dist_pres = ff.create_distplot([returns.values.tolist()], [selected_president], show_hist=True, show_rug=False)
fig_dist_pres.update_layout(
    title=f'🌍 Distribution interactive - {selected_president}',
    xaxis_title='Rendement mensuel',
    yaxis_title='Densité'
)
st.plotly_chart(fig_dist_pres, use_container_width=True)

# Volatilité glissante interactive par président
st.markdown(f"### 📉 Volatilité glissante sur 12 mois ({selected_president})")
rolling_vol = returns.rolling(window=12).std()
fig_vol_pres = go.Figure()
fig_vol_pres.add_trace(go.Scatter(
    x=rolling_vol.index,
    y=rolling_vol.values,
    mode='lines',
    name=selected_president,
    line=dict(color=color)
))
fig_vol_pres.update_layout(
    title=f'📉 Volatilité interactive sur 12 mois - {selected_president}',
    xaxis_title='Date',
    yaxis_title='Volatilité'
)
st.plotly_chart(fig_vol_pres, use_container_width=True)

# 📊 Distribution interactive globale
returns_list = [assets[p].values.tolist() for p in presidents if not assets[p].empty]
labels = [p for p in presidents if not assets[p].empty]
if returns_list:
    fig_dist = ff.create_distplot(returns_list, labels, show_hist=False, show_rug=False)
    fig_dist.update_layout(
        title='🌍 Distribution des rendements mensuels par président',
        xaxis_title='Rendement mensuel',
        yaxis_title='Densité'
    )
    st.plotly_chart(fig_dist, use_container_width=True)
else:
    st.warning("⚠️ Pas assez de données pour créer le graphique de distribution.")

# 📊 Volatilité glissante interactive globale
st.header("📉 Volatilité glissante (12 mois)")
fig_vol = go.Figure()
for name in presidents:
    if not assets[name].empty:
        rolling_vol = assets[name].rolling(window=12).std()
        fig_vol.add_trace(go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol.values,
            mode='lines',
            name=name,
            line=dict(color=presidents[name]['color'])
        ))
fig_vol.update_layout(
    title='Volatilité glissante sur 12 mois - Comparaison par président',
    xaxis_title='Date',
    yaxis_title='Volatilité'
)
st.plotly_chart(fig_vol, use_container_width=True)

# ✍️ Analyse détaillée et conclusion
st.header("📖 Analyse détaillée par président et conclusion")

analyse_text = """
### Jacques Chirac (1995-2006, bleu)
- Croissance stable du CAC40 avec pics de volatilité liés à la bulle internet (2000-2002).
- Rendements mensuels concentrés, skewness légèrement négative.

### Nicolas Sarkozy (2007-2011, vert)
- Rendements faibles, volatilité très élevée.
- Crise financière de 2008 très visible : chute brutale et événements extrêmes fréquents.

### François Hollande (2012-2016, orange)
- Rendements moyens positifs, stabilité relative.
- Marché se stabilise après la crise financière avec moins d’extrêmes.

### Emmanuel Macron (2017-2024, rouge)
- Début de mandat marqué par forte hausse, mais crises ponctuelles importantes (Covid-19 2020, crise énergétique 2022).
- Distribution et volatilité montrent l’impact des événements exceptionnels.

---

### 🔹 Conclusion générale
- Les rendements moyens ne montrent pas toujours de différences statistiquement significatives entre présidents, mais les **graphiques interactifs révèlent la dynamique réelle du marché**.
- Les périodes de crise (dotcom, 2008, Covid-19, énergie 2022) sont les principaux facteurs de volatilité et d’écarts de rendement.
- Les présidences avec moins de crises visibles (Chirac, Hollande) ont des distributions plus concentrées et une volatilité moindre.
- La présidence qui a le mieux performé sur l’indice est **Emmanuel Macron**, principalement grâce à la forte hausse initiale du CAC40 malgré les crises ponctuelles.
- L’analyse visuelle et interactive complète parfaitement les statistiques classiques et permet de comprendre le **contexte macroéconomique et ses effets sur le marché**.
- Cette approche peut être réutilisée pour comparer d’autres indices ou périodes.

📚 *Source des données : Yahoo Finance. Visualisations interactives réalisées avec Plotly.*
"""
st.markdown(analyse_text)
