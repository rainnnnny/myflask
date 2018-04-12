import os
import sys
import math
import hashlib
import random
import pprint

from flask import Flask, session, request, render_template, jsonify, Response, g

import pymysql

from . import logger

app = Flask(__name__)
app.DEBUG = True

app.config.from_pyfile('config.py')
app.secret_key = 'B1[s:9k04zY!S2x7fYII"knO^MXY0-@SU'

log = logger.getlogger('main')


# ====================== test ======================
@app.route('/test/')
def test():

    print('TTTEST:', app.config.get('TTTEST'))
    print(dir(request))

    testsc()

    return render_template('test.html')


def testsc():
    print(session)
    print(request.cookies)

    if 'uid' not in session:
        x = hashlib.md5(str(random.random()).encode('utf8'))
        session['uid'] = x.hexdigest()
        session['list'] = []



# ====================== main ======================
@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/shiki', methods=['GET', 'POST'])
def shiki():
    log.info("hello, %s" % request.args)
    shiki = request.form.get('shiki')
    result = {'success':False, 'shiki':shiki}
    
    if not shiki:
        return jsonify(result)
    
    insert_items(shiki, request.remote_addr)
    result['success'] = True
    return jsonify(result)


@app.route('/getrandom/')
def getrandom():
    testsc()
    
    db = get_db()
    mtuple = tuple(session['list'])
    if mtuple:
        db.execute(
            'select * from items where id not in %s order by rand() limit 3;' % str(mtuple))
    else:
        db.execute('select * from items order by rand() limit 3;')

    res = []
    res_all = db.fetchall()
    
    cur_list = session['list']
    for item in res_all:        
        if item[0] in cur_list:
            continue
        res.append(item[1])
        print(item[0], cur_list)
        cur_list.append(item[0])
    
    session['list'] = cur_list
    log.info("%s" % cur_list)
    return jsonify(res)


@app.route('/clear/')
def clear():
    if 'uid' in session:
        session.pop('uid')
    if 'list' in session:
        session.pop('list')
    return ""

# ====================== db ======================
def get_db():
    if not hasattr(g, 'db'):
        # 注意指定charset避免乱码
        db = pymysql.connect("localhost", "root",
                             "qwer1234", "mytest", charset='utf8')
        g.db = db
    return g.db.cursor()


@app.teardown_appcontext
def close_db(error):
    # Closes the database again at the end of the request.
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


