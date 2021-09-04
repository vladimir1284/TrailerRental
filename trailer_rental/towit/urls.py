from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from towit.views import *

urlpatterns = [
   path('dashboard/',  dashboard, name='dashboard'),
   path('new_trailer/',  TrailerCreateView.as_view(), name='new_trailer'),
   path('new_contact/',  ContactCreateView.as_view(), name='new_contact'),
   path('update_contact/<slug:pk>',  ContactUpdateView.as_view(), name='update_contact'),
   path('update_contract/<slug:pk>',  ContractUpdateView.as_view(), name='update_contract'),
   path('delete_contract/<slug:id>',  delete_contract, name='delete_contract'),
   path('change_contract_stage/<slug:id>/<int:stage>',  change_contract_stage, name='change_contract_stage'),
   path('capture_signature/<int:lease_id>/<position>',  HandWritingCreateView.as_view(), name='capture_signature'),
   path('update_trailer/<slug:pk>',  TrailerUpdateView.as_view(), name='update_trailer'),
   path('update_maintenance/<slug:pk>',  MaintenanceUpdateView.as_view(), name='update_trailer'),
   path('trailers/',  trailers, name='trailers'),
   path('contacts/',  contacts, name='contacts'),
   path('contracts/',  contracts, name='contracts'),
   path('trailer/<int:id>',  trailer_detail, name='trailer_detail'),
   path('trailer_json/<int:id>',  trailer_json, name='trailer_json'),
   path('contact/<int:id>',  contact_detail, name='contact_detail'),
   path('contract/<int:id>',  contract_detail, name='contract_detail'),
   path('delete_trailer/<int:id>',  delete_trailer, name='delete_trailer'),
   path('maintenances/<int:trailer_id>',  maintenances, name='maintenances'),
   path('delete_trailer_image/<int:id>',  delete_trailer_image, name='delete_trailer_image'),
   path('new_maintenance/<int:trailer_id>',  MaintenanceCreateView.as_view(), name='new_maintenance'),
   path('new_lessee/<int:contact_id>',  LesseeCreateView.as_view(), name='new_lessee_from_contact'),
   path('new_lessee/trailer/<int:trailer_id>',  LesseeCreateView.as_view(), name='new_lessee_from_trailer'),
   path('new_lessee/',  LesseeCreateView.as_view(), name='new_lessee'),
   path('new_contract/<int:lessee_id>/',  LeaseCreateView.as_view(), name='new_contract'),
   # path('trailers/',  generate_pdf, name='trailers'),
    path('', dashboard, name='dashboard'),
]