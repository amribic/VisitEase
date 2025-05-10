from DoctorLetter import DoctorLetter
from LabReport import LabReport
from MedicationPlan import MedicationPlan

generated_dict = {
  "patientName": "König, Sebastian",
  "patientDateOfBirth": "06.01.1961",
  "dateOfLetter": "11.03.2025",
  "reasonForReferral": "kardiologische Verlaufskontrolle",
  "anamnesis": [
    "Die Vorstellung des Patienten erfolgte zur kardiologischen Verlaufskontrolle.",
    "Erfreulicherweise ist nach stattgehabter Spontankonversion der erstmaligen Vorhofflimmerepisode im letzten Sommer keine erneute absolute Arrhythmie mehr aufgetreten. Auch von der Smart Watch des Patienten wurde keine anhaltende Rhythmusstörung dokumentiert. Daher hat der Patient verabredungsgemäß nach drei Monaten wieder eine Umstellung von Lixiana auf ASS vorgenommen.",
    "Unter Ozempic hat sich eine deutliche Gewichtsabnahme eingestellt, worunter sich der 64-Jährige auch wohler fühle. Progrediente kardiale  Beschwerden ließen sich nicht eruieren. Einmal traten Schmerzen in der Magengegend auf, die auf entsprechende Medikamente gut ansprachen, so dass hier wohl eine primär gastrale Genese und keine etwaige kardiale zu Grunde lag."
  ],
  "clinicalFindings": {
    "RR": {
      "value": "110/70 mmHg",
      "location": "bds."
    },
    "EKG": {
      "rhythm": "Durchgehend normofrequenter Sinusrhythmus",
      "frequency": "65 Schlägen/min",
      "atrialActivity": "Unauffällige Vorhoferregung",
      "avBlock": "AV-Block 1° (PQ 240 ms)",
      "axis": "Indifferenztyp",
      "rWaveProgression": "Normale R-Progression in den Brustwandableitungen",
      "tWave": "neg. T-Welle in II, III, aVF und V6",
      "ves": "keine VES",
      "sves": "keine SVES im Rhythmusstreifen"
    },
    "Echocardiography": {
      "heartSize": "Deutlich vergrößertes Herz",
      "leftVentricle": "Leicht dilatierter linker Ventrikel (LVVd ca. 170 ml)",
      "atria": "Leicht- bis mittelgradig dilatierten Vorhöfen (LA 90 ml)",
      "leftVentricularFunction": "Leicht- bis mittelgradig reduzierte linksventrikuläre Pumpfunktion (EF ca. 45-50%)",
      "eARatio": "umgekehrtes E/A-Verhältnis als Zeichen der diast. Relaxationsstörung",
      "wallMotion": "Hypokinesie der posterior-inferior-septalen Wandabschnitte",
      "valves": "Leicht degenerative Klappenveränderungen ohne hämodynamische Relevanz. Minimale Aortenklappeninsuffizienz Geringgradige Mitralklappeninsuffizienz",
      "rightHeart": "Unauffällige Verhältnisse auf der rechten Seite des Herzens.",
      "centralVeins": "Keine zentralvenöse Stauung",
      "pericardium": "kein Perikarderguss",
      "aortaAscendens": "Ao. asc. ca. 4,0 cm"
    },
    "StressEchocardiography": {
      "position": "Linksseitenlage",
      "workloadIncrease": "Stufenweise Steigerung der Belastung um jeweils 2 Minuten von 50 Watt bis 100 Watt",
      "reasonForStopping": "Abbruch der Belastung wegen körperlicher Erschöpfung, Beinermüdung.",
      "chestPain": "Unter Belastung keine thorakalen Beschwerden.",
      "heartRateIncrease": "Herzfrequenzanstieg von ca. 72 auf 98/min",
      "bloodPressureIncrease": "Blutdruckanstieg von 110/70 auf max. 160/90 mmHg",
      "borgScale": "Subj Belastungsempfinden nach Borg: 14 (etwas anstrengend bis schwer)",
      "oxygenSaturation": "Sättigung in Ruhe 98%, unter Belastung 98%",
      "hrRrResponse": "Regelrechtes HF-/RR-Verhalten.",
      "ischemiaSigns": "Keine spez. Ischämiezeichen bei unveränderten ERBS wie in Ruhe.",
      "myocardialContractility": "Mit Ausnahme der in Ruhe bekannten WBST adäquate Kontraktilitätszunahme des übrigen Myokards."
    }
  },
  "assessment": [
    "Im 12-Kanal-EKG zeigte sich ein normofrequenter Sinusrhythmus um 65/min. mit bekannten erstgradigen AV-Block sowie vorbeschriebener T-Negativierung inferior und in V6.",
    "Der Ruheblutdruck war bds normoton",
    "Echokardiographisch lag eine leicht bis mittelgradig reduzierte linksventrikuläre Pumpfunktion bei Hypokinesie der posterioren, inferioren und septalen Wandabschnitte vor. Höhergradige Klappenvitien fanden sich nicht. Die beginnende Ascendensektasie war mit 4,0 cm niveaustabil zu beziffern. Zu einer Größenzunahme der linken Herzhöhlen ist es nicht gekommen.",
    "Stressechokardiographisch gelang in Linksseitenlage eine Belastung bis 100 Watt. Unter regelrechtem Blutdruck- und Herzfrequenzverhalten waren keine spezifischen Ischämiezeichen nachweisbar bei unveränderten Endstreckenveränderungen wie in Ruhe. Mit Ausnahme der vorbestehenden Wandbewegungsstörungen bot sich ansonsten eine adäquate Kontraktilitätszunahme der übrigen Myokardabschnitte.",
    "Insofern ergab sich kein sicherer Hinweis für einen Progress der KHK bei diesbzgl auch fehlenden Beschwerden.",
    "Insofern scheint ein Festhalten am medikamentös-konservativen Therapiekonzept legitim. Von einer im Vorfeld diskutierten Umstellung der Medikation auf Entresto möchte Herr Kern eher Abstand nehmen, da er mit der gegebenen Tabletteneinstellung seit Jahren gut zurechtkommt und sich auch keine Verschlechterung der Messparameter eingestellt hat.",
    "Insofern scheint diese Vorgehensweise legitim",
    "Sollten sich wegweisende Beschwerden einstellen oder erneutes Vorhofflimmern, bitten wir jederzeit um umgehende Kontaktaufnahme.",
    "In letzterem Fall wäre dann die Wiederaufnahme der oralen Antikoagulation zwingend.",
    "Da die einmalige Vorhofflimmerepisode letztes Jahr subjektiv deutlich verspürt wurde und seither eine nahezu lückenlose Überwachung durch die Smart Watch besteht, die auch nachts getragen wird, dürfte das Risiko unerkannter intermittierender Vorhofflimmerepisoden zum jetzigen Zeitpunkt als sehr gering eingestuft werden."
  ],
  "plan": [
    "Festhalten am medikamentös-konservativen Therapiekonzept"
  ],
  "medication": {
    "substance": "null",
    "medicationName": "null",
    "dosage": "null",
    "pillForm": "null",
    "numberMorning": "null",
    "numberNoon": "null",
    "numberEvening": "null",
    "numberNight": "null",
    "unit": "null",
    "notes": "null"
  },
  "contactInformation": {
    "address": "Wilhelmstr 55-63\n53721 Siegburg",
    "website": "www.siegburgmed.de",
    "phone": "(02241) 265-330",
    "fax": "(02241) 265-3344",
    "email": "kardiologie@siegburgmed.de",
    "bankName": "Apo-Bank Köln",
    "iban": "DE38300606010006613128",
    "bic": "DAAEDEDDXXX"
  },
  "labData": {
    "unit": "null",
    "value": "null",
    "referenceRange": "null",
    "testName": "null"
  },
  "filePath": "null"
}


