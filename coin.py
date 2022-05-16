import time
import datetime
from datetime import datetime
from tokenize import Double
import requests
from DatabaseHelper  import DatabaseHelper

def convert(datetime_str):
    datetime_str = time.mktime(datetime_str)
      
    format = "%b %d %Y %r" # The format
    dateTime = time.strftime(format, time.gmtime(datetime_str))
    return dateTime


start = (2021, 1, 1, 0, 0, 0, 6, 48, 1) # año mes dia hora min seg toma las 3 de la mañana por el gmt2016-01-01 03:00:00
end = (2021, 12, 31, 9, 7, 0, 1, 48, 0) #"2016-12-31 12:07:00 "

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
#print(response.json()) # This method is convenient when the API returns JSON
dbcoin = DatabaseHelper()

for ord in response.json():
    print("price:", ord["price"])
    print("market_cap:", ord["market_cap"])
    print("timestamp1:", ord["timestamp"])
    print("timestamp2:",datetime.fromtimestamp(float(ord["timestamp"])))
    #strptime(convert(start), "%b %d %Y %H:%M:%S %p"
    print('---')
    print(dbcoin.cursor.execute("INSERT INTO historical (coin,type,price,volume,market_cap,timestamp) VALUES (%s,%s,%s,%s,%s,%s)", ("ETH","ETHHASH",int(ord["price"]),int(ord["volume"]), int(ord["market_cap"]),datetime.strftime(datetime.fromtimestamp(float(ord["timestamp"])),'%Y-%m-%d %H:%M:%S'))))
#dbcoin.DBQuery("INSERT INTO table_test (coin,type,price,volume,market_cap,timestamp) VALUES (%s,%s,%f,%i,%i,%i)", ("ETH","ETHHASH",ord["price"],ord["volume"], ord["market_cap"], ord["timestamp"]))
#int(round(datetime.timestamp(datetime.strptime(str(ord["timestamp"]), "%Y-%m-%d %H:%M:%S"))
dbcoin.DBQuery("Select * from historical")
#now = datetime.now()

#print("now =", now)
#now1= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#now1= datetime.fromtimestamp(now)
#
# 
#print("now 1=", now1)