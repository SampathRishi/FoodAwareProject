import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="FOODAWARE - Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF5722;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .chart-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #e1f5fe;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0277BD;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='main-header'>📊 FOODAWARE Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Insights Dashboard for Food Recommendation System</p>", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_connection():
    conn = sqlite3.connect('./database/database.db')
    return conn

# Load data from database
@st.cache_data
def load_data():
    conn = get_connection()
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    food_items_df = pd.read_sql_query("SELECT * FROM food_items", conn)
    orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
    return users_df, food_items_df, orders_df

# Load data
users_df, food_items_df, orders_df = load_data()

# Sidebar with filters
with st.sidebar:
    st.markdown("<h2 class='sub-header'>Filters</h2>", unsafe_allow_html=True)
    
    # Date range filter
    st.write("**Date Range**")
    
    # Convert timestamp to datetime
    orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
    min_date = orders_df['timestamp'].min().date()
    max_date = orders_df['timestamp'].max().date()
    
    start_date = st.date_input("Start Date", min_date)
    end_date = st.date_input("End Date", max_date)
    
    # Weather filter
    st.write("**Weather Condition**")
    weather_options = ["All"] + list(orders_df['weather'].unique())
    selected_weather = st.selectbox("Select Weather", weather_options)
    
    # Mood filter
    st.write("**User Mood**")
    mood_options = ["All"] + list(orders_df['mood'].unique())
    selected_mood = st.selectbox("Select Mood", mood_options)
    
    # Apply filters
    filtered_orders = orders_df.copy()
    
    # Date filter
    filtered_orders = filtered_orders[(filtered_orders['timestamp'].dt.date >= start_date) & 
                                     (filtered_orders['timestamp'].dt.date <= end_date)]
    
    # Weather filter
    if selected_weather != "All":
        filtered_orders = filtered_orders[filtered_orders['weather'] == selected_weather]
    
    # Mood filter
    if selected_mood != "All":
        filtered_orders = filtered_orders[filtered_orders['mood'] == selected_mood]
    
    # Show filter summary
    st.markdown("---")
    st.write("**Active Filters:**")
    st.write(f"Date Range: {start_date} to {end_date}")
    st.write(f"Weather: {selected_weather}")
    st.write(f"Mood: {selected_mood}")
    st.write(f"Total Orders: {len(filtered_orders)}")

# Main dashboard area
tab1, tab2, tab3 = st.tabs(["Overview", "Food Analysis", "User Behavior"])

