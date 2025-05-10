from .LabReport import LabReport
from .MedicationPlan import MedicationPlan

class DoctorLetter:
    def __init__(self, reasonForReferral: str, anamnesis: list, clinicalFindings: dict, assessment: list, plan: list, medication: MedicationPlan, labData: LabReport, filePath: str):
        self.reasonForReferral = reasonForReferral
        self.anamnesis = anamnesis
        self.clinicalFindings = clinicalFindings
        self.assessment = assessment
        self.plan = plan
        self.medication = medication
        self.labData = labData
        self.filePath = filePath

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
    
    def to_dict(self):
        doctorLetter = {
            "reasonForReferral": self.reasonForReferral,
            "anamnesis": self.anamnesis,
            "clinicalFindings": self.clinicalFindings,
            "assessment": self.assessment,
            "plan": self.plan,
            "medication": [medicationEntry.to_dict() for medicationEntry in self.medication],
            "labData": [labDataEntry.to_dict() for labDataEntry in self.labData],
            "filePath": self.filePath
        }
        return doctorLetter