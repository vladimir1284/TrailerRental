from django.contrib import admin
from .models import Trailer, Owners, Stage, TrailerType, Status, TrailerPicture

admin.site.register(Trailer)
admin.site.register(Owners)
admin.site.register(Stage)
admin.site.register(TrailerType)
admin.site.register(Status)
admin.site.register(TrailerPicture)