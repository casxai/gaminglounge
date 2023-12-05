from django.contrib import admin
from .models import User


#to register user table/app in the admin site
# admin.site.register(User)


# #to customize what to display in admin site
# class UserAdmin(admin.ModelAdmin):
#     fields = ['id', 'email']

# admin.site.register(User, UserAdmin)