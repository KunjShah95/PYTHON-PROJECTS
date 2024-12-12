import json
import os
from ossaudiodev import SOUND_MIXER_SPEAKER
from turtle import listen

from sklearn.kernel_ridge import KernelRidge

# User Authentication
def authenticate_user(username, password):
    user_data = load_user_data(username)
    if user_data and user_data['password'] == password:
        return True
    return False

def load_user_data(username):
    try:
        with open(f"{username}_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_user_data(username, password):
    user_data = {
        'password': password,
        'preferences': {}
    }
    with open(f"{username}_data.json", "w") as f:
        json.dump(user_data, f)

def set_password(username):
    password = input("Set your password: ")
    save_user_data(username, password)
    print("Password set successfully.")

def reset_password(username):
    user_data = load_user_data(username)
    if user_data:
        new_password = input("Enter your new password: ")
        user_data['password'] = new_password
        save_user_data(username, user_data['password'])
        print("Password reset successfully.")
    else:
        print("User not found. Please set a password first.")

# Main Loop
def main():
    username = input("Enter your username: ")
    
    # Check if user data exists
    if not load_user_data(username):
        print("No user found. Setting up your account.")
        set_password(username)
    else:
        password = input("Enter your password: ")
        if not authenticate_user(username, password):
            print("Authentication failed.")
            return

    user_id = username  # Use username as user_id for simplicity

    while True:
        command = listen()
        if command:
            response = KernelRidge.respond(command)
            SOUND_MIXER_SPEAKER(response)
            
            # Example command handling
            if "reset password" in command.lower():
                reset_password(username)
            # Add other command handling as needed...

if __name__ == "__main__":
    main()
