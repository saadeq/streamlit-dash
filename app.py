import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime
import yfinance as yf



st.title('streamlit dashboard')
st.markdown("""
BTC candlestick chart in  different Timeframe
""")

option = st.selectbox("select your Timeframe",
                      ('month', 'week', 'day')
                     )

st.write('you selected', option)
#if option == 'month':
    #st.write('it work')
tickerSymbol = 'BTC-USD'
today = datetime.now()

if option == 'month':
    option = '1mo'
elif option == 'week':
    option = '1wk'    
elif option == 'day':
    option = '1D'  
else:
    option = '1mo'   

def get_data(ticker):
    tickerData = yf.Ticker(ticker)
    tickerDf = tickerData.history(start='2015-1-2', end=today, interval=option)
    return tickerDf
dff = get_data(tickerSymbol) 
#st.write('#')

fig = go.Figure(data=[go.Candlestick(x=dff.index,
                open=dff['Open'], high=dff['High'],
                low=dff['Low'], close=dff['Close'])
                     ])
fig.update_layout(xaxis_rangeslider_visible=False, title="Price of BTC over Time", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig)


st.write('#')
st.markdown("""
this app create just for test deploy project on streamlit cloud
""")

df = pd.DataFrame({
    "Date": ["2023-01-03", "2023-03-01", "2022-05-01", "2022-05-30", "2022-01-05"],
    "N_active": [25, 36, 22, 42, 25]
})


df["Date"] = pd.to_datetime(df["Date"])

# Create the "Quarter" column
df["Quarter"] = pd.PeriodIndex(df["Date"], freq="Q")
st.write('#')

quarterly_sum = df.groupby("Quarter")["N_active"].sum()

st.write('### bar chart')

def plot_bar_chart(data):
    fig = go.Figure(data=[go.Bar(x=data.index.strftime("%Y-Q%q"), y=data.values)])
    fig.update_layout(title="Quarterly Active Users", xaxis_title="Quarter", yaxis_title="N_active")
    st.plotly_chart(fig)


quarters = quarterly_sum.index.strftime("%Y-Q%q").tolist()
st.write('#')
selected_quarters = st.multiselect("Select Quarters", quarters, default=quarters)

# Filter the quarterly_sum data for the selected quarters
filtered_data = quarterly_sum[quarterly_sum.index.strftime("%Y-Q%q").isin(selected_quarters)]
st.write('#')

plot_bar_chart(filtered_data)

