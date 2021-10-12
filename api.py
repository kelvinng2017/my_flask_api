from python_shutil_rmtree import *
import sys
import time
import json
import os
import datetime
from datetime import datetime as dt
import show_and_save_log_file
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

from flask import Flask
app = Flask(__name__)

my_server = MyServer()

@app.route("/getSomeData")
def getSomeData():
    kelvin_debug_log.logger.debug("hello")
    return my_server.globalData

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8787,debug=True)