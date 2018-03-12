import math
from flask import Flask, session, request, render_template, jsonify, Response, g
import pymysql

app = Flask(__name__)
app.DEBUG = True
# app.config.from_pyfile('config.py')

app.config.update(
    DATABASE='mysql://root:qwer1234@localhost:3306/items',
    SECRET_KEY='development key',
    USERNAME='root',
    PASSWORD='qwer1234'
)


alled = False


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

    print(app.config.get('a'))

    db = get_db()
    db.execute('select * from items;')
    print(db.fetchall())

    for each in dir(request):
        print(each, ':', '------------', getattr(request, each))

    return render_template('test.html')


@app.route('/ajaxhello/')
def ajaxhello():
    print(request.args)
    shiki = request.args['shiki']
    if shiki:
        insert_items(shiki, request.remote_addr)
        return shiki


@app.route('/ajaxall/')
def get_all():
    global alled
    if alled:
        return Response()
    alled = True
    db = get_db()
    db.execute('select * from books;')

    res = []
    res_all = db.fetchall()
    
    for each in res_all:
        print(each[1], type(each[1]), each[1].encode('utf8'))
        res.append(each[1])
    
    return jsonify(res)

def get_db():
    if not hasattr(g, 'db'):
        print('get_db')
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


