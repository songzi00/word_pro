from django.db import models

# Create your models here.

# 用户
class User(models.Model):
    name = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=256)
    email = models.CharField(unique=True, max_length=254)
    sex = models.CharField(max_length=32)

    class Meta:
        db_table = 'myapp_user'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    types = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField()

    class Meta:
        db_table = 'myapp_book'

# 生词表
class Word(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=128)
    word = models.CharField(max_length=128)

    class Meta:
        db_table = 'myapp_word'