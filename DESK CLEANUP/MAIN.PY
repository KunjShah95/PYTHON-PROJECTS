import os
import shutil

# Path to the folder you want to clean
folder_to_clean = r'C:\Users\KUNJ\Desktop'  # <-- Change this to your Desktop or any folder

# File type categories
file_types = {
    'Images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Music': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css'],
    'Others': []
}

def create_folder(folder_name):
    folder_path = os.path.join(folder_to_clean, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def move_file(file_name, dest_folder):
    shutil.move(os.path.join(folder_to_clean, file_name),
                os.path.join(dest_folder, file_name))

def cleanup():
    for file in os.listdir(folder_to_clean):
        file_path = os.path.join(folder_to_clean, file)
        if os.path.isfile(file_path):
            moved = False
            for folder, extensions in file_types.items():
                if any(file.lower().endswith(ext) for ext in extensions):
                    dest_folder = create_folder(folder)
                    move_file(file, dest_folder)
                    moved = True
                    break
            if not moved:
                dest_folder = create_folder('Others')
                move_file(file, dest_folder)

if __name__ == "__main__":
    cleanup()
    print("✅ Cleanup Completed!")
def clear_temp_files():
    temp_folder = os.environ.get('TEMP')
    if temp_folder:
        for file in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        print("✅ Temporary files cleared!")
    else:
        print("❌ Temporary folder not found!")

if __name__ == "__main__":
    cleanup()
    print("✅ Cleanup Completed!")
    clear_temp_files()
