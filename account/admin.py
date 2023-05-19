from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()

# admin.site.register(User)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','name','is_active','is_staff')
    search_fields = ['email','name']
    ordering = ['name']
    list_filter = ['is_active']
    list_editable = ['is_staff']
    


admin.site.register(User,UserAdmin)


#кастомизация аккаунта
