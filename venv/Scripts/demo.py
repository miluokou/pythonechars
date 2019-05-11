from flask import Flask,render_template,url_for
import pymssql
from sql import MSSQL
from pymongo import MongoClient
import collections.abc
# //pip install pymongo

app = Flask(__name__)


ms = MSSQL(host="localhost", user="sa", pwd="root", db="xinhai")
client = MongoClient('localhost', 27017)
url = 'http://example.webscraping.com/view/united-kingdom-239'
html = 'f'
db = client.cache
resListValue = ms.ExecQuery("SELECT score_raw,score_t from v_result where score_raw is not null and score_t is not null")
db.resList.insert({'key': 'resListKey', 'resListValue': resListValue})
ressss = db.webpage.find_one({'key': ''})

# try:
#     if 'resList' in db:
#         resListRes = db.resList
#     # else:
#     #     db.resList = ms.ExecQuery("SELECT COUNT(1) from v_result;")
#     #     resListRes = db.resList
# except :
#     db.resList = ms.ExecQuery("SELECT COUNT(1) from v_result;")
#     resListRes = db.resList
#     pass


# @app.route('/demo')
# def my_echart():
    # resList = ms.ExecQuery("SELECT top(2) * FROM v_result")
    # resList = ms.ExecQuery("SELECT COUNT(1) from v_result;")
    # return render_template('my_template.html',resList =resList)
@app.route('/')
def index():


    return render_template('hello.html',db=ressss[html])

# @app.route('/hello')
# def hello():
    # return json.dumps(resList, ensure_ascii=False)
    # return render_template('hello.html',resList=resListRes)

if __name__ == "__main__":

    app.run(debug = True)

