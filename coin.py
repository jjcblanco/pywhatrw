import time
import datetime
from datetime import datetime
import requests

def convert(datetime_str):
    datetime_str = time.mktime(datetime_str)
      
    format = "%b %d %Y %r" # The format
    dateTime = time.strftime(format, time.gmtime(datetime_str))
    return dateTime


start = (2021, 12, 4, 10, 7, 00, 1, 48, 0)
end = (2021, 13, 4, 10, 7, 00, 1, 48, 0)
print(datetime.now)
print(convert(start))
print(convert(end))

dt_object1 = datetime.strptime(convert(start), "%b %d %Y %H:%M:%S %p")
print("dt_object1 =", dt_object1)

dt_object2 = datetime.strptime(convert(end), "%b %d %Y %H:%M:%S %p")
print("dt_object2 =", dt_object2)


tm1=int(round(datetime.timestamp(dt_object1)))
tm2=int(round(datetime.timestamp(dt_object2)))

#response = requests.get("http://api.open-notify.org/astros.json")
query = {'coin':'ETH', 'start':tm1, 'end':tm2,'period':'1h'}
print(query)
response = requests.get("https://api.coin360.com/coin/historical", params=query)

#print(response)

#print(response.content) # Return the raw bytes of the data payload
#print(response.text) # Return a string representation of the data payload
print(response.json()) # This method is convenient when the API returns JSON
