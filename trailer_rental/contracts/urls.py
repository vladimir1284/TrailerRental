from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, newContract, generate_pdf

urlpatterns = [
                  path('new_contract/',  newContract, name='new_contract'),
                  path('new_contract/generate_pdf/',  generate_pdf, name='generate_pdf'),
                  path('', index, name='index'),
               ]