from django.contrib import admin
from .Models import Poll, Choice, Response

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Response)