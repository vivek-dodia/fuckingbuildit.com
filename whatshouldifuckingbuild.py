from flask import Flask, request, jsonify, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import openai
from dotenv import load_dotenv
import os
import geoip2.database

load_dotenv()  # This loads the environment variables from .env

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
limiter.init_app(app)
api_key = os.getenv('OPENAI_API_KEY')
GEOIP_DB_PATH = 'path/to/GeoLite2-Country.mmdb'  # Update with the path to your GeoLite2 database

def get_country(ip_address):
    try:
        with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
            response = reader.country(ip_address)
            return response.country.iso_code
    except Exception as e:
        print(f"Error getting country from IP: {e}")
        return None

@app.before_request
def block_country():
    if not request.remote_addr.startswith(('127.', '192.', '10.')):  # Skip local IPs
        country = get_country(request.remote_addr)
        if country not in ['US', 'CA']:  # Allow only US and Canada
            abort(403)  # Forbidden access

def call_gpt_api(keywords):
    prompt = f"Generate three Python project ideas based on the following technologies: {keywords}. Categorize the ideas into beginner, advanced, and expert levels."
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-3.5-turbo-1106",  # Ensure this is the correct model you have access to
        "messages": [{"role": "system", "content": prompt}]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return "Error: Unable to generate idea"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_idea', methods=['POST'])
@limiter.limit("5 per hour")  # Apply rate limiting to this endpoint
def generate_idea():
    print("generate_idea route called")
    user_input = request.json['keywords']
    generated_idea = call_gpt_api(user_input)
    return jsonify({'idea': generated_idea})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
