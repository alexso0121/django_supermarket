from django.contrib import admin
from .models import Product_series, Products, newuser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import newuser

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class newuserInline(admin.StackedInline):
    model = newuser
    can_delete = False
    verbose_name_plural = 'newuser'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = [newuserInline, ]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(newuser)

admin.site.register(Product_series)
admin.site.register(Products)
