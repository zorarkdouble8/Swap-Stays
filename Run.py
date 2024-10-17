from flask import render_template, request, redirect
from Application import app
from Application.Database_Funcs.Place import get_places, add_place

@app.route("/")
def home():
    return render_template("Home/Home.html")

# Display a list of places
@app.route("/places")
def places():
    # Fetch all the places from the database
    places_list = get_places()
    return render_template("Places/Places.html", places=places_list)

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

# Redirects all logged-in users to a certain page (adjust as needed)
def redirect_logged_in():
    return render_template("Home/Home.html")

#run the program
if (__name__ == "__main__"):
    app.run(debug=True)
