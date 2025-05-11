from flask import Flask, redirect, session, request, render_template_string, flash, url_for, jsonify
from healthapp.google_fit import get_flow, get_steps, get_heart_rate, get_calories, get_distance, save_fitness_data
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from image_data.gemini_api import call_gemini_api
from voice_chat import voice_chat_bp
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import json
from collections import defaultdict
import datetime
import os
from datetime import timedelta
from flask_cors import CORS
from PIL import Image
import tempfile
import io
import uuid
from threading import Lock
import asyncio
import wave
from flask import make_response
import openai
from dotenv import load_dotenv

conversations = {}
conversations_lock = Lock()

app = Flask(__name__)
# Enable CORS for localhost development
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:3000'])
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Register blueprints
app.register_blueprint(voice_chat_bp, url_prefix='/api')

# Initialize Firebase
try:
    firebase_credentials = {
        "type": os.getenv('FIREBASE_TYPE'),
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
        "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
        "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
    }
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'avi-cdtm-hack-team-1613.firebasestorage.app'
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
    full_name = request.form.get('fullName')
    date_of_birth = request.form.get('dateOfBirth')
    
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        
        db.collection('users').document(user.uid).set({
            'email': email,
            'full_name': full_name,
            'date_of_birth': date_of_birth,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        
        flask_user = User(user.uid, email)
        login_user(flask_user, remember=True)
        
        session['user_id'] = user.uid
        session['email'] = email
        session.modified = True
        print('test1')
        try:
            # Get a reference to the default storage bucket associated with your project
            print('test')
            bucket = storage.bucket(name='avi-cdtm-hack-team-1613.firebasestorage.app')
            print(f"Accessed bucket: {bucket.name}")

            # --- Create the "Folder" (by creating an empty object) ---
            # Cloud Storage uses a flat namespace. We simulate folders by creating
            # objects with names containing '/'. Creating an empty object like this
            # makes the folder appear in the console.

            # Get a blob (object) reference with the desired "folder" name
            blob = bucket.blob(f'users/{user.uid}/user-info')

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
            return jsonify({'error': 'Invalid state'}), 400
            
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
            # Always try to get steps and distance (basic activity data)
            steps = get_steps(creds.token)
            distance = get_distance(creds.token) / 1000
            
            # Try to get heart rate and calories, but don't fail if not available
            try:
                heart_rate = get_heart_rate(creds.token)
            except Exception as e:
                print(f"Error getting heart rate data: {e}")
                heart_rate = {"average": 0, "min": 0, "max": 0}
                
            try:
                calories = get_calories(creds.token)
            except Exception as e:
                print(f"Error getting calories data: {e}")
                calories = 0
            
            if save_fitness_data(user_id, steps, heart_rate, calories, distance):
                # Return a success response that will be handled by the popup window
                return '''
                <html>
                    <body>
                        <script>
                            window.opener.postMessage({ type: 'GOOGLE_FIT_SUCCESS' }, '*');
                            window.close();
                        </script>
                    </body>
                </html>
                '''
            else:
                return '''
                <html>
                    <body>
                        <script>
                            window.opener.postMessage({ type: 'GOOGLE_FIT_ERROR', error: 'Failed to save fitness data' }, '*');
                            window.close();
                        </script>
                    </body>
                </html>
                '''
        except Exception as e:
            app.logger.error(f"Error fetching fitness data: {e}")
            return '''
            <html>
                <body>
                    <script>
                        window.opener.postMessage({ type: 'GOOGLE_FIT_ERROR', error: 'Failed to fetch fitness data' }, '*');
                        window.close();
                    </script>
                </body>
            </html>
            '''
    except Exception as e:
        app.logger.error(f"Error in callback: {e}")
        return '''
        <html>
            <body>
                <script>
                    window.opener.postMessage({ type: 'GOOGLE_FIT_ERROR', error: 'Authentication failed' }, '*');
                    window.close();
                </script>
            </body>
        </html>
        '''

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
                    'average': heart_rate['average'],
                    'min': heart_rate['min'],
                    'max': heart_rate['max']
                },
                'calories': calories,
                'distance': distance
            }
        })
    except Exception as e:
        app.logger.error(f"Error fetching fitness data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    image_type = request.args.get('image_type')
    uuid = request.args.get('uuid')
    file = request.files.get('image')
    if file and file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        user_id = current_user.id
        bucket = storage.bucket(name='avi-cdtm-hack-team-1613.firebasestorage.app')
        blob = bucket.blob(f'users/{user_id}/image-data/{image_type}/{uuid}/{file.filename}')
        blob.upload_from_file(file, content_type=file.content_type)
        return jsonify({'success': True, 'message': 'Image uploaded successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid image format'}), 400

def download_images_from_firebase(user_id, image_type, usid):
    bucket = storage.bucket(name='avi-cdtm-hack-team-1613.firebasestorage.app')
    prefix = f'users/{user_id}/image-data/{image_type}/{usid}/'
    blobs = list(bucket.list_blobs(prefix=prefix))

    image_files = []
    for blob in sorted(blobs, key=lambda b: b.name):
        img_data = blob.download_as_bytes()
        image_files.append(io.BytesIO(img_data))

    return image_files


def upload_pdf_to_firebase(local_pdf_path, user_id, file_type, uuid):
    bucket = storage.bucket(name='avi-cdtm-hack-team-1613.firebasestorage.app')
    blob = bucket.blob(f'users/{user_id}/pdf-data/{file_type}/{uuid}.pdf')
    blob.upload_from_filename(local_pdf_path, content_type='application/pdf')
    return blob.public_url

def convert_images_to_pdf_and_upload(image_streams, user_id, image_type, uuid):
    try:
        # First, combine all images into a single PDF
        images = []
        for stream in image_streams:
            img = Image.open(stream).convert('RGB')
            images.append(img)

        if not images:
            raise ValueError("No images found")

        # Create a temporary PDF with all images
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            images[0].save(tmp.name, save_all=True, append_images=images[1:])
            tmp_path = tmp.name

        print(f"Image type: {image_type}")
        
        # Make a single Gemini API call with the combined PDF
        data = call_gemini_api(tmp_path, image_type)
        
        # Format the data based on type
        if (image_type == "labData" or image_type == "medicationPlan"):
            data = {image_type: data, 'created_at': firestore.SERVER_TIMESTAMP}
        else:
            data['created_at'] = firestore.SERVER_TIMESTAMP
        print(f"Got the data: \n{data}")
        db.collection('users').document(user_id).collection(image_type).document(uuid).set(data)

        # Upload the combined PDF to Firebase
        pdf_url = upload_pdf_to_firebase(tmp_path, user_id, image_type, uuid)
        
        # Clean up the temporary file
        os.remove(tmp_path)

        return pdf_url
    except Exception as e:
        print(f"Error converting/uploading PDF: {e}")
        return None

@app.route('/convert-images-to-pdf', methods=['POST'])
@login_required
def convert_images_to_pdf():
    image_type = request.form.get('image_type')
    uuid = request.form.get('uuid')
    print(image_type, uuid)
    if not image_type or not uuid:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    user_id = current_user.id
    print(user_id)
    
    # Download all images for this upload
    image_streams = download_images_from_firebase(user_id, image_type, uuid)
    if not image_streams:
        return jsonify({'success': False, 'message': 'No images found in Firebase'}), 404

    # Process all images at once
    pdf_url = convert_images_to_pdf_and_upload(image_streams, user_id, image_type, uuid)
    
    if pdf_url:
        return jsonify({'success': True, 'pdf_url': pdf_url})
    else:
        return jsonify({'success': False, 'message': 'PDF generation failed'}), 500


@app.route('/get-structured-data', methods=["GET"])
def get_structured_data():
    user_id = request.args.get('user_id')
    return model_user_data(user_id)

def model_user_data(uuid: str):

    user_ref = db.collection('users').document(uuid)

    sub_collections = user_ref.collections()

    user_model_dict = defaultdict()

    for collection in sub_collections:
        docs = collection.order_by(field_path="created_at", direction=firestore.Query.DESCENDING).limit(1)
        for doc in docs.stream():
            doc_dict = doc.to_dict()
            doc_dict['created_at'] = datetime.datetime.fromtimestamp(doc_dict['created_at'].timestamp()).strftime('%d-%m-%Y')
            user_model_dict[collection.id] = doc_dict

    return user_model_dict

@app.route('/get-pdf-by-type-for-user', methods=["GET"])
def get_user_type_pdf():
    user_id = request.args.get('user_id')
    file_type = request.args.get('file_type')

    if not user_id or not file_type:
        return jsonify({"error": "Missing user_id or file_type"}), 400
    
    prefix = f"users/{user_id}/pdf-data/{file_type}/"

    try:
        bucket = storage.bucket(name='avi-cdtm-hack-team-1613.firebasestorage.app')
        blobs = list(bucket.list_blobs(prefix=prefix))

        if not blobs:
            return jsonify({"error": "No files found"}), 404
        
        newest_blob = sorted(blobs, key=lambda b:b.updated, reverse=True)[0]

        url = newest_blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="GET",
            response_disposition='inline' #i frame preview
        )

        return jsonify({"url": url, "name": newest_blob.name})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-user-ids', methods=["GET"])
