from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from towit.views import trailer_detail, TrailerCreateView, trailers, TrailerUpdateView

urlpatterns = [
   path('new_trailer/',  TrailerCreateView.as_view(), name='new_trailer'),
   path('update_trailer/<slug:pk>',  TrailerUpdateView.as_view(), name='update_trailer'),
   path('trailers/',  trailers, name='trailers'),
   path('trailer/<int:id>',  trailer_detail, name='trailer-detail'),
   # path('trailers/',  generate_pdf, name='trailers'),
   # path('', index, name='index'),
]