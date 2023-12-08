from flask import Flask, request, jsonify, render_template
import requests
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

app = Flask(__name__)

api_key = os.getenv('OPENAI_API_KEY')

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
def generate_idea():
    print("generate_idea route called")  # Add this line
    user_input = request.json['keywords']
    generated_idea = call_gpt_api(user_input)
    return jsonify({'idea': generated_idea})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    

