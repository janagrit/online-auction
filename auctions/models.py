from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    
    title = models.CharField(max_length=64)
    listing_seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, default=True, on_delete=models.CASCADE)
    CATEGORY = (
                ('No category', 'No category'),
                ('Home Furniture', 'Home Furniture'),
                ('Electronics', 'Electronics'),
                ('Health&Beauty', 'Health&Beauty'),
                ('Fashion', 'Fashion'),
                ('Food', 'Food'),
                ('Other', 'Other')
                )

    STATUS = (
            ('Sold', 'Sold'),
            ('Active', 'Active')
            )

    description = models.TextField(max_length=20000)
    comments = models.ManyToManyField('Comment', blank=True)
    starting_bid = models.IntegerField(blank=True, null=True)
    imageURL = models.URLField(max_length=3000, blank=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    status = models.CharField(max_length=200, choices=STATUS)
    posted_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title} [{self.listing_seller}]"


class Bid(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="object")

    def __str__(self):
        return f"{self.value} {self.item}"

class Comment(models.Model):
    comment = models.TextField(max_length=200, default=True)
    posted_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item", default=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_constraint=False, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} {self.user}"


class PersonalWatchlist(models.Model):
    user = models.ForeignKey(User, db_constraint=False,  on_delete=models.CASCADE, related_name='user_for_the_watchlist')
    item = models.ForeignKey(Listing, db_constraint=False, on_delete=models.CASCADE, related_name="watch")

    def __str__(self):
        return f"{self.user} {self.item}"


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.category}"

