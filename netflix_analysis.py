# -*- coding: utf-8 -*-
"""Netflix Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JaV6iCJnHLF0jjES8njT8w5cheFAaQ9a
"""

import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob

df=pd.read_csv('netflix_titles.csv')
df.shape

df.columns

df['director']

"""**RATINGS ON NETFLIX**"""

df['rating']

rating_group = df.groupby(['rating']).size().reset_index(name='counts')
rating_group

pieChart = px.pie(rating_group, values='counts', names='rating',
                  title='Distribution of Content Ratings on Netflix',
                  color_discrete_sequence=px.colors.qualitative.Set3)
pieChart.show()

"""**TOP 5 DIRECTORS ON NETFLIX**"""

df['director']=df['director'].fillna('No Director Mentioned')
df['director']

director_df=df['director'].str.split(',',expand=True).stack()
director_df

director_df=director_df.to_frame()
director_df

director_df.columns=['Director']
director_df

directors=director_df.groupby(['Director']).size().reset_index(name='Total Content')
directors

directors=directors[directors.Director !='No Director Specified']
directors=directors.sort_values(by=['Total Content'],ascending=False)
top_directors=directors.head()
top_directors

top_directors=top_directors.sort_values(by=['Total Content'])
top_directors

director_plot=px.bar(top_directors,x='Director',y='Total Content',title='Top 5 Directors on Netflix')
director_plot.show()

"""From above, Rajiv Chilaka is top Director on Netflix.

**TOP 5 ACTORS ON NETFLIX**
"""

df['cast']=df['cast'].fillna('No Cast Specified')
df['cast']

cast_df=df['cast'].str.split(',',expand=True).stack()
cast_df=cast_df.to_frame()
cast_df.columns=['Actor']
cast_df

actors_df=cast_df.groupby(['Actor']).size().reset_index(name='Total Content')
actors_df=actors_df[actors_df.Actor !='No Cast Specified']
actors_df

actors_df=actors_df.sort_values(by=['Total Content'],ascending=False)
top_actors=actors_df.head()
top_actors=top_actors.sort_values(by=['Total Content'])
top_actors

actor_plot=px.bar(top_actors,x='Actor',y='Total Content', title='Top 5 Actors on Netflix')
actor_plot.show()

"""From above plot, Anupam Kher is the top Actor on Netflix.

**CONTENT PRODUCED OVER YEARS**
"""

release_df=df[['type','release_year']]
release_df

release_df=release_df.rename(columns={"release_year": "Release Year"})
release_df

release_df=release_df.groupby(['Release Year','type']).size().reset_index(name='Total Content')
release_df

release_df=release_df[release_df['Release Year']>=2010]
release_df

release_plot = px.line(release_df, x="Release Year", y="Total Content", color='type',title='Content produced over the years on Netflix')
release_plot.show()

"""Both movies and TV shows have experienced decrease since 2018.

**SENTIMENT ANALYSIS ON NETFLIX**
"""

final_df=df[['release_year','description']]
final_df=final_df.rename(columns={'release_year':'Release Year'})
final_df

for index,row in final_df.iterrows():
    z=row['description']
    testimonial=TextBlob(z)
    p=testimonial.sentiment.polarity
    if p==0:
        sent='Neutral'
    elif p>0:
        sent='Positive'
    else:
        sent='Negative'
    final_df.loc[[index,2],'Sentiment']=sent

final_df

final_df=final_df.groupby(['Release Year','Sentiment']).size().reset_index(name='Total Content')
final_df

final_df=final_df[final_df['Release Year']>=2010]
sentiment_plot = px.bar(final_df, x="Release Year", y="Total Content", color="Sentiment", title="Sentiment of content on Netflix")
sentiment_plot.show()

"""
The graph illustrates that the combined quantity of positive content consistently surpasses the sum of neutral and negative content."""