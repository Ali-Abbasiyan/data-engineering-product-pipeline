import requests

url = "https://dummyjson.com/products"

response = requests.get(url, timeout=30)

data = response.json()

print("Status Code:", response.status_code)
print("Total Products:", data["total"])
print("Returned Products:", len(data["products"]))
print("Skip:", data["skip"])
print("Limit:", data["limit"])