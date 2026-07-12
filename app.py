
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title('Data Cleaning & EDA Web App')
st.write('This is an interactive web application to showcase the cleaned dataset and its exploratory data analysis.')

# Load the cleaned data
@st.cache_data
def load_data():
    data = pd.read_csv('cleaned_dataset.csv')
    return data

df_cleaned = load_data()

st.header('Cleaned Dataset')
st.dataframe(df_cleaned)

st.header('Summary Statistics for Score')
st.write(df_cleaned['Score'].describe())

# You can add more visualizations here from your EDA steps
# For example, a histogram of the 'Score' column:
import matplotlib.pyplot as plt
import seaborn as sns

st.header('Distribution of Scores')
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
sns.histplot(df_cleaned['Score'], kde=True, ax=ax_hist)
ax_hist.set_title('Distribution of Scores')
ax_hist.set_xlabel('Score')
ax_hist.set_ylabel('Frequency')
st.pyplot(fig_hist)


# You can also add the Average Score by City Bar Plot
st.header('Average Score by City')
avg_score_by_city = df_cleaned.groupby('City')['Score'].mean().sort_values(ascending=False).reset_index()
fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
sns.barplot(x='City', y='Score', data=avg_score_by_city, hue='City', palette='viridis', legend=False, ax=ax_bar)
ax_bar.set_title('Average Score by City')
ax_bar.set_xlabel('City')
ax_bar.set_ylabel('Average Score')
ax_bar.tick_params(axis='x', rotation=45)
st.pyplot(fig_bar)
