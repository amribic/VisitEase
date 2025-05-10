from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import time

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

myfile = client.files.upload(file="/home/jonasbiermann/VisitEase/backend/patient/image-data/pdfs/image-7.pdf")

SCHEMA = {
    "patientName": {
      "type": "string",
      "description": "The patient's full name."
    },
    "patientDateOfBirth": {
      "type": "string",
      "description": "The patient's date of birth (e.g., DD.MM.YYYY)."
    },
    "dateOfLetter": {
      "type": "string",
      "description": "The date the letter was written (e.g., DD.MM.YYYY)."
    },
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
      "type": "object",
      "description": "Clinical findings. Keys are finding types (e.g., 'RR', 'EKG'), values are dictionaries with finding details.",
      "additionalProperties": {
        "type": "object",
        "properties": {},
        "additionalProperties": True
      }
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
      ],
      "description": "Medication plan details."
    },
    "contactInformation": {
      "type": "object",
      "properties": {
        "address": {
          "type": "string"
        },
        "website": {
          "type": "string"
        },
        "phone": {
          "type": "string"
        },
        "fax": {
          "type": "string"
        },
        "email": {
          "type": "string"
        },
        "bankName": {
          "type": "string"
        },
        "iban": {
          "type": "string"
        },
        "bic": {
          "type": "string"
        }
      },
      "required": [
        "address",
        "website",
        "phone",
        "fax",
        "email",
        "bankName",
        "iban",
        "bic"
      ],
      "description": "Contact information."
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
    "filePath": {
      "type": ["string", "null"],
      "description": "File path (if applicable)."
  },
  "required": [
    "patientName",
    "patientDateOfBirth",
    "dateOfLetter",
    "reasonForReferral",
    "anamnesis",
    "clinicalFindings",
    "assessment",
    "plan",
    "medication",
    "contactInformation",
    "labData",
    "filePath"
  ]
}

PROMPT = f"""
You are an expert medical document analysis tool. Your task is to analyze the provided PDF document and extract information.

Follow these rules strictly:

* Analyze the document and extract information as accurately as possible.
* If a field cannot be determined from the document, set its value to "none".
* ALWAYS return valid JSON format.
The valid JSON format must follow the schema provided below.
{json.dumps(SCHEMA)}
Return the JSON object in a format that can be easily parsed by a computer program.
* Do not include any explanations or additional text outside the JSON object.
* Do not include any comments in the JSON object.
* Do not include any metadata or additional information in the JSON object.
* Do not include any keys or values that are not specified in the schema.
* Do not include any extra spaces or line breaks in the JSON object.
* Do not include any quotes or special characters in the JSON object.
* Do not include any HTML or XML tags in the JSON object.
Analyze the provided PDF now.
"""
start_time = time.time()
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = [PROMPT, myfile],
)
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")

response = response.text

responses = response.split("\n")
json_reponse = responses[1]

json_obj = json.loads(json_reponse)
with open("/home/jonasbiermann/VisitEase/backend/patient/image-data/model-output/model-output-1.json", "w") as json_file:
    json.dump(json_obj, json_file, indent=4, ensure_ascii=False)
