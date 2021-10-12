from crypt import methods
from python_shutil_rmtree import *
import sys
import time
import json
import os
import datetime
from datetime import datetime as dt
import show_and_save_log_file
import numpy as np
import pandas as pd
#delete_log_file()

f =open('./config.json','r')
data = json.load(f)
f.close()
log_file_path = data.get('log_file_path')
timeNow = datetime.datetime.now()
file_name_time = timeNow.strftime("%Y-%m-%d_%Hh%Mm%Ss")
if not os.path.exists(os.path.join(os.getcwd()+log_file_path)):
    print("creeate log file folder")
    os.makedirs(os.path.join(os.getcwd()+""+log_file_path+""))
file_name_path = os.getcwd()+log_file_path
kelvin_debug_log = show_and_save_log_file.Logger(file_name_path+""+os.path.basename(__file__)+"_"+file_name_time +
                                    ".log", level='debug')

kelvin_debug_log.logger.debug("hello")

class MyServer:
    def __init__(self):
        self.globalData = "hello"
        self.tpe ={
            "id": 0,
            "city_name": "Taipei",
            "country_name": "Taiwan",
            "is_capital": True,
            "location": {
                "longitude": 121.569649,
                "latitude": 25.036786
            }
        }
        self.nyc = {
            "id": 1,
            "city_name": "New York",
            "country_name": "United States",
            "is_capital": False,
            "location": {
                "longitude": -74.004364,
                "latitude": 40.710405
            }
        }
        self.ldn = {
            "id": 2,
            "city_name": "London",
            "country_name": "United Kingdom",
            "is_capital": True,
            "location": {
                "longitude": -0.114089,
                "latitude": 51.507497
            }
        }
        self.cities = [self.tpe,self.nyc,self.ldn]
    
    def find_year(self,year):
        self.year =str(year+1)
        return self.year+" "+self.globalData
    
    def find_name(self,name):
        self.name = name

        return self.globalData+" "+self.name

    def read_csv(self,file_name):
        gapminder = pd.read_csv(file_name)
        self.gapminder_list = []
        nrows = gapminder.shape[0]
        for i in range(nrows):
            ser = gapminder.loc[i, :]
            row_dict = {}
            for idx, val in zip(ser.index, ser.values):
                if type(val) is str:
                    row_dict[idx] = val
                elif type(val) is np.int64:
                    row_dict[idx] = int(val)
                elif type(val) is np.float64:
                    row_dict[idx] = float(val)
            self.gapminder_list.append(row_dict)
        return self.gapminder_list

from flask import Flask
from flask import jsonify, request
app = Flask(__name__)
#app.config["JSON_AS_ADCII"] = True

my_server = MyServer()

@app.route("/",methods=['GET'])
def getSomeData():
    kelvin_debug_log.logger.debug("hello")
    return "<h1>"+my_server.find_name("Flask!")+"</h1>"


@app.route('/cities/all', methods=['GET'])
def cities_all():
    return jsonify(my_server.cities)

@app.route('/cities',methods=['GET'])
def city_name():
    if 'city_name' in request.args:
        city_name = request.args['city_name']
    else:
        return "Error: No city_name provided. Plsease specify a city name."
    results = []
    for city in  my_server.cities:
        if city['city_name'] == city_name:
            results.append(city)
    return jsonify(results)
    
@app.route('/gapminder/all', methods=['GET'])
def gapminder_all():
    return jsonify(my_server.read_csv("gapminder.csv"))

@app.route('/gapminder', methods=['GET'])
def country():
    if 'country' in request.args:
        country = request.args['country']
    else:
        return "Error: No country provided. Please specify a country."
    results = []

    for elem in my_server.read_csv("gapminder.csv"):
        if elem['country'] == country:
            results.append(elem)

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8788,debug=True)