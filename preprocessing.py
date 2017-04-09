
# coding: utf-8

# ## Read data and create dataframe

# In[1]:

import csv #Final files are to be exported in CSV
import pysal as ps #Input file is in DBF; pysal is used to convert it to pandas dataframe
import pandas as pd #Dataframe is the data structure used


# In[2]:

filename = "data/SINASC13_GEO.dbf"


# In[3]:

def dbf2DF(dbfile): #Reads in DBF files and returns Pandas DF
    db = ps.open(dbfile)
    d = {col: db.by_col(col) for col in db.header} #Convert dbf to dictionary
    pandasDF = pd.DataFrame(d) #Convert to Pandas DF
    db.close() 
    return pandasDF


# In[4]:

dataset = dbf2DF(filename)


# ## Calculates Robson group

# In[5]:

def getRobsonGroup(row):
    if (row['QTDPARTNOR'] == '00' and 
        row['QTDPARTCES'] == '00' and 
        row['GRAVIDEZ'] == '1' and 
        row['TPAPRESENT'] == '1' and 
        int(row['SEMAGESTAC']) >= 37 and 
        row['STTRABPART'] == '2'):
        robson = '01'
    elif (row['QTDPARTNOR'] == '00' and 
          row['QTDPARTCES'] == '00' and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '1' and 
          int(row['SEMAGESTAC']) >= 37 and 
          (row['STTRABPART'] == '1' or 
          row['STCESPARTO'] == '1')):
        robson = '02'
    elif (row['QTDPARTNOR'] != '00' and 
          row['QTDPARTCES'] == '00' and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '1' and 
          int(row['SEMAGESTAC']) >= 37 and 
          row['STTRABPART'] == '2'):
        robson = '03'
    elif (row['QTDPARTNOR'] != '00' and 
          row['QTDPARTCES'] == '00' and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '1' and 
          int(row['SEMAGESTAC']) >= 37 and 
          (row['STTRABPART'] == '1' or 
          row['STCESPARTO'] == '1')):
        robson = '04'
    elif (row['QTDPARTCES'] != '00' and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '1' and 
          int(row['SEMAGESTAC']) >= 37):
          robson = '05'
    elif (row['QTDPARTNOR'] == '00' and 
          row['QTDPARTCES'] == '00' and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '2'):
          robson = '06'
    elif ((row['QTDPARTNOR'] != '00' or 
          row['QTDPARTCES'] != '00') and 
          row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '2'):
        robson = '07'
    elif (row['GRAVIDEZ'] == '2' or
          row['GRAVIDEZ'] == '3'):
        robson = '08'
    elif row['TPAPRESENT'] == '3':
        robson = '09'
    elif (row['GRAVIDEZ'] == '1' and 
          row['TPAPRESENT'] == '1' and 
          int(row['SEMAGESTAC']) < 37):
        robson = '10'
    else: 
        robson = '11'
    return robson


# In[6]:

datasetRC = dataset.drop(dataset[dataset['SEMAGESTAC'] == ''].index)  # Avoids error converting from "" to int below
datasetRC = datasetRC.drop(datasetRC[datasetRC.CODESTAB == ''].index) # Drops unidentified facilitys
datasetRC = datasetRC.drop(datasetRC[datasetRC.PARTO == ''].index)    # Drops uknown type of birth


# Gets the robson group for each birth

# In[7]:

datasetRC['ROBSON_GROUP'] = datasetRC.apply(getRobsonGroup, axis=1)


# ## Create score

# Sets format of date

# In[8]:

datasetRC['DTNASC'] = datasetRC.DTNASC.str[-4:] + datasetRC.DTNASC.str[-6:-4]


# Select columns Facility ID, Robson Group and Type of Birth

# In[9]:

filteredRC = datasetRC.groupby(['CODESTAB', 'ROBSON_GROUP', 'PARTO']
                         ).size(
                         ).reset_index(
                         ).rename(columns={0:'CONTAGEM'})


# Pivots table to have both Robson Group and Type of Birth on the columns

# In[10]:

pivotedRC = pd.pivot_table(filteredRC, values='CONTAGEM', index=['CODESTAB', 'PARTO'], columns=['ROBSON_GROUP']
                          ).reset_index(
                          ).fillna(value=0)


# In[11]:

pivotedRC2 = pd.pivot_table(pivotedRC, values=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'], index=['CODESTAB'], columns=['PARTO']
                           ).reset_index(
                           ).fillna(value=0)


# In[12]:

pivotedRC2.columns = [' '.join(col).strip() for col in pivotedRC2.columns.values]


# In[13]:

totalRC = pivotedRC2


# Creates dataframe with total of births by group per facility

# In[14]:

for group in range(1, 11):
    if group != 10:
        totalRC['TotalG' + str(group)] =  totalRC['0' + str(group) + ' 1'] + totalRC['0' + str(group) + ' 2']
    else:
        totalRC['TotalG' + str(group)] =  totalRC[str(group) + ' 1'] + totalRC[str(group) + ' 2']


# In[15]:

totalByGroup = totalRC[['CODESTAB', 'TotalG1', 'TotalG2', 'TotalG3', 'TotalG4', 'TotalG5', 'TotalG6', 'TotalG7', 'TotalG8', 'TotalG9', 'TotalG10']]


# Creates dataframe with porcentage per type of birth

# In[16]:

porcRC = totalRC['CODESTAB'].to_frame()


# In[17]:

for group in range(1, 11):
    for parto in range(1, 3):
        if group != 10:
            columnName = '0' + str(group) + ' ' + str(parto)
        else: 
            columnName = str(group) + ' ' + str(parto)
        letter = 'V' if parto == 1 else 'C'
        newColumn = 'G' + str(group) + letter
        porcRC[newColumn] = totalRC[columnName] / totalRC['TotalG' + str(group)]  


