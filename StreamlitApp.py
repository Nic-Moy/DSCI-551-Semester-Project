#Nicolas Moy
#DSCI 551 Semester Project

import streamlit as st
from Project import load_csv, dataFrame

st.set_page_config(page_title="NBA Data Analysis", layout="wide", page_icon="🏀")

st.title("🏀 NBA 2022/2023 Season Data Analysis")

csv_options = {
    "Player Stats": "NBA CSVs/player.csv",
    "Warriors Stats": "NBA CSVs/WarriorsStats.csv"
}
selected_file = st.selectbox("Select a dataset", list(csv_options.keys()))
data, column_names = load_csv(csv_options[selected_file])
df = dataFrame(data, column_names)

#Show the loaded DataFrame using st.write() or custom display
st.subheader("Raw Data")
st.write(f"Shape: {df.shape}")
st.text(df)  # Uses the __str__ method (first 10 rows, 5 columns)

#Option to show all data:
if st.checkbox("Show all rows and columns"):
    st.text(df.display_all())
