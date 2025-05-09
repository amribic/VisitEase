import os
from google_auth_oauthlib.flow import Flow
import requests
import datetime

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'client_secret.json')


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


def get_steps(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = end_time - 86400000  # last 24 hours

    body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta"
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

    steps = 0
    try:
        for bucket in res.json().get("bucket", []):
            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    steps += point["value"][0]["intVal"]
    except Exception as e:
        print("Error parsing step data:", e)

    return steps