from django.shortcuts import render
import pyrebase
from django.contrib import auth
#from django.views.decorators.csrf import csrf_exempt

config = {
    'apiKey': "AIzaSyAb6SIG6NHgbwFoaY1VI8M_Jvf4avudqNI",
    'authDomain': "django-test-9c64f.firebaseapp.com",
    'databaseURL': "https://django-test-9c64f-default-rtdb.firebaseio.com",
    'projectId': "django-test-9c64f",
    'storageBucket': "django-test-9c64f.appspot.com",
    'messagingSenderId': "606678089088",
    'appId': "1:606678089088:web:2e0b3e42225b77bcf89565",
    'measurementId': "G-JDM5Q95H99",
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, 'signIn.html')

#@csrf_exempt
def postsign(request):
    email = request.POST.get('email-signIn')
    password = request.POST.get('password-signIn')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message = 'Invalid credentials.'
        return render(request, 'signIn.html', {
            'message': message,
        })
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    
    name = database.child('users').child(a).child('details').child('name').get().val()
    
    return render(request, 'welcome.html', {
        'name': name,
        'email': email,
        })
    
def logout(request):
    auth.logout(request)
    return render(request, 'signIn.html')

def signUp(request):
    return render(request, 'signUp.html')

def postsignup(request):
    name = request.POST.get('username-register')
    email = request.POST.get('email-signUp')
    password = request.POST.get('password-signUp')
        
    try:
        user = authe.create_user_with_email_and_password(email, password)
    except:
        message = 'Invalid credentials.'
        return render(request, 'signUp.html', {
            'message': message,
        })
        
    uid = user['localId']
    data = {
        'name': name,
        'status': '1',
    }
    database.child('users').child(uid).child('details').set(data)

    return render(request, 'signIn.html')
    
def create(request):
    return render(request, 'create.html')

def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    
    tz = pytz.timezone('America/Sao_Paulo')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    
    data = {
        'work': work,
        'progress': progress,
    }
    
    database.child('users').child(a).child('report').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request, 'welcome.html', {
        'name': name,
    })