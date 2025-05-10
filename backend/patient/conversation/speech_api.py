import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from collections import defaultdict
import json
import datetime
import asyncio
from google import genai
from dotenv import load_dotenv
import os
import wave
from google.cloud import speech_v1p1beta1 as speech

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
      ],
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
      ],
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
    },
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

def getSchemas():
    return SCHEMA_DOCTOR_LETTER, SCHEMA_MEDICATION_PLAN, SCHEMA_LAB_DATA, SCHEMA_INSURANCE_CARD

SCHEMA_CONVERSATION = {
    "transcription": {
        "type": "string",
        "description": "A transcription of the conversation with speaker recognition, i.e.: \"(Speaker A) I know you've been experiencing chest pains, has this come up in the past 4 weeks? (Speaker B) No, luckily since we changed my medication I have not had problems with severe chest pains, only occasional little instances but nothing comparing to what I had before. (Speaker A) That's great to hear! [Rest of Conversation]\""
    },
    "summary": {
        "type": "string",
        "description": "A neutral summary of the conversation."
    },
    "questionAndAnswer": {
        "type": "dict",
        "description": "A dictionary of your (the models) questions (keys) and the users answers (values). This can be paraphrased but the meaning should stay the same."
    }
}

# Initialize Firebase
try:
    cred = credentials.Certificate('../../../avi-cdtm-hack-team-1613-firebase-adminsdk-fbsvc-14ccd2ea46.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'avi-cdtm-hack-team-1613.firebasestorage.app'
    })
except ValueError:
    pass
db = firestore.client()

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

print(GOOGLE_API_KEY)


client = genai.Client(api_key=GOOGLE_API_KEY)
model = "gemini-2.0-flash-live-001"
config = {"response_modalities": ["AUDIO"]}

def export_config():
    return client, model, config

def transcribe_audio_in_memory(audio_content):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )
    response = client.recognize(config=config, audio=audio)
    transcription = ""
    for result in response.results:
        alternative = result.alternatives[0]
        speaker_tag = alternative.words[0].speaker_tag if alternative.words else 1
        speaker = "Speaker A" if speaker_tag == 1 else "Speaker B"
        transcription += f"({speaker}) {alternative.transcript} "
    return transcription.strip()

def process_transcription(transcription):
    prompt = f"""Given the following transcription of a conversation between a healthcare professional (Speaker A) and a patient (Speaker B):

{transcription}

Please provide the following in JSON format:
{SCHEMA_CONVERSATION}
Extract the questions asked by the healthcare professional and the patient's answers. Paraphrase if needed but preserve the meaning."""
    response = client.generate_content(
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        model="gemini-2.0-flash"
    )
    structured_data = json.loads(response.text)
    structured_data["transcription"] = transcription
    structured_data["created_at"] = firestore.SERVER_TIMESTAMP
    return structured_data