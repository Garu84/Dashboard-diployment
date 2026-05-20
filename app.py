import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

st.write(
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

# cards

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

st.subheader("Retention Rate Trend Over Time")

retention_data = (
    filtered_df
    .groupby("Year")["Retention Rate (%)"]
    .mean()
    .reset_index())

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.lineplot(
    data=retention_data,
    x="Year",
    y="Retention Rate (%)",
    marker="o",
    ax=ax1)

ax1.set_title("Retention Rate Trend Over Time")

st.pyplot(fig1)

# satisfation chart bard

st.subheader("Student Satisfaction by Year")

satisfaction_data = (
    filtered_df
    .groupby("Year")["Student Satisfaction (%)"]
    .mean()
    .reset_index())

fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=satisfaction_data,
    x="Year",
    y="Student Satisfaction (%)",
    ax=ax2)

ax2.set_title("Student Satisfaction by Year")

st.pyplot(fig2)

# spring vs fall pie chart

st.subheader("Spring vs Fall Enrollment Comparison")

term_data = (
    filtered_df
    .groupby("Term")["Enrolled"]
    .sum())

fig3, ax3 = plt.subplots(figsize=(7, 7))

ax3.pie(
    term_data,
    labels=term_data.index,
    autopct="%1.1f%%")

ax3.set_title("Spring vs Fall Enrollment Comparison")

st.pyplot(fig3)

# faculty distribution

st.subheader("Faculty Enrollment Distribution")

faculty_data = {
    "Engineering": filtered_df["Engineering Enrolled"].sum(),
    "Business": filtered_df["Business Enrolled"].sum(),
    "Arts": filtered_df["Arts Enrolled"].sum(),
    "Science": filtered_df["Science Enrolled"].sum()}

faculty_df = pd.DataFrame({
    "Faculty": faculty_data.keys(),
    "Students": faculty_data.values()})

fig4, ax4 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=faculty_df,
    x="Faculty",
    y="Students",
    ax=ax4)

ax4.set_title("Faculty Enrollment Distribution")

st.pyplot(fig4)

# Data table

st.subheader("Dataset Preview")

st.dataframe(filtered_df)