import random
from datetime import datetime, timedelta
from Application import db, app
from Application.Models import Place

# Hotel data
luxury_hotels = [
    "Hilton Garden Inn", "Marriott Downtown", "Hyatt Place", "The Westin Suites",
    "DoubleTree by Hilton", "Courtyard by Marriott", "Renaissance Hotel",
    "Embassy Suites by Hilton", "AC Hotel by Marriott", "Hilton University Plaza",
    "Hotel Indigo", "Homewood Suites by Hilton", "Aloft Gainesville University Area",
    "SpringHill Suites by Marriott", "Drury Inn & Suites", "Residence Inn by Marriott",
    "TownePlace Suites by Marriott", "Hampton Inn & Suites", "Staybridge Suites",
    "Holiday Inn Express & Suites"
]

mid_range_hotels = [
    "Comfort Suites", "Fairfield Inn & Suites by Marriott", "La Quinta Inn & Suites",
    "Country Inn & Suites", "Best Western Gateway Grand", "Wingate by Wyndham",
    "Sleep Inn & Suites", "Quality Inn University", "Baymont by Wyndham",
    "Holiday Inn University", "Reitz Union Hotel - University of Florida"
]

budget_hotels = [
    "Days Inn by Wyndham", "Super 8 by Wyndham", "Red Roof Inn Plus+",
    "Motel 6 Gainesville", "Econo Lodge University", "America’s Best Value Inn",
    "Quality Inn Gainesville I-75", "Budget Inn Gainesville", "Rodeway Inn",
    "Knights Inn Gainesville", "Extended Stay America", "Travelodge by Wyndham",
    "Howard Johnson by Wyndham", "Studio 6 Gainesville", "Suburban Extended Stay Hotel",
    "Value Lodge Gainesville", "Gainesville Lodge", "Gator Inn", "Sunshine Inn & Suites",
    "The University Motel"
]

# Airbnb data
airbnbs = [
    "Duckpond Guesthouse Hideaway", "Charming Private Bedroom at the University of FL",
    "Cunningham: fiber wifi workdesk, 50\" tv+streams", "Private bedroom 2 second floor townhouse",
    "Cozy room in quiet neighborhood", "Cute Tiny Container Home", "Downtown Studio - 1/2 Mile from UF Campus",
    "Cozy home near historic Duckpond", "GATOR LIVING!- 2 Queens 2 Bath Close to UF/Shands",
    "Beautiful Guest Studio- Sleeps 4- Walk to Stadium", "Cozy studio w/ kitchen & laundry - 6 min from UF!",
    "Close to UF, airport, big yard", "The Port - Near UF, with Parking", "Condo in Central Gainesville",
    "Wooded Oasis: Blue Room-4 miles to UF", "Vintage Cottage - 1 mile from UF",
    "Harmony Tiny House-10 min to UF & Airport", "One Block to UF Campus! 1bed 1bath",
    "Beautiful House close to UF", "Private cottage convenient to downtown and UF"
]

# Random amenities
amenities_list = ["Free Wi-Fi", "Pool", "Gym", "Breakfast included", "Parking", "Pet-friendly"]

# Random distance from campus (between 0.1 and 4 miles)
def random_distance():
    return f"{random.uniform(0.1, 4):.1f} miles"

# Random rating between 3.0 and 5.0
def random_rating():
    return round(random.uniform(3.0, 5.0), 1)

# Generate a random start date and availability period between 3 months and 300 days
def random_date_range():
    # Define the start date in 2024 and end date in 2025
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2025, 10, 31)
    
    # Calculate the total number of days between the two dates
    total_days = (end_date - start_date).days

    # Generate a random start date that is always in 2024
    random_start = start_date + timedelta(days=random.randint(0, (datetime(2024, 12, 31) - start_date).days))
    
    # Generate a random duration for availability: between 90 days (3 months) and 300 days
    random_duration = timedelta(days=random.randint(90, 300))
    
    # Calculate the random end date, making sure it doesn't exceed the defined end date
    random_end = random_start + random_duration
    if random_end > end_date:
        random_end = end_date

    return random_start, random_end

# Seed function
def seed_places():
    places = []

    # Luxury Hotels: $200 to $500, 2-4 guests
    for hotel in luxury_hotels:
        available_from, available_to = random_date_range()
        places.append(Place(
            place_name=hotel,
            place_type="Hotel",
            price=random.uniform(200, 500),
            amenities=", ".join(random.sample(amenities_list, k=3)),  # 3 random amenities
            rating=random_rating(),
            campus_distance=random_distance(),
            guests_num=random.randint(2, 4),
            available_from=available_from.date(),  # Using date() to extract only the date part
            available_to=available_to.date()
        ))

    # Mid-Range Hotels: $100 to $200, 2-4 guests
    for hotel in mid_range_hotels:
        available_from, available_to = random_date_range()
        places.append(Place(
            place_name=hotel,
            place_type="Hotel",
            price=random.uniform(100, 200),
            amenities=", ".join(random.sample(amenities_list, k=2)),  # 2 random amenities
            rating=random_rating(),
            campus_distance=random_distance(),
            guests_num=random.randint(2, 4),
            available_from=available_from.date(),
            available_to=available_to.date()
        ))

    # Budget-Friendly Hotels: $50 to $100, 2-4 guests
    for hotel in budget_hotels:
        available_from, available_to = random_date_range()
        places.append(Place(
            place_name=hotel,
            place_type="Hotel",
            price=random.uniform(50, 100),
            amenities=", ".join(random.sample(amenities_list, k=1)),  # 1 random amenity
            rating=random_rating(),
            campus_distance=random_distance(),
            guests_num=random.randint(2, 4),
            available_from=available_from.date(),
            available_to=available_to.date()
        ))

    # Airbnb Listings: $25 to $150, 2-6 guests
    for airbnb in airbnbs:
        available_from, available_to = random_date_range()
        places.append(Place(
            place_name=airbnb,
            place_type="Airbnb",
            price=random.uniform(25, 150),
            amenities=", ".join(random.sample(amenities_list, k=2)),  # 2 random amenities
            rating=random_rating(),
            campus_distance=random_distance(),
            guests_num=random.randint(2, 6),
            available_from=available_from.date(),
            available_to=available_to.date()
        ))

    # Add all places to session and commit
    with app.app_context():
        db.session.bulk_save_objects(places)
        db.session.commit()

# Execute seed function
if __name__ == '__main__':
    with app.app_context():
        print("Seeding database with hotel and Airbnb data...")
        seed_places()
        print("Database seeding complete!")
