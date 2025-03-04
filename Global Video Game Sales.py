#!/usr/bin/env python
# coding: utf-8

# # 🎮 Global Video Game Sales - Data Analysis
# 
# ## 📌 Project Overview
# This project analyzes global video game sales using a dataset from Kaggle. The aim of this project is to explore things like most popular genres, title, consoles and more.
# 
# ## 📊 Dataset Details
# - Source: Kaggle (Link : https://www.kaggle.com/datasets/asaniczka/video-game-sales-2024)
# 

# # 🔄 Data Loading & Preprocessing
# Before diving into analysis, let us load the dataset and inspect its structure.

# In[1]:


# Loading the dataset
import pandas as pd

video_games = pd.read_csv("/Users/venkat/Downloads/Global Video Game Sales/Video+Game+Sales/vgchartz-2024.csv")

# Checking the dataset
video_games.head()


# In[2]:


# Exploring the dataset

video_games.info()


# ## 🔧 Data Cleaning
# We handle missing and inconsistent data, rename columns for the sake of visualization and handle any incorrect data types

# In[3]:


# Check for null_values
video_games.isnull().sum()


# In[4]:


# Converting release_date column into datetime format

video_games['release_date'] = pd.to_datetime(video_games['release_date'],errors='coerce')

video_games.info()


# In[5]:


#Renaming columns for better understanding
video_games.rename(columns={'title':'Title','console':'Console','genre':'Genre','publisher':'Publisher','developer':'Developer'},inplace=True)

video_games.info()


# In[6]:


#Extracting release_year from the release_date column

video_games = video_games.assign(release_year = lambda x:x['release_date'].dt.year)

video_games.info()


# In[7]:


video_games.head()


# In[8]:


video_games.describe()


# # Exploratory Data Analysis

# ## 📈 Sales Trends Over the Years
# Analyzing yearly trends helps us understand how the gaming industry has evolved.

# In[9]:


#This dataframe calculates sum of total_sales by release_year

annual_sales = video_games.groupby('release_year',as_index=False).agg({'total_sales':'sum'})

annual_sales.head()


# In[10]:


# Creating a line chart here to plot total sales by year

import plotly.express as px

px.line(annual_sales,x='release_year',y='total_sales')


# # Top 10 titles

# In[11]:


#This dataframe contains the ten highest selling titles by total_sales ranked from highest to lowest

top10_titles = (
    video_games.groupby("Title",as_index=False).
    agg({'total_sales':'sum'}).
    sort_values('total_sales',ascending=False).
    iloc[:10]
)
top10_titles.head(10)


# In[12]:


#Creating a bar chart of the top ten selling titles of all time

px.bar(top10_titles,x='Title',y='total_sales')


# # Building a Dashboard

# In[ ]:


pip install jinja2==3.0.3


# In[13]:


# Import necessary libraries
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import numpy as np

# Load dataset, parse release_date as datetime, rename columns for clarity, and add a release_year column

video_games = (pd.read_csv("/Users/venkat/Downloads/Global Video Game Sales/Video+Game+Sales/vgchartz-2024.csv",parse_dates=['release_date']).
               rename({'title':'Title','console':'Console','genre':'Genre','publisher':'Publisher',
                       'developer':'Developer'},axis=1).
               assign(release_year = lambda x:x['release_date'].dt.year)
              )

# Initializing the Dash app

app = Dash(__name__)


# Defining the layout of the Dash app

app.layout = dbc.Container([
    html.H1("Video game explorer",style={'text-align':'center'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown("**Select A Category**"),
                dcc.Dropdown(
                id="category-dropdown",
                options=["Title","Genre","Publisher","Developer","Console"],value="Title",className="dbc"),
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dcc.Markdown("**Select A Region**"),
                dcc.RadioItems(
                id="region-radio",
                options={
                    'total_sales':'World Total',
                    'na_sales':'North America',
                    'jp_sales':"Japan",
                    'pal_sales':'Europe/Africa',
                    'other_sales':'Rest of World'}, value='total_sales',className="dbc"),
            ])
        ]),]),
    html.Br(),
    dbc.Row(dcc.Graph(id="sales-line")),
    html.Br(),
    dbc.Row(dcc.Graph(id="rankings-bar")),
])


# Defining the callback function to update both graphs based on user selections
@app.callback(
Output('sales-line','figure'),
Output('rankings-bar','figure'),
Input('category-dropdown','value'),
Input('region-radio','value'),
)

# The two charts created above have been added to the dashboard which will allow us to select title, genre, 
# publisher, developer and console with a dropdown and total_sales, jp_sales, na_sales, pal_sales 
# and other_sales with radio buttons



def vg_plotter(category, region):
    
    annual_sales=video_games.groupby("release_year",as_index=False).agg({region:"sum"})
    
    fig = px.line(
        annual_sales,
        x='release_year',
        y=region,
        title=f"Video Game Sales in {region} Over Time"
    ).update_layout(title_x=0.5)
    
    top10_sellers = (
        video_games
        .groupby(category, as_index=False)
        .agg({region:"sum"})
        .sort_values(region, ascending=False)
        .iloc[:10]
    )
    
    fig2 = px.bar(
        top10_sellers,
        x=category,
        y=region,
        title=f"Top Video Game Sales by Category"
    ).update_layout(title_x=0.5)
    
    return fig, fig2

#Run the dash app
if __name__ == "__main__":
    app.run_server()

               


# # 🏆 Key Insights & Takeaways
# 1. The Sports and Action genres dominate total global sales.
# 2. Video game sales peaked in the year 2008, with a decline afterward.
# 3. EA Canada tops the list for Video Game sales when categorised based on Developer
# 4. PS2 console dominates the industry.
