from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass  

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="wins")

    def current_price(self):
        highest = self.bids.order_by('-amount').first()
        return highest.amount if highest else self.starting_bid

    def __str__(self):
        return f"{self.title} (${self.current_price()})"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} - {self.amount}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched_by")

    class Meta:
        unique_together = ('user', 'listing')
