from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import time
from .classes.DoctorLetter import DoctorLetter
from .classes.MedicationPlan import MedicationPlan
from .classes.LabReport import LabReport
from .classes.InsuranceCard import InsuranceCard

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

def createMedicationPlan(json_obj, file_path) -> list[MedicationPlan]:
    medicationPlanEntries = []
    for jsonMedicationPlan in json_obj:
        medicationPlan = MedicationPlan(
            substance=jsonMedicationPlan["substance"],
            medicationName=jsonMedicationPlan["medicationName"],
            dosage=jsonMedicationPlan["dosage"],
            pillForm=jsonMedicationPlan["pillForm"],
            numberMorning=jsonMedicationPlan["numberMorning"],
            numberNoon=jsonMedicationPlan["numberNoon"],
            numberEvening=jsonMedicationPlan["numberEvening"],
            numberNight=jsonMedicationPlan["numberNight"],
            unit=jsonMedicationPlan["unit"],
            notes=jsonMedicationPlan["notes"],
            filePath = file_path
        )
        medicationPlanEntries.append(medicationPlan)
    return medicationPlanEntries

def createLabData(json_obj, file_path) -> list[LabReport]:
    labDataEntries = []
    for jsonLabData in json_obj:
        labData = LabReport(
            unit=jsonLabData["unit"],
            value=jsonLabData["value"],
            referenceRange=jsonLabData["referenceRange"],
            testName=jsonLabData["testName"],
            filePath=file_path
        )
        labDataEntries.append(labData)
    return labDataEntries

def createDoctorLetter(json_obj, file_path) -> DoctorLetter:
    doctorLetter = DoctorLetter(
        reasonForReferral=json_obj["reasonForReferral"],
        anamnesis=json_obj["anamnesis"],
        clinicalFindings=json_obj["clinicalFindings"],
        assessment=json_obj["assessment"],
        plan=json_obj["plan"],
        medication=createMedicationPlan(json_obj["medication"], file_path),
        labData=createLabData(json_obj['labData'], file_path),
        filePath=file_path
    )
    return doctorLetter

def createInsuranceCard(json_obj, file_path) -> InsuranceCard:
   insuranceCard = InsuranceCard(
      name = json_obj["name"],
      insuranceProvider = json_obj["insuranceProvider"],
      insuranceNumber = json_obj["insuranceNumber"],
      customerNumber = json_obj["customerNumber"],
      cardNumber = json_obj["cardNumber"],
      birthDate = json_obj["birthDate"],
      seventhIdentityNumber = json_obj["seventhIdentityNumber"],
      expirationDate = json_obj["expirationDate"]
   )
   return insuranceCard

def call_gemini_api(file_path: str, document_type: str):
      
  load_dotenv()

  GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

  client = genai.Client(api_key=GOOGLE_API_KEY)

  myfile = client.files.upload(file=file_path)

  if (document_type == "doctorLetter"):
    SCHEMA = SCHEMA_DOCTOR_LETTER
  elif (document_type == "medicationPlan"):
    SCHEMA = SCHEMA_MEDICATION_PLAN
  elif (document_type == "labData"):
    SCHEMA = SCHEMA_LAB_DATA
  elif (document_type == "insuranceCard"):
     SCHEMA = SCHEMA_INSURANCE_CARD
  else:
    raise ValueError("Invalid document type. Must be 'doctorLetter', 'medicationPlan', or 'labData'.")

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
  """ with open("/home/jonasbiermann/VisitEase/backend/patient/image-data/model-output/model-output-1.json", "w") as json_file:
      json.dump(json_obj, json_file, indent=4, ensure_ascii=False) """

  if (document_type == "doctorLetter"):
    return createDoctorLetter(json_obj, file_path).to_dict()
  elif (document_type == "medicationPlan"):
     return [medicationPlan.to_dict() for medicationPlan in createMedicationPlan(json_obj["medication"], file_path)]
  elif (document_type == "labData"):
    return [labData.to_dict() for labData in createLabData(json_obj["labData"], file_path)]
  elif (document_type == 'insuranceCard'):
     return createInsuranceCard(json_obj, file_path).to_dict()
  else:
    raise ValueError("Invalid document type. Must be 'doctorLetter', 'medicationPlan', or 'labData'.") 


if __name__ == "__main__":
  # Example usage
  file_path = "/home/jonasbiermann/VisitEase/backend/patient/image_data/pdfs/image-2.pdf"
  document_type = "insuranceCard" 
  data = call_gemini_api(file_path, document_type)

  with open("/home/jonasbiermann/VisitEase/backend/patient/image_data/insurance-card-1.json", "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4, ensure_ascii=False)
