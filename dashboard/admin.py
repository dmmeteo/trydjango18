from django.contrib import admin
from forms import BookForm
from models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'slug',
    ]
    readonly_fields = ['updated', 'timestamp', 'added_by', 'last_edit_by']

    form = BookForm

admin.site.register(Book, BookAdmin)