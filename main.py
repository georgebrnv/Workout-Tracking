import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")

GENDER = "male"
WEIGHT_KG = 76
HEIGHT_CM = 181
AGE = 22

print(APP_KEY, APP_ID)

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
query_input = input("What exercise did you do and for how long(miles, hrs)? ")

sheety_url = os.environ.get("SHEETY_URL")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

parameters = {
    "query": query_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

auth_header = {
    "Authorization": f"Basic {os.environ.get('AUTH_HEADER')}",
}

nutr_response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
nutr_response.raise_for_status()
result = nutr_response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
          "date": today_date,
          "time": now_time,
          "exercise": exercise["name"].title(),
          "duration": exercise["duration_min"],
          "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(url=sheety_url, json=sheet_inputs, headers=auth_header)
    print(sheet_response.text)
