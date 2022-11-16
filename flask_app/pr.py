from flask import Flask, render_template, request, redirect, url_for,jsonify
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import pickle
from tensorflow import keras
    
home_rank = 20
home_squad_size = 20
home_avg_age = 30
home_total_value = 20000
away_rank = 50  
away_squad_size = 20
away_avg_age = 30
away_total_value = 10000

X = np.array([[home_rank, home_squad_size, home_avg_age, home_total_value, 
away_rank, away_squad_size, away_avg_age, away_total_value]])

model = keras.models.load_model('worldcup_modelv1.h5')
pred = model.predict(X)

# model = keras.models.load_model('worldcup_modelv1.h5')
# pred = model.predict(X)

list = ['away win', 'draw', 'home win']

print(list[np.argmax(pred[0])])

