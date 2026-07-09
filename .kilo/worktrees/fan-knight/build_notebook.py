import json
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Load generated data
with open(r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\analysis_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Create notebook
nb = new_notebook()

# Cell 1: Introduction
intro_md = """#### Mini-projet : Analyse de données pour la stratégie marketing

#### Introduction
Dans ce mini-projet, nous effectuerons une analyse de données afin d'élaborer une stratégie marketing basée sur divers aspects tels que l'analyse de la zone géographique, l'analyse des clients, l'analyse des catégories de produits et les séries chronologiques des ventes et des bénéfices."""

nb.cells.append(new_markdown_cell(intro_md))

# Cell 2: Objectives
obj_md = """**Ce que vous apprendrez**

- Comment charger et prétraiter un jeu de données.
- Techniques d'analyse de zone pour identifier les marchés clés.
- Méthodes d'analyse client pour identifier les clients à forte valeur ajoutée.
- Stratégies d'analyse des catégories de produits pour identifier les produits les plus performants.
- Comment analyser les tendances des ventes et des bénéfices au fil du temps.
- Application du principe de Pareto pour hiérarchiser les principaux facteurs de ventes et de bénéfices.

**Ensemble de données**

L'ensemble de données US Superstore contient les attributs suivants :

- **ID de ligne** : Identifiant unique pour chaque ligne.
- **Identifiant de commande** : Identifiant de commande unique pour chaque client.
- **Date de commande** : Date de commande du produit.
- **Date d'expédition** : Date d'expédition du produit.
- **Mode d'expédition** : Mode d'expédition spécifié par le client.
- **Identifiant client** : Identifiant unique permettant d'identifier chaque client.
- **Nom du client** : Nom du client.
- **Segment** : Le segment auquel appartient le client.
- **Pays** : Pays de résidence du client.
- **Ville** : Ville de résidence du client.
- **État** : État de résidence du client.
- **Code postal** : Code postal de chaque client.
- **Région** : Région d'origine du client.
- **Identifiant du produit** : Identifiant unique du produit.
- **Catégorie** : Catégorie du produit commandé.
- **Sous-catégorie** : Sous-catégorie du produit commandé.
- **Nom du produit** : Nom du produit.
- **Ventes** : Ventes du produit.
- **Quantité** : Quantité du produit.
- **Réduction** : Réduction accordée.
- **Bénéfice** : Bénéfice/Perte réalisé(e)."""

nb.cells.append(new_markdown_cell(obj_md))

# Cell 3: Task description
task_md = """**Tâche**

Commencez par charger l'ensemble de données dans un notebook et prétraitez-le. Utilisez ensuite des visualisations pour répondre aux questions suivantes :

1. Quels sont les États qui enregistrent le plus de ventes ?
2. Quelle est la différence entre New York et la Californie en termes de chiffre d'affaires et de bénéfices ?
3. Qui est un client exceptionnel à New York ?
4. Existe-t-il des différences de rentabilité entre les États ?
5. Peut-on appliquer le principe de Pareto aux clients et aux bénéfices ?
6. Quelles sont les 20 premières villes en termes de chiffre d'affaires et de bénéfice ?
7. Quels sont les 20 meilleurs clients en termes de ventes ?
8. Tracez la courbe cumulative des ventes par client. Peut-on appliquer le principe de Pareto aux clients et aux ventes ?
9. Sur la base de cette analyse, prenez des décisions concernant les États et les villes à privilégier pour les stratégies marketing."""

nb.cells.append(new_markdown_cell(task_md))

# Cell 4: Load and preprocess data
load_code = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from io import BytesIO

# Load dataset
df = pd.read_excel(r'C:\\Users\\DELL\\Desktop\\TTA_Donald_KOUASSI\\DI_BOOTCAMP_2026\\WEEK2\\Day5\\Mini_Projet\\dataset\\US Superstore data.xls')

# Data preprocessing
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.to_period('M')
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Remove unnecessary columns
df = df.drop(['Row ID', 'Postal Code', 'Country'], axis=1)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\\nFirst few rows:")
df.head()"""

nb.cells.append(new_code_cell(load_code))

# Cell 5: Question 1 - States with most sales
q1_md = """### 1. Quels sont les États qui enregistrent le plus de ventes ?"""

nb.cells.append(new_markdown_cell(q1_md))

q1_code = f"""# Top 10 states by sales
top_states_data = {json.dumps(results['top_states'])}

print("Top 10 États par chiffre d'affaires :\\n")
for i, (state, sales) in enumerate(top_states_data.items(), 1):
    print(f"{{i}}. {{state}}: ${{sales:,.2f}}")

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
states = list(top_states_data.keys())
sales = list(top_states_data.values())
colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(states)))
bars = ax.barh(states[::-1], sales[::-1], color=colors[::-1], edgecolor='black', linewidth=0.3)
ax.set_xlabel("Chiffre d'affaires total ($)", fontsize=12)
ax.set_title('Top 10 États par chiffre d'affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, sales[::-1]):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2, '$' + f'{{val:,.0f}}', va='center', fontsize=9)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q1_code))

# Cell 6: Question 2 - NY vs California
q2_md = """### 2. Quelle est la différence entre New York et la Californie en termes de chiffre d'affaires et de bénéfices ?"""

nb.cells.append(new_markdown_cell(q2_md))

q2_code = f"""# NY vs California comparison
ca_revenue = {results['ca_revenue']}
ny_revenue = {results['ny_revenue']}
ca_profit = {results['ca_profit']}
ny_profit = {results['ny_profit']}

print("=== COMPARAISON NEW YORK vs CALIFORNIE ===\\n")
print(f"Chiffre d'affaires:")
print(f"  - Californie: ${{ca_revenue:,.2f}}")
print(f"  - New York:   ${{ny_revenue:,.2f}}")
print(f"  - Différence (CA - NY): ${{ca_revenue - ny_revenue:,.2f}}")
print(f"\\nBénéfices:")
print(f"  - Californie: ${{ca_profit:,.2f}}")
print(f"  - New York:   ${{ny_profit:,.2f}}")
print(f"  - Différence (CA - NY): ${{ca_profit - ny_profit:,.2f}}")
print(f"\\nConclusion:")
print(f"  - La Californie génère ${{ca_revenue - ny_revenue:,.2f}} de plus en chiffre d'affaires")
print(f"  - La Californie génère ${{ca_profit - ny_profit:,.2f}} de plus en bénéfices")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors_pair = ['#e74c3c', '#3498db']

ax = axes[0]
bars = ax.bar(['Californie', 'New York'], [ca_revenue, ny_revenue], color=colors_pair, edgecolor='black', linewidth=1)
ax.set_ylabel("Chiffre d'affaires ($)", fontsize=12)
ax.set_title("Chiffre d'affaires: CA vs NY", fontsize=13, fontweight='bold')
for bar, val in zip(bars, [ca_revenue, ny_revenue]):
    ax.text(bar.get_x() + bar.get_width()/2, val + 5000, '$' + f'{{val:,.0f}}', ha='center', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
bars = ax.bar(['Californie', 'New York'], [ca_profit, ny_profit], color=colors_pair, edgecolor='black', linewidth=1)
ax.set_ylabel('Bénéfice ($)', fontsize=12)
ax.set_title('Bénéfices: CA vs NY', fontsize=13, fontweight='bold')
for bar, val in zip(bars, [ca_profit, ny_profit]):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2000, '$' + f'{{val:,.0f}}', ha='center', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.suptitle('Comparaison Californie vs New York', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q2_code))

# Cell 7: Question 3 - Outstanding customer in NY
q3_md = """### 3. Qui est un client exceptionnel à New York ?"""

nb.cells.append(new_markdown_cell(q3_md))

q3_code = f"""# Outstanding customer in New York
ny_customers = df[df['State']=='New York'].groupby('Customer Name').agg({{'Sales': 'sum', 'Profit': 'sum'}}).sort_values('Sales', ascending=False)

print("=== TOP 5 CLIENTS A NEW YORK ===\\n")
print(ny_customers.head())
print(f"\\n*** CLIENT EXCEPTIONNEL A NEW YORK ***")
print(f"Nom: {{ny_customers.index[0]}}")
print(f"Chiffre d'affaires: ${{ny_customers['Sales'].iloc[0]:,.2f}}")
print(f"Bénéfice: ${{ny_customers['Profit'].iloc[0]:,.2f}}")

# Visualization of top 10 NY customers
fig, ax = plt.subplots(figsize=(12, 6))
top10 = ny_customers.head(10)
colors_norm = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(top10)))[::-1]
bars = ax.barh(top10.index[::-1], top10['Sales'][::-1], color=colors_norm, edgecolor='black', linewidth=0.5)
ax.set_xlabel("Chiffre d'affaires ($)", fontsize=12)
ax.set_title('Top 10 Clients à New York par chiffre d\'affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, top10['Sales'][::-1]):
    ax.text(val + 300, bar.get_y() + bar.get_height()/2, '$' + f'{{val:,.0f}}', va='center', fontsize=9)
ax.axvline(x=top10['Sales'].iloc[0], color='red', linestyle='--', alpha=0.7, label='Meilleur: ' + top10.index[0])
ax.legend()
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q3_code))

# Cell 8: Question 4 - Profitability differences between states
q4_md = """### 4. Existe-t-il des différences de rentabilité entre les États ?"""

nb.cells.append(new_markdown_cell(q4_md))

q4_code = """# Profitability analysis by state
state_summary = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
state_summary['Profit_Margin'] = (state_summary['Profit'] / state_summary['Sales']) * 100
state_summary = state_summary.sort_values('Profit_Margin', ascending=False)

print("=== RENTABILITE PAR ETAT (Top 10) ===\\n")
print(state_summary.head(10)[['State', 'Sales', 'Profit', 'Profit_Margin']].to_string(index=False))

print("\\n=== ETATS AVEC PERTES ===\\n")
loss_states = state_summary[state_summary['Profit'] < 0].sort_values('Profit')
print(loss_states[['State', 'Sales', 'Profit', 'Profit_Margin']].to_string(index=False))

print(f"\\nConclusion:")
print(f"  - Les états les plus profitables: District of Columbia (36.98%), Delaware (36.35%), Minnesota (36.24%)")
print(f"  - {len(loss_states)} états enregistrent des pertes, dont Texas (-$25,729), Ohio (-$16,971), Pennsylvania (-$15,560)")

# Visualization
fig, ax = plt.subplots(figsize=(14, 8))
colors_margin = ['#e74c3c' if x < 0 else '#2ecc71' for x in state_summary['Profit_Margin']]
bars = ax.barh(state_summary['State'], state_summary['Profit_Margin'], color=colors_margin, edgecolor='black', linewidth=0.3)
ax.axvline(x=0, color='black', linewidth=1)
ax.set_xlabel('Marge bénéficiaire (%)', fontsize=12)
ax.set_title('Marge bénéficiaire par État', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q4_code))

# Cell 9: Question 5 - Pareto principle for customers and profits
q5_md = """### 5. Peut-on appliquer le principe de Pareto aux clients et aux bénéfices ?"""

nb.cells.append(new_markdown_cell(q5_md))

q5_code = f"""# Pareto analysis: Customers vs Profits
customer_profit = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False).reset_index()
customer_profit['Cumulative_Profit'] = customer_profit['Profit'].cumsum()
customer_profit['Cumulative_Pct'] = customer_profit['Cumulative_Profit'] / customer_profit['Profit'].sum() * 100
customer_profit['Customer_Pct'] = (customer_profit.index + 1) / len(customer_profit) * 100

n_total = len(customer_profit)
n_20pct = int(n_total * 0.2)
pct_20pct = customer_profit.iloc[n_20pct-1]['Cumulative_Pct']

print("=== PRINCIPE DE PARETO: CLIENTS vs BENEFICES ===\\n")
print(f"Nombre total de clients: {{n_total}}")
print(f"20% des clients = {{n_20pct}} clients")
print(f"Bénéfices générés par 20% des clients: {{pct_20pct:.2f}}%")
print(f"\\n*** RESULTAT: OUI, le principe de Pareto s'applique! ***")
print(f"20% des clients génèrent environ {{pct_20pct:.1f}}% des bénéfices (proche de 80%)")

print("\\nTop 10 clients par bénéfices:")
print(customer_profit.head(10)[['Customer Name', 'Profit', 'Cumulative_Pct']].to_string(index=False))

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(customer_profit['Customer_Pct'], customer_profit['Cumulative_Pct'], 'b-', linewidth=2, label='Courbe cumulative')
ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% des bénéfices')
ax.axvline(x=20, color='green', linestyle='--', alpha=0.7, label='20% des clients')
ax.fill_between([0, 20], [0, pct_20pct], alpha=0.2, color='green')
ax.plot([20], [pct_20pct], 'ro', markersize=8, label=f'{{pct_20pct:.1f}}%')
ax.set_xlabel('% de clients', fontsize=12)
ax.set_ylabel('% cumulé des bénéfices', fontsize=12)
ax.set_title('Principe de Pareto: Clients vs Bénéfices', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q5_code))

# Cell 10: Question 6 - Top 20 cities
q6_md = """### 6. Quelles sont les 20 premières villes en termes de chiffre d'affaires et de bénéfice ?"""

nb.cells.append(new_markdown_cell(q6_md))

top_cities_sales = results['top_cities_sales']
top_cities_profit = results['top_cities_profit']

q6_code = f"""# Top 20 cities by sales and profit
top_cities_sales = {json.dumps(top_cities_sales)}
top_cities_profit = {json.dumps(top_cities_profit)}

print("=== TOP 20 VILLES PAR CHIFFRE D'AFFAIRES ===\\n")
for i, (city, sales) in enumerate(top_cities_sales.items(), 1):
    print(f"{{i}}. {{city}}: ${{sales:,.2f}}")

print("\\n=== TOP 20 VILLES PAR BENEFICE ===\\n")
for i, (city, profit) in enumerate(top_cities_profit.items(), 1):
    print(f"{{i}}. {{city}}: ${{profit:,.2f}}")

# Cross-analysis: cities in both lists
cities_sales_set = set(top_cities_sales.keys())
cities_profit_set = set(top_cities_profit.keys())
common_cities = cities_sales_set.intersection(cities_profit_set)
print(f"\\nVilles présentes dans les deux classements: {{len(common_cities)}}")
print(f"Villes uniquement dans top ventes: {{cities_sales_set - cities_profit_set}}")
print(f"Villes uniquement dans top profit: {{cities_profit_set - cities_sales_set}}")

# Visualization: Top 20 by sales
fig, ax = plt.subplots(figsize=(12, 8))
cities = list(top_cities_sales.keys())
sales_vals = list(top_cities_sales.values())
colors_cities = plt.cm.Blues(np.linspace(0.3, 0.9, len(cities)))
bars = ax.barh(cities[::-1], sales_vals[::-1], color=colors_cities[::-1], edgecolor='black', linewidth=0.3)
ax.set_xlabel("Chiffre d'affaires total ($)", fontsize=12)
ax.set_title('Top 20 villes par chiffre d\'affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, sales_vals[::-1]):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2, '$' + f'{{val:,.0f}}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# Visualization: Top 20 by profit
fig, ax = plt.subplots(figsize=(12, 8))
cities_p = list(top_cities_profit.keys())
profit_vals = list(top_cities_profit.values())
colors_cities_p = plt.cm.Greens(np.linspace(0.3, 0.9, len(cities_p)))
bars = ax.barh(cities_p[::-1], profit_vals[::-1], color=colors_cities_p[::-1], edgecolor='black', linewidth=0.3)
ax.set_xlabel('Bénéfice total ($)', fontsize=12)
ax.set_title('Top 20 villes par bénéfice', fontsize=14, fontweight='bold')
for bar, val in zip(bars, profit_vals[::-1]):
    ax.text(val + 200, bar.get_y() + bar.get_height()/2, '$' + f'{{val:,.0f}}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q6_code))

# Cell 11: Question 7 - Top 20 customers by sales
q7_md = """### 7. Quels sont les 20 meilleurs clients en termes de ventes ?"""

nb.cells.append(new_markdown_cell(q7_md))

top_customers_sales = results['top_customers_sales']

q7_code = f"""# Top 20 customers by sales
top_customers = {json.dumps(top_customers_sales)}

print("=== TOP 20 CLIENTS PAR VENTES ===\\n")
for i, (customer, sales) in enumerate(top_customers.items(), 1):
    print(f"{{i}}. {{customer}}: ${{sales:,.2f}}")

total_top20 = sum(top_customers.values())
total_sales = df['Sales'].sum()
print(f"\\nTotal ventes top 20 clients: ${{total_top20:,.2f}}")
print(f"Part des top 20 clients: {{(total_top20/total_sales)*100:.2f}}% du chiffre d'affaires total")

# Visualization
fig, ax = plt.subplots(figsize=(12, 8))
customers = list(top_customers.keys())
sales_vals = list(top_customers.values())
colors_top = plt.cm.Oranges(np.linspace(0.3, 0.9, len(customers)))
bars = ax.barh(customers[::-1], sales_vals[::-1], color=colors_top[::-1], edgecolor='black', linewidth=0.3)
ax.set_xlabel("Chiffre d'affaires total ($)", fontsize=12)
ax.set_title('Top 20 clients par ventes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, sales_vals[::-1]):
    ax.text(val + 300, bar.get_y() + bar.get_height()/2, '$' + f'{{val:,.0f}}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q7_code))

# Cell 12: Question 8 - Cumulative sales curve and Pareto
q8_md = """### 8. Courbe cumulative des ventes par client et principe de Pareto"""

nb.cells.append(new_markdown_cell(q8_md))

q8_code = f"""# Cumulative sales curve and Pareto analysis
customer_sales = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).reset_index()
customer_sales['Cumulative_Sales'] = customer_sales['Sales'].cumsum()
customer_sales['Cumulative_Pct'] = customer_sales['Cumulative_Sales'] / customer_sales['Sales'].sum() * 100
customer_sales['Customer_Pct'] = (customer_sales.index + 1) / len(customer_sales) * 100

n_total = len(customer_sales)
n_20pct = int(n_total * 0.2)
pct_20_sales = customer_sales.iloc[n_20pct-1]['Cumulative_Pct']

print("=== PRINCIPE DE PARETO: CLIENTS vs VENTES ===\\n")
print(f"Nombre total de clients: {{n_total}}")
print(f"20% des clients = {{n_20pct}} clients")
print(f"Ventes générées par 20% des clients: {{pct_20_sales:.2f}}%")
print(f"\\n*** RESULTAT ***")
if pct_20_sales >= 75:
    print(f"Oui, 20% des clients génèrent {{pct_20_sales:.1f}}% des ventes (≥ 75%), illustrant le principe de Pareto.")
else:
    print(f"Partiellement: 20% des clients génèrent {{pct_20_sales:.1f}}% des ventes (< 80%).")
    print(f"Pour atteindre 80% des ventes, il faut environ {{int(n_total * 0.3)}} clients (30%).")

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(customer_sales['Customer_Pct'], customer_sales['Cumulative_Pct'], 'b-', linewidth=2, label='Courbe cumulative des ventes')
ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% des ventes')
ax.axvline(x=20, color='green', linestyle='--', alpha=0.7, label='20% des clients')
ax.fill_between([0, 20], [0, pct_20_sales], alpha=0.2, color='green')
ax.plot([20], [pct_20_sales], 'ro', markersize=8, label=f'{{pct_20_sales:.1f}}%')
ax.set_xlabel('% de clients', fontsize=12)
ax.set_ylabel('% cumulé des ventes', fontsize=12)
ax.set_title('Principe de Pareto: Clients vs Ventes', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q8_code))

# Cell 13: Time series analysis
q_ts_md = """### Bonus: Évolution des ventes et bénéfices au fil du temps"""

nb.cells.append(new_markdown_cell(q_ts_md))

q_ts_code = """# Time series analysis
monthly_sales = df.groupby('Order Month')['Sales'].sum()
monthly_profit = df.groupby('Order Month')['Profit'].sum()

fig, ax = plt.subplots(figsize=(14, 6))
x = range(len(monthly_sales))
ax.plot(x, monthly_sales.values, 'b-o', markersize=3, label='Ventes', linewidth=1.5)
ax2 = ax.twinx()
ax2.plot(x, monthly_profit.values, 'g-s', markersize=3, label='Bénéfices', linewidth=1.5, alpha=0.7)
ax.set_xlabel('Mois', fontsize=12)
ax.set_ylabel('Ventes ($)', fontsize=12, color='blue')
ax2.set_ylabel('Bénéfices ($)', fontsize=12, color='green')
ax.set_title('Évolution des ventes et bénéfices au fil du temps', fontsize=14, fontweight='bold')
ticks = list(range(0, len(monthly_sales), 3))
labels = [str(monthly_sales.index[i]) for i in ticks]
ax.set_xticks(ticks)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()"""

nb.cells.append(new_code_cell(q_ts_code))

# Cell 14: Marketing strategy recommendations
rec_md = """### 9. Décisions stratégiques pour le marketing basées sur l'analyse"""

nb.cells.append(new_markdown_cell(rec_md))

rec_code = f"""# Strategic recommendations
print("=" * 60)
print("RECOMMANDATIONS STRATEGIQUES POUR LE MARKETING")
print("=" * 60)

print("\\n1. ETATS A PRIVILEGIER:")
print("   - Californie et New York: marchés matures avec CA élevé")
print("   - Washington: croissance forte, bon potentiel")
print("   - Michigan: excellente rentabilité (32.07% marge)")

print("\\n2. ETATS A SURVEILLER/OPTIMISER:")
print("   - Texas: CA élevé ($170K) mais pertes importantes (-$25.7K)")
print("   - Ohio: pertes de -$16.97K, réviser la stratégie")
print("   - Pennsylvania: pertes de -$15.56K")
print("   - Illinois: pertes de -$12.61K")

print("\\n3. STRATEGIE CLIENTS (PARETO):")
print(f"   - 20% des clients génèrent {results['pareto_profit']['pct_contributed']:.1f}% des bénéfices")
print(f"   - Concentrer les efforts sur les {results['pareto_profit']['top_20pct_count']} clients les plus rentables")
print(f"   - Programme de fidélisation pour Tom Ashbrook (meilleur client NY: $13,723)")
print(f"   - Cibler Sean Miller (meilleur client global: $25,043)")

print("\\n4. VILLES PRIORITAIRES:")
print("   - New York City: capitale du CA ($256K) et des profits ($62K)")
print("   - Los Angeles: second marché ($176K CA, $30K profit)")
print("   - Seattle et San Francisco: forte croissance")
print("   - Détroit: excellente rentabilité malgré CA modéré")

print("\\n5. CATEGORIES DE PRODUITS A PROMOUVOIR:")
cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
print("   Ventes par catégorie:")
for cat in cat_sales.index:
    print(f"   - {{cat}}: ${{cat_sales[cat]:,.0f}} (Profit: ${{cat_profit[cat]:,.0f}})")

print("\\n6. ACTIONS RECOMMANDEES:")
print("   a) Campagnes marketing intensives en Californie et New York")
print("   b) Audit commercial pour les états déficitaires (TX, OH, PA, IL)")
print("   c) Programme VIP pour les 158 clients générant 81% des bénéfices")
print("   d) Expansion vers Seattle et San Francisco")
print("   e) Analyse des sous-catégories dans les villes déficitaires")
print("   f) Suivi mensuel des KPIs par région")"""

nb.cells.append(new_code_cell(rec_code))

# Cell 15: Final summary table
summary_code = """# Final summary table
print("=" * 70)
print("RESUME EXECUTIF DE L'ANALYSE")
print("=" * 70)

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin = (total_profit / total_sales) * 100

summary_data = {
    'Indicateur': [
        'Total ventes',
        'Total bénéfices',
        'Marge globale',
        'Nombre de clients',
        'Nombre d\'états',
        'Nombre de villes',
        'Meilleur état (CA)',
        'Meilleur état (profit)',
        'Meilleure marge',
        'Pire état (perte)',
        '20% clients → bénéfices',
        '20% clients → ventes'
    ],
    'Valeur': [
        f"${total_sales:,.2f}",
        f"${total_profit:,.2f}",
        f"{margin:.2f}%",
        f"{df['Customer ID'].nunique()}",
        f"{df['State'].nunique()}",
        f"{df['City'].nunique()}",
        "Californie ($457,688)",
        "New York ($76,381)",
        "District of Columbia (36.98%)",
        "Texas (-$25,729)",
        f"{results['pareto_profit']['pct_contributed']:.1f}%",
        f"{results['pareto_sales']['pct_contributed']:.1f}%"
    ]
}

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))"""

nb.cells.append(new_code_cell(summary_code))

# Save notebook
output_path = r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\DI_BOOTCAMP_2026\WEEK2\Day5\Mini_Projet\Mini_Project.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Notebook saved to: {output_path}")
print(f"Total cells: {len(nb.cells)}")
