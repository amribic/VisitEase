from flask import Flask, redirect, session, request, render_template_string, flash, url_for, jsonify
from healthapp.google_fit import get_flow, get_steps, get_heart_rate, get_calories, get_distance, save_fitness_data
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import json
import os
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for localhost development
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize Firebase
try:
    cred = credentials.Certificate('../../avi-cdtm-hack-team-1613-firebase-adminsdk-fbsvc-14ccd2ea46.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'avi-cdtm-hack-team-1613.appspot.com'
    })
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

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = auth.get_user_by_email(email)
        flask_user = User(user.uid, email)
        login_user(flask_user, remember=True)
        
        session['user_id'] = user.uid
        session['email'] = email
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Login successful'})
    except auth.UserNotFoundError:
        return jsonify({'success': False, 'message': 'User not found'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        
        db.collection('users').document(user.uid).collection('profile').document('data').set({
            'email': email,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        
        flask_user = User(user.uid, email)
        login_user(flask_user, remember=True)
        
        session['user_id'] = user.uid
        session['email'] = email
        session.modified = True
        
        try:
            # Get a reference to the default storage bucket associated with your project
            bucket = storage.bucket()
            print(f"Accessed bucket: {bucket.name}")

            # --- Create the "Folder" (by creating an empty object) ---
            # Cloud Storage uses a flat namespace. We simulate folders by creating
            # objects with names containing '/'. Creating an empty object like this
            # makes the folder appear in the console.

            # Get a blob (object) reference with the desired "folder" name
            blob = bucket.blob(f'users/{user.uid}/image-data')

            # Upload an empty string (or empty bytes) to create the object.
            # This is how you make the folder visible without putting a file inside yet.
            blob.upload_from_string('')

            print(f"Successfully created 'folder' (empty object) named: users/{user.uid}/image-data")

        except Exception as e:
            print(f"An error occurred while accessing storage or creating the folder: {e}")

        return jsonify({'success': True, 'message': 'Signup successful'})
        
    except auth.EmailAlreadyExistsError:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
        return jsonify({'error': 'Not authenticated'}), 401
        
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
        return jsonify({'url': auth_url})
    except Exception as e:
        app.logger.error(f"Error in /authorize: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/oauth2callback')
def oauth2callback():
    try:
        # Get state from request
        state = json.loads(request.args.get('state', '{}'))
        user_id = state.get('user_id')
        email = state.get('email')
        
        if not user_id or not email:
            return redirect('http://localhost:5173/login')
            
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
        
        # Fetch and store fitness data
        try:
            steps = get_steps(creds.token)
            heart_rate = get_heart_rate(creds.token)
            calories = get_calories(creds.token)
            distance = get_distance(creds.token) / 1000
            
            save_fitness_data(user_id, steps, heart_rate, calories, distance)
        except Exception as e:
            app.logger.error(f"Error fetching fitness data: {e}")
        
        # Redirect back to the same page with success parameter
        return redirect('http://localhost:5173/google-fit?success=true')
    except Exception as e:
        app.logger.error(f"Error in callback: {e}")
        return redirect('http://localhost:5173/login')

@app.route('/fitness')
@login_required
def fitness():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
        
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Not connected to Google Fit'}), 401

    try:
        steps = get_steps(access_token)
        heart_rate = get_heart_rate(access_token)
        calories = get_calories(access_token)
        distance = get_distance(access_token) / 1000

        save_fitness_data(current_user.id, steps, heart_rate, calories, distance)

        return jsonify({
            'connected': True,
            'data': {
                'steps': steps,
                'heart_rate': {
                    'average': heart_rate.average,
                    'min': heart_rate.min,
                    'max': heart_rate.max
                },
                'calories': calories,
                'distance': distance
            }
        })
    except Exception as e:
        app.logger.error(f"Error fetching fitness data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True, use_reloader=False)