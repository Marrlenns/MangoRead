from rest_framework import generics, mixins, viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Comment
from users.permissions import IsOwnerOrReadOnly
from .filters import BookFilter
from .models import Genre, Category, Book
from .paginations import BookPagination
from .serializers import (
    GenreSerializer, CategorySerializer, BookDetailSerializer, BookListSerializer,
    CommentSerializer, CommentCreateSerializer, BookCommentsSerializer
)


class GenreViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for viewing Genre model instances."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for viewing Category model instances."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ViewSet for viewing Book model instances."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    pagination_class = BookPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = BookFilter
    search_fields = 'title'.split()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer


class BookCommentViewSet(viewsets.ModelViewSet):
    """Viewing and adding comments for a specific Book model instance."""
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return BookCommentsSerializer if self.request.method in permissions.SAFE_METHODS else CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data['book'] = Book.objects.get(pk=self.kwargs['pk'])
        serializer.save()


class CommentViewSet(generics.RetrieveUpdateDestroyAPIView):
    """View and edit one comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]