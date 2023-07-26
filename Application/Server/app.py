#import Flask 
from flask import Flask, render_template, request
import numpy as np
#import pandas as pd
import joblib
import imdb
import os

MoviesData= joblib.load('Movies_Datase.pkl') 
X = joblib.load('Movies_Learned_Features.pkl') 
my_ratings = np.zeros((9724,1))
my_movies=[]
my_added_movies=[]

def computeCost(X, y, theta):
   m=y.size
   s=np.dot(X,theta)-y
   j=(1/(2*m))*(np.dot(np.transpose(s),s))
   print(j)
   return j

def gradientDescent(X, y, theta, alpha, num_iters):  
    m = float(y.shape[0])
    theta = theta.copy()
    for i in range(num_iters):
        theta=(theta)-(alpha/m)*(np.dot(np.transpose((np.dot(X,theta)-y)),X))
    return theta


def checkAndAdd(movie,rating):
    try:
            if isinstance(int(rating), str):
                    pass
    except ValueError:
            return (3)
    if (int(rating) <= 5 and int(rating) >= 0):
            movie = movie.lower()
            movie=movie+' '
            if movie not in MoviesData['title'].unique():
                return(1)
            else:
                index=MoviesData[MoviesData['title']==movie].index.values[0]
                my_ratings[index] = rating
                movieid=MoviesData.loc[MoviesData['title']==movie, 'movieid']
                if movie in my_added_movies:
                        return(2)
                my_movies.append(movieid)
                my_added_movies.append(movie)
                return(0)
    else:
            return(-1)
def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url
#create an instance of Flask
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/addMovie/', methods=['GET','POST'])
def addMovie():
    val=request.form.get('movie_name')
    rating=request.form.get('rating')
    flag=checkAndAdd(val,rating)
    if (flag==1):
            processed_text="Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"
            return render_template('home.html',processed_text=processed_text)
    elif (flag==-1):
            processed_text="please enter rating between 1-5 this application follows five-star rating system"
            return render_template('home.html',processed_text=processed_text)
    elif (flag==2):
            processed_text="The movie has already been added by you"
            return render_template('home.html',processed_text=processed_text)
    elif (flag==3):
            processed_text="Invalid Input! Please enter a number between 0-5 in the rating field"
            return render_template('home.html',processed_text=processed_text)
    else:        
            processed_text="Successfully added movie to your rated movies"
            movie_text=", you've rated "+rating+" stars to movie: "+val
            
            return render_template('home.html',processed_text=processed_text,movie_text=movie_text,my_added_movies=my_added_movies)
    
@app.route('/reset/', methods=['GET','POST'])
def reset():
        global my_ratings
        global my_movies
        global my_added_movies
        
        my_ratings = np.zeros((9724,1))
        my_movies=[]
        my_added_movies=[]
        processed_text='Successfull reset'
        return render_template('home.html',processed_text=processed_text)