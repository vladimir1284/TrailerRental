from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from towit.views import *
from towit.view.tracker import trackers, tracker_data, TrackerCreateView, TrackerUpdateView, tracker_detail_n, delete_tracker, trackers_data, tracker_detail, tracker_export, tracker_debug, debug_detail, trackers_table

urlpatterns = [
    # Entry point
    path('', dashboard, name='dashboard'),
    path('dashboard/',  dashboard, name='dashboard'),
    # Trailer
    path('new_trailer/',  TrailerCreateView.as_view(), name='new_trailer'),
    path('update_trailer/<slug:pk>',  TrailerUpdateView.as_view(), name='update_trailer'),
    path('trailers/',  trailers, name='trailers'),
    path('trailer/<int:id>',  trailer_detail, name='trailer_detail'),
    path('delete_trailer/<int:id>',  delete_trailer, name='delete_trailer'),
    path('trailer_json/<int:id>',  trailer_json, name='trailer_json'),
    # Maintenance
    path('new_maintenance/<int:trailer_id>',  MaintenanceCreateView.as_view(), name='new_maintenance'),
    path('update_maintenance/<slug:pk>',  MaintenanceUpdateView.as_view(), name='update_maintenance'),
    path('maintenances/<int:trailer_id>',  maintenances, name='maintenances'),
    # Trailer pictures
    path('new_picture/<int:trailer_id>',  TrailerPictureCreateView.as_view(), name='new_picture'),
    path('share_images/<ids>',  share_images, name='share_images'),
    path('delete_trailer_images/<ids>',  delete_trailer_images, name='delete_trailer_images'),
    # Contacts
    path('new_contact/',  ContactCreateView.as_view(), name='new_contact'),
    path('contact/<int:id>',  contact_detail, name='contact_detail'),
    path('update_contact/<slug:pk>',  ContactUpdateView.as_view(), name='update_contact'),
    path('contacts/',  contacts, name='contacts'),
    # Lessee
    path('new_lessee/<int:contact_id>',  LesseeCreateView.as_view(), name='new_lessee_from_contact'),
    path('new_lessee/trailer/<int:trailer_id>',  LesseeCreateView.as_view(), name='new_lessee_from_trailer'),
    path('new_lessee/',  LesseeCreateView.as_view(), name='new_lessee'),
    # Contracts
    path('new_contract/<int:lessee_id>/',  LeaseCreateView.as_view(), name='new_contract'),
    path('contract/<int:id>',  contract_detail, name='contract_detail'),
    path('contract_signed/<int:id>',  contract_detail_signed, name='contract_detail_signed'),
    path('upload_contract_document/<int:id>',  ContractDocumentCreateView.as_view(), name='upload_contract_document'),
    path('contracts/',  contracts, name='contracts'),
    path('update_contract/<slug:pk>',  ContractUpdateView.as_view(), name='update_contract'),
    path('delete_contract/<slug:id>',  delete_contract, name='delete_contract'),
    path('change_contract_stage/<slug:id>/<int:stage>',  change_contract_stage, name='change_contract_stage'),
    path('capture_signature/<int:lease_id>/<position>',  HandWritingCreateView.as_view(), name='capture_signature'),
    # Tracker
    path('new_tracker/<int:trailer_id>',  TrackerCreateView.as_view(), name='new_tracker'),
    path('update_tracker/<slug:pk>',  TrackerUpdateView.as_view(), name='update_tracker'),
    path('delete_tracker/<int:id>',  delete_tracker, name='delete_tracker'),
    path('tracker_detail/<int:id>',  tracker_detail, name='tracker_detail'),
    path('tracker_detail/<int:id>/<int:n>',  tracker_detail_n, name='tracker_detail_n'),
    path('trackers_map/',  trackers, name='trackers'),
    path('trackers/',  trackers_table, name='trackers_table'),
    path('trackers_map/data', trackers_data, name='trackers_json'),
    path('tracker_data', tracker_data, name='tracker_data'),
    path('tracker_debug', tracker_debug, name='tracker_debug'),
    path('debug_detail/<int:id>',  debug_detail, name='debug_detail'),
    path('tracker_export/<int:id>', tracker_export, name='tracker_export'),
]