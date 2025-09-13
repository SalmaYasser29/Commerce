from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Listing, Category, Bid, Comment, Watchlist

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User

def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["description"]
        start_bid = Decimal(request.POST["starting_bid"])
        image_url = request.POST.get("image_url", "")
        category_id = request.POST.get("category")
        category = Category.objects.get(pk=category_id) if category_id else None

        listing = Listing.objects.create(
            title=title,
            description=desc,
            starting_bid=start_bid,
            image_url=image_url,
            category=category,
            owner=request.user
        )
        return redirect("listing", listing_id=listing.id)

    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": categories
    })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user_won = False
    in_watchlist = False

    # Check if user won the listing
    if not listing.active and listing.winner == request.user:
        user_won = True

    # Check if user has added this listing to their watchlist
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user_won": user_won,
        "in_watchlist": in_watchlist
    })

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        try:
            amount = Decimal(request.POST["bid_amount"])
        except:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Invalid bid format."
            })

        current = listing.bids.order_by('-amount').first()
        current_price = current.amount if current else listing.starting_bid

        if amount <= current_price:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Bid must be greater than current price.",
                "comments": listing.comments.all(),
                "bids": listing.bids.all()
            })

        Bid.objects.create(bidder=request.user, listing=listing, amount=amount)
        return redirect("listing", listing_id=listing.id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.method == "POST":
        content = request.POST.get('comment', '').strip()
        if content:
            Comment.objects.create(author=request.user, listing=listing, content=content)
    
    return redirect('listing', listing_id=listing.id)

@login_required
def toggle_watch(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    entry = Watchlist.objects.filter(user=request.user, listing=listing).first()
    if entry:
        entry.delete()
    else:
        Watchlist.objects.create(user=request.user, listing=listing)
    return redirect("listing", listing_id=listing.id)

@login_required
def watchlist(request):
    items = Listing.objects.filter(watched_by__user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": items
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category_listings(request, cat_id):
    cat = get_object_or_404(Category, pk=cat_id)
    listings = Listing.objects.filter(active=True, category=cat)
    return render(request, "auctions/category_listings.html", {
        "category": cat,
        "listings": listings
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user != listing.owner:
        return HttpResponseForbidden()
    
    highest = listing.bids.order_by('-amount').first()
    if highest:
        listing.winner = highest.bidder  # set winner
    listing.active = False
    listing.save()
    return redirect("listing", listing_id=listing.id)

@login_required
def my_wins(request):
    wins = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/my_wins.html", {"wins": wins})
