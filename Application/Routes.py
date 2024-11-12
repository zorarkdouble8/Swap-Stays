from flask import render_template, request, redirect, abort
from Application import app
from flask import request, session, jsonify
from Application.Database_Funcs.User import *
from Application.Database_Funcs.Place import *
from Application.Models import User
from datetime import date, timedelta

@app.route("/places/<int:place_id>")
def booking_page(place_id):
    #get the page via the page id
    place = get_place(place_id=place_id)

    return render_template("Home/Booking.html", stay=place)

@app.route("/", methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        print("PARAMS: ", request.form["checkin"], request.form["checkout"], request.form["num_guests"], request.form["miles_campus"])

        # Fetch all the places from the database
        places_list = get_places()
        return render_template("Search/Places.html", places=places_list)

    return render_template("Home/Home.html")

#TODO replace username with the actual user's username?
@app.route("/user")
def userHome():
    if ("UserId" in session):
        user_id = session["UserId"]

        user = get_user(user_id)

        return render_template("User/Home.html", user=user)
    else:
        print("Not logged in!")

        abort(404)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if (is_logged_in()):
        return redirect("/user")

    if (request.method == "POST"):
        user = verify_login(request.form["username"], request.form["password"])
        if (user == None):
            error = "Error: wrong password or username"
        else:
            return redirect_logged_in(user)
    
    return render_template("Login/Login.html", error=error)

@app.route('/places/<int:place_id>/transaction', methods=['GET', 'POST'])
def transaction(place_id):
    place = get_place(place_id)

    if (request.method == 'POST'):
        #perform transaction

        #TODO: perform error detection!
        name = request.form.get("name")
        phone_num = request.form.get("phone-number")
        email = request.form.get("email")
        credit_card = request.form.get("credit-card")
        ccv = request.form.get("ccv")
        expiration_date = request.form.get("expiration-date")
        total_price = request.form.get("price")


        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        num_guests = request.form.get('num_guests')

        return f"Transaction completed for {name}."

    return render_template('/Home/Transaction.html', place=place)

@app.route("/register", methods=["GET", "POST"])
def createUser():
    error = None

    if (is_logged_in()):
        return redirect("/user")

    if (request.method == "POST"):
        #Create a user!
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_pass = request.form["confirm_password"]

        #TODO prevent SQL injection
        if (password == confirm_pass):
            user = create_user(username, password, email)

            if (user != None and verify_login(username, password)):  
                return redirect_logged_in(user)
            elif (user != None):
                error = "failed to create user, please try again" #TODO Perhaps because usernames are unique
            else:
                error = "failed to log user in!" #TODO Perhaps because usernames are unique
        else:
            error = "Passwords are not equal!"

    return render_template("Login/CreateUser.html", error=error)

#redirects all logged in users to a certain page
#returns: render template
def redirect_logged_in(user: User):
    print("User: ", user)
    #create cookie
    session["UserId"] = user.id

    return redirect("/user", 301)

#checks the cookie to determine if there's a user logged in
def is_logged_in() -> bool:
    if ("UserId" in session):
        return True
    else:
        return False


# Display a list of places
@app.route("/places")
def places():
    # Fetch all the places from the database
    places_list = get_places()
    return render_template("Search/Places.html", places=places_list)

# Route to add a new place
@app.route("/add_place", methods=["GET", "POST"])
def create_place():
    error = None
    if request.method == "POST":
        # Retrieve form data
        place_name = request.form["place_name"]
        place_type = request.form["type"]
        price = request.form["price"]
        amenities = request.form["amenities"]
        rating = request.form["rating"]
        campus_distance = request.form["campus_distance"]

        # Add the place to the database
        did_add_place = add_place(place_name, place_type, price, amenities, rating, campus_distance)

        if did_add_place:
            return redirect("/places")
        else:
            error = "Failed to add the place. Please try again."

    return render_template("Places/AddPlace.html", error=error)


@app.route('/search', methods=['GET'])
def search():
    # Retrieve parameters from the request, using None as default if not provided
    guests = request.args.get('guests', type=int)
    from_nights = request.args.get('fromNights', type=int)
    to_nights = request.args.get('toNights', type=int)
    amenities = request.args.get('amenities')

    # Call search_places with parameters, allowing them to be None if not provided
    results = search_places(guests=guests, from_nights=from_nights, to_nights=to_nights, amenities=amenities)

    # Pass results to the places.html template
    return render_template("Search/Places.html", places=results)