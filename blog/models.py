
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, SlugField, TextField
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
from django.utils import timezone
from django.urls import reverse

# Create your models here.

# Creating model managers


class PublishedManager(models.Manager):
    """ Retrieve all post with the `published` status"""

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status="published")


class Post(models.Model):
    """ Represent a single post a user create in the blog"""
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )

    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique_for_date="published_date")
    author = ForeignKey(User, on_delete=CASCADE, related_name="blog_posts")
    body = TextField()
    published_date = DateTimeField(default=timezone.now)
    created_date = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    objects = Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager

    class Meta:
        ordering = ("-published_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[self.published_date.year, self.published_date.month, self.published_date.day, self.slug])
