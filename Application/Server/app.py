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
