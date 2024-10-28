import os
from bing_image_downloader import downloader

def download_generic_airbnb_images():
    output_dir = "static/images/gainesville_airbnbs"
    try:
        # Only download if directory doesn't already exist to avoid duplication
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            downloader.download("Gainesville Airbnb", limit=20, output_dir=output_dir, adult_filter_off=True, force_replace=False, timeout=5)
            print("Generic Airbnb images downloaded successfully.")
        else:
            print("Generic Airbnb images already downloaded.")
    except Exception as e:
        print(f"Failed to download generic Airbnb images: {e}")

if __name__ == '__main__':
    download_generic_airbnb_images()
