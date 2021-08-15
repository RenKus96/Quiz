from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ['raiting']

admin.site.register(CustomUser, CustomUserAdmin)
