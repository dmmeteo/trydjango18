from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'timestamp', 'updated', 'content')
    list_filter = ['timestamp']
    fieldsets = [
        ('Title of post', {'fields': ['title']}),
        ('Content of post', {'fields': ['content']})
    ]

admin.site.register(Post, PostAdmin)
