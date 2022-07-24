from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.db import IntegrityError
from django.db.transaction import commit
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import BidForm, AuctionForm, CommentForm
from .models import User, Listing, Bid, PersonalWatchlist, Comment


def index(request):
    a_listings = Listing.objects.all()
    customer = User.objects.all()
    total_customers = customer.count()
    total = a_listings.count()
    active = a_listings.filter(status='Active').count()
    sold = a_listings.filter(status='Sold').count()

    active_listings = Listing.objects.filter(status='Active')
    category_id = request.GET.get("category", None)
    if category_id is None:
        listings = Listing.objects.filter(status='Active')
    else:
        listings = Listing.objects.filter(status='Active', category=category_id)

    context = {

        'total': total,
        'active': active,
        'sold': sold,
        'total_customers': total_customers,
        'listings': listings,
        "categories": categories,
        "active_listings": active_listings,
        "message": "Active Listings: "
    }
    return render(request, "auctions/index.html", context)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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




def active_listings(request):
    active_listings = Listing.objects.all()
    category_id = request.GET.get("category", None)
    if category_id is None:
        listings = Listing.objects.filter(status='Active')
    else:
        listings = Listing.objects.filter(status='Active', category=category_id)

    return render(request, "auctions/active_listings.html", {
        "listings": listings,
        "categories": categories,
        "active_listings": active_listings,

    })


def listings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    listings = Listing.objects.all()

    context = {

        'listings': listings,
        'listing': listing,
    }
    return render(request, "auctions/listings.html", context)


def listing(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    listing = Listing.objects.get(id=pk)
    bid_List = Bid.objects.filter(item=pk)
    bids = Bid.objects.filter(item=pk)
    watchlist = PersonalWatchlist.objects.filter(user=request.user, item=pk)
    comments = Comment.objects.filter(item=listing)

    context = {
        'Bids': bids,
        "listing": listing,
        "bid_form": BidForm(),
        "form": AuctionForm(),
        "num_bids": len(bid_List),
        "watchlist": watchlist,
        "comments": comments,
        "c_form": CommentForm()
    }

    return render(request, "auctions/listing.html", context)


def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            listing1 = form.save(commit=False)
            listing1.listing_seller = request.user
            listing1.status = 'Active'
            if listing1.starting_bid is None:
                listing1.starting_bid = 1
            listing1.save()

            message = 'Your item was listed successfully. Click "My Auctions" to view it.'
            return redirect('/', {"message": message})
    return render(request, "auctions/create_listing.html", {"form": AuctionForm()})


def update_listing(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    listing = Listing.objects.get(id=pk)
    form = AuctionForm(instance=listing)

    if request.method == 'POST':
        form = AuctionForm(request.POST, instance=listing)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {"form": form}
    return render(request, "auctions/create_listing.html", context)


def delete_listing(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    listing_delete = Listing.objects.all()
    listing = Listing.objects.filter(id=pk, listing_seller=request.user)

    if request.method == "POST":
        listing.delete()
        return redirect('/')

    context = {"form": listing,
               "listing_delete": listing_delete}
    return render(request, "auctions/delete_listing.html", context)



def place_bid(request):
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid = bid_form.cleaned_data["value"]
            item_id = bid_form.cleaned_data["item_id"]

            listing = Listing.objects.get(id=item_id)
            if (bid > listing.starting_bid):

                new_bid = Bid()
                new_bid.value = bid
                new_bid.item = listing
                new_bid.user = request.user
                new_bid.save()
                Listing.objects.filter(pk=item_id).update(starting_bid=bid)
                return redirect("listing", item_id)

            else:
                return render(request, "auctions/error.html", {
                    "message": "The value of the bid made is equal or less than the actual price. Please Try again"
                })


def close_listing(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    if request.method == "POST":
        if listing.status == 'Active' and "close" in request.POST:
            listing.status = 'Sold'
            listing.save()
            messages.info(request, "You closed this listing")
            return redirect("listing", item_id)
    return redirect("listing", item_id)


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    watchlist = PersonalWatchlist.objects.filter(user=request.user)
    totalW = watchlist.count()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "totalW": totalW

    })


def add_watchlist(request, item_id):
    listing = Listing.objects.get(id=item_id)
    try:
        w_item = PersonalWatchlist.objects.get(item=listing, user=request.user)
    except:
        w_item = None

    if not w_item:
        watch_item = PersonalWatchlist()
        watch_item.user = request.user
        watch_item.item = listing
        watch_item.save()

    return redirect("listing", item_id)


def remove_watchlist(request, item_id):
    listing = Listing.objects.get(id=item_id)
    try:
        w_item = PersonalWatchlist.objects.get(item=listing, user=request.user)
    except:
        w_item = None
    w_item.delete()
    return redirect("listing", item_id)


def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            opinion = form.cleaned_data["comment"]
            item_id = form.cleaned_data["item_id"]
            listing = Listing.objects.get(id=item_id)
            c = Comment()
            c.comment = opinion
            c.user = request.user
            c.item = listing
            c.save()

            return redirect("listing", item_id)

    return render(request, "auctions/error.html", {
        "message": "Some problem happened while you submitted your Comment"
    })


def categories(request):
    listings = Listing.objects.all()
    categories = []
    filtered_listings = []
    for listing in listings:
        if listing.category not in categories:
            categories.append(listing.category)
    if request.method == "POST":
        filtered_listings = listings.filter(category=request.POST["category"])
    return render(request, "auctions/categories.html", {
        'categories': categories,
        'listings': filtered_listings,
        'length': len(filtered_listings)}
                  )

