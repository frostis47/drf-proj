from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Payment, Subscription

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Payment)
admin.site.register(Subscription)