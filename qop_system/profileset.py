import json
import os
import const

class ProfileSet:
    def __init__(self):
        self.R4Data = list()
        self.QOPData = list()
        self.RANKData = list()
        self.GraphsColors = ["#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"]
        self.GraphsValues = ["1", "100", "10", "0", "1000", "10"]
        self.AproxColors = ["#000000", "#000000"]
        self.AproxValues = ["1", "100", "10", "0", "1000", "10"]
        
        if not os.path.isfile("profile.json"):
            return
        
        with open("profile.json", 'r') as f:
            jsText = json.load(f)
            self.__dict__ = json.loads(jsText)
        
    def SaveToFile(self):
        with open("profile.json", 'w') as f:
            jsText = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
            json.dump(jsText, f)
            
    def DataPrint(self, setList):
        retval = ""
        for item in setList:
            retval += str(item['Number']) + ' ' + str(item['Time']) + ' ' + str(item['Value']) + '\n'
        return retval
      
    def GenRankData(self):
        self.RANKData = list()
        for r4 in self.R4Data:
            for qop in self.QOPData:
                if qop['Number'] == r4['Number']: 
                    self.RANKData.append({'Number' : r4['Number'], 'Time' : qop['Time'], 'Value' : r4['Value'] - qop['Value']})
                    break
            
    def GenR4Data(self):
        self.R4Data = list()
        for qop in self.QOPData:
            for rank in self.RANKData:
                if rank['Number'] == qop['Number']: 
                    self.R4Data.append({'Number' : qop['Number'], 'Time' : qop['Time'], 'Value' : rank['Value'] + qop['Value']})
                    break

    def GenQOPData(self):
        self.QOPData = list()
        for r4 in self.R4Data:
            for rank in self.RANKData:
                if rank['Number'] == r4['Number']: 
                    self.R4Data.append({'Number' : r4['Number'], 'Time' : rank['Time'], 'Value' : r4['Value'] - rank['Value']})
                    break
                
    def ReadData(self, file, typeLoad):
        newList = list()
        while True:
            line = file.readline().rstrip()
            if not line:
                break
        
            items = line.split(' ')
            if len(items) != 3:
                continue
        
            newList.append({'Number' : int(items[0]), 'Time' : float(items[1]), 'Value' : int(items[2])})
            
        if typeLoad == const.FOR_R4:
            self.R4Data = newList
        elif typeLoad == const.FOR_QOP:
            self.QOPData = newList
        elif typeLoad == const.FOR_RANK:
            self.RANKData = newList
        
    def AppendData(self, filename, typeLoad):
        with open(filename, 'r') as f:
            if typeLoad == const.FOR_ALL:
                self.R4Data = list()
                self.QOPData = list()
                self.RANKData = list()
                
                while True:
                    line = f.readline().rstrip()
                    if not line:
                        break
                    
                    items = line.split(' ')
                    if len(items) != 5:
                        return 0
                    
                    self.R4Data.append({'Number' : int(items[0]), 'Time' : float(items[1]), 'Value' : int(items[2])})
                    self.QOPData.append({'Number' : int(items[0]), 'Time' : float(items[1]), 'Value' : int(items[2])})
                    self.RANKData.append({'Number' : int(items[0]), 'Time' : float(items[1]), 'Value' : int(items[2])})
            else:
                self.ReadData(f, typeLoad)
                if len(self.R4Data) and len(self.QOPData) != "":
                    self.GenRankData()
                elif len(self.RANKData) != "" and len(self.QOPData):
                    self.GenR4Data()  
                elif len(self.RANKData) != "" and len(self.R4Data) != "":
                    self.GenQOPData()   
            return 1