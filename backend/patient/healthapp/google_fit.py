import os
from google_auth_oauthlib.flow import Flow
import requests
import datetime
from firebase_config import db
from firebase_admin import firestore

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Define scopes in order of importance
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',  # Most important - for steps and distance
    'https://www.googleapis.com/auth/fitness.heart_rate.read',  # Optional - for heart rate
    'https://www.googleapis.com/auth/fitness.body.read'  # Optional - for body metrics
]
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(__file__))))), 'client_secret.json')


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

    try:
        res = requests.post(
            'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate',
            headers=headers,
            json=body
        )
        res.raise_for_status()  # Raise an exception for bad status codes
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fitness data: {e}")
        return {"bucket": []}


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
    try:
        data = get_fitness_data(access_token, "com.google.heart_rate.bpm")
        heart_rates = []
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
    try:
        fitness_ref = db.collection('users').document(user_id).collection('fitness_data').document('google_fit')
        fitness_ref.set({
            'steps': steps,
            'heart_rate': heart_rate,
            'calories': calories,
            'distance': distance,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        print(f"Error saving fitness data: {e}")
        return False