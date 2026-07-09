import pandas as pd
import numpy as np
import json
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

df = pd.read_excel(r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\DI_BOOTCAMP_2026\WEEK2\Day5\Mini_Projet\dataset\US Superstore data.xls')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Month'] = df['Order Date'].dt.to_period('M')

results = {}

# ===== 1. TEXTE: ETATS AVEC LE PLUS DE VENTES =====
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False)
top_states = state_sales.head(10)
results['top_states'] = {k: round(v, 2) for k, v in top_states.items()}
results['top_state_names'] = top_states.index.tolist()

# ===== 2. TEXTE: NY vs CALIFORNIE =====
ny_revenue = float(df[df['State']=='New York']['Sales'].sum())
ca_revenue = float(df[df['State']=='California']['Sales'].sum())
ny_profit = float(df[df['State']=='New York']['Profit'].sum())
ca_profit = float(df[df['State']=='California']['Profit'].sum())
results['ny_revenue'] = round(ny_revenue, 2)
results['ca_revenue'] = round(ca_revenue, 2)
results['ny_profit'] = round(ny_profit, 2)
results['ca_profit'] = round(ca_profit, 2)
results['ca_ny_diff_revenue'] = round(ca_revenue - ny_revenue, 2)
results['ca_ny_diff_profit'] = round(ca_profit - ny_profit, 2)

# ===== 3. TEXTE: CLIENT EXCEPTIONNEL A NY =====
ny_customers = df[df['State']=='New York'].groupby('Customer Name').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=False)
best_ny_customer = ny_customers.index[0]
best_ny_sales = float(ny_customers['Sales'].iloc[0])
best_ny_profit = float(ny_customers['Profit'].iloc[0])
results['best_ny_customer'] = best_ny_customer
results['best_ny_sales'] = round(best_ny_sales, 2)
results['best_ny_profit'] = round(best_ny_profit, 2)

# ===== 4. TEXTE: RENTABILITE PAR ETAT =====
state_summary = df.groupby('State').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
state_summary['Profit_Margin'] = (state_summary['Profit'] / state_summary['Sales']) * 100
state_summary = state_summary.sort_values('Profit_Margin')
results['most_profitable_states'] = state_summary.tail(5)[['State', 'Profit', 'Profit_Margin']].to_dict('records')
results['loss_states'] = state_summary[state_summary['Profit'] < 0][['State', 'Profit', 'Profit_Margin']].sort_values('Profit').to_dict('records')

# ===== 5. TEXTE: PARETO CLIENTS vs BENEFICES =====
customer_profit = df.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False).reset_index()
customer_profit['Cumulative_Profit'] = customer_profit['Profit'].cumsum()
customer_profit['Cumulative_Pct'] = customer_profit['Cumulative_Profit'] / customer_profit['Profit'].sum() * 100
n20 = int(len(customer_profit) * 0.2)
results['pareto_profit'] = {
    'total_customers': len(customer_profit),
    'top_20pct_count': n20,
    'pct_contributed': round(customer_profit.iloc[n20-1]['Cumulative_Pct'], 2)
}

# ===== 6. TEXTE: TOP 20 VILLES PAR VENTES ET PROFIT =====
city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(20)
city_profit = df.groupby('City')['Profit'].sum().sort_values(ascending=False).head(20)
results['top_cities_sales'] = {k: round(v, 2) for k, v in city_sales.items()}
results['top_cities_profit'] = {k: round(v, 2) for k, v in city_profit.items()}

# ===== 7. TEXTE: TOP 20 CLIENTS PAR VENTES =====
customer_sales = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(20)
results['top_customers_sales'] = {k: round(v, 2) for k, v in customer_sales.items()}

# ===== 8. TEXTE: COURBE CUMULATIVE VENTES PAR CLIENT =====
customer_sales_all2 = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).reset_index()
customer_sales_all2['Cumulative_Sales'] = customer_sales_all2['Sales'].cumsum()
customer_sales_all2['Cumulative_Pct'] = customer_sales_all2['Cumulative_Sales'] / customer_sales_all2['Sales'].sum() * 100
n20_s = int(len(customer_sales_all2) * 0.2)
results['pareto_sales'] = {
    'total_customers': len(customer_sales_all2),
    'top_20pct_count': n20_s,
    'pct_contributed': round(customer_sales_all2.iloc[n20_s-1]['Cumulative_Pct'], 2)
}

# Save results
with open('analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("TEXT RESULTS SAVED")
print(json.dumps(results, indent=2, ensure_ascii=False))
