from flask import render_template, request, redirect, abort
from Application import app
from flask import request, session, jsonify
from Application.Database_Funcs.User import *
from Application.Database_Funcs.Place import *
from Application.Database_Funcs.Review import *
from Application.Database_Funcs.List import *
from Application.Models import User, List
from datetime import date, timedelta
from sendgrid import Mail, SendGridAPIClient

@app.route("/places/<int:place_id>/add_list")
def add_list1(place_id):
    user = get_user_obj()

    #is user logged in
    if (user != None):
        list = List(place_id, user.id)

        add_list(list)
        return redirect(f"/places/{place_id}", 302)
    else:
        return "<h1>Error</h1>"
    
@app.route("/places/<int:place_id>/remove_list")
def remove_list1(place_id):
    user = get_user_obj()

    #is the user logged in
    if (user != None):
        for list in user.lists:
            if (list.place_id == place_id):
                remove_list(list)
                break

        return redirect(f"/places/{place_id}", 302)
    else:
        return "<h1>Error</h1>"

def is_logged_in():
    return "UserId" in session

def get_user_obj():
    if is_logged_in():
        return db.session.get(User, session["UserId"])
    return None

@app.route("/places/<int:place_id>")
def booking_page(place_id):
    #get the page via the page id
    place = get_place(place_id=place_id)
    user = get_user_obj()

    on_list = False
    if (user != None):
        for list in user.lists:
            if (list.place_id == place_id):
                on_list = True
                break

    return render_template("Home/Booking.html", stay=place, user=user, on_list=on_list)

@app.route('/places/<int:place_id>/add_review', methods=['POST'])
def add_review_route(place_id):
    if 'UserId' in session:
        user_id = session['UserId']
        user = get_user(user_id)  # Replace with your user retrieval function

        if user and request.form:
            review_text = request.form.get('review_text')
            stars = request.form.get('review_stars', type=int)

            # Ensure stars is valid
            if not stars or stars < 1 or stars > 5:
                return "Invalid rating. Please select a rating between 1 and 5.", 400

            if review_text and stars:
                new_review = add_review(place_id, user.id, user.username, review_text, stars)

                if new_review:
                    return redirect(f'/places/{place_id}')
                else:
                    return "Failed to add review. Please try again.", 500
            else:
                return "Invalid input. Please make sure all fields are filled.", 400
        else:
            return "User not found or invalid request.", 404
    else:
        return redirect('/login')


@app.route("/", methods=["GET", "POST"])
def home():
    if (request.method == "POST"):
        # retrieve data for summary
        checkin = request.form.get("checkin")
        checkout = request.form.get("checkout")
        num_guests = request.form.get("guests")

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

        places = []
        for list in user.lists:
            places.append(get_place(list.place_id))

        return render_template("User/Home.html", user=user, places=places)
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

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        num_guests = request.form.get('num_guests')
        price = request.form.get('price')
        name = request.form.get('place_name')
        return render_template('/Home/Transaction.html',place_name=name, price=price, checkin=checkin, checkout=checkout, num_guests=num_guests)

    return render_template('/Home/Transaction.html')

@app.route('/process_transaction', methods=['POST'])
def process_transaction():
    name = request.form.get('name')
    price = request.form.get('price')
    place_name = request.form.get('place_name')
    email = request.form.get("e-mail")

    email = Mail(from_email="swampstays@gmail.com", to_emails=email, 
                 subject="Payment for booking", html_content=f"""
                 <strong>Hi {name},</strong>
                 <p>Your booking has been booked!</p>
                 <p>
                    Reciept:
                        Payed ${price} a night for {place_name} 
                </p>
                 """)
    
    try:
        send_grid = SendGridAPIClient(os.environ["SEND_GRID_KEY"])
        send_grid.send(email)
        return "Transaction completed and email sent."
    except Exception as e:
        return f"<h1>Error! {e}</h1>"

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

#if the user is logged in, this retrns the user object, else it returns none
def get_user_obj() -> User:
    if ("UserId" in session):
        user_id = session["UserId"]

        return get_user(user_id)
    
    return None
#if the user is logged in, this retrns the user object, else it returns none
def get_user_obj() -> User:
    if ("UserId" in session):
        user_id = session["UserId"]

        return get_user(user_id)
    
    return None

# Display a list of places
@app.route("/places")
def places():
    # Fetch all the places from the database
    places_list = get_places()

    # Check if the user is logged in
    user = get_user_obj() if is_logged_in() else None

    return render_template("Search/Places.html", places=places_list, user=user)


def get_user(id: int) -> User:
    try:
        user = db.session.get(User, id)
        print(f"Retrieved User: {user}")
        return user
    except Exception as e:
        print(e)
        return None

@app.route('/search', methods=['GET'])
def search():
    # Retrieve parameters from the request
    num_guests = request.args.get('num_guests', type=int)
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    miles_campus = request.args.get('miles_campus')
    # Retrieve user object
    user = None
    if 'UserId' in session:
        user_id = session['UserId']
        user = get_user(user_id)

    # Retrieve search parameters
    guests = request.args.get('guests', type=int)
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    amenities = request.args.get('amenities')

    # Call `search_places` with parameters
    results = search_places(guests=num_guests, checkin=checkin, checkout=checkout, campus_distance=miles_campus)

    # Render filtered results to the places template
    return render_template("Search/Places.html", places=results)

    # Render results to the template
    return render_template("Search/Places.html", places=results, user=user)

    
@app.route('/admin/add_place', methods=['GET', 'POST'])
def admin_add_place():
    if 'UserId' in session:
        user_id = session['UserId']
        user = get_user(user_id)
        
        if user and user.is_admin:
            if request.method == 'POST':
                # Get form data
                place_name = request.form['place_name']
                place_type = request.form['place_type']
                price = request.form['price']
                amenities = request.form['amenities']
                rating = request.form['rating']
                campus_distance = request.form['campus_distance']
                guests_num = request.form['guests_num']
                available_from = request.form['available_from']
                available_to = request.form['available_to']
                image_path = request.form['image_path']
                
                # Add the place to the database
                add_place(
                    place_name, place_type, float(price), amenities, float(rating),
                    campus_distance, int(guests_num), date.fromisoformat(available_from),
                    date.fromisoformat(available_to), image_path
                )
                return redirect('/places')
            
            return render_template('User/AddPlace.html')
        else:
            return "Unauthorized access", 403
    else:
        return redirect('/login')

@app.route('/admin/delete_place/<int:place_id>', methods=['POST'])
def admin_delete_place(place_id):
    if 'UserId' in session:
        user_id = session['UserId']
        user = get_user(user_id)

        if user and user.is_admin:
            try:
                place = get_place(place_id)
                if place:
                    db.session.delete(place)
                    db.session.commit()
                    return redirect('/places')
                else:
                    return "Place not found", 404
            except Exception as e:
                print(f"Error deleting place: {e}")
                db.session.rollback()
                return "Error occurred while deleting place", 500
        else:
            return "Unauthorized access", 403
    else:
        return redirect('/login')

