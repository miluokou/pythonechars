from flask import Flask,render_template,url_for
import pymssql
from pymongo import MongoClient
import collections.abc
# //pip install pymongo
from sql import MSSQL
app = Flask(__name__)


ms = MSSQL(host="localhost", user="sa", pwd="root", db="xinhai")
# resList = ms.ExecQuery("SELECT * FROM aat1")


# # print(resListValue)
client = MongoClient('localhost', 27017)
db = client.cache

def MongoCache(Query,sql):
    QueryKey = Query+'Key'
    QueryValue = Query+'Value'
    res = db[Query].find_one({QueryKey: 'resultTableQueryResult'})
    try:
        if QueryValue in res :
            resExist = res[QueryValue]
        else:
            # resultTableQueryResult = ms.ExecQuery("SELECT studentid,score_raw,score_t from result WHERE score_raw is not null")
            resExist = ms.ExecQuery(sql)
            db[Query].insert({QueryKey: 'resultTableQueryResult', QueryValue: resExist})
    except:
        resExist = ms.ExecQuery(sql)
        db[Query].insert({QueryKey: 'resultTableQueryResult', QueryValue: resExist})
        pass
    return resExist
resultSql = 'SELECT studentid,score_raw,score_t from result WHERE score_raw is not null'
resultExistRes = MongoCache('result',resultSql)

    # try:
    #     if 'QueryValue' in res :
    #         resExist = res['QueryValue']
    #     else:
    #         resultTableQueryResult = ms.ExecQuery("SELECT studentid,score_raw,score_t from result WHERE score_raw is not null")
    #         resExist =resultTableQueryResult
    #         db.MssQuery.insert({'QueryKey': 'resultTableQueryResult', 'QueryValue': resultTableQueryResult})
    # except:
    #     resultTableQueryResult = ms.ExecQuery("SELECT studentid,score_raw,score_t from result WHERE score_raw is not null")
    #     resExist = resultTableQueryResult
    #     db.MssQuery.insert({'QueryKey': 'resultTableQueryResult', 'QueryValue': resultTableQueryResult})
    #



# MongoRes = db.col.find()
# MongoRes = db.MssQuery.find_one({'key': 'resultTableQueryResult'})
# if "QueryValue" in MongoRes:
#     reflactData = db.MssQuery.
# db.resList.insert({'QueryKey': 'resultTableQueryResult', 'QueryValue': resultTableQueryResult})
# if 'resultTableQueryResult' in ressss:

# db.resList.insert({'key': 'resultTableSueryResult', 'value': resultTableSueryResult})
# url = 'http://example.webscraping.com/view/united-kingdom-239'
# html = 'f'
# db = client.cache
# db.resList.insert({'key': 'resListKey', 'resListValue': resListValue})
# ressss = db.webpage.find_one({'key': ''})

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

    return render_template('hello.html',resListValue = resultExistRes)

# @app.route('/hello')
# def hello():
    # return json.dumps(resList, ensure_ascii=False)
    # return render_template('hello.html',resList=resListRes)

if __name__ == "__main__":

    app.run(debug = True)

