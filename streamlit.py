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

st.title("📊 Étude du CAC40 sous les présidences françaises 🇫🇷")
st.markdown("""
Analyse interactive des **performances du CAC40** par président français (1995-2024).  
Explorez rendement, volatilité et distribution des rendements mensuels.
""")

# 🧑‍💼 Paramètres
presidents = {
    'Jacques Chirac': {'start': '1995-01-01', 'end': '2006-12-31', 'color': 'blue'},
    'Nicolas Sarkozy': {'start': '2007-01-01', 'end': '2011-12-31', 'color': 'green'},
    'François Hollande': {'start': '2012-01-01', 'end': '2016-12-31', 'color': 'orange'},
    'Emmanuel Macron': {'start': '2017-01-01', 'end': '2024-12-31', 'color': 'red'}
}

# Sidebar
st.sidebar.header("⚙️ Paramètres")
ticker = st.sidebar.text_input("Indice boursier :", "^FCHI")
interval = st.sidebar.selectbox("Intervalle :", ["1mo", "1wk", "1d"], index=0)

# 📦 Téléchargement et calculs
assets = {}
summary_stats = []

for name, info in presidents.items():
    with st.spinner(f"Chargement {name}..."):
        data = yf.download(ticker, start=info['start'], end=info['end'], interval=interval)['Close']
        returns = data.pct_change().dropna()

        vol = returns.std()
        mean = returns.mean()
        perf = (data.iloc[-1] / data.iloc[0] - 1)
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
st.header("📈 Résumé statistique")
st.dataframe(df_summary.round(4), use_container_width=True)

# 🧪 Comparaison ANOVA
anova = stats.f_oneway(*[assets[p] for p in presidents])
f_stat = float(anova.statistic)
p_val = float(anova.pvalue)
st.write(f"**F-statistic:** {f_stat:.3f} | **p-value:** {p_val:.3f}")
if p_val <= 0.05:
    st.success("✅ Différence significative détectée.")
else:
    st.info("⚠️ Aucune différence significative.")

# 📊 Graphique Plotly - Rendements moyens
df_summary['Mean Return Value'] = df_summary['Mean Return'].apply(float)
fig_bar = px.bar(df_summary, x='President', y='Mean Return Value', color='President',
                 title='📊 Rendement mensuel moyen par président')
fig_bar.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_bar.update_layout(yaxis_tickformat=".2%", xaxis_title=None, yaxis_title="Rendement moyen")
st.plotly_chart(fig_bar, use_container_width=True)

# 📊 Graphique Plotly - Distribution des rendements
returns_list = []
labels = []

for p in presidents:
    if p in assets and not assets[p].empty:
        returns_list.append(assets[p].dropna().tolist())
        labels.append(p)

# Vérifier qu'il reste au moins une série
if returns_list:
    fig_dist = ff.create_distplot(returns_list, labels, show_hist=False, show_rug=False)
    fig_dist.update_layout(title="🌍 Distribution des rendements mensuels")
    st.plotly_chart(fig_dist, use_container_width=True)
else:
    st.warning("⚠️ Pas assez de données pour créer le graphique de distribution.")


# 📊 Graphique Plotly - Volatilité glissante
fig_vol = go.Figure()
for name, info in presidents.items():
    rolling_vol = assets[name].rolling(12).std()
    fig_vol.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol.values, mode='lines', name=name,
                                 line=dict(color=info['color'])))
fig_vol.update_layout(title="📉 Volatilité glissante sur 12 mois",
                      xaxis_title="Date", yaxis_title="Volatilité")
st.plotly_chart(fig_vol, use_container_width=True)
