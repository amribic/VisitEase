from collections import defaultdict
from flask import Blueprint, request, jsonify, send_file, session
import openai
import os
import json
import datetime
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from google.cloud import texttospeech
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import firestore, credentials
import io

# Load environment variables
load_dotenv()

# Initialize Firebase with environment variables
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
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
    }
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
    })
except ValueError:
    pass

# Initialize Firestore client
db = firestore.client()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your OpenAI API key.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Initialize Google Cloud TTS client with credentials from environment
google_cloud_credentials = {
    "type": os.getenv('GOOGLE_TYPE'),
    "project_id": os.getenv('GOOGLE_PROJECT_ID'),
    "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('GOOGLE_CLIENT_EMAIL'),
    "client_id": os.getenv('GOOGLE_CLIENT_ID'),
    "auth_uri": os.getenv('GOOGLE_AUTH_URI'),
    "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_CERT_URL')
}
credentials = service_account.Credentials.from_service_account_info(google_cloud_credentials)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

voice_chat_bp = Blueprint('voice_chat', __name__)

SCHEMA_DOCTOR_LETTER = {
    "reasonForReferral": {
        "type": "string",
        "description": "The reason for the patient's referral."
    },
    "anamnesis": {
        "type": "array",
        "items": {
            "type": "string"
        },
        "description": "A list of anamnesis statements."
    },
    "clinicalFindings": {
        "type": "array",
        "description": "Clinical findings. This is an array of strings that contain information about the patient's clinical findings.",
        "items": {
            "type": "string"
        },
    },
    "assessment": {
        "type": "array",
        "items": {
            "type": "string"
        },
        "description": "A list of assessment statements."
    },
    "plan": {
        "type": "array",
        "items": {
            "type": "string"
        },
        "description": "A list of plan statements."
    },
    "medication": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "substance": {
                    "type": ["string", "null"]
                },
                "medicationName": {
                    "type": ["string", "null"]
                },
                "dosage": {
                    "type": ["string", "null"]
                },
                "pillForm": {
                    "type": ["string", "null"]
                },
                "numberMorning": {
                    "type": ["number", "null"]
                },
                "numberNoon": {
                    "type": ["number", "null"]
                },
                "numberEvening": {
                    "type": ["number", "null"]
                },
                "numberNight": {
                    "type": ["number", "null"]
                },
                "unit": {
                    "type": ["string", "null"]
                },
                "notes": {
                    "type": ["string", "null"]
                }
            },
            "required": [
                "substance",
                "medicationName",
                "dosage",
                "pillForm",
                "numberMorning",
                "numberNoon",
                "numberEvening",
                "numberNight",
                "unit",
                "notes"
            ]
        },
        "description": "Medication plan details."
    },
    "labData": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "unit": {
                    "type": ["string", "null"]
                },
                "value": {
                    "type": ["number", "null"]
                },
                "referenceRange": {
                    "type": ["string", "null"]
                },
                "testName": {
                    "type": ["string", "null"]
                }
            },
            "required": [
                "unit",
                "value",
                "referenceRange",
                "testName"
            ]
        },
        "description": "A list of lab data entries."
    },
    "required": [
        "reasonForReferral",
        "anamnesis",
        "clinicalFindings",
        "assessment",
        "plan",
        "medication",
        "labData"
    ]
}

SCHEMA_MEDICATION_PLAN = {
    "medication": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "substance": {
                    "type": ["string", "null"]
                },
                "medicationName": {
                    "type": ["string", "null"]
                },
                "dosage": {
                    "type": ["string", "null"]
                },
                "pillForm": {
                    "type": ["string", "null"]
                },
                "numberMorning": {
                    "type": ["number", "null"]
                },
                "numberNoon": {
                    "type": ["number", "null"]
                },
                "numberEvening": {
                    "type": ["number", "null"]
                },
                "numberNight": {
                    "type": ["number", "null"]
                },
                "unit": {
                    "type": ["string", "null"]
                },
                "notes": {
                    "type": ["string", "null"]
                }
            },
            "required": [
                "substance",
                "medicationName",
                "dosage",
                "pillForm",
                "numberMorning",
                "numberNoon",
                "numberEvening",
                "numberNight",
                "unit",
                "notes"
            ]
        },
        "description": "Medication plan details."
    }
}

SCHEMA_LAB_DATA = {
    "labData": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "unit": {
                    "type": ["string", "null"]
                },
                "value": {
                    "type": ["number", "null"]
                },
                "referenceRange": {
                    "type": ["string", "null"]
                },
                "testName": {
                    "type": ["string", "null"]
                }
            },
            "required": [
                "unit",
                "value",
                "referenceRange",
                "testName"
            ]
        },
        "description": "A list of lab data entries."
    }
}

SCHEMA_INSURANCE_CARD = {
    "name": {
        "type": "string",
        "description": "The full name (first and last) of the insured person."
    },
    "insuranceProvider": {
        "type": "string",
        "description": "The name of the insurance provider."
    },
    "insuranceNumber": {
        "type": "string",
        "description": "The number of the insurance. Can be found on bottom left of insurance card."
    },
    "customerNumber": {
        "type": "string",
        "description": "The identifier of the insured person, also known as Versichertennummer. Might start with a letter, usually on bottom of insurance card."
    },
    "cardNumber": {
        "type": "string",
        "description": "The identifying number of the card. Can be found on the back of the card on the bottom left."
    },
    "birthDate": {
        "type": "string",
        "description": "Birthdate of the insured person in DD.MM.YYYY format. Can be found on the back of the insurance card on the right side."
    },
    "seventhIdentityNumber": {
        "type": "string",
        "description": "Kennnummer des Trägers/Krankenkasse"
    },
    "expirationDate": {
        "type": "string",
        "description": "Expiration date of the insurance card. Can be found on the bottom right of the backside of the card."
    }
}

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

@voice_chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        message = data['message']

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
            
        # Get user data using model_user_data function
        user_model_dict = model_user_data(user_id)
        
        # Enhanced system prompt for medical data collection
        system_prompt = f"""You are an empathetic healthcare professional who is supposed to have a short conversation with a patient who potentially already shared some relevant patient data like recent lab results, doctor's letters, their insurance card information and a medication plan. Your goal is to use the context provided in a single dictionary to derive natural language questions that can bring valuable insight into the state and well-being of the patient for a doctor but also not overwhelm the user in their complexity and length. Make sure to use relatively simple language and be empathetic.

        The following schemas detail how the inputs of the user might be structured for each type of input. These inputs are possible:
        * insuranceCard (Insurance Card Data)
        * doctorLetter (The most recent Doctor Letter (Arztbrief))
        * labData (The most recent data gathered from a laboratory analysis)
        * medicationPlan (A medication plan detailing what medication to take at which times)
        The Schema are defined as follows
        insuranceCard:
        {SCHEMA_INSURANCE_CARD}
        doctorLetter:
        {SCHEMA_DOCTOR_LETTER}
        labData:
        {SCHEMA_LAB_DATA}
        medicationPlan:
        {SCHEMA_MEDICATION_PLAN}
        You will receive the contextual user data in a dictionary that uses the previously defined inputs as keys (i.e. 'insuranceCard', 'doctorLetter', 'labData', 'medicationPlan') and the corresponding dictionary (defined by the SCHEMA) as the value.
        Your task is to lead a natural conversation and ask a maximum of 5 questions to find out how the patient feels. Your goal is to find out what the doctors can't describe in their letters and lab analysis - the patients feelings and emotions. 
        If you notice that the patient wants to end the conversation specifically ask him if he wants to end the conversation. Usually you can assume that they want to continue but if you notice the patient getting aggravated feel free to ask them to stop right there. You can also just end the conversation early by saying these are all the questions I wanted to ask today, thank you for your time. That way the user doesn't even realize that you just purposefully ended the conversation in order to avoid confrontation.
        For undefined behavior, i.e. queries or answers that have nothing to do with the medical history of the patient and are in general not related to the healthcare of the patient at all are not to be answered. You can just respond with the standard reponse of: "At this time I'm not able to make a comment about this specific topic, let's continue talking about your health".
        Do not try to match the users style of speaking (i.e. slang, millenial...) as this might irritate them. The following dictonary is the described user context:
        {json.dumps(user_model_dict, indent=4, ensure_ascii=False)}"""
        
        # Special handling for initial message
        if message == 'start':
            initial_prompt = f"""Based on the patient's data, start the conversation with a specific question about their health. DO NOT use generic greetings or ask how you can help. Instead, immediately ask about something specific from their medical data. For example:
            - If they have lab results, ask about how they're feeling regarding those specific results
            - If they have a medication plan, ask about their experience with the medications
            - If they have a doctor's letter, ask about their condition mentioned in the letter
            The patient's data is: {json.dumps(user_model_dict, indent=4, ensure_ascii=False)}"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": initial_prompt}
                ]
            )
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
        
        return jsonify({'response': response.choices[0].message.content})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@voice_chat_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['file']
        if not audio_file.filename:
            return jsonify({'error': 'No audio file selected'}), 400

        # Save the audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            # Transcribe using OpenAI's Whisper API
            with open(temp_file.name, 'rb') as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio
                )
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            return jsonify({'text': transcript.text})
    except Exception as e:
        print(f"Error in transcribe endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@voice_chat_bp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",  # Using a natural-sounding female voice
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,  # Slightly slower for more natural speech
            pitch=0.0  # Natural pitch
        )

        # Perform the text-to-speech request
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(response.audio_content)
            temp_file_path = temp_file.name

        # Send the audio file
        return send_file(
            temp_file_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='speech.mp3'
        )

    except Exception as e:
        print(f"Error in text-to-speech endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500 