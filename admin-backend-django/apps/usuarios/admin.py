from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


class UsuarioCreacionForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('usuario', 'nombre', 'rol')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreacionForm
    list_display = ('usuario', 'nombre', 'rol', 'estado', 'last_login')
    list_filter = ('rol', 'estado')
    search_fields = ('usuario', 'nombre')
    ordering = ('usuario',)
    filter_horizontal = ()
    readonly_fields = ('last_login', 'creado_en')
    fieldsets = (
        (None, {'fields': ('usuario', 'password')}),
        ('Datos', {'fields': ('nombre', 'rol', 'estado', 'is_superuser')}),
        ('Fechas', {'fields': ('last_login', 'creado_en')}),
    )
    add_fieldsets = (
        (None, {'fields': ('usuario', 'nombre', 'rol', 'password1', 'password2')}),
    )
