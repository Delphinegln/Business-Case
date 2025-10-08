# Identifier le président avec la meilleure performance totale
best_president = df_summary.loc[df_summary['Total Performance'].idxmax(), 'President']
best_perf = df_summary['Total Performance'].max()

# ✍️ Analyse contextuelle détaillée par président avec mention du meilleur
st.header("📖 Analyse détaillée par président")

analyse_text = f"""
### Jacques Chirac (1995-2006, bleu)
- Croissance globalement stable du CAC40.
- La bulle internet (2000-2002) provoque des pics de volatilité et des rendements négatifs ponctuels.
- Rendements mensuels concentrés autour de la moyenne, avec skewness légèrement négative pendant la bulle.

### Nicolas Sarkozy (2007-2011, vert)
- Rendements plus faibles en moyenne et volatilité très élevée.
- La crise financière de 2008 est clairement visible : chute brutale du CAC40 et volatilité maximale.
- Distribution des rendements très étalée, avec kurtosis élevée.

### François Hollande (2012-2016, orange)
- Rendements moyens légèrement positifs mais plus stables que sous Sarkozy.
- Les fluctuations restent modérées, sans choc systémique majeur.

### Emmanuel Macron (2017-2024, rouge)
- Début de mandat marqué par une forte hausse du CAC40.
- Crises ponctuelles importantes : pandémie Covid-19 (2020) et crise énergétique (2022) causent des pics de volatilité.
- Distribution des rendements très dispersée pendant ces événements.

---

### 🔹 Conclusion générale
- Les rendements moyens ne montrent pas toujours de différences statistiquement significatives entre présidents, mais les graphiques interactifs révèlent la dynamique réelle du marché.
- Les périodes de crise (dotcom, 2008, Covid-19, énergie 2022) sont les principaux facteurs de volatilité et d’écarts de rendement.
- Les présidences avec moins de crises visibles (Chirac, Hollande) ont des distributions plus concentrées et une volatilité moindre.
- **Le président ayant le mieux performé sur l'indice CAC40 est {best_president} avec une performance totale de {best_perf:.2%}.**
- L’étude démontre que l’analyse visuelle et interactive complète parfaitement les statistiques classiques, permettant de comprendre le contexte macroéconomique et ses effets sur le marché.

📚 *Source des données : Yahoo Finance. Visualisations interactives réalisées avec Plotly.*
"""

st.markdown(analyse_text)
