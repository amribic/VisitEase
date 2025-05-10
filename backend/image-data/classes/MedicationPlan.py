class MedicationPlan:
    def __init__(self, substance: str, medicationName: str, dosage: str, pillForm: str, numberMorning: float, numberNoon: float, numberEvening: float, numberNight: float, unit: str, notes: str, filePath: str):
        self.substance = substance
        self.medicationName = medicationName
        self.dosage = dosage
        self.pillForm = pillForm
        self.numberMorning = numberMorning
        self.numberNoon = numberNoon
        self.numberEvening = numberEvening
        self.numberNight = numberNight
        self.unit = unit
        self.notes = notes
        self.filePath = filePath

    def __init__(self, medicationDict: dict):
        self.substance = medicationDict.get("substance", "")
        self.medicationName = medicationDict.get("medicationName", "")
        self.dosage = medicationDict.get("dosage", "")
        self.pillForm = medicationDict.get("pillForm", "")
        self.numberMorning = medicationDict.get("numberMorning", 0.0)
        self.numberNoon = medicationDict.get("numberNoon", 0.0)
        self.numberEvening = medicationDict.get("numberEvening", 0.0)
        self.numberNight = medicationDict.get("numberNight", 0.0)
        self.unit = medicationDict.get("unit", "")
        self.notes = medicationDict.get("notes", "")

    def getSubstance(self):
        return self.substance

    def getMedicationName(self):
        return self.medicationName

    def getDosage(self):
        return self.dosage

    def getPillForm(self):
        return self.pillForm

    def getNumberMorning(self):
        return self.numberMorning

    def getNumberNoon(self):
        return self.numberNoon

    def getNumberEvening(self):
        return self.numberEvening

    def getNumberNight(self):
        return self.numberNight

    def getUnit(self):
        return self.unit

    def getNotes(self):
        return self.notes

    def getFilePath(self):
        return self.filePath