from flask import Blueprint, request, jsonify, send_file
import openai
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from google.cloud import texttospeech
from google.oauth2 import service_account
import io

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your OpenAI API key.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Get the path to the Google Cloud credentials file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../..'))
cred_path = os.path.join(project_root, 'avi-cdtm-hack-team-1613-9531c63909da.json')

# Initialize Google Cloud TTS client with credentials
credentials = service_account.Credentials.from_service_account_file(cred_path)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

voice_chat_bp = Blueprint('voice_chat', __name__)

@voice_chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        message = data['message']
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant. Provide clear, accurate, and empathetic responses to health-related questions."},
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