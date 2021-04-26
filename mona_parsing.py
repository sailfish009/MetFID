# -*- coding: utf-8 -*-
"""
Parsing the MONA data

@author: kuijun @ 3/25/2021
@edited: kuijun @ 3/31/2021
"""

import json
import pandas as pd
import pickle

#------------------File handle---------------
input_file = "MoNA-export-LC-MS-MS_Negative_Mode.json"
with open(input_file, 'rb') as handle:
    mona = json.load(handle)

output_file = "MONA2021_LC-MS-MS_Negative.p"
output_csv = 'MONA2021_LC-MS-MS_Negative.csv'

#-----------Parsing json into list-----------
mona_data = [0]*len(mona)

index = 0
for i in mona:
    metaData = i["metaData"]
    metadict = {}
    for a in metaData:
        metadict[a["name"]]=a["value"]
    
    c_metaData =i["compound"][0]["metaData"]
    c_metadict = {}
    for a in c_metaData:
        c_metadict[a["name"]]=a["value"]
    
    #name:
    try:
        names = []
        for n in i["compound"][0]["names"]:
            names.append(n["name"])
            names1 =str(names)
    except:
        names1 = ""

    #inchiKey:
    try:
        inchikey = i["compound"][0]["inchiKey"]
    except:
        try:
            inchikey = c_metadict["InChIKey"]
        except:
            inchikey = ""
    #smiles:
    try:
        smiles = c_metadict["SMILES"]
    except:
        smiles = ""
    
    #id:
    try:
        spectrum_id = i["id"]
    except:
        spectrum_id = ""
        
    #Experimentation:
    Experimentation = ""
    #Source:
    try:
        Source = metadict["ionization"]
    except:
        Source = ""
    
    #Ion_Mode:
    try:
        Ion_Mode = metadict["ionization mode"]
    except:
        Ion_Mode = ""    
    
    #Adduct:
    try:
        Adduct = metadict["precursor type"]
    except:
        Adduct = ""     
    
    #Precursor_Mass
    try:
        Precursor_Mass = metadict["precursor m/z"]
    except:
        Precursor_Mass = "" 
    #Exact_mass
    try:
        Exact_mass = metadict["exact mass"]
    except:
        Exact_mass = ""
    
    #Instrument_Type = metaData[9]["value"]
    try:
        Instrument_Type = metadict["instrument type"]
    except:
        Instrument_Type = ""
        
    #Instrument = metaData[8]["value"]
    try:
        Instrument = metadict["instrument"]
    except:
        Instrument = ""
    
    #Collision_Energy = metaData[13]["value"]
    try:
        Collision_Energy = metadict["collision energy"]
    except:
        Collision_Energy = ""
    
    
    #Mass_Accuracy = metaData[27]["value"]
    try:
        Mass_Accuracy = metadict["mass accuracy"]
    except:
        Mass_Accuracy = ""
    #library:
    try:
        library  = i["library"]["library"]
    except:
        library = ""
    
    #External_IDs
    try:
        CAS_id = "CAS "+str(c_metadict["cas"])
        Pubchem_id = "Pubchem "+str(c_metadict["pubchem cid"])
        Chemspider_id = "Chemspider "+str(c_metadict["chemspider"])
        External_IDs = [CAS_id, Pubchem_id, Chemspider_id]
    except:
        External_IDs = ""
        
    spectrum = i["spectrum"]
    peaks = spectrum.split()
    Number_of_Peaks = len(peaks)
    Mass = [i.split(":")[0] for i in peaks]
    Mass = [float(i) for i in Mass]
    Intensity = [i.split(":")[1] for i in peaks]
    Intensity = [float(i) for i in Intensity]
    
    test = [names1, inchikey, smiles, spectrum_id,Experimentation,Source, Ion_Mode, 
           Adduct, Precursor_Mass, Exact_mass, Instrument_Type, Instrument, 
           Collision_Energy, Mass_Accuracy, library, External_IDs, 
           Number_of_Peaks, Mass, Intensity]
    mona_data[index] = test
    index += 1


df = pd.DataFrame (mona_data)
df.columns = ["names1", "inchikey", "smiles", "spectrum_id", "Experimentation",
              "Source", "Ion_Mode", "Adduct", "Precursor_Mass", "Exact_mass", 
              "Instrument_Type", "Instrument", "Collision_Energy", "Mass_Accuracy", 
              "library", "External_IDs", "Number_of_Peaks", "Mass", "Intensity"]

# ----------------- Output --------------------------------------------------
pickle_out = open(output_file, "wb")
pickle.dump(df, pickle_out)
pickle_out.close()

df.to_csv(output_csv, index=False)