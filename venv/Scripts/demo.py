from flask import Flask,Response,render_template,url_for
import pymssql
from pymongo import MongoClient
import collections.abc
# //pip install pymongo
from sql import MSSQL
import json

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
resultSum = len(resultExistRes)
resultExistRes2 ={}
scoreMoreThan160 = {}
sub_health = {}
ObviousSymptoms = {}
psychologicalIntervention = {}
SeriousProblems = {}
for resultSingle in resultExistRes:
    if resultSingle[1].split('|')[-2] > '160' :
        scoreMoreThan160[resultSingle[0]] = resultSingle[1].split('|')[-2]
        if resultSingle[2].split('|')[-1] >= '2' and resultSingle[2].split('|')[-1]< '3':
            sub_health[resultSingle[0]] = resultSingle[2].split('|')[-1]
        if resultSingle[2].split('|')[-1] >= '3' and resultSingle[2].split('|')[-1]< '4':
            ObviousSymptoms[resultSingle[0]] = resultSingle[2].split('|')[-1]
        if resultSingle[2].split('|')[-1] >= '4' and resultSingle[2].split('|')[-1]< '5':
            psychologicalIntervention[resultSingle[0]] = resultSingle[2].split('|')[-1]
        if resultSingle[2].split('|')[-1] >= '5':
            SeriousProblems[resultSingle[0]] = resultSingle[2].split('|')[-1]
    resultExistRes2[resultSingle[0]] = resultSingle[1].split('|')[-2]

scoreMoreThan160Count = len(scoreMoreThan160)
subHealthCount = len(sub_health)
ObviousSymptomsCount = len(ObviousSymptoms)
psychologicalInterventionCount = len(psychologicalIntervention)
SeriousProblemsCount = len(SeriousProblems)

    # '总分大于160分的人数':scoreMoreThan160Count,
    # '亚健康人数': subHealthCount,
    # '明显症状人数': ObviousSymptomsCount,
    # '需要心理干预人数': psychologicalInterventionCount,
    # '严重心理问题人数': SeriousProblemsCount,
    # # '人数':(scoreMoreThan160Count-subHealthCount-ObviousSymptomsCount-psychologicalInterventionCount-SeriousProblemsCount)
# }

@app.route('/api/test')
def test():
    CountDetail = [
        # {'value':scoreMoreThan160Count,'name' :'总分大于160分的人数'},
        {'value': 1, 'name': '严重心理问题人数'},
        {'value': (ObviousSymptomsCount / scoreMoreThan160Count) * 100, 'name': '明显症状人数'},
        {'value': 1, 'name': '需要心理干预人数'},
        {'value': (subHealthCount / scoreMoreThan160Count) * 100, 'name': '亚健康人数'},
    ]
    return Response(json.dumps(CountDetail), mimetype='application/json')

@app.route('/api/zhuzhuangY')
def zhuzhuangY():
    CountDetail = [
        SeriousProblemsCount,
        ObviousSymptomsCount,
        psychologicalInterventionCount,
        subHealthCount
        ]
    return Response(json.dumps(CountDetail), mimetype='application/json')

@app.route('/api/score')
def score():
    return Response(json.dumps(resultExistRes2), mimetype='application/json')
# return render_template('hello.html',resListValue = resultExistRes2)
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/hello')
# def hello():
    # return json.dumps(resList, ensure_ascii=False)
    # return render_template('hello.html',resList=resListRes)

if __name__ == "__main__":

    app.run(debug = True)

