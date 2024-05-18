import requests

# GET
api_url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(api_url)
print(response.json())
print(response.status_code)

# POST
api_url = "https://jsonplaceholder.typicode.com/todos"
todo = {"userId": 1, "title": "Buy milk", "completed": False}
response = requests.post(api_url, json=todo)
print(response.json())
print(response.status_code)

# PUT
api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.get(api_url)
print(response.json())
print(response.status_code)

# PATCH
api_url = "https://jsonplaceholder.typicode.com/todos/10"
todo = {"title": "Mow lawn"}
response = requests.patch(api_url, json=todo)
print(response.json())
print(response.status_code)

# DELETE
api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.delete(api_url)
print(response.json())
print(response.status_code)
