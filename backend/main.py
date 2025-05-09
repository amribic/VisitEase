from flask import Flask, redirect, session, request
from healthapp.data_extraction import get_flow, get_steps

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
    return redirect('/steps')


@app.route('/steps')
def steps():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/authorize')

    steps = get_steps(access_token)
    return f"Steps in last 24 hours: {steps}"


if __name__ == '__main__':
    app.run(port=8080, debug=True)