class User:

    #Constructor
    def __init__(self,name, gender, username, email, password):
        self.name= name
        self.gender= gender
        self.username = username
        self.email=email
        self.password  = password


    #Métodos getter & setter
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name=name

    def getGender(self):
        return self.gender
    
    def setGender(self, gender):
        self.gender=gender

    def getUsername(self):
        return self.username
    
    def setUsername(self, username):
        self.username=username
    
    def getEmail(self):
        return self.email
    
    def setEmail(self, email):
        self.email=email

    def getPassword(self):
        return self.password
    
    def setPassword(self, password):
        self.password=password
