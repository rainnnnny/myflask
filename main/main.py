import math
from flask import Flask, session, request, render_template, jsonify, Response, g
import pymysql
from . import logger

app = Flask(__name__)
app.DEBUG = True

app.config.from_pyfile('config.py')


log = logger.getlogger('main')


@app.route('/')
@app.route('/index/')
def index():
    data = {'hello':'hello'}
    user = session.get('curID') or request.cookies.get('curID')
    if user:
        data['user'] = user
    return render_template('index.html', data=data)

    if request.method == 'POST':# 当提交表单时
        acc = request.POST['account']
        psw = request.POST['password']
        bRemember = request.POST.getlist('remember')
        iResult = Authenticate(acc, psw)
        if iResult == AUTH_SUCCESS:
            if bRemember:
                session['curID'] = acc
            response = redirect('/index/')
            response.set_cookie("curID", acc)#, secure=True)
            return response
        else:
            return render_template('login.html', {'sResult':AUTH_MSG[iResult]})
            # return HttpResponse(AUTH_MSG[iResult])
    else:
        return render_template('login.html')

@app.route('/test/')
def test():

    print('TTTEST:', app.config.get('TTTEST'))

    db = get_db()
    db.execute('select * from items;')
    print(db.fetchall())

    # for each in dir(request):
    #     print(each, ':', '------------', getattr(request, each))

    return render_template('test.html')


@app.route('/shiki/')
def shiki():
    log.info("hello, %s" % request.args)
    shiki = request.args['shiki']
    if shiki:
        insert_items(shiki, request.remote_addr)
        return shiki


@app.route('/getall/')
def get_all():
    db = get_db()
    db.execute('select * from items;')

    res = []
    res_all = db.fetchall()
    
    for each in res_all:
        res.append(each[0])
    
    return jsonify(res)

def get_db():
    if not hasattr(g, 'db'):
        # 注意指定charset避免乱码
        db = pymysql.connect("localhost", "root",
                             "qwer1234", "mytest", charset='utf8')
        g.db = db
    return g.db.cursor()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


def insert_items(msg, ip):
    cursor = get_db()
    db = g.db

    sql = "insert into items values ('%s', now(), '%s')" % (msg, ip)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


