from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/watch", views.toggle_watch, name="toggle_watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:cat_id>", views.category_listings, name="category_listings"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("my_wins", views.my_wins, name="my_wins"),
]
