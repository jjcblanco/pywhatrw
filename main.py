# importing the module
import pywhatkit
import time
import pyautogui
import keyboard as k
from datetime import datetime
import sys

# using Exception Handling to avoid
# unprecedented errors
try:

# sending message to receiver
# using pywhatkit
    
    print (sys.path)
     #   print(pyautogui.position())
    now = datetime.now()
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    pywhatkit.sendwhatmsg("+5491164470566","No soy homero chino \n",12, 57, False, 30)
    time.sleep(2)
    pyautogui.click(546, 670)
    time.sleep(5)
    k.press_and_release('enter')
    

    print("Successfully Sent!")

except:

# handling exception
# and printing error message
    print("An Unexpected Error!")
