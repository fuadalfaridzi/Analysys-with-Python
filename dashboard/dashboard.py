import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
merged_data = pd.read_csv("merged_file.csv")


# Convert 'dteday' to datetime format
merged_data['dteday'] = pd.to_datetime(merged_data['dteday'])

# Set consistent color palettes
sns.set_palette("coolwarm")

# Dashboard Title
st.title("Bike Rental Data Dashboard")

# Documentation for each section
st.markdown("## Introduction")
st.markdown("""
This dashboard analyzes bike rental data, focusing on seasonal trends, weather conditions, and peak rental times. The data has been merged from two different sources, providing both hourly and daily insights.
""")

# 1. Daily Bike Rentals Over Time
st.subheader("Daily Bike Rentals Over Time")
st.markdown("""
This section visualizes the total bike rentals over time, with a highlight on the most recent day of rentals.
""")

recent_day = merged_data.groupby('dteday')['cnt_day'].sum().reset_index()
most_recent_day = recent_day.sort_values(by='dteday', ascending=False).head(1)

st.write(f"The most recent day with bike rentals: **{most_recent_day['dteday'].iloc[0].date()}**")

# Visualization for Daily Rentals
plt.figure(figsize=(12, 6))
sns.lineplot(x='dteday', y='cnt_day', data=recent_day, color='blue')
plt.title('Daily Bike Rentals Over Time')
plt.xlabel('Date')
plt.ylabel('Total Rentals')
plt.axvline(x=most_recent_day['dteday'].iloc[0], color='red', linestyle='--', label='Most Recent Rental Day')
plt.legend()
st.pyplot(plt)

# 2. Season with the Most Rented Bikes
st.subheader("Total Bike Rentals by Season")
st.markdown("""
This section identifies which season had the most bike rentals, providing insights into seasonal rental patterns.
""")

# Group by 'season' and sum the 'cnt_day' column
season_rentals = merged_data.groupby('season')['cnt_day'].sum().reset_index()
season_rentals['season'] = season_rentals['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
most_rented_season_name = season_rentals.sort_values(by='cnt_day', ascending=False).iloc[0]['season']


max_value = season_rentals['cnt_day'].max()
colors = ['blue' if value == max_value else 'lightblue' for value in season_rentals['cnt_day']]

# Visualization for Total Bike Rentals by Season
plt.figure(figsize=(8, 6))
sns.barplot(x='season', y='cnt_day', data=season_rentals, palette=colors)
plt.title('Total Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Total Rentals')
st.pyplot(plt)

st.write(f"The {most_rented_season_name} season experienced the highest number of bike rentals, indicating a peak in demand during this time") 

# 3. Bike Rentals by Weather Condition
st.subheader("Total Bike Rentals by Weather Condition")
st.markdown("""
This section analyzes the impact of weather conditions on bike rentals, highlighting which conditions are most favorable for rentals.
""")

weather_rentals = merged_data.groupby('weathersit_day')['cnt_day'].sum().reset_index()
weather_rentals['weathersit_day'] = weather_rentals['weathersit_day'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
})

# Visualization: Bike Rentals by Weather Condition
plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit_day', y='cnt_day', data=weather_rentals, palette='coolwarm')
plt.title('Total Bike Rentals by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Total Rentals')
plt.xticks(rotation=45)
st.pyplot(plt)

st.markdown("""
This dashboard provides a comprehensive view of bike rental trends and factors influencing them, such as season, weather, and time of day.
""")

# 4. Clustering Hourly Rentals
st.subheader("Clustering Hourly Rentals")
st.markdown("""
In this section, we cluster the bike rentals by hour to identify peak times for rentals.
""")

hour_df = pd.read_csv("dashboard/hour.csv")
geo_df = hour_df.groupby('hr')['cnt'].sum().reset_index()

# Plot the data to find hotspots
plt.figure(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', data=geo_df)
plt.title('Bike Rental Count by Hour of the Day')
plt.xlabel('Hour')
plt.ylabel('Number of Rentals')
plt.show()
st.pyplot(plt)


