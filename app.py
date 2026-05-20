import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="University Analytics Dashboard",
    layout="wide")

# load data
@st.cache_data
def load_data():
    return pd.read_csv("university_student_data.csv")

df = load_data()

# title
st.title("University Student Analytics Dashboard")

st.markdown(
    "Interactive dashboard for enrollment, retention, and student satisfaction analysis.")

# sidebar filters
st.sidebar.header("Dashboard Filters")

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique()))

selected_terms = st.sidebar.multiselect(
    "Select Term",
    options=df["Term"].unique(),
    default=df["Term"].unique())

# filter data
filtered_df = df[
    (df["Year"].isin(selected_years)) &
    (df["Term"].isin(selected_terms))]

# kpi cards

avg_retention = round(filtered_df["Retention Rate (%)"].mean(), 2)
avg_satisfaction = round(filtered_df["Student Satisfaction (%)"].mean(), 2)
total_enrolled = filtered_df["Enrolled"].sum()
total_applications = filtered_df["Applications"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Retention", f"{avg_retention}%")
col2.metric("Average Satisfaction", f"{avg_satisfaction}%")
col3.metric("Total Enrolled", total_enrolled)
col4.metric("Applications", total_applications)

# retention trend

retention_data = (
    filtered_df
    .groupby("Year")["Retention Rate (%)"]
    .mean()
    .reset_index())

fig1 = px.line(
    retention_data,
    x="Year",
    y="Retention Rate (%)",
    markers=True,
    title="Retention Rate Trend Over Time")

st.plotly_chart(fig1, use_container_width=True)

# satisfation barchar

satisfaction_data = (
    filtered_df
    .groupby("Year")["Student Satisfaction (%)"]
    .mean()
    .reset_index())

fig2 = px.bar(
    satisfaction_data,
    x="Year",
    y="Student Satisfaction (%)",
    title="Student Satisfaction by Year")

st.plotly_chart(fig2, use_container_width=True)

# spting vs fall pie chart

term_data = (
    filtered_df
    .groupby("Term")["Enrolled"]
    .sum()
    .reset_index())

fig3 = px.pie(
    term_data,
    values="Enrolled",
    names="Term",
    title="Spring vs Fall Enrollment Comparison",
    hole=0.4)

st.plotly_chart(fig3, use_container_width=True)

# faculty distribution

faculty_df = pd.DataFrame({
    "Faculty": ["Engineering", "Business", "Arts", "Science"],
    "Students": [
        filtered_df["Engineering Enrolled"].sum(),
        filtered_df["Business Enrolled"].sum(),
        filtered_df["Arts Enrolled"].sum(),
        filtered_df["Science Enrolled"].sum()]})

fig4 = px.bar(
    faculty_df,
    x="Faculty",
    y="Students",
    title="Faculty Enrollment Distribution")

st.plotly_chart(fig4, use_container_width=True)

# data table
st.subheader("Dataset Preview")
st.dataframe(filtered_df)