# In[18]:

porcRC = porcRC.fillna(value=0)


# Creates dataframe with total of births per group and birth

# In[19]:

GXCTable = totalRC.iloc[:, :21].rename(columns={'01 1':'G1V', '01 2':'G1C', '02 1':'G2V', '02 2':'G2C', '03 1':'G3V', '03 2':'G3C', '04 1':'G4V', '04 2':'G4C', '05 1':'G5V', '05 2':'G5C', '06 1':'G6V', '06 2':'G6C', '07 1':'G7V', '07 2':'G7C', '08 1':'G8V', '08 2':'G8C', '09 1':'G9V', '09 2':'G9C', '10 1':'G10V', '10 2':'G10C'})


# Creates dataframe with total of births per facility

# In[20]:

totalBirths = filteredRC[['CODESTAB', 'CONTAGEM']].groupby('CODESTAB').sum(
            ).reset_index(
            ).rename(columns={'CONTAGEM':'CONT_PARTO'})


# Creates dataframe with total of C-section (cesareana)

# In[21]:

totalCSec = filteredRC.loc[filteredRC.PARTO == '2'][['CODESTAB', 'CONTAGEM']].groupby('CODESTAB').sum(
            ).reset_index(
            ).rename(columns={'CONTAGEM':'CONT_CES'})


# Creates table with support variables to calculate the attributes for chi squared

# In[22]:

finalSupport = GXCTable.merge(totalByGroup, how='outer').merge(totalCSec, how='outer').merge(totalBirths, how='outer')


# Creates table with attributes for chi squared

# In[23]:

finalAttr = finalSupport['CODESTAB'].to_frame()


# In[24]:

for group in range(1, 11):
    
    #A: GxC / (GxC + GxV) (porcentage)
    finalAttr['A' + str(group)] = finalSupport['G' + str(group) + 'C'] / finalSupport['TotalG' + str(group)]
    
    #B: GxC / Total Cesareas
    finalAttr['B' + str(group)] = finalSupport['G' + str(group) + 'C'] / finalSupport['CONT_CES']
    
    #C: GxC / Total Partos
    finalAttr['C' + str(group)] = finalSupport['G' + str(group) + 'C'] / finalSupport['CONT_PARTO']


# In[25]:

#D: (Total Cesareas / Total Partos)
finalAttr['D'] = finalSupport['CONT_CES'] / finalSupport['CONT_PARTO']


# In[26]:

finalAttr = finalAttr.fillna(value = 0)


# Dictionary with reference values for Robison group porcentage according to http://onlinelibrary.wiley.com/doi/10.1111/1471-0528.13509/pdf

# In[27]:

robisonDict = {'G1A': 0.098, 'G1B': 0.293, 'G1C': 0.029, 'G2A': 0.399, 'G2B': 0.088, 'G2C': 0.035, 'G3A': 0.030, 'G3B': 0.401, 'G3C': 0.012, 'G4A': 0.237, 'G4B': 0.064, 'G4C': .015, 'G5A': 0.744, 'G5B': 0.072, 'G5C': 0.053, 'G6A': 0.785, 'G6B': 0.012, 'G6C': .009, 'G7A': 0.738, 'G7B': 0.015, 'G7C': 0.011, 'G8A': 0.577, 'G8B': 0.009, 'G8C': 0.005, 'G9A': 0.886, 'G9B': 0.004, 'G9C': 0.003, 'G10A': 0.251, 'G10B': 0.042, 'G10C': 0.010, 'GTR1': 0.185, 'GTR2': 1.000, 'GTR3': 0.185}


# In[28]:

scoreAux = finalAttr['CODESTAB'].to_frame()


# Calculates chi squared values

# In[29]:

def chi2(A, E): #chi squared function
    return pow((A - E), 2)/E


# In[30]:

for group in range(1, 11):
    #for type in ['A', 'B', 'C']:
    for type in ['A']: # removed B and C; they don't add degrees of freedom 
        scoreAux['S' + type + str(group)] = chi2(finalAttr[type + str(group)], robisonDict['G' + str(group) + type])


# In[31]:

scoreAux['D'] = chi2(finalAttr['D'], robisonDict['GTR1'])
# scoreAux['D'] = 2 * chi2(finalAttr['D'], robisonDict['GTR1']) Being consistent with cell above


# In[32]:

scoreAux['SCORE'] = scoreAux.sum(axis=1)


# Final table for input in website with scores and amount of birth per group and type of birth

# In[33]:

score = GXCTable.merge(scoreAux[['CODESTAB', 'SCORE']]).fillna(value=0)


# Applies function Rank to get a better distributed score

# In[34]:

rankedScore = score['SCORE'].rank(method='min')


# In[35]:

score["SCORE"] = rankedScore


# Assigns score -1 to facilities with less than 20 births per year 

# In[36]:

invalidFacilities = list(totalBirths[totalBirths['CONT_PARTO'] < 20]['CODESTAB'])


# In[37]:

def filterScore(facility):
    return -1 if facility['CODESTAB'] in invalidFacilities else facility['SCORE']


# In[38]:

score['SCORE'] = score.apply(filterScore, axis=1)


# Sorts by rank

# In[39]:

score = score.sort_values(by='SCORE', ascending=False)


# Exports to CSV

# In[40]:

scoreInvalidFacilities = score.loc[score['SCORE'] == -1]


# In[41]:

scoreInvalidFacilities.to_csv('data/invalidFacilities.csv', index=False)


# In[42]:

scoreValidFacilities = score.loc[score['SCORE'] != -1]


# In[43]:

scoreValidFacilities.to_csv('data/validFacilities.csv', index=False)

