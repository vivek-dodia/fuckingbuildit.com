import os
import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

def test_gpt_api():
    prompt = "Translate the following English text to French: 'Hello, how are you?'"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-4",  # You can change this to the specific model you want to test
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 60
    }

    response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)
    
    if response.status_code == 200:
        print("Success! Here's the response from GPT:")
        print(response.json()['choices'][0]['text'].strip())
    else:
        print(f"Failed to connect to GPT API. Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == '__main__':
    test_gpt_api()
