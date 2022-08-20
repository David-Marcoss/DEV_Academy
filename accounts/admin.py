from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from .models import User, modelprofessor,modelaluno,redefinir_senha

# Register your models here.


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Informações Pessoais", {"fields": ("is_Teacher",'nome','imageperfil')}),
    )

admin.site.register(modelprofessor) #adciona tabela cursos no admin
admin.site.register(modelaluno) #adciona tabela cursos no admin
admin.site.register(redefinir_senha) #adciona tabela redefinir_senha  no admin

