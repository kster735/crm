from django.shortcuts import render
from .models import User, Contact, Message
from django.db import connection

def index(request):
    user_list = User.objects.all()
    template ='crm/index.html'
    context = {
        'user_list': user_list,
    }
    return render(request, template, context)

def contacts(request, user_id):
    contacts_list = Contact.objects.filter(user = user_id)
    return render(request, 'crm/contacts.html', {'contacts_list': contacts_list, 'user_id': user_id})

def contacts_insert_form(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
    user = dictfetchall(cursor)
    cursor.close()
    return render(request, 'crm/contacts_insert_form.html', {'user': user[0]})

def contact_store(request, user_id):
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
    cursor = connection.cursor()
    cursor.execute(sql, [str(user_id), cfname, clname, cemail, cphone, cmobile, caddress, ccompany, cvatno])
    return render(request, 'crm/users.html')

def users(request, user_id):
    user_list = User.objects.all()
    template ='crm/users.html'
    context = {
        'user_list': user_list,
        'user_id': user_id,
    }
    return render(request, template, context)

def users_insert_form(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
    user = dictfetchall(cursor)
    cursor.close()
    return render(request, 'crm/users_insert_form.html', {'user': user[0]})


def messages(request, user_id):
    return render(request, 'crm/messages.html', {'user_id': user_id})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def test(request):
    testcontext = "ok"
    if request.method == "POST":
        testcontext = request.POST['message']
    return render(request, 'crm/test.html', {'testcontext': testcontext})