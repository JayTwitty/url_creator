from django.contrib import admin

# Register your models here.
from app.models import URL, Click

admin.site.register(URL)
admin.site.register(Click)