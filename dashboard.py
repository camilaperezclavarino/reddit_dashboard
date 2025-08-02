import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("reddit_data.csv", parse_dates=["date"])
    return df
df = load_data()
# --------------------Mental Health Filter--------------------
mental_states = df["mental state"].fillna("Unknown").unique() #replaces empty w/ "Unknown", makes list of mental states
st.sidebar.header("Filter Posts by Mental State")
selected_states = st.sidebar.multiselect("Select Mental State(s)", mental_states, default = mental_states)

#-------------------Filter Data---------------------
filtered_data = df[df["mental state"].fillna("Unknown").isin(selected_states)]


#------------------Data Display----------------------
st.title("Reddit Data")

# Daily Post Volume
daily_posts_data = filtered_data.groupby("date").size().reset_index(name="post_count") #creates data frame w 2 columns (date and post count)
dp_line_chart = px.line(daily_posts_data, x = "date", y = "post_count", title="Daily Post Volume", labels={
    "date": "Day",
    "post_count": "Number of Posts"
})
dp_line_chart.update_traces(hovertemplate="Date: %{x|%Y-%m-%d}<br>Posts: %{y}") #
st.plotly_chart(dp_line_chart)


# Mental State Breakdown
mental_state_counts = filtered_data.fillna("Unknown")["mental state"].value_counts().reset_index() #creates data frame w mental state and count columns
# mental_state_chart = px.bar(mental_state_counts, x="mental state", y="count", title="Mental State Breakdown", labels={
#     "mental state": "Mental State",
#     "count": "Number of Posts with Mental State"
# })

chart_type = st.radio("Select chart type for mental state breakdown:", ["Bar Chart", "Pie Chart"])


if chart_type == "Bar Chart":
    mental_state_chart = px.bar(mental_state_counts, x="mental state", y="count", title="Mental State Breakdown", labels={
    "mental state": "Mental State",
    "count": "Number of Posts with Mental State"
})
    mental_state_chart.update_traces(hovertemplate="Mental State: %{x}<br>Posts: %{y}")
else:
    mental_state_chart = px.pie(mental_state_counts, values = "count", names="mental state", title="Mental State Breakdown", labels={
    "mental state": "Mental State",
    "count": "Number of Posts"
})
    mental_state_chart.update_traces(hovertemplate="Mental State: %{label}<br>Posts: %{value}")



st.plotly_chart(mental_state_chart)


#
