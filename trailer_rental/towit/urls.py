from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from towit.views import *

urlpatterns = [
   path('new_trailer/',  TrailerCreateView.as_view(), name='new_trailer'),
   path('new_contact/',  ContactCreateView.as_view(), name='new_contact'),
   path('update_trailer/<slug:pk>',  TrailerUpdateView.as_view(), name='update_trailer'),
   path('update_maintenance/<slug:pk>',  MaintenanceUpdateView.as_view(), name='update_trailer'),
   path('trailers/',  trailers, name='trailers'),
   path('contacts/',  contacts, name='contacts'),
   path('trailer/<int:id>',  trailer_detail, name='trailer_detail'),
   path('contact/<int:id>',  contact_detail, name='contact_detail'),
   path('delete_trailer/<int:id>',  delete_trailer, name='delete_trailer'),
   path('maintenances/<int:trailer_id>',  maintenances, name='maintenances'),
   path('delete_trailer_image/<int:id>',  delete_trailer_image, name='delete_trailer_image'),
   path('new_maintenance/<int:trailer_id>',  MaintenanceCreateView.as_view(), name='new_maintenance'),
   # path('trailers/',  generate_pdf, name='trailers'),
   # path('', index, name='index'),
]