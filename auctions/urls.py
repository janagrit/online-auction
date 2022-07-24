from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active_listings", views.active_listings, name="active_listings"),
    path("listings", views.listings, name="listings"),
    path('listing/<str:pk>', views.listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('update_listing/<int:pk>/', views.update_listing, name="update_listing"),
    path('delete_listing/<int:pk>/', views.delete_listing, name="delete_listing"),
    path("close_listing/<int:item_id>", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:item_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:item_id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("categories", views.categories, name="categories")

]
