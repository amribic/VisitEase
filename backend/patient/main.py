from flask import Flask, redirect, session, request, render_template_string, flash, url_for
from healthapp.google_fit import get_flow, get_steps, get_heart_rate, get_calories, get_distance, save_fitness_data
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Firebase
try:
    cred = credentials.Certificate('../../avi-cdtm-hack-team-1613-firebase-adminsdk-fbsvc-14ccd2ea46.json')
    firebase_admin.initialize_app(cred)
except ValueError:
    pass
db = firestore.client()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    if 'user_id' in session and session['user_id'] == user_id:
        return User(user_id, session['email'])
    return None

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template_string('''
            <h1>Welcome, {{ current_user.email }}!</h1>
            <p><a href="{{ url_for('authorize') }}" class="button">Connect Google Fit</a></p>
            <p><a href="{{ url_for('logout') }}">Logout</a></p>
            <style>
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4285f4;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #357abd;
                }
            </style>
        ''')
    return render_template_string('''
        <h1>Welcome to Fitness Tracker</h1>
        <p><a href="{{ url_for('login') }}">Login</a></p>
        <p><a href="{{ url_for('signup') }}">Sign Up</a></p>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            user = auth.get_user_by_email(email)
            flask_user = User(user.uid, email)
            login_user(flask_user, remember=True)
            
            session['user_id'] = user.uid
            session['email'] = email
            session.modified = True
            
            return redirect(url_for('index'))
        except auth.UserNotFoundError:
            flash('User not found')
        except Exception as e:
            flash(f'Error: {str(e)}')
            
    return render_template_string('''
        <h1>Login</h1>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <p style="color: red;">{{ message }}</p>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <p>Email: <input type="email" name="email" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <p><input type="submit" value="Login"></p>
        </form>
        <p><a href="{{ url_for('signup') }}">Don't have an account? Sign up</a></p>
    ''')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            
            db.collection('users').document(user.uid).set({
                'email': email,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            flask_user = User(user.uid, email)
            login_user(flask_user, remember=True)
            
            session['user_id'] = user.uid
            session['email'] = email
            session.modified = True
            
            return redirect(url_for('index'))
            
        except auth.EmailAlreadyExistsError:
            flash('Email already exists')
        except Exception as e:
            flash(f'Error: {str(e)}')
    
    return render_template_string('''
        <h1>Sign Up</h1>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <p style="color: red;">{{ message }}</p>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <p>Email: <input type="email" name="email" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <p><input type="submit" value="Sign Up"></p>
        </form>
        <p><a href="{{ url_for('login') }}">Already have an account? Login</a></p>
    ''')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize')
@login_required
def authorize():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    try:
        flow = get_flow()
        # Include user ID in state
        state = {
            'user_id': current_user.id,
            'email': current_user.email
        }
        session['state'] = state
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=json.dumps(state)
        )
        return redirect(auth_url)
    except Exception as e:
        app.logger.error(f"Error in /authorize: {e}")
        return f"An error occurred: {e}", 500

@app.route('/oauth2callback')
def oauth2callback():
    try:
        # Get state from request
        state = json.loads(request.args.get('state', '{}'))
        user_id = state.get('user_id')
        email = state.get('email')
        
        if not user_id or not email:
            return redirect(url_for('login'))
            
        # Create user object and log them in
        user = User(user_id, email)
        login_user(user, remember=True)
        
        # Store in session
        session['user_id'] = user_id
        session['email'] = email
        
        # Get the token
        flow = get_flow()
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        session['access_token'] = creds.token
        session.modified = True
        
        return redirect(url_for('fitness'))
    except Exception as e:
        app.logger.error(f"Error in callback: {e}")
        return redirect(url_for('login'))

@app.route('/fitness')
@login_required
def fitness():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    access_token = session.get('access_token')
    if not access_token:
        return render_template_string('''
            <h1>Connect to Google Fit</h1>
            <p>You need to connect your Google Fit account to view your fitness data.</p>
            <p><a href="{{ url_for('authorize') }}" class="button">Connect Google Fit</a></p>
            <p><a href="{{ url_for('index') }}">Back to Home</a></p>
            <style>
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4285f4;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }
                .button:hover {
                    background-color: #357abd;
                }
            </style>
        ''')

    steps = get_steps(access_token)
    heart_rate = get_heart_rate(access_token)
    calories = get_calories(access_token)
    distance = get_distance(access_token) / 1000

    save_fitness_data(current_user.id, steps, heart_rate, calories, distance)

    return render_template_string('''
        <h1>Your Fitness Data (Last 24 Hours)</h1>
        <p>Steps: {{ steps }}</p>
        <p>Heart Rate:</p>
        <ul>
            <li>Average: {{ "%.1f"|format(heart_rate.average) }} BPM</li>
            <li>Minimum: {{ "%.1f"|format(heart_rate.min) }} BPM</li>
            <li>Maximum: {{ "%.1f"|format(heart_rate.max) }} BPM</li>
        </ul>
        <p>Calories Burned: {{ "%.1f"|format(calories) }} kcal</p>
        <p>Distance: {{ "%.2f"|format(distance) }} km</p>
        <p><a href="{{ url_for('index') }}">Back to Home</a></p>
        <p><a href="{{ url_for('authorize') }}">Refresh Data</a></p>
    ''', steps=steps, heart_rate=heart_rate, calories=calories, distance=distance)

if __name__ == '__main__':
    app.run(port=8080, debug=True, use_reloader=False)