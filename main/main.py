import math
from flask import Flask, session, request, render_template
app = Flask(__name__)
app.DEBUG = True

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
def formhello():
    return render_template('test.html')


@app.route('/ajaxhello/')
def ajaxhello():
    print(request.args)
    return request.args['shiki']

# AUTH END
