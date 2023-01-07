from rest_framework import serializers
from .models import Genre, Category, Book
from users.models import Comment


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model instances."""
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model instances."""
    class Meta:
        model = Category
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    """Serializer for Book model instances."""
    class Meta:
        model = Book
        fields = "title image release_year".split()


class BookDetailSerializer(serializers.ModelSerializer):
    """Serializer for a specific Book model instance."""
    type = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "id title type release_year genre description comments".split()

    def get_genre(self, manga):
        return [i.title for i in manga.genre.all()]

    def get_type(self, manga):
        return manga.type.title

    def get_comments(self, manga):
        answer = []
        for i in manga.comment.all():
            ans_lst = {}
            ans_lst["image"] = f"http://127.0.0.1:8000/{i.author.image.url}"
            ans_lst["username"] = i.author.username
            ans_lst["nickname"] = i.author.nickname
            ans_lst["text"] = i.text
            answer.append(ans_lst)
        return answer


class BookCommentsSerializer(serializers.ModelSerializer):
    """Serializer for comments of a specific Book model instance."""
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "comments".split()

    def get_comments(self, manga):
        answer = []
        for i in manga.comment.all():
            ans_lst = {}
            ans_lst["image"] = f"http://127.0.0.1:8000/{i.author.image.url}"
            ans_lst["username"] = i.author.username
            ans_lst["nickname"] = i.author.nickname
            ans_lst["text"] = i.text
            answer.append(ans_lst)
        return answer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model instances."""
    book = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_book(self, comment):
        return comment.book.title

    def get_author(self, comment):
        ans = {
            "username": comment.author.username,
            "nickname": comment.author.nickname
        }
        return ans


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Comment model instances."""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = 'id author text book'.split()
        read_only_fields = "id book".split()