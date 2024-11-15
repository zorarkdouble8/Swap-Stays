import os
import shutil

# Path to your project directory
project_path = r'C:\Users\gabal\OneDrive\Desktop\SwampStays\Swap-Stays\Application\static\images'


# Iterate through the main folders in the project path
for folder_name in os.listdir(project_path):
    main_folder_path = os.path.join(project_path, folder_name)

    # Check if the path is a directory
    if os.path.isdir(main_folder_path):
        # Construct the path to the nested folder
        nested_folder_name = folder_name.replace('_', ' ') + ' Gainesville Gainesville'
        nested_folder_path = os.path.join(main_folder_path, nested_folder_name)

        # Check if the nested folder exists
        if os.path.exists(nested_folder_path) and os.path.isdir(nested_folder_path):
            # Move all images (or files) from the nested folder to the main folder
            for item in os.listdir(nested_folder_path):
                item_path = os.path.join(nested_folder_path, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, os.path.join(main_folder_path, item))
                    print(f'Moved: {item} from {nested_folder_path} to {main_folder_path}')

            # Remove the now-empty nested folder
            os.rmdir(nested_folder_path)
            print(f'Removed nested folder: {nested_folder_path}')

print('Nested folder cleanup completed.')
