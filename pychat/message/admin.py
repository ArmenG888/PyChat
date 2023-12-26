from django.contrib import admin
from .models import dm, message, server

admin.site.register(dm)
admin.site.register(message)
admin.site.register(server)