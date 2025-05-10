import os
from google_auth_oauthlib.flow import Flow
import requests
import datetime
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing firebase_config
sys.path.append(str(Path(__file__).parent.parent.parent))
from firebase_config import get_firestore_db
from firebase_admin import firestore

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(__file__))))), 'client_secret.json')

# Initialize Firestore
db = get_firestore_db()


def get_flow():
    try:
        if not os.path.exists(CLIENT_SECRETS_FILE):
            raise FileNotFoundError(f"client_secret.json not found at {CLIENT_SECRETS_FILE}")
        return Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
    except Exception as e:
        print(f"Error in get_flow: {e}")
        raise


def get_fitness_data(access_token, data_type):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = end_time - 86400000  # last 24 hours

    body = {
        "aggregateBy": [{
            "dataTypeName": data_type
        }],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }

    res = requests.post(
        'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate',
        headers=headers,
        json=body
    )

    return res.json()


def get_steps(access_token):
    data = get_fitness_data(access_token, "com.google.step_count.delta")
    steps = 0
    try:
        for bucket in data.get("bucket", []):
            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    steps += point["value"][0]["intVal"]
    except Exception as e:
        print("Error parsing step data:", e)
    return steps


def get_heart_rate(access_token):
    data = get_fitness_data(access_token, "com.google.heart_rate.bpm")
    heart_rates = []
    try:
        for bucket in data.get("bucket", []):
            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    heart_rates.append(point["value"][0]["fpVal"])
        return {
            "average": sum(heart_rates) / len(heart_rates) if heart_rates else 0,
            "min": min(heart_rates) if heart_rates else 0,
            "max": max(heart_rates) if heart_rates else 0
        }
    except Exception as e:
        print("Error parsing heart rate data:", e)
        return {"average": 0, "min": 0, "max": 0}


def get_calories(access_token):
    data = get_fitness_data(access_token, "com.google.calories.expended")
    calories = 0
    try:
        for bucket in data.get("bucket", []):
            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    calories += point["value"][0]["fpVal"]
    except Exception as e:
        print("Error parsing calories data:", e)
    return calories


def get_distance(access_token):
    data = get_fitness_data(access_token, "com.google.distance.delta")
    distance = 0
    try:
        for bucket in data.get("bucket", []):
            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    distance += point["value"][0]["fpVal"]
    except Exception as e:
        print("Error parsing distance data:", e)
    return distance  # in meters

# Save fitness data to Firestore
def save_fitness_data(user_id, steps, heart_rate, calories, distance):
    fitness_ref = db.collection("fitness_data").document(user_id)
    fitness_ref.set({
        'steps': steps,
        'heart_rate': heart_rate,
        'calories': calories,
        'distance': distance,
        'timestamp': firestore.SERVER_TIMESTAMP  # Automatically set the timestamp when data is added
    })