from flask import Flask,render_template,url_for
import pymssql
from sql import MSSQL


app = Flask(__name__)


ms = MSSQL(host="localhost", user="sa", pwd="root", db="xinhai")

@app.route('/demo')
def my_echart():
    # resList = ms.ExecQuery("SELECT top(2) * FROM v_result")
    resList = ms.ExecQuery("SELECT COUNT(1) from v_result;")
    return render_template('my_template.html',resList =resList)
@app.route('/')
def index():

    return render_template('index.html')
@app.route('/hello')
def hello():
    resList = ms.ExecQuery("SELECT COUNT(1) from v_result;")
    # return json.dumps(resList, ensure_ascii=False)
    return render_template('hello.html',resList=resList)

if __name__ == "__main__":

    app.run(debug = True)

