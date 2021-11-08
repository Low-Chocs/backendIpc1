class Image:

    
    #Constructor
    def __init__(self,url, date, category, author):
        self.url= url
        self.date= date
        self.category = category
        self.author=author
        self.Like= []
        self.tipo= "image"

    
    def like(self,username):
        print(username)
        try:
            name = self.Like.index(username)
        except:
            name = "Its not in the list"
            print("Entre a exception")
        
        if(name=="Its not in the list"):
            self.Like.append(username)
        else:
            self.Like.remove(username)
    
    
    #Métodos getter & setter
    def getLike(self):
        cantidad =len(self.Like)
        print(self.Like)
        return cantidad

    def getUrl(self):
        return self.url

    def getTipo(self):
        return self.tipo
    
    def setUrl(self, url):
        self.url=url

    def getDate(self):
        return self.date
    
    def setDate(self, Date):
        self.date=Date

    def getCategory(self):
        return self.category
    
    def setCategory(self, category):
        self.category=category
    
    def getAuthor(self):
        return self.author
    
    def setAuthor(self, author):
        self.author=author

    def ordenamiento(list):
        newList=[]
        print(len(newList))
        if(len(list)>1):
            
            for i in range(1,len(list)):
                for j in range(len(list)-i):
                    newList.append(list[j])
                    if(int(list[j].getLike())<int(list[j+1].getLike())):
                        list[j]=list[j+1] 
                        list[j+1]=newList[0]
    



