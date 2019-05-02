from django.contrib import admin
from django.contrib.auth import get_user_model
from cuentas.models import User
from cuentas.models import Perfil
from django.contrib.auth.admin import UserAdmin

class PersonalizarUserAdmin(UserAdmin):
    fieldsets =()
    list_filter = ('admin',)
    list_display = ('email','nombre','apellido','perfil')
    add_fieldsets =(
     (None, {
     'fields':('email','password1','password2','perfil'),
     }),
    )
    ordering = ('email',)
    filter_horizontal = ()




User = get_user_model()
admin.site.register(Perfil)
admin.site.register(User,PersonalizarUserAdmin)


# Register your models here.
