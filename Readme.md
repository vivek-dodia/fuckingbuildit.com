## to use it

clone the repo

create .env similar to the example one and insert your openapi key

## editing the py

in case you are just self hosting, make sure to comment out all the flask limiter commands or if you plan on publically host it, make sure you have correct rate limiting place

*limiter = Limiter(key_func=get_remote_address, default_limits=["100 per day", "20 per hour"])*

## running directly by calling the .py locally or creating the dockerfile / image to run it locally or any serverless platform

## running directly by calling the .py locally

once in the same directory, just run the .py and it should bring up the flask server and you should be able to access it via localhost:5000 / localip:5000 / 127.0.0.1:5000 

and 

### debug if you are getting error once the flask is up but not returning any queries, comment out or enable these print statements
```
response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return "Error: Unable to generate idea"
```
### changing the gpt model to run the api against

https://platform.openai.com/docs/models

```
data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [{"role": "system", "content": prompt}]
    }
```
### editing the input validation for queries, edit the following
```
pattern = re.compile("^[a-zA-Z0-9, ]+$")
```

## creating the dockerfile / image to run it locally or any serverless platform

in the same directly as the cloned repo, create a dockerfile and put the following in it

```
### Use an official Python runtime as a base image
FROM python:3.9-slim

### Set the working directory in the container to /app
WORKDIR /app

### Copy the current directory contents into the container at /app
COPY . /app

### Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

### Make port 5000 available to the world outside this container, feel free to change the port
EXPOSE 5000

### Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

### Run whatshouldifuckingbuild.py when the container launches
CMD ["python", "whatshouldifuckingbuild.py"]

save the file and run the following to build the image and save it locally

docker build -t whatshouldifuckingbuild .

run it locally via 

docker run -p 5000:5000 whatshouldifuckingbuild
```