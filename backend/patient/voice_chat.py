from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your OpenAI API key.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

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