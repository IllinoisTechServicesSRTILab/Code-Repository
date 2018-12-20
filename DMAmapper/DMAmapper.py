import pandas as pd
import pyparsing as pp

########
#
# These two functions are for reading and writing to the dataframe and the csv.
#
########

def LoadCSVtoDF():
    tempDF = pd.read_csv('DMA Dataframe.csv', index_col = 'dmaID')
    tempDF.columns = ['regionName','cityList']
    tempDF['cityList'] = tempDF['cityList'].apply(lambda x: pp.commaSeparatedList.copy().addParseAction(pp.tokenMap(lambda s: s.strip('\''))).parseString(x[1:-1]).asList())
    for cl in tempDF['cityList']:
        try:
            cl.remove('')
        except:
            pass            
    return tempDF
    
def WriteDFtoCSV(argDF):
    argDF.to_csv('DMA Dataframe.csv', encoding = 'utf-8')



# Function accepts a file of city names and adds them to appropriate region's
# list if new.  Writes updates to the csv and returns updated dataframe

def AddNewCities(inFile, topDF):
    tempDF = pd.read_csv(inFile, header = 0)
    tempDF.columns = ['dma','city']
    for row in tempDF.iterrows():
        if row[1][1] not in topDF.loc['#'+str(row[1][0]),'cityList']:
              topDF.loc['#'+str(row[1][0]),'cityList'].append(row[1][1])
    WriteDFtoCSV(topDF)
    return(topDF)



# Function accepts one of either dma, region, or city and returns 
# a list containg the other two.

def ReturnInfo(inDF, dma = None, region = None, city = None):
    if city == None:
        if region == None:
            return list(inDF.loc[dma])
        else:
            inDF = inDF.reset_index().set_index('regionName')
            return list(inDF.loc[region])
    elif region == None:
        for row in inDF.iterrows():
            if city in row[1][1]:
                return [row[0],row[1][0]]
    else:
        return ("No info in dataframe")


# Function accepts a file of possible city names and returns a list of ones not
# currently in any region.

def MissingCities(inDF, filename):
    tempDF = pd.read_csv(filename)
    tempDF.columns = ['city']
    missing = tempDF['city'].tolist()
    for city in tempDF['city']:
        for row in inDF['cityList']:
            if city in row:
                missing.remove(city)
    return missing


def main():
    dmaDF = LoadCSVtoDF()
    print(ReturnInfo(dmaDF, city = 'Danbury, CT'))
    print(ReturnInfo(dmaDF, dma = '#501'))
    print(ReturnInfo(dmaDF, region = 'New York'))
    print(dmaDF.head().to_string())
    #dmaDF = AddNewCities('example.csv', dmaDF)
    #print(MissingCities(dmaDF, 'Check Missing Cities.csv'))


if __name__ == "__main__":
    main()
        
