import pandas as pd
from sqlalchemy import create_engine


types = {
            "EVA_NR": int,
            "DS100": str,
            "IFOPT": str,
            "NAME": str,
            "Verkehr": str,
            "Laenge": float,
            "Breite": float,
            "Betreiber_Name": str,
            "Betreiber_Nr": int
        }


def getDataFromLink(link):
    dataFrame = pd.read_csv(link, delimiter=";")
    return dataFrame
    


def createSQLiteFile(df):
    df.to_sql("trainstops", 'sqlite:///trainstops.sqlite',if_exists='replace', index=False)
    
    
def changeDataType(df,types):
    df = df.astype(types)
    return df
    
    
    
def cleanData(data):
    data.drop(columns=["Status"], inplace=True)
    data = data[data["Verkehr"].isin(["FV","RV","nur DPN"])]
    data['Laenge'] = data['Laenge'].str.replace(',','.')
    data['Breite'] = data['Breite'].str.replace(',','.')
    data["Laenge"] = pd.to_numeric(data["Laenge"])
    data["Breite"] = pd.to_numeric(data["Breite"])
    data["EVA_NR"] = pd.to_numeric(data["EVA_NR"])
    data["Betreiber_Nr"] = pd.to_numeric(data["Betreiber_Nr"])
    data= data[~(data["Laenge"] < 90) & data["Laenge"] > -90]
    data= data[~(data["Breite"] < 90) & data["Breite"] > -90]
    data = data.dropna()
    print(type(data['IFOPT']))
    data = data[data['IFOPT'].str.contains(r'^[a-zA-Z]{2}:[0-9]*:[0-9]+(:[0-9]+)?$')]
    data.IFOPT = data.IFOPT.astype(str)
    return data
    

link = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
df = getDataFromLink(link)
df = cleanData(df)
df = changeDataType(df,types)
createSQLiteFile(df)
