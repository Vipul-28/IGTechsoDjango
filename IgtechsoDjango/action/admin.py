from django.contrib import admin
from action.models import User,Blog,BooksAndBrochure
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

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','blog_title','blog_question','blog_description','blog_date','blog_image')

    fieldsets = [
        ("Blog info", {"fields": ('blog_title','blog_question','blog_description','blog_date','blog_image')}),
    ]
    search_fields = ["blog_title"]
    ordering = ["blog_date"]
    filter_horizontal = []
admin.site.register(Blog,BlogAdmin)



class BooksAndBrochureAdmin(admin.ModelAdmin):
    list_display = ('id','title','author','publisher','description','type','category','image','book','YOP','pages','view','read')

    fieldsets = [
        ("Blog info", {"fields": ('title','author','publisher','description','type','category','image','book','YOP','pages','view','read')}),
    ]
    search_fields = ["title"]
    ordering = ["YOP"]
    filter_horizontal = []
admin.site.register(BooksAndBrochure,BooksAndBrochureAdmin)
