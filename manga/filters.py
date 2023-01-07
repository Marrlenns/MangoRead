from django_filters.rest_framework import ModelMultipleChoiceFilter, FilterSet, RangeFilter
from manga.models import Book, Category, Genre


class BookFilter(FilterSet):
    """Book filtering"""
    type = ModelMultipleChoiceFilter(queryset=Category.objects.all())
    release_year = RangeFilter()
    genre = ModelMultipleChoiceFilter(queryset=Genre.objects.all())

    class Meta:
        model = Book
        fields = ["release_year", "type", "genre"]
