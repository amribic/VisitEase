from LabReport import LabReport

class DoctorLetter:
    def __init__(self, anamnesis: str, admittanceStatus: str, therapyAndProgress: str, results: str, labData: LabReport, filePath: str):
        self.anamnesis = anamnesis
        self.admittanceStatus = admittanceStatus
        self.therapyAndProgress = therapyAndProgress
        self.results = results
        self.labData = labData
        self.filePath = filePath
    
    def __init__(self, doctorDict: dict):
        self.anamnesis = doctorDict.get("anamnesis", "")
        self.admittanceStatus = doctorDict.get("admittanceStatus", "")
        self.therapyAndProgress = doctorDict.get("therapyAndProgress", "")
        self.results = doctorDict.get("results", "")
        self.labData = LabData(doctorDict.get("labData", {}))

    def getAnamnesis(self):
        return self.anamnesis

    def getAdmittanceStatus(self):
        return self.admittanceStatus

    def getTherapyAndProgress(self):
        return self.therapyAndProgress

    def getResults(self):
        return self.results

    def getLabData(self):
        return self.labData

    def getFilePath(self):
        return self.filePath