def get_user_ids():
    user_docs = db.collection('users').stream()
    return [doc.id for doc in user_docs]

@app.route('/get-user-basic-profile', methods=["GET"])
def get_user_basic_profile():
    user_id = request.args.get('user_id')
    doc = db.collection('users').document(user_id).get()
    if doc.exists:
        data = doc.to_dict()
        return jsonify({
            'user_id': user_id,
            'full_name': data.get('full_name', 'Unknown Patient'),
            'date_of_birth': data.get('date_of_birth', ''),
            'email': data.get('email', ''),
            'created_at': str(data.get('created_at', ''))
        })
    else:
        return jsonify({
            'user_id': user_id,
            'full_name': 'Unknown Patient',
            'date_of_birth': '',
            'email': '',
            'created_at': ''
        })

# --- DOCTOR CHAT ENDPOINT ---
@app.route('/api/doctor-chat', methods=['POST'])
def doctor_chat():
    try:
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'OpenAI API key not set'}), 500
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user_id = data['user_id']
        user_context = model_user_data(user_id)

        # Always prepend a system prompt
        system_prompt = {"role": "system", "content": "You are GPT-4o, a highly specialized clinical‐decision support assistant, directly integrated into the workflow of a board-certified physician. Your purpose is to help the doctor work faster, safer, and more confidently.\nKnowledge & Evidence\nAlways draw on the latest peer-reviewed literature, clinical guidelines (e.g. ACCF/AHA, NICE, WHO, UpToDate), and standard textbooks.\nWhen you state data (e.g. sensitivities, drug dosages, study outcomes), cite your source and year (e.g. \"per 2024 ACC/AHA Guideline\").\nIf you're uncertain or the question lies outside established guidelines, ask a clarifying question or suggest consulting a subspecialist.\nTone & Style\nUse concise, precise language and standard medical terminology.\nWhen communicating patient-facing language or lay explanations, translate jargon into clear, empathic phrasing.\nMaintain professional neutrality—avoid jargon overload, value‐judgments, or sensationalism.\nWorkflow Integration\nSummarize key findings in bullet points or tables (e.g. differential diagnoses, drug dosing, management algorithms).\nFlag \"high–priority\" safety concerns (e.g. drug interactions, red-flag symptoms) at the top of your response.\nWhen requested, generate templated notes (SOAP, H&P, discharge summaries) that adhere to common EHR formatting.\nInteraction Guidelines\nIf the doctor's query is ambiguous, ask one focused clarifying question rather than guessing.\nOffer to drill down into epidemiology, pathophysiology, diagnostics, therapeutics, or patient education as needed.\nBe ready to generate visual aids (charts, algorithm diagrams) on request, formatted for quick review.\nYou exist to make each clinical encounter safer, more efficient, and more evidence‐based—think like an attending physician's most trusted senior resident. Keep the responses short and concise. Only output text and not any weird formatting."}

        # If frontend sends a full messages array, use it (prepend context as system message)
        if 'messages' in data:
            messages = data['messages']
            # Prepend a system message with patient context if not already present
            if not messages or messages[0].get('role') != 'system' or messages[0].get('content') != system_prompt['content']:
                messages = [system_prompt, {"role": "system", "content": f"Patient context: {json.dumps(user_context, ensure_ascii=False)}"}] + messages
            elif len(messages) == 1 or messages[1].get('role') != 'system' or not messages[1].get('content', '').startswith('Patient context:'):
                messages = [messages[0], {"role": "system", "content": f"Patient context: {json.dumps(user_context, ensure_ascii=False)}"}] + messages[1:]
        else:
            # Otherwise, build a single-turn message
            if 'message' not in data:
                return jsonify({'error': 'Missing message'}), 400
            message = data['message']
            messages = [
                system_prompt,
                {"role": "system", "content": f"Patient context: {json.dumps(user_context, ensure_ascii=False)}"},
                {"role": "user", "content": message}
            ]

        import openai
        client = openai.OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        return jsonify({'response': response.choices[0].message.content})
    except Exception as e:
        print(f"Error in doctor_chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True, use_reloader=False)