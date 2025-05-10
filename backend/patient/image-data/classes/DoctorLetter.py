from LabReport import LabReport
from MedicationPlan import MedicationPlan

class DoctorLetter:
    def __init__(self, patientName: str, patientDateOfBirth: str, dateOfLetter: str, reasonForReferral: str, anamnesis: list, clinicalFindings: dict, assessment: list, plan: list, medication: MedicationPlan, contactInformation: dict, labData: LabReport, filePath: str):
        self.patientName = patientName
        self.patientDateOfBirth = patientDateOfBirth
        self.dateOfLetter = dateOfLetter
        self.reasonForReferral = reasonForReferral
        self.anamnesis = anamnesis
        self.clinicalFindings = clinicalFindings
        self.assessment = assessment
        self.plan = plan
        self.medication = medication
        self.contactInformation = contactInformation
        self.labData = labData
        self.filePath = filePath

    def getPatientName(self) -> str:
        return self.patientName

    def getPatientDateOfBirth(self):
        return self.patientDateOfBirth

    def getDateOfLetter(self):  
        return self.dateOfLetter

    def getReasonForReferral(self):
        return self.reasonForReferral

    def getClinicalFindings(self):
        return self.clinicalFindings

    def getAssessment(self):
        return self.assessment

    def getPlan(self):
        return self.plan

    def getMedication(self):
        return self.medication

    def getContactInformation(self):
        return self.contactInformation

    def getAnamnesis(self):
        return self.anamnesis

    def getLabData(self):
        return self.labData

    def getFilePath(self):
        return self.filePath