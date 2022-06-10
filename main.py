import requests
from datetime import datetime
from time import sleep
import smtplib

MY_EMAIL = "name@gmail.com"
MY_PASSWORD = "password"
TO_EMAIL = "name@gmail.com"
MY_LAT = 12.971599
MY_LONG = 77.594566

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def within_lat_long():
    return MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()

while True:
    if time_now.hour >= sunset and within_lat_long():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr = MY_EMAIL,
                to_addrs = TO_EMAIL,
                msg = "Subject: ISS is here\n\nLook into the sky and spot it!!"
            )
    sleep(60)