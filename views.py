from django.shortcuts import render
from .models import User, Contact, Customer

def index(request):
    user_list = User.objects.all()
    template ='crm/index.html'
    context = {
        'user_list': user_list,
    }
    return render(request, template, context)

def customers(request, user_id):
    customers_list = Customer.objects.filter(user = user_id)
    return render(request, 'crm/customers.html', {'customers_list': customers_list, 'user_id': user_id})

