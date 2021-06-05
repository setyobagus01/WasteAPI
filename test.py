import requests

BASE = "http://127.0.0.1:5000/"

data = [{"wasteType": "Clothes", "description": "Clothes are the things that people wear, such as shirts , coats , trousers , and dresses."}]

for i in range(len(data)):
    response = requests.put(BASE + "api/waste", data[i])
    print(response.json())

input()
response = requests.get(BASE + "/api/waste/2")
print(response.json())
