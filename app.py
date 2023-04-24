import pandas as pd
import streamlit as st
import plotly.graph_objs as go

# Create the DataFrame
df = pd.DataFrame({
    "Date": ["2023-01-03", "2023-03-01", "2022-05-01", "2022-05-30", "2022-01-05"],
    "N_active": [25, 36, 22, 42, 25]
})


df["Date"] = pd.to_datetime(df["Date"])

# Create the "Quarter" column
df["Quarter"] = pd.PeriodIndex(df["Date"], freq="Q")
st.write(df)

quarterly_sum = df.groupby("Quarter")["N_active"].sum()
st.write(quarterly_sum)
# Define a function to plot the bar chart 
def plot_bar_chart(data):
    fig = go.Figure(data=[go.Bar(x=data.index.strftime("%Y-Q%q"), y=data.values)])
    fig.update_layout(title="Quarterly Active Users", xaxis_title="Quarter", yaxis_title="N_active")
    st.plotly_chart(fig)

# Use Streamlit's multiselect widget to allow the user to select which quarter to display
quarters = quarterly_sum.index.strftime("%Y-Q%q").tolist()
st.write(quarters)
selected_quarters = st.multiselect("Select Quarters", quarters, default=quarters)

# Filter the quarterly_sum data for the selected quarters
filtered_data = quarterly_sum[quarterly_sum.index.strftime("%Y-Q%q").isin(selected_quarters)]
st.write(filtered_data)

plot_bar_chart(filtered_data)
