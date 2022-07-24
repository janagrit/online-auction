from django.contrib import admin
from .models import User, Comment, Bid, Listing, PersonalWatchlist, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(PersonalWatchlist)
admin.site.register(Category)

