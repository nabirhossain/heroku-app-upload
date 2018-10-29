from django.contrib import admin
from .models import post, category 

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = category

admin.site.register(category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ["__str__",'post_category','posted_on']
    list_filter = ['posted_on','post_author']
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = post

admin.site.register(post, PostAdmin)