# Tab 1: Overview
with tab1:
    st.markdown("<h2 class='sub-header'>System Overview</h2>", unsafe_allow_html=True)
    
    # Key metrics row
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(users_df)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Users</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metrics_col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(food_items_df)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Food Items</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metrics_col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(filtered_orders)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total Orders</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metrics_col4:
        # Calculate average rating
        avg_rating = filtered_orders['rating'].mean() if 'rating' in filtered_orders.columns else 0
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{avg_rating:.1f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Avg. Rating</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Orders over time chart
    st.markdown("<h3>Orders Over Time</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Group by date and count orders
    orders_by_date = filtered_orders.groupby(filtered_orders['timestamp'].dt.date).size().reset_index(name='count')
    orders_by_date.columns = ['date', 'count']
    
    # Create time series chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(orders_by_date['date'], orders_by_date['count'], marker='o', linestyle='-', color='#1976D2')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Orders')
    ax.set_title('Orders Trend Over Time')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Weather and Mood Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Weather Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Count orders by weather
        weather_counts = filtered_orders['weather'].value_counts()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True, explode=[0.05] * len(weather_counts),
              colors=plt.cm.tab10.colors)
        ax.axis('equal')
        ax.set_title('Order Distribution by Weather')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Mood Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Count orders by mood
        mood_counts = filtered_orders['mood'].value_counts()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(mood_counts, labels=mood_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True, explode=[0.05] * len(mood_counts),
              colors=plt.cm.Set3.colors)
        ax.axis('equal')
        ax.set_title('Order Distribution by Mood')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: Food Analysis
with tab2:
    st.markdown("<h2 class='sub-header'>Food Items Analysis</h2>", unsafe_allow_html=True)
    
    # Merge food items with orders to get item popularity
    merged_df = pd.merge(
        filtered_orders, 
        food_items_df,
        left_on='food_id',
        right_on='food_id'
    )
    
    # Top Food Items
    st.markdown("<h3>Most Popular Food Items</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Count orders by food item
    food_popularity = merged_df['name'].value_counts().reset_index()
    food_popularity.columns = ['Food Item', 'Order Count']
    food_popularity = food_popularity.head(10)  # Top 10
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_plot = sns.barplot(x='Order Count', y='Food Item', data=food_popularity, palette='viridis')
    ax.set_xlabel('Number of Orders')
    ax.set_ylabel('Food Item')
    ax.set_title('Top 10 Most Popular Food Items')
    
    # Add count labels
    for i, v in enumerate(food_popularity['Order Count']):
        ax.text(v + 0.5, i, str(v), va='center')
    
    st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Food Distribution by Cuisine and Category
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Distribution by Cuisine</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Count orders by cuisine
        cuisine_counts = merged_df['cuisine'].value_counts()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(cuisine_counts, labels=cuisine_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True, explode=[0.05] * len(cuisine_counts),
              colors=plt.cm.tab20.colors)
        ax.axis('equal')
        ax.set_title('Order Distribution by Cuisine')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Distribution by Category</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Count orders by category
        category_counts = merged_df['category'].value_counts()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True, explode=[0.05] * len(category_counts),
              colors=plt.cm.Pastel1.colors)
        ax.axis('equal')
        ax.set_title('Order Distribution by Food Category')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Weather-Food Matrix
    st.markdown("<h3>Weather-Food Relationship Matrix</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Create a matrix of weather vs food categories
    if 'category' in merged_df.columns and 'weather' in merged_df.columns:
        matrix_data = pd.crosstab(merged_df['weather'], merged_df['category'])
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        heatmap = sns.heatmap(matrix_data, annot=True, cmap='YlGnBu', fmt='d', cbar_kws={'label': 'Number of Orders'})
        ax.set_xlabel('Food Category')
        ax.set_ylabel('Weather')
        ax.set_title('Relationship Between Weather and Food Category')
        st.pyplot(fig)
    else:
        st.warning("Missing data columns for Weather-Food matrix")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Similar situation with Mood-Food Matrix
    st.markdown("<h3>Mood-Food Relationship Matrix</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Create a matrix of mood vs food categories
    if 'category' in merged_df.columns and 'mood' in merged_df.columns:
        matrix_data = pd.crosstab(merged_df['mood'], merged_df['category'])
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        heatmap = sns.heatmap(matrix_data, annot=True, cmap='RdPu', fmt='d', cbar_kws={'label': 'Number of Orders'})
        ax.set_xlabel('Food Category')
        ax.set_ylabel('Mood')
        ax.set_title('Relationship Between Mood and Food Category')
        st.pyplot(fig)
    else:
        st.warning("Missing data columns for Mood-Food matrix")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: User Behavior
with tab3:
    st.markdown("<h2 class='sub-header'>User Behavior Analysis</h2>", unsafe_allow_html=True)
    
    # User Demographics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Age Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Create histogram of user ages
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(users_df['age'], bins=10, kde=True, color='skyblue')
        ax.set_xlabel('Age')
        ax.set_ylabel('Number of Users')
        ax.set_title('User Age Distribution')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Gender Distribution</h3>", unsafe_allow_html=True)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Count users by gender
        gender_counts = users_df['gender'].value_counts()
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', 
              startangle=90, shadow=True, explode=[0.05] * len(gender_counts),
              colors=['#ff9999','#66b3ff'])
        ax.axis('equal')
        ax.set_title('User Gender Distribution')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # User Order Frequency
    st.markdown("<h3>User Order Frequency</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Count orders by user
    user_order_counts = filtered_orders['user_id'].value_counts().reset_index()
    user_order_counts.columns = ['User ID', 'Order Count']
    
    # Merge with user data to get names
    user_order_counts = pd.merge(
        user_order_counts,
        users_df[['user_id', 'name']],
        left_on='User ID',
        right_on='user_id'
    ).drop('user_id', axis=1)
    
    # Sort and get top 10
    user_order_counts = user_order_counts.sort_values('Order Count', ascending=False).head(10)
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_plot = sns.barplot(x='Order Count', y='name', data=user_order_counts, palette='mako')
    ax.set_xlabel('Number of Orders')
    ax.set_ylabel('User Name')
    ax.set_title('Top 10 Users by Order Frequency')
    
    # Add count labels
    for i, v in enumerate(user_order_counts['Order Count']):
        ax.text(v + 0.5, i, str(v), va='center')
    
    st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # User Cuisine Preferences
    st.markdown("<h3>User Cuisine Preferences</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Extract cuisine preferences (handling different formats)
    cuisine_preferences = []
    for pref in users_df['cuisine_preferences']:
        if isinstance(pref, str):
            if '[' in pref:
                # Handle list stored as string
                try:
                    prefs = eval(pref)
                    cuisine_preferences.extend(prefs)
                except:
                    # Fallback if eval fails
                    cuisine_preferences.append(pref)
            else:
                # Handle comma-separated string
                prefs = [p.strip() for p in pref.split(',')]
                cuisine_preferences.extend(prefs)
    
    # Count preferences
    cuisine_counts = pd.Series(cuisine_preferences).value_counts()
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_plot = sns.barplot(x=cuisine_counts.values, y=cuisine_counts.index, palette='viridis')
    ax.set_xlabel('Number of Users')
    ax.set_ylabel('Cuisine')
    ax.set_title('User Cuisine Preferences')
    
    # Add count labels
    for i, v in enumerate(cuisine_counts.values):
        ax.text(v + 0.5, i, str(v), va='center')
    
    st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dietary Restrictions
    st.markdown("<h3>User Dietary Restrictions</h3>", unsafe_allow_html=True)
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Extract dietary restrictions (handling different formats)
    dietary_restrictions = []
    for restriction in users_df['dietary_restrictions']:
        if isinstance(restriction, str):
            if '[' in restriction:
                # Handle list stored as string
                try:
                    restrictions = eval(restriction)
                    dietary_restrictions.extend(restrictions)
                except:
                    # Fallback if eval fails
                    dietary_restrictions.append(restriction)
            else:
                # Handle comma-separated string
                restrictions = [r.strip() for r in restriction.split(',')]
                dietary_restrictions.extend(restrictions)
    
    # Count restrictions
    dietary_counts = pd.Series(dietary_restrictions).value_counts()
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_plot = sns.barplot(x=dietary_counts.values, y=dietary_counts.index, palette='mako')
    ax.set_xlabel('Number of Users')
    ax.set_ylabel('Dietary Restriction')
    ax.set_title('User Dietary Restrictions')
    
    # Add count labels
    for i, v in enumerate(dietary_counts.values):
        ax.text(v + 0.5, i, str(v), va='center')
    
    st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("FOODAWARE - Analytics Dashboard - Final Project")
st.markdown("© 2025 - All Rights Reserved")