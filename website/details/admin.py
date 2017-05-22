from django.contrib import admin
from .models import Entities, Topic

# Register your models here.
admin.site.register(Topic)
admin.site.register(Entities)