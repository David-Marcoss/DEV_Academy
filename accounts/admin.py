from django.contrib import admin

from .models import modelprofessor,modelaluno

# Register your models here.


<<<<<<< Updated upstream
=======
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Informações Pessoais", {"fields": ("is_Teacher",'nome','imageperfil')}),
    )

>>>>>>> Stashed changes
admin.site.register(modelprofessor) #adciona tabela cursos no admin
admin.site.register(modelaluno) #adciona tabela cursos no admin

