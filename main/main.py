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

@app.route('/formhello/')
def formhello():
    return request.form['hello']


@app.route('/ajaxhello/')
def ajaxhello():
    b = request.args.get('b', '')
    print('bbbbbbbb': b)
    return request.form['a']


def logout(request):
    try:
        del session['curID']
    except KeyError:
        pass
    response = redirect('/index/')
    response.delete_cookie('curID')
    return response

def Authenticate(acc, psw):
    oQuerySet = User.objects.filter(Account=acc)
    if not oQuerySet:
        return AUTH_ACCERROR
    oUser = oQuerySet[0]
    if not oUser.PswVerify(psw):
        return AUTH_PSWERROR
    return AUTH_SUCCESS

# AUTH END
