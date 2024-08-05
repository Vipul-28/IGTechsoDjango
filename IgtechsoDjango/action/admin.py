from django.contrib import admin
from action.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserModalAdmin(BaseUserAdmin):
    list_display = ["email", "user_name","first_name","last_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ('user_name','last_name','first_name')}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "user_name","first_name","last_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


admin.site.register(User, UserModalAdmin)
