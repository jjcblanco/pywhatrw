import requests

#response = requests.get("http://api.open-notify.org/astros.json")
query = {'coin':'BTC', 'convert':'application/json'}
response = requests.get("https://api.coin360.com/#/Coins/CoinLatestGet", params=query)
#print(response)

#print(response.content) # Return the raw bytes of the data payload
#print(response.text) # Return a string representation of the data payload
print(response.json()) # This method is convenient when the API returns JSON
