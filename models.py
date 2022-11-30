from django.db import models

# Create your models here.

class User(models.Model):
    user_firstname = models.CharField(max_length=255)
    user_lastname = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_username = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_phone = models.CharField(max_length=255)
    user_photo = models.CharField(max_length=255)
    user_type = models.IntegerField(default=0)
    user_level_access = models.IntegerField(default=0)
    user_is_active = models.BooleanField(default=True)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_firstname = models.CharField(max_length=255)
    customer_lastname = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_username = models.CharField(max_length=255)
    customer_password = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    customer_company = models.CharField(max_length=255)
    customer_vat_no = models.CharField(max_length=9)

    def __str__(self):
        return self.customer_firstname + " " + self.customer_lastname + ",      Εταιρεία: " + self.customer_company

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_id = models.IntegerField()
    contact_title = models.CharField(max_length=255)
    contact_content = models.CharField(max_length=255)
    contact_customer = models.CharField(max_length=255)
    contact_datetime = models.DateTimeField()
    contact_channel = models.CharField(max_length=255)
    contact_files = models.DateField()
    contact_due_date = models.CharField(max_length=255)

