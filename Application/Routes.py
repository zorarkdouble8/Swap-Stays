from flask import render_template, request, redirect
from Application import app
from flask import request, session, jsonify
from Application.Database_Funcs.User import verify_login, create_user
from Application.Database_Funcs.Place import get_places, add_place
from Application.Models import User
from datetime import date, timedelta


@app.route("/")
def home():
    return render_template("Home/Home.html")

#TODO replace username with the actual user's username?
@app.route("/username")
def userHome():
    return render_template("User/Home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if (request.method == "POST"):
        user = verify_login(request.form["username"], request.form["password"])
        if (user == None):
            error = "Error: wrong password or username"
        else:
            session["UserId"] = user.id
            return redirect_logged_in(user)
    
    return render_template("Login/Login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def createUser():
    error = None
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
    return render_template("User/Home.html", user=user)

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

    # Convert results to JSON format
    return jsonify([{
        'place_name': place.place_name,
        'place_type': place.place_type,
        'price': place.price,
        'amenities': place.amenities,
        'rating': place.rating,
        'campus_distance': place.campus_distance,
        'guests_num': place.guests_num,
        'available_from': place.available_from,
        'available_to': place.available_to
    } for place in results])
