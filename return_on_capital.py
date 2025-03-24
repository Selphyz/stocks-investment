#%%
from yahooquery import Ticker
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
#%%
# Lista de tickers
tickers = ['MSFT', 'AMZN', 'TSLA', 'AAPL', 'GOOG']

# Crear un diccionario para almacenar los resultados
resultados = {
    'Ticker': [],
    'ROC': [],
    'PE_Ratio': []
}
#%%
arg = [
    "YPF","GGAL","BMA","PAMP","BBAR","EDN","LOMA","SUP","CEPU"
]
#%%
# Obtener datos para cada ticker
def plot_ticker(stocks):
    for ticker in stocks:
        stock = Ticker(ticker)

        # Obtener datos financieros
        balance_sheet = stock.balance_sheet().T
        financial_data = stock.financial_data[ticker]
        key_stats = stock.key_stats[ticker]

        # Calcular ROC (Return on Capital)
        try:
            ebitda = financial_data.get('ebitda')
            total_debt = financial_data.get('totalDebt', 0)
            total_cash = financial_data.get('totalCash', 0)
            if ebitda is None:
                raise ValueError("EBITDA no disponible para el ticker: {}".format(ticker))
            roc = (ebitda / (total_debt + total_cash)) * 100
        except Exception as e:
            print("Error al calcular ROC para el ticker {}: {}".format(ticker, e))
            roc = 0

        # Obtener P/E Ratio
        pe_ratio = key_stats.get('forwardPE', 0)

        # Agregar al diccionario
        resultados['Ticker'].append(ticker)
        resultados['ROC'].append(round(roc, 2))
        resultados['PE_Ratio'].append(round(pe_ratio, 2))
#%%
# Crear DataFrame
df = pd.DataFrame(resultados)
#%%
# Crear visualización
plt.figure(figsize=(12, 6))

# Subplot para ROC
plt.subplot(1, 2, 1)
sns.barplot(data=df, x='Ticker', y='ROC')
plt.title('Retorno sobre Capital (%)')
plt.xticks(rotation=45)

# Subplot para P/E Ratio
plt.subplot(1, 2, 2)
sns.barplot(data=df, x='Ticker', y='PE_Ratio')
plt.title('P/E Ratio')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
#%%
# Mostrar tabla de resultados
print("\nResultados detallados:")
print(df.to_string(index=False))
#%%
ypf = pd.read_excel("statements/YPF_datos_financieros.xlsx")
ypf.head()
#%%
from yahooquery import Ticker
import pandas as pd

# Create Ticker object
tick = "AAPL"
ticker = Ticker(tick)

# Get financial data
# 1. Get annual financial statements (income statement, balance sheet, cash flow)
income_stmt = ticker.income_statement(frequency='a')
balance_sheet = ticker.balance_sheet(frequency='a')

# Check if we got valid data
if isinstance(income_stmt, pd.DataFrame) and isinstance(balance_sheet, pd.DataFrame):
    # Filter for the last 5 years
    income_stmt = income_stmt.sort_values('asOfDate', ascending=False).head(5)
    balance_sheet = balance_sheet.sort_values('asOfDate', ascending=False).head(5)

    # Merge the data
    financial_data = pd.merge(income_stmt, balance_sheet, on='asOfDate', how='outer')

    # Set the date as index and sort by date (newest first)
    financial_data.set_index('asOfDate', inplace=True)
    financial_data.sort_index(ascending=False, inplace=True)

print(f"Error retrieving data for {tick}")

print(f"Financial data for {tick} (last 5 years):")
print(financial_data)

# Save to CSV
financial_data.to_csv(f"{tick}_financial_data.csv")
print(f"Data saved to {tick}_financial_data.csv")
#%%

#%%