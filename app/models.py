from unicodedata import category
from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user_id = models.IntegerField(null=False, blank=False, default=-1)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    desc = models.TextField(max_length=100, null=False, blank=False)
    image = CloudinaryField('image')

    def __str__(self):
        return self.desc

    def get_id(self):
        return self.user_id
