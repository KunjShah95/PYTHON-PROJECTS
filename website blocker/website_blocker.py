# access_blocker.py
from flask import Flask, redirect, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Get the secret key from environment variable

# Load or initialize access data
def load_access_data():
    if os.path.exists('access_data.json'):
        with open('access_data.json', 'r') as f:
            return json.load(f)
    return {}

def save_access_data(data):
    with open('access_data.json', 'w') as f:
        json.dump(data, f)

@app.route('/access/<site>')
def access_site(site):
    # List of allowed social media sites
    social_media_sites = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']
    
    print(f"Attempting to access: {site}")  # Debugging line

    # Check if the requested site is in the allowed list
    if site not in social_media_sites:
        return jsonify({"error": "Access Denied: Not a social media site."}), 403

    # Load access data
    access_data = load_access_data()
    user_id = request.remote_addr  # Using IP address as a simple user identifier

    # Initialize user access data if not present
    if user_id not in access_data:
        access_data[user_id] = {'count': 0, 'date': str(datetime.now().date())}

    # Check if the day has changed
    today = str(datetime.now().date())
    if access_data[user_id]['date'] != today:
        access_data[user_id] = {'count': 0, 'date': today}

    # Check access limit
    if access_data[user_id]['count'] < 20:
        access_data[user_id]['count'] += 1
        save_access_data(access_data)
        return redirect(f'http://{site}')
    else:
        return jsonify({"error": "Access limit reached for today."}), 403

if __name__ == '__main__':
    app.run(debug=True)