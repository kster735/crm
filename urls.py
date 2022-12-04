from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('users/<int:user_id>/', views.users, name='users'),
    path('users/<int:user_id>/users_insert_form/', views.users_insert_form, name='users_insert_form'), 
    path('users/<int:user_id>/contacts/', views.contacts, name='contacts'),
    path('users/<int:user_id>/contacts/contacts_insert_form/', views.contacts_insert_form, name='contacts_insert_form'),
    path('users/<int:user_id>/contacts/contacts_insert_form/contact_store/', views.contact_store, name='contact_store'),
    path('users/<int:user_id>/messages/', views.messages, name='messages'),
]