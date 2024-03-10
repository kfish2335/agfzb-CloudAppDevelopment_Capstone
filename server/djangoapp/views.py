import json
import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

# from .restapis import related methods
from . import restapis

# from .models import related models
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST["username"]
        password = request.POST["psw"]
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            print("logged in")
            return redirect("djangoapp:index")
        else:
            # If not, return to login page again
            return render(request, "djangoapp/user_login.html", context)
    else:
        return render(request, "djangoapp/user_login.html", context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    # If it is a POST request
    elif request.method == "POST":
        # Get user information from request.POST
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "http://localhost:5000/api/get_reviews?id="
        # Get dealers from the URL
        dealerships = restapis.get_dealer_by_id_from_cf(url, dealer_id)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.review for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "POST":
        url = "http://localhost:5000/api/get_reviews?id="
        # Get dealers from the URL
        if request.user.is_authenticated:
            data = request.POST
            review = {
                "dealership": int(dealer_id),
                "name": request.user.username,
                "review": data["review"],
                "purchase": data["purchase"],
                "time": datetime.utcnow().isoformat(),
                "purchase": data.get("purchasecheck") == "on",
            }

            if data.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(
                    data.get("purchasedate"), "%m/%d/%Y"
                ).isoformat()
                car = CarModel.objects.get(pk=data["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = int(car.year.strftime("%Y"))
            json_payload = {"review": review}
            url = "http://localhost:5000/api/review"
            restapis.post_request(
                url=url, json_payload=json_payload, dealer_id=dealer_id
            )
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
