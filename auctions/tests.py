from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Listing, Category

User = get_user_model()

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.cat = Category.objects.create(name="Electronics")
        self.listing = Listing.objects.create(
            title="Phone",
            description="New phone",
            starting_bid=100,
            owner=self.user,
            category=self.cat
        )

    def test_listing_defaults_to_active(self):
        self.assertTrue(self.listing.active)

    def test_current_price_returns_starting_bid(self):
        self.assertEqual(self.listing.current_price(), 100)
