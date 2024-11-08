import os
import random
from datetime import datetime, timedelta
os.environ["TESTING"] = "False"
from Application import db, app
from Application.Models import Place
#from bing_image_downloader import downloader  # Ensure bing_image_downloader is installed

# Hotel and Airbnb data
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

airbnbs = [
    "Duckpond Guesthouse Hideaway", "Charming Private Bedroom at the University of FL",
    "Cunningham: fiber wifi workdesk, 50\" tv+streams", "Private bedroom 2nd floor townhouse",
    "Cozy room in quiet neighborhood", "Cute Tiny Container Home", "Downtown Studio - 1/2 Mile from UF Campus",
    "Cozy home near historic Duckpond", "GATOR LIVING! - 2 Queens 2 Bath Close to UF/Shands",
    "Beautiful Guest Studio- Sleeps 4- Walk to Stadium", "Cozy studio w/ kitchen & laundry - 6 min from UF!",
    "Close to UF, airport, big yard", "The Port - Near UF, with Parking", "Condo in Central Gainesville",
    "Wooded Oasis: Blue Room - 4 miles to UF", "Vintage Cottage - 1 mile from UF",
    "Harmony Tiny House-10 min to UF & Airport", "One Block to UF Campus! 1bed 1bath",
    "Beautiful House close to UF", "Private cottage convenient to downtown and UF"
]

# Sample amenities list
amenities_list = ["Free Wi-Fi", "Pool", "Gym", "Breakfast included", "Parking", "Pet-friendly"]

# Helper functions
def random_distance():
    return f"{random.uniform(0.1, 4):.1f} miles"

def random_rating():
    return round(random.uniform(3.0, 5.0), 1)

def random_date_range():
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2025, 10, 31)
    random_start = start_date + timedelta(days=random.randint(0, (datetime(2024, 12, 31) - start_date).days))
    random_duration = timedelta(days=random.randint(90, 300))
    random_end = min(random_start + random_duration, end_date)
    return random_start, random_end

def clean_name(name):
    return "".join(c if c.isalnum() or c.isspace() else "_" for c in name).strip()

def download_image(place_name, target_dir):
    # Ensure directory exists
    os.makedirs(target_dir, exist_ok=True)
    search_term = f"{place_name} Gainesville"
    try:
        downloader.download(search_term, limit=1, output_dir=target_dir, adult_filter_off=True, timeout=5)
        return os.path.join(target_dir, f"{place_name}.jpg")
    except Exception as e:
        print(f"Failed to download image for {place_name}: {e}")
        return os.path.join("static/images", "default.jpg")

def get_random_airbnb_image():
    airbnb_dir = "static/images/gainesville_airbnbs"
    if os.path.exists(airbnb_dir):
        airbnb_images = os.listdir(airbnb_dir)
        if airbnb_images:
            return os.path.join(airbnb_dir, random.choice(airbnb_images))
    return "static/images/default.jpg"

# Seed function
def seed_places():
    places = []
    all_hotels = [
        (luxury_hotels, "Hotel", 200, 500),
        (mid_range_hotels, "Hotel", 100, 200),
        (budget_hotels, "Hotel", 50, 100)
    ]
    
    # Generate hotel entries
    for hotels, place_type, min_price, max_price in all_hotels:
        for hotel in hotels:
            available_from, available_to = random_date_range()
            hotel_dir = os.path.join("static/images", clean_name(hotel))
            image_path = download_image(hotel, hotel_dir)
            places.append(Place(
                place_name=hotel,
                place_type=place_type,
                price=random.uniform(min_price, max_price),
                amenities=", ".join(random.sample(amenities_list, k=3)),
                rating=random_rating(),
                campus_distance=random_distance(),
                guests_num=random.randint(2, 4),
                available_from=available_from.date(),
                available_to=available_to.date(),
                image_path=image_path
            ))

    # Generate Airbnb entries with random images from the downloaded set
    for airbnb in airbnbs:
        available_from, available_to = random_date_range()
        image_path = get_random_airbnb_image()
        places.append(Place(
            place_name=airbnb,
            place_type="Airbnb",
            price=random.uniform(25, 150),
            amenities=", ".join(random.sample(amenities_list, k=2)),
            rating=random_rating(),
            campus_distance=random_distance(),
            guests_num=random.randint(2, 6),
            available_from=available_from.date(),
            available_to=available_to.date(),
            image_path=image_path
        ))

    # Add all places to session and commit
    with app.app_context():
        db.session.bulk_save_objects(places)
        db.session.commit()
        print("Database seeded with hotel and Airbnb data.")

# Execute seed function
if __name__ == '__main__':
    with app.app_context():
        seed_places()
