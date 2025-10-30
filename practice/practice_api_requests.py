import requests

# Make a request to get all products
response = requests.get('https://fakestoreapi.com/products?limit=5')

# Check if the request was successful
print("Status Code:", response.status_code)

# Get the data as JSON (converts to Python list/dict)
products = response.json()

# Print how many products we got
print("Number of products:", len(products))

# Print the first product to see its structure
print("\nFirst product:")
print(products[0])



