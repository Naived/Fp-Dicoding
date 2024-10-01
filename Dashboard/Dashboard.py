import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data_file = 'RTUD.csv'  # The path to your data
df = pd.read_csv(data_file)

# Convert 'order_approved_at' column to datetime and handle missing values
df['order_approved_at'] = pd.to_datetime(df['order_approved_at'], errors='coerce')
filtered_df = df.dropna(subset=['order_approved_at'])  # Drop rows where 'order_approved_at' is missing

# Sidebar for date range selection
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", filtered_df['order_approved_at'].min())
end_date = st.sidebar.date_input("End Date", filtered_df['order_approved_at'].max())

# Filter data based on the selected date range
filtered_df = filtered_df[(filtered_df['order_approved_at'] >= pd.to_datetime(start_date)) & 
                          (filtered_df['order_approved_at'] <= pd.to_datetime(end_date))]


# Main Title
st.title("E-Commerce Public Data Analysis")

# Key Metrics
total_orders = filtered_df['order_id'].nunique()
total_revenue = filtered_df['price'].sum()
st.subheader(f"Total Orders: {total_orders}")
st.subheader(f"Total Revenue: R$ {total_revenue:,.2f}")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
daily_orders = filtered_df.groupby(filtered_df['order_approved_at'].dt.date)['order_id'].count()
st.line_chart(daily_orders)

# Customer Spend Money
st.subheader("Customer Spend Money")
daily_spend = filtered_df.groupby(filtered_df['order_approved_at'].dt.date)['price'].sum()
st.line_chart(daily_spend)

# Order Items
st.subheader("Order Items")
total_items = filtered_df['order_item_id'].count()
average_items = filtered_df.groupby('order_id')['order_item_id'].count().mean()
st.write(f"Total Items: {total_items}")
st.write(f"Average Items per Order: {average_items:.2f}")

# Order Items by Product Category
st.subheader("Order Items by Category")
category_sales = filtered_df['product_category_name_english'].value_counts().head(10)
fig = px.bar(category_sales, x=category_sales.index, y=category_sales.values, labels={'x':'Category', 'y':'Sales'})
st.plotly_chart(fig)

# Review Scores
st.subheader("Review Scores")
review_scores = filtered_df['review_score'].value_counts().sort_index()
fig = px.bar(review_scores, x=review_scores.index, y=review_scores.values, labels={'x':'Rating', 'y':'Count'})
st.plotly_chart(fig)

# Customer Demographics
st.subheader("Customer Demographics")
customer_state_counts = filtered_df['customer_state'].value_counts().head(10)
fig = px.bar(customer_state_counts, x=customer_state_counts.index, y=customer_state_counts.values, labels={'x':'State', 'y':'Number of Customers'})
st.plotly_chart(fig)

# Copyright Section
st.markdown("Copyright (C) Naived")