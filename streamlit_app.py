import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ----------------------
# Streamlit Page Config
# ----------------------
st.set_page_config(
    page_title="Economic Indicators Visualizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Economic Indicators Visualizer")
st.markdown("Explore World Bank economic data interactively.")

# ----------------------
# Sidebar
# ----------------------
st.sidebar.header("Options")

# Select country/countries
countries = st.sidebar.multiselect(
    "Select Country/Countries",
    [
        # Africa
        "South Africa", "Nigeria", "Kenya", "Egypt", "Ghana",
        "Ethiopia", "Tanzania", "Uganda", "Morocco", "Algeria",
        "Zimbabwe", "Zambia", "Botswana", "Namibia", "Mozambique",
        "Angola", "Senegal", "Ivory Coast", "Cameroon",

        # North America
        "United States", "Canada", "Mexico",

        # South America
        "Brazil", "Argentina", "Chile", "Colombia", "Peru",

        # Europe
        "United Kingdom", "Germany", "France", "Italy", "Spain",
        "Netherlands", "Sweden", "Norway", "Switzerland", "Russia",

        # Asia
        "China", "India", "Japan", "South Korea", "Indonesia",
        "Saudi Arabia", "Turkey", "United Arab Emirates",
        "Pakistan", "Bangladesh",

        # Oceania
        "Australia", "New Zealand"
    ],
    default=["South Africa", "Nigeria"]
)
# Check if user selected at least one country
if not countries:
    st.warning("Please select at least one country from the sidebar.")
    st.stop()  # Stop execution until user selects a country

# Indicators
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
indicator_name = st.sidebar.selectbox("Select Indicator", list(indicators.keys()))
indicator_code = indicators[indicator_name]

# Year range
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=1961, max_value=2025,
    value=(2001, 2022)
)

# Log scale option
log_scale = st.sidebar.checkbox("Log Scale (Y-axis)", value=False)

# --------------------------------------------------------------------
# Fetch Data from World Bank API
# --------------------------------------------------------------------
def fetch_data(country, indicator, start, end):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start}:{end}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()[1]
            if data:
                values = []
                for item in data:
                    values.append({
                        "Country": item["country"]["value"],
                        "Year": int(item["date"]),
                        "Value": item["value"]
                    })
                return pd.DataFrame(values)
        except Exception as e:
            st.error(f"Error parsing data for {country}: {e}")
    else:
        st.error(f"Failed to fetch data for {country}")
    return pd.DataFrame(columns=["Country", "Year", "Value"])

# ----------------------
# Prepare Data
# ----------------------
all_data = pd.DataFrame()

for c in countries:
    # Convert human-readable country name to World Bank country code
    mapping = {
    # Africa
    "South Africa": "ZAF",
    "Nigeria": "NGA",
    "Kenya": "KEN",
    "Egypt": "EGY",
    "Ghana": "GHA",
    "Ethiopia": "ETH",
    "Tanzania": "TZA",
    "Uganda": "UGA",
    "Morocco": "MAR",
    "Algeria": "DZA",
    "Zimbabwe": "ZWE",
    "Zambia": "ZMB",
    "Botswana": "BWA",
    "Namibia": "NAM",
    "Mozambique": "MOZ",
    "Angola": "AGO",
    "Senegal": "SEN",
    "Ivory Coast": "CIV",
    "Cameroon": "CMR",

    # North America
    "United States": "USA",
    "Canada": "CAN",
    "Mexico": "MEX",

    # South America
    "Brazil": "BRA",
    "Argentina": "ARG",
    "Chile": "CHL",
    "Colombia": "COL",
    "Peru": "PER",

    # Europe
    "United Kingdom": "GBR",
    "Germany": "DEU",
    "France": "FRA",
    "Italy": "ITA",
    "Spain": "ESP",
    "Netherlands": "NLD",
    "Sweden": "SWE",
    "Norway": "NOR",
    "Switzerland": "CHE",
    "Russia": "RUS",

    # Asia
    "China": "CHN",
    "India": "IND",
    "Japan": "JPN",
    "South Korea": "KOR",
    "Indonesia": "IDN",
    "Saudi Arabia": "SAU",
    "Turkey": "TUR",
    "United Arab Emirates": "ARE",
    "Pakistan": "PAK",
    "Bangladesh": "BGD",

    # Oceania
    "Australia": "AUS",
    "New Zealand": "NZL"
    }
    country_code = mapping.get(c, "ZAF")

    df = fetch_data(country_code, indicator_code, start_year, end_year)
    all_data = pd.concat([all_data, df], ignore_index=True)

# ----------------------
# Visualization
# ----------------------
if not all_data.empty:
    fig = px.line(
        all_data,
        x="Year",
        y="Value",
        color="Country",
        title=f"{indicator_name} ({start_year}-{end_year})",
        log_y=log_scale
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📄 Raw Data")
    st.dataframe(all_data)
else:
    st.warning("No data available for the selected options.")
    
    # ----------------------
    # Extra Comparison: Latest Year
    # ----------------------
    latest_year = all_data["Year"].max()
    latest_data = all_data[all_data["Year"] == latest_year]

    if not latest_data.empty:
        st.subheader(f"📊 {indicator_name} in {latest_year}")
        fig_bar = px.bar(
            latest_data,
            x="Country",
            y="Value",
            color="Country",
            title=f"{indicator_name} Comparison ({latest_year})"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------------------------------------------------------------
    # Download Option
    # ---------------------------------------------------------------------
    st.subheader("⬇️ Download Data")
    csv = all_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="economic_data.csv",
        mime="text/csv"
    )


