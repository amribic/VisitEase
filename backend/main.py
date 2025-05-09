from flask import Flask, redirect, session, request
from healthapp.google_fit import get_flow, get_steps, get_heart_rate, get_calories, get_distance

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return '<a href="/authorize">Connect Google Fit</a>'


@app.route('/authorize')
def authorize():
    try:
        flow = get_flow()
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        session['state'] = state
        return redirect(auth_url)
    except Exception as e:
        app.logger.error(f"Error in /authorize: {e}")
        return f"An error occurred: {e}", 500


@app.route('/oauth2callback')
def oauth2callback():
    flow = get_flow()
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    session['access_token'] = creds.token
    return redirect('/fitness')


@app.route('/fitness')
def fitness():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/authorize')

    steps = get_steps(access_token)
    heart_rate = get_heart_rate(access_token)
    calories = get_calories(access_token)
    distance = get_distance(access_token) / 1000  # Convert to kilometers

    return f"""
    <h1>Your Fitness Data (Last 24 Hours)</h1>
    <p>Steps: {steps}</p>
    <p>Heart Rate:</p>
    <ul>
        <li>Average: {heart_rate['average']:.1f} BPM</li>
        <li>Minimum: {heart_rate['min']:.1f} BPM</li>
        <li>Maximum: {heart_rate['max']:.1f} BPM</li>
    </ul>
    <p>Calories Burned: {calories:.1f} kcal</p>
    <p>Distance: {distance:.2f} km</p>
    """


if __name__ == '__main__':
    app.run(port=8080, debug=True)