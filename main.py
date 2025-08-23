import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Mapping of countries to World Bank codes ---
country_codes = {
    # Africa
    "South Africa": "ZA", "Nigeria": "NG", "Kenya": "KE", "Egypt": "EG", "Ghana": "GH",
    "Ethiopia": "ET", "Tanzania": "TZ", "Uganda": "UG", "Morocco": "MA", "Algeria": "DZ",
    "Zimbabwe": "ZW", "Zambia": "ZM", "Botswana": "BW", "Namibia": "NA", "Mozambique": "MZ",
    "Angola": "AO", "Senegal": "SN", "Ivory Coast": "CI", "Cameroon": "CM",

    # North America
    "United States": "US", "Canada": "CA", "Mexico": "MX",

    # South America
    "Brazil": "BR", "Argentina": "AR", "Chile": "CL", "Colombia": "CO", "Peru": "PE",

    # Europe
    "United Kingdom": "GB", "Germany": "DE", "France": "FR", "Italy": "IT", "Spain": "ES",
    "Netherlands": "NL", "Sweden": "SE", "Norway": "NO", "Switzerland": "CH", "Russia": "RU",

    # Asia
    "China": "CN", "India": "IN", "Japan": "JP", "South Korea": "KR", "Indonesia": "ID",
    "Saudi Arabia": "SA", "Turkey": "TR", "United Arab Emirates": "AE",
    "Pakistan": "PK", "Bangladesh": "BD",

    # Oceania
    "Australia": "AU", "New Zealand": "NZ"
}

# --- Indicators dictionary ---
indicators = {
    "GDP (current US$)": "NY.GDP.MKTP.CD",
    "GDP growth (%)": "NY.GDP.MKTP.KD.ZG",
    "GDP per capita (US$)": "NY.GDP.PCAP.CD",
    "Inflation (%)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)": "SL.UEM.TOTL.ZS",
    "Youth Unemployment (%)": "SL.UEM.1524.ZS",
    "Population, total": "SP.POP.TOTL",
    "Life Expectancy (years)": "SP.DYN.LE00.IN",
    "Health expenditure (% of GDP)": "SH.XPD.CHEX.GD.ZS",
    "Education expenditure (% of GDP)": "SE.XPD.TOTL.GD.ZS",
    "Foreign direct investment (% of GDP)": "BX.KLT.DINV.WD.GD.ZS",
    "Exports (% of GDP)": "NE.EXP.GNFS.ZS",
    "Imports (% of GDP)": "NE.IMP.GNFS.ZS",
    "Internet users (% of population)": "IT.NET.USER.ZS",
    "Mobile cellular subscriptions (per 100 people)": "IT.CEL.SETS.P2",
    "Current account balance (% of GDP)": "BN.CAB.XOKA.GD.ZS",
    "Government debt (% of GDP)": "GC.DOD.TOTL.GD.ZS",
    "Poverty headcount ratio ($2.15/day)": "SI.POV.DDAY"
}

# --- Fetch data function ---
def fetch_data(country_code, indicator):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) < 2 or not data[1]:
            return None
        df = pd.DataFrame(data[1])
        df = df[['date', 'value']].dropna()
        df['date'] = df['date'].astype(int)
        df.sort_values('date', inplace=True)
        return df
    except:
        return None

# --- Streamlit App ---
st.title("🌍 Economic Indicators Visualizer")

# Sidebar country/indicator selection
countries = st.sidebar.multiselect(
    "Select Country/Countries", list(country_codes.keys()),
    default=["South Africa", "Nigeria"]
)
indicator_name = st.sidebar.selectbox("Select Indicator", list(indicators.keys()))
indicator_code = indicators[indicator_name]

if not countries:
    st.info("Please select at least one country from the sidebar.")
else:
    # Plot data for each country
    plt.figure(figsize=(10, 5))
    for country in countries:
        df = fetch_data(country_codes[country], indicator_code)
        if df is not None:
            plt.plot(df["date"], df["value"], marker="o", label=country)

    plt.title(f"{indicator_name}")
    plt.xlabel("Year")
    plt.ylabel(indicator_name)
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)   # ✅ Use Streamlit to render the figure




