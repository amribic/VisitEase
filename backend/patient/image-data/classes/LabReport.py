class LabReport:
    def __init__(self, unit: str, value: float, referenceRange: str, testName: str, filePath: str):
        self.unit = unit
        self.value = value
        self.referenceRange = referenceRange
        self.testName = testName
        self.filePath = filePath

    def __init__(self, labDataDict: dict):
        self.unit = labDataDict.get("unit", "")
        self.value = labDataDict.get("value", 0.0)
        self.referenceRange = labDataDict.get("referenceRange", "")
        self.testName = labDataDict.get("testName", "")
        self.filePath = labDataDict.get("filePath", "")

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