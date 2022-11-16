from flask import Flask, render_template, request, redirect, url_for,jsonify
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import pickle
from tensorflow import keras
from logging import FileHandler,WARNING


app = Flask(__name__)
model = keras.models.load_model('worldcup_modelv1.h5')
#model = pickle.load(open('./model/model.pkl','rb'))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/worldcup')
def worldcup():

    conn = pymysql.connect(host='localhost', user='root', password='비밀번호 입력', #######비밀번호 입력 #############
    db='football', charset='utf8')

    cur = conn.cursor()

    cur.execute("""
    SELECT * 
    FROM all_data
    ORDER BY date DESC
    LIMIT 50;
    """)

    val = cur.fetchall()

    conn.close()

    # return render_template('worldcup.html', val = val)
    #return str(val)
    return render_template('worldcup.html', val=val)

@app.route('/worldcup/<nation>')
def all_data(nation):
    
    conn = pymysql.connect(host='localhost', user='root', password='비밀번호 입력', ### 비밀번호 입력 ###
    db='football', charset='utf8')

    cur = conn.cursor()

    cur.execute("""
    SELECT * 
    FROM all_data
    WHERE (home_team = %s) OR (away_team = %s)
    ORDER BY date DESC
    LIMIT 50;
    """,[nation, nation])

    val = cur.fetchall()

    conn.close()

    return render_template('nation_records.html',nation = nation, val=val)



@app.route('/pred', methods=['GET','POST'])
def pred():
    return render_template('keras.html')


@app.route('/pred_confirm', methods=['GET','POST'])
def pred_confirm():

    home_rank = float(request.form['home_rank'])
    home_squad_size = float(request.form['home_sq_size'])
    home_avg_age = float(request.form['home_avg_age'])
    home_total_value = float(request.form['home_T_value'])
    away_rank = float(request.form['away_rank'])
    away_squad_size = float(request.form['away_sq_size'])
    away_avg_age = float(request.form['away_avg_age'])
    away_total_value = float(request.form['away_T_value'])

    X = np.array([[home_rank, home_squad_size, home_avg_age, home_total_value, 
    away_rank, away_squad_size, away_avg_age, away_total_value]])

    
    pred = model.predict(X)
    
    list = ['away win', 'draw', 'home win']

    pred_value = list[np.argmax(pred[0])]


    conn = pymysql.connect(host='localhost', user='root', password='비밀번호 입력', ###########비밀번호 입력##############
    db='football', charset='utf8')

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE if not exists User_input (home_rank float, home_squad_size float, home_avg_age float,
    home_total_value float, away_rank float, away_squad_size float, away_avg_age float, away_total_value float, result VARCHAR(10));""")

    cur.execute(f"""
    INSERT INTO User_input (home_rank, home_squad_size, home_avg_age,
    home_total_value, away_rank, away_squad_size, away_avg_age, away_total_value, result) VALUES ({home_rank}, {home_squad_size},
    {home_avg_age}, {home_total_value}, {away_rank}, {away_squad_size}, {away_avg_age}, {away_total_value}, "{pred_value}");""")

    conn.commit()
    conn.close()

    return render_template('keras_confirm.html',pred_value=pred_value)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
    

if __name__ == "__main__":              
    app.run(debug=True)