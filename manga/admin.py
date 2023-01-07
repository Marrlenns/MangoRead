from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = 'title release_year type'.split()
    fields = 'image title description release_year type genre'.split()


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
