from secrets import SystemRandom
from requests import post
from time import sleep

if __name__ == "__main__":
    while True:
        post("http://127.0.0.1:5001/api/weather/post",
             json ={'temp': round(SystemRandom().uniform(25.5, 30), 2),
                    'hum': round(SystemRandom().uniform(30.1, 40), 2),
                    'press': round(SystemRandom().uniform(950.1, 1000), 2)})
        sleep(1)