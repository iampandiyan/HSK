import pandas as pd
import numpy as np

class Univariate():
   
    def quanQual(self,dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            if(dataset[columnName].dtype=='O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
    
    def createDescriptiveTable(self,dataset):
        quanColumns=self.quanQual(dataset)[0]
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max","Kurtosis","Skew"],columns=quanColumns)        
        for columnName in quanColumns:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
            descriptive[columnName]["Kurtosis"]=dataset[columnName].kurtosis()
            descriptive[columnName]["Skew"]=dataset[columnName].skew()
        return descriptive
    
    def getOutliers(self,dataset):
        lesser=[]
        greater=[]
        quanColumns=self.quanQual(dataset)[0]
        descriptive=self.createDescriptiveTable(dataset)
        for columnName in quanColumns:
            if(descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if(descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]):
                greater.append(columnName)
        return lesser,greater
        
    def removeOutlier(self,dataset):    
        descriptive=self.createDescriptiveTable(dataset)
        lesserCoulmNames=self.getOutliers(dataset)[0]
        greaterColumnNames=self.getOutliers(dataset)[1]
        for columnName in lesserCoulmNames:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]=descriptive[columnName]["Lesser"]
        for columnName in greaterColumnNames:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]

    def createFrequencyTable(self,columnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_values","Frequency","Relative_Frequency","Cumsum"])
        freqTable["Unique_values"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"]=(freqTable["Frequency"]/103)
        freqTable["Cumsum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable
    
 