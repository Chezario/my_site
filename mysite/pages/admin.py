from django.contrib import admin
from .models import Printers, Room, Security, Broker, SecurityTransaction


admin.site.register(Room)
admin.site.register(Printers)
admin.site.register(Security)
admin.site.register(Broker)
admin.site.register(SecurityTransaction)

