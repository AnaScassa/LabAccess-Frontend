from django.contrib import admin

# Register your models here.
from .models import Usuario, Acesso
admin.site.register(Usuario)
admin.site.register(Acesso)
