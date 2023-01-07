from django.urls import path
from . import views

LIST = {'get': 'list'}
RETRIEVE = {'get': 'retrieve'}
RETRIEVE_CREATE = {'get': 'retrieve', 'post': 'create'}

urlpatterns = [
    path('genres/', views.GenreViewSet.as_view(LIST)),
    path('categories/', views.CategoryViewSet.as_view(LIST)),

    path('books/', views.BookViewSet.as_view(LIST)),
    path('books/<int:pk>/', views.BookViewSet.as_view(RETRIEVE)),

    path('books/<int:pk>/comments/', views.BookCommentViewSet.as_view(RETRIEVE_CREATE)),
    path('comments/<int:pk>/', views.CommentViewSet.as_view()),

]