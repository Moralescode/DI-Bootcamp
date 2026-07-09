import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

df = pd.read_excel(r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\DI_BOOTCAMP_2026\WEEK2\Day5\Mini_Projet\dataset\US Superstore data.xls')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Month'] = df['Order Date'].dt.to_period('M')

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# ===== 1. STATES SALES =====
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=True).tail(15)
fig, ax = plt.subplots(figsize=(12, 6))
cmap = plt.cm.Blues(np.linspace(0.3, 0.9, len(state_sales)))
bars = ax.barh(state_sales.index, state_sales.values, color=cmap, edgecolor='black', linewidth=0.3)
ax.set_xlabel('Chiffre d affaires total ($)', fontsize=12)
ax.set_title('Top 15 Etats par chiffre d affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, state_sales.values):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2, '$' + f'{val:,.0f}', va='center', fontsize=9)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
img1 = fig_to_base64(fig)
plt.close()
print('img1 done')

# ===== 2. NY vs CALIFORNIE =====
ny_ca = df[df['State'].isin(['New York', 'California'])].groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'})
ny_ca = ny_ca.reindex(['California', 'New York'])
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors_pair = ['#e74c3c', '#3498db']
ax = axes[0]
bars = ax.bar(ny_ca.index, ny_ca['Sales'], color=colors_pair, edgecolor='black', linewidth=1)
ax.set_ylabel('Chiffre d affaires ($)', fontsize=12)
ax.set_title('Chiffre d affaires: CA vs NY', fontsize=13, fontweight='bold')
for bar, val in zip(bars, ny_ca['Sales']):
    ax.text(bar.get_x() + bar.get_width()/2, val + 5000, '$' + f'{val:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
bars = ax.bar(ny_ca.index, ny_ca['Profit'], color=colors_pair, edgecolor='black', linewidth=1)
ax.set_ylabel('Benefice ($)', fontsize=12)
ax.set_title('Benefices: CA vs NY', fontsize=13, fontweight='bold')
for bar, val in zip(bars, ny_ca['Profit']):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2000, '$' + f'{val:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.suptitle('Comparaison Californie vs New York', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
img2 = fig_to_base64(fig)
plt.close()
print('img2 done')

# ===== 3. CLIENT EXCEPTIONNEL A NY =====
ny_customers = df[df['State']=='New York'].groupby('Customer Name').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12, 6))
colors_norm = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(ny_customers)))[::-1]
bars = ax.barh(ny_customers.index[::-1], ny_customers['Sales'][::-1], color=colors_norm, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Chiffre d affaires ($)', fontsize=12)
ax.set_title('Top 10 Clients a New York par chiffre d affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, ny_customers['Sales'][::-1]):
    ax.text(val + 300, bar.get_y() + bar.get_height()/2, '$' + f'{val:,.0f}', va='center', fontsize=9)
ax.axvline(x=ny_customers['Sales'].iloc[0], color='red', linestyle='--', alpha=0.7, label='Meilleur: ' + ny_customers.index[0])
ax.legend()
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
img3 = fig_to_base64(fig)
plt.close()
print('img3 done')

# ===== 4. RENTABILITE PAR ETAT =====
state_summary = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
state_summary['Profit_Margin'] = (state_summary['Profit'] / state_summary['Sales']) * 100
state_summary = state_summary.sort_values('Profit_Margin')
fig, ax = plt.subplots(figsize=(14, 8))
colors_margin = ['#e74c3c' if x < 0 else '#2ecc71' for x in state_summary['Profit_Margin']]
bars = ax.barh(state_summary['State'], state_summary['Profit_Margin'], color=colors_margin, edgecolor='black', linewidth=0.3)
ax.axvline(x=0, color='black', linewidth=1)
ax.set_xlabel('Marge beneficiaire (%)', fontsize=12)
ax.set_title('Marge beneficiaire par Etat', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for bar, val in zip(bars, state_summary['Profit_Margin']):
    if val < 0:
        ax.text(val - 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', ha='right', fontsize=8, color='white', fontweight='bold')
plt.tight_layout()
img4 = fig_to_base64(fig)
plt.close()
print('img4 done')

# ===== 5. PARETO CLIENTS vs BENEFICES =====
customer_profit = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False).reset_index()
customer_profit['Cumulative_Profit'] = customer_profit['Profit'].cumsum()
customer_profit['Cumulative_Pct'] = customer_profit['Cumulative_Profit'] / customer_profit['Profit'].sum() * 100
customer_profit['Customer_Pct'] = (customer_profit.index + 1) / len(customer_profit) * 100
n20 = int(len(customer_profit) * 0.2)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(customer_profit['Customer_Pct'], customer_profit['Cumulative_Pct'], 'b-', linewidth=2, label='Courbe cumulative')
ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% des benefices')
ax.axvline(x=20, color='green', linestyle='--', alpha=0.7, label='20% des clients')
ax.fill_between([0, 20], [0, customer_profit.iloc[n20-1]['Cumulative_Pct']], alpha=0.2, color='green')
ax.plot([20], [customer_profit.iloc[n20-1]['Cumulative_Pct']], 'ro', markersize=8, label=f'{customer_profit.iloc[n20-1]["Cumulative_Pct"]:.1f}%')
ax.set_xlabel('% de clients', fontsize=12)
ax.set_ylabel('% cumule des benefices', fontsize=12)
ax.set_title('Principe de Pareto: Clients vs Benefices', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(alpha=0.3)
plt.tight_layout()
img5 = fig_to_base64(fig)
plt.close()
print('img5 done')

# ===== 6a. TOP 20 VILLES PAR VENTES =====
city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=True).tail(20)
fig, ax = plt.subplots(figsize=(12, 8))
cmap_c = plt.cm.Blues(np.linspace(0.3, 0.9, len(city_sales)))
bars = ax.barh(city_sales.index, city_sales.values, color=cmap_c, edgecolor='black', linewidth=0.3)
ax.set_xlabel('Chiffre d affaires total ($)', fontsize=12)
ax.set_title('Top 20 villes par chiffre d affaires', fontsize=14, fontweight='bold')
for bar, val in zip(bars, city_sales.values):
    ax.text(val + 2000, bar.get_y() + bar.get_height()/2, '$' + f'{val:,.0f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
img6a = fig_to_base64(fig)
plt.close()
print('img6a done')

# ===== 6b. TOP 20 VILLES PAR PROFIT =====
city_profit = df.groupby('City')['Profit'].sum().sort_values(ascending=True).tail(20)
fig, ax = plt.subplots(figsize=(12, 8))
cmap_p = plt.cm.Greens(np.linspace(0.3, 0.9, len(city_profit)))
bars = ax.barh(city_profit.index, city_profit.values, color=cmap_p, edgecolor='black', linewidth=0.3)
ax.set_xlabel('Benefice total ($)', fontsize=12)
ax.set_title('Top 20 villes par benefice', fontsize=14, fontweight='bold')
for bar, val in zip(bars, city_profit.values):
    ax.text(val + 200, bar.get_y() + bar.get_height()/2, '$' + f'{val:,.0f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
img6b = fig_to_base64(fig)
plt.close()
print('img6b done')

# ===== 6c. TOP 20 VILLES VENTES + COULEUR PROFIT =====
fig, ax = plt.subplots(figsize=(12, 7))
top_cities = df.groupby('City').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=False).head(20)
top_cities = top_cities.sort_values('Sales', ascending=True)
colors_scatter = ['#e74c3c' if p < 0 else '#3498db' for p in top_cities['Profit']]
bars = ax.barh(top_cities.index, top_cities['Sales'], color=colors_scatter, edgecolor='black', linewidth=0.3)
ax.set_xlabel('Chiffre d affaires total ($)', fontsize=12)
ax.set_title('Top 20 villes - Ventes (bleu: profit positif, rouge: profit negatif)', fontsize=14, fontweight='bold')
for bar, (sales, profit) in zip(bars, top_cities.values):
    color = 'green' if profit >= 0 else 'red'
    ax.text(sales + 2000, bar.get_y() + bar.get_height()/2, '$' + f'{profit:,.0f}', va='center', fontsize=8, color=color)
ax.grid(axis='x', alpha=0.3)
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#3498db', label='Profit positif'), Patch(facecolor='#e74c3c', label='Profit negatif')]
ax.legend(handles=legend_elements, loc='lower right')
plt.tight_layout()
img6c = fig_to_base64(fig)
plt.close()
print('img6c done')

# ===== 7. TOP 20 CLIENTS PAR VENTES =====
customer_sales_all = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=True).tail(20)
fig, ax = plt.subplots(figsize=(12, 8))
colors_top = plt.cm.Oranges(np.linspace(0.3, 0.9, len(customer_sales_all)))
bars = ax.barh(customer_sales_all.index, customer_sales_all.values, color=colors_top, edgecolor='black', linewidth=0.3)
ax.set_xlabel('Chiffre d affaires total ($)', fontsize=12)
ax.set_title('Top 20 clients par ventes', fontsize=14, fontweight='bold')
for bar, val in zip(bars, customer_sales_all.values):
    ax.text(val + 300, bar.get_y() + bar.get_height()/2, '$' + f'{val:,.0f}', va='center', fontsize=8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
img7 = fig_to_base64(fig)
plt.close()
print('img7 done')

# ===== 8. COURBE CUMULATIVE VENTES PAR CLIENT =====
customer_sales_all2 = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).reset_index()
customer_sales_all2['Cumulative_Sales'] = customer_sales_all2['Sales'].cumsum()
customer_sales_all2['Cumulative_Pct'] = customer_sales_all2['Cumulative_Sales'] / customer_sales_all2['Sales'].sum() * 100
customer_sales_all2['Customer_Pct'] = (customer_sales_all2.index + 1) / len(customer_sales_all2) * 100
n20_s = int(len(customer_sales_all2) * 0.2)
pct_20_s = float(customer_sales_all2.iloc[n20_s-1]['Cumulative_Pct'])

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(customer_sales_all2['Customer_Pct'], customer_sales_all2['Cumulative_Pct'], 'b-', linewidth=2, label='Courbe cumulative des ventes')
ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% des ventes')
ax.axvline(x=20, color='green', linestyle='--', alpha=0.7, label='20% des clients')
ax.fill_between([0, 20], [0, pct_20_s], alpha=0.2, color='green')
ax.plot([20], [pct_20_s], 'ro', markersize=8, label=f'{pct_20_s:.1f}% des ventes par 20% des clients')
ax.set_xlabel('% de clients', fontsize=12)
ax.set_ylabel('% cumule des ventes', fontsize=12)
ax.set_title('Principe de Pareto: Clients vs Ventes', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(alpha=0.3)
plt.tight_layout()
img8 = fig_to_base64(fig)
plt.close()
print('img8 done')

# ===== 9. VENTES PAR MOIS =====
monthly_sales = df.groupby('Order Month')['Sales'].sum()
monthly_profit = df.groupby('Order Month')['Profit'].sum()
fig, ax = plt.subplots(figsize=(14, 6))
x = range(len(monthly_sales))
ax.plot(x, monthly_sales.values, 'b-o', markersize=3, label='Ventes', linewidth=1.5)
ax2 = ax.twinx()
ax2.plot(x, monthly_profit.values, 'g-s', markersize=3, label='Benefices', linewidth=1.5, alpha=0.7)
ax.set_xlabel('Mois', fontsize=12)
ax.set_ylabel('Ventes ($)', fontsize=12, color='blue')
ax2.set_ylabel('Benefices ($)', fontsize=12, color='green')
ax.set_title('Evolution des ventes et benefices au fil du temps', fontsize=14, fontweight='bold')
ticks = list(range(0, len(monthly_sales), 3))
labels = [str(monthly_sales.index[i]) for i in ticks]
ax.set_xticks(ticks)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.grid(alpha=0.3)
plt.tight_layout()
img9 = fig_to_base64(fig)
plt.close()
print('img9 done')

# Save all images as numpy-friendly dict
import json
imgs = {
    'img1': img1,
    'img2': img2,
    'img3': img3,
    'img4': img4,
    'img5': img5,
    'img6a': img6a,
    'img6b': img6b,
    'img6c': img6c,
    'img7': img7,
    'img8': img8,
    'img9': img9,
}
with open('chart_images.json', 'w', encoding='utf-8') as f:
    json.dump(imgs, f, ensure_ascii=False)

print('ALL CHARTS GENERATED AND SAVED')
print('chart_images.json saved')
for k, v in imgs.items():
    print(f'{k}: {len(v)} chars')
