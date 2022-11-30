from django.contrib import admin
from .models import User, Contact, Customer
# Register your models here.

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Customer)