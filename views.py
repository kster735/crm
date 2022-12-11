from django.shortcuts import render, redirect
from .models import User, Contact, Message
from django.db import connection

def index(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_username = request.session['user_username']
        print(user_username)
        context = {'user_id': user_id, 'user_username': user_username}
        template = 'crm/index.html'
        return render(request, template, context)
    else:
        return redirect('login')
        
def landing(request):
    if not 'user_id' in request.session:
        return render(request, 'crm/landing.html')
    else:
        return redirect('index')


def login(request):
    if request.method == 'POST':
        username = request.POST['userUserName']
        password = request.POST['userPassword']
        cursor = connection.cursor()
        sql  = "SELECT * "
        sql += "FROM crm_user WHERE "
        sql += "user_username=%s and user_password=%s"
        cursor.execute(sql, [username, password])
        user = dictfetchall(cursor)
        if user:
            request.session['user_id'] = user[0]['id']
            request.session['user_username'] = user[0]['user_username']
            request.session.set_expiry(1200)
            return redirect('index')
        else:
            return render(request, 'crm/login.html', {'errormsg': 'Please enter valid Username or Password.', 'username': username})
    return render(request, 'crm/login.html')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('login')
    return redirect('login')


def contacts(request, user_id, viewuserid = None, error = None):
    if not isloggedin(request):
        return redirect('login')
    
    if viewuserid == None:
        contacts_list = Contact.objects.filter(user = user_id)
    else:
        contacts_list = Contact.objects.filter(user = viewuserid)
        user_id = viewuserid
    return render(request, 'crm/contacts.html', {'contacts_list': contacts_list, 'user_id': user_id, 'errormessage': error})

def contacts_insert_form(request, user_id, viewuserid, error=None):
    if not isloggedin(request):
        return redirect('login')
    
    if user_id == viewuserid:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
        user = dictfetchall(cursor)
        cursor.close()
        return render(request, 'crm/contacts_insert_form.html', {'user': user[0], 'user_id': user_id, 'errormessage': error})
    return redirect('index')

def contact_store(request, user_id, viewuserid):
    if not isloggedin(request):
        return redirect('login')
    cfname = request.POST['contactFirstName']
    clname = request.POST['contactLastName']
    cemail = request.POST['contactEmail']
    cphone =request.POST['contactPhone']
    cmobile =request.POST['contactMobile']
    caddress = request.POST['contactAddress']
    ccompany = request.POST['contactCompany']
    cvatno = request.POST['contactVatNo']
    sql = "INSERT INTO crm_contact (`user_id`,`contact_firstname`,`contact_lastname`,`contact_email`,`contact_phone`,`contact_mobile`,`contact_address`, `contact_company`,`contact_vat_no`)"
    sql += " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor = connection.cursor()
        cursor.execute(sql, [str(user_id), cfname, clname, cemail, cphone, cmobile, caddress, ccompany, cvatno])
        cursor.close()
        sql = "SELECT * FROM crm_contact WHERE user_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [str(user_id)])
        contacts_list = Contact.objects.filter(user = user_id)
        cursor.close()
        return render(request, 'crm/contacts.html', {'contacts_list': contacts_list, 'user_id': user_id})
    except:
        error = 'An error has occured'
        return redirect('contacts_insert_form', user_id = user_id, viewuserid = user_id, error=error)

def users(request, user_id):
    if not isloggedin(request):
        return redirect('login')
    user_list = User.objects.all()
    template ='crm/users.html'
    context = {
        'user_list': user_list,
        'user_id': user_id,
    }
    return render(request, template, context)

def users_insert_form(request, user_id):
    if not isloggedin(request):
        return redirect('login')

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
    user = dictfetchall(cursor)
    cursor.close()
    return render(request, 'crm/users_insert_form.html', {'user': user[0]})

def user_store(request):
    pass

def messages(request, user_id):
    if not isloggedin(request):
        return redirect('login')

    return render(request, 'crm/messages.html', {'user_id': user_id})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def test(request):
    
    sessionduration = request.session.get_expiry_age() 
    cookieage = request.session.get_session_cookie_age()
    # user_id = request.session['user_id']
    cookiecontext = {'cookieage': cookieage, 'sessionduration': sessionduration}
    message = {'message': 'ok'}
    if request.method == "POST":
        message = {'message': request.POST['message']}
    context = message | cookiecontext
    return render(request, 'crm/test.html', context)

def isloggedin(req) -> bool:
    if 'user_id' in req.session:
        return True
    return False
