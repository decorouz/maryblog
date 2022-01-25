
# Core django import
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
from django.utils import timezone
from django.urls import reverse
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField, SlugField, TextField

# Third party imports
from taggit.managers import TaggableManager

# Creating model managers


class PublishedManager(models.Manager):
    """ Retrieve all post with the `published` status"""

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    """ Represent a single post a user create in the blog"""
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )

    # Blog Model fields

    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique_for_date="published_date")
    author = ForeignKey(User, on_delete=models.CASCADE,
                        related_name="blog_posts")
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
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

    tags = TaggableManager()


class Comment(models.Model):
    post = ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = CharField(max_length=25, null=False, blank=False)
    email = EmailField()
    body = TextField(null=False, blank=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    # Field used to manually deactivate inappropiate comment
    active = BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