patientName = generated_dict.get("patientName", "")
patientDateOfBirth = generated_dict.get("patientDateOfBirth", "")
dateOfLetter = generated_dict.get("dateOfLetter", "")
reasonForReferral = generated_dict.get("reasonForReferral", "")
anamnesis = generated_dict.get("anamnesis", [])
clinicalFindings = generated_dict.get("clinicalFindings", {})
assessment = generated_dict.get("assessment", [])
plan = generated_dict.get("plan", [])
medication = MedicationPlan(generated_dict.get("medication", {}))
contactInformation = generated_dict.get("contactInformation", {})
labData = LabReport(generated_dict.get("labData", {}))
filePath = generated_dict.get("filePath", "")
doctorLetter = DoctorLetter(
    patientName,
    patientDateOfBirth,
    dateOfLetter,
    reasonForReferral,
    anamnesis,
    clinicalFindings,
    assessment,
    plan,
    medication,
    contactInformation,
    labData,
    filePath
)

print(doctorLetter.getPatientName(), "\n")
print(doctorLetter.getPatientDateOfBirth(), "\n")
print(doctorLetter.getDateOfLetter(), "\n")
print(doctorLetter.getReasonForReferral(), "\n")
print(doctorLetter.getAnamnesis(), "\n")
print(doctorLetter.getClinicalFindings(), "\n")
print(doctorLetter.getAssessment(), "\n")
print(doctorLetter.getPlan(), "\n")
print(doctorLetter.getMedication(), "\n")
print(doctorLetter.getContactInformation(), "\n")
print(doctorLetter.getLabData(), "\n")
print(doctorLetter.getFilePath(), "\n")