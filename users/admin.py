from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FriendRequest

class UserAdmin(BaseUserAdmin):
    list_display = ('name','email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'timestamp', 'is_accepted')
    list_filter = ('is_accepted',)
    search_fields = ('from_user__email', 'to_user__email')

admin.site.register(FriendRequest, FriendRequestAdmin)
