class InsuranceCard:
    def __init__(self, name: str, insuranceProvider: str, insuranceNumber: str, customerNumber: str, cardNumber: str, birthDate: str, seventhIdentityNumber: str, expirationDate: str):
        self.name = name
        self.insuranceProvider = insuranceProvider
        self.insuranceNumber = insuranceNumber
        self.customerNumber = customerNumber
        self.cardNumber = cardNumber
        self.birthDate = birthDate
        self.seventhIdentityNumber = seventhIdentityNumber
        self.expirationDate = expirationDate


    def getName(self):
        return self.name
    
    def getInsuranceProvider(self):
        return self.insuranceProvider
    
    def getInsuranceNumber(self):
        return self.insuranceNumber
    
    def getCustomerNumber(self):
        return self.customerNumber
    
    def getCardNumber(self):
        return self.cardNumber
    
    def getBirthDate(self):
        return self.birthDate
    
    def getSeventhIdentityNumber(self):
        return self.seventhIdentityNumber
    
    def getExpirationDate(self):
        return self.expirationDate
    
    def to_dict(self):
        return {
            "name": self.name,
            "insuranceProvider": self.insuranceProvider,
            "insuranceNumber": self.insuranceNumber,
            "customerNumber": self.customerNumber,
            "cardNumber": self.cardNumber,
            "birthDate": self.birthDate,
            "seventhIdentityNumber": self.seventhIdentityNumber,
            "expirationDate": self.expirationDate
        }