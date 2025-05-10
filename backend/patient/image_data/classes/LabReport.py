class LabReport:
    def __init__(self, unit: str, value: float, referenceRange: str, testName: str, filePath: str):
        self.unit = unit
        self.value = value
        self.referenceRange = referenceRange
        self.testName = testName
        self.filePath = filePath
        
    def getUnit(self):
        return self.unit

    def getValue(self):
        return self.value

    def getReferenceRange(self):
        return self.referenceRange

    def getTestName(self):
        return self.testName

    def getFilePath(self):
        return self.filePath
    
    def to_dict(self):
        return {
            "unit": self.unit,
            "value": self.value,
            "referenceRange": self.referenceRange,
            "testName": self.testName,
            "filePath": self.filePath
        }