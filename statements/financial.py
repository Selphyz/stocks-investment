#%%
import pandas as pd
import yahooquery as yq
from yahooquery import Ticker
import matplotlib.pyplot as plt
#%%
def convertir_fecha_a_trimestre(fecha):
    return f"{fecha.year}-Q{(fecha.month - 1) // 3 + 1}"
#%%
# Declarar nombre del ticker a trabajar
# simbolo = "GOOG"
# # # Descargar datos históricos
# ticker = Ticker(simbolo)
# ticker.key_stats[simbolo]
#%%
def guardar_estados_financieros(simbolo):
    # Crear un archivo Excel con múltiples hojas
    with pd.ExcelWriter(f"{simbolo}_datos_financieros.xlsx") as writer:
        # Balance
        ticker = Ticker(simbolo)
        balance = ticker.balance_sheet().T
        balance.columns = pd.to_datetime(balance.iloc[0], format='%d/%m/%Y %H:%M:%S')
        # Renombrar los nombres de las columnas con formato "30/06/2021  0:00:00" as "2021-Q2"
        if pd.api.types.is_datetime64_any_dtype(balance.columns):
            balance.columns = balance.columns.to_period("Q").strftime("%Y-Q%q")
        else:
            balance.columns = pd.to_datetime(balance.columns, errors='coerce').to_period("Q").strftime("%Y-Q%q")
        balance.to_excel(writer, sheet_name="Balance")

        # Estado de resultados
        nulos = ticker.income_statement().T.isna().mean()
        ingresos = ticker.income_statement().T
        ingresos.columns = pd.to_datetime(ingresos.iloc[0], format='%d/%m/%Y %H:%M:%S')
        ingresos.columns = pd.to_datetime(ingresos.columns).to_period("Q").strftime("%Y-Q%q")
        ingresos.to_excel(writer, sheet_name="Estado_Resultados")

        # Flujo de efectivo
        flujo = ticker.cash_flow().T
        flujo.columns = pd.to_datetime(flujo.iloc[0], format='%d/%m/%Y %H:%M:%S')
        flujo.columns = pd.to_datetime(flujo.columns).to_period("Q").strftime("%Y-Q%q")
        flujo.to_excel(writer, sheet_name="Flujo_Efectivo")

        historial = ticker.history(period="max")
        historial.head()
        historial.to_excel(writer, sheet_name="Historial")

        # Información adicional
        info = ticker.asset_profile
        pd.DataFrame(info).to_excel(writer, sheet_name="Información")

    print(f"Datos financieros de {simbolo} guardados exitosamente")

#%%
# Declarar nombre del ticker a trabajar
# simbolo = "GOOG"
# # # Descargar datos históricos
# ticker = Ticker(simbolo)
# ticker.key_stats[simbolo]
#%%
guardar_estados_financieros("SAN")
#%%
# Visualizar cambio del balance de la empresa a lo largo del tiempo
balance = ticker.balancesheet
balance = balance.dropna(axis=1, how="all")
balance = balance.dropna(axis=0, how="all")
balance = balance.T # Transponer para visualización
balance
#%%
def obtener_y_graficar_balances(ticker_symbol="TSLA", valores=None):
    """
    Obtiene datos de balance de yfinance y genera gráficos de tarta comparativos.

    Args:
        ticker_symbol: El símbolo del ticker (ej. "TSLA").
        valores: Lista de valores a graficar.
    """

    if valores is None:
        valores = [
            "Treasury Shares Number",
            "Ordinary Shares Number",
            "Share Issued",
            "Total Debt",
            "Tangible Book Value",
            "Invested Capital",
            "Working Capital",
            "Net Tangible Assets",
            "Capital Lease Obligations",
            "Common Stock Equity"
        ]

    stock = Ticker(ticker_symbol)

    try:
        balance_sheet = stock.balance_sheet
    except Exception as e:
        print(f"Error al obtener el balance: {e}")
        return

    if balance_sheet.empty:
        print("No se encontraron datos de balance.")
        return

    # Obtener los dos últimos años disponibles
    years = balance_sheet.columns[:2]
    if len(years) < 2:
        print("No hay suficientes datos para comparar dos años.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))  # Dos subplots uno al lado del otro
    fig.suptitle(f"Comparación de Balances de {ticker_symbol} ({years[0].year} vs {years[1].year})", fontsize=16)


    for i, year in enumerate(years):
        data = balance_sheet[year].loc[valores].dropna() # Seleccionar valores y quitar NaN
        if data.empty: # Comprobar si hay datos para graficar
            axes[i].set_title(f"Sin datos disponibles para {year.year}")
            continue

        axes[i].pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
        axes[i].set_title(f"Balance {year.year}")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustar layout para evitar superposición de títulos
    plt.show()
#%%
obtener_y_graficar_balances()

# Ejemplo con valores específicos:
valores_especificos = ["Total Debt", "Common Stock Equity", "Working Capital"]
obtener_y_graficar_balances(valores=valores_especificos)

#%%
