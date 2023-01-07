from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Book(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()
    description = models.TextField()
    type = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book')
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title