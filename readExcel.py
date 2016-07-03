# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:27:34 2016

@author: Franziska
"""
import random
from random import randint
import pandas
import xlrd
import xlwt

#read in the disclosure and prompt tables from excel
disclosure_df=pandas.read_excel('dictionaries/disclosures.xlsx', sheetname='Disclosures')
prompt_df=pandas.read_excel('dictionaries/disclosures.xlsx', sheetname='Prompts')


used_disclosures = {}
workbook = xlrd.open_workbook('usedids/used_ids.xlsx')
sheet = workbook.sheet_by_index(0)   
for i in range(11):
    cell_value_class = sheet.cell(0,i).value
    cell_value_id = sheet.col_values(i,1,None)
    cell_value_id = filter(None, cell_value_id)
    used_disclosures[cell_value_class] = cell_value_id
    
    
#drop the columns that are not needed
disclosure_df.drop(['Topic','Valence','Parameters','Self-Disclosure','SD_ITA','Gesture','ClosingY','ClosingN'], axis=1,inplace=True)
prompt_df.drop(['Parameter','Prompt','Prompt_ITA'], axis=1, inplace=True)

#drop the empty disclosure
disclosure_df = disclosure_df[disclosure_df.ID != 'SDEmpty']

#split the disclosures into four different dataframes according to intimacy lvl
discDF_lvl0 = disclosure_df[disclosure_df['Level']==0]
discDF_lvl1 = disclosure_df[disclosure_df['Level']==1]
discDF_lvl2 = disclosure_df[disclosure_df['Level']==2]
discDF_lvl3 = disclosure_df[disclosure_df['Level']==3]

#picking a random item from dataframe
def get_random_disclosure(df_disc, participantID):
    #some start value
    key = df_disc.iloc[1]['ID']
    disclosure = df_disc[df_disc["ID"] == key]
    list_used = used_disclosures[participantID]
    print(type(key))
    print(type(list_used))
    #check whether it is in the list of already used items
    while key in list_used:
        #get random index
        key = random.choice(df_disc["ID"].tolist())
        #get row at this index
        disclosure = df_disc[df_disc["ID"] == key]
        print(type(key))
    #add the ID of chosen disclosure to list of used IDs    
    used_disclosures[participantID].append(key)
    #return triple of used dic, text to speak, and associated prompt
    return [disclosure['SD_NL'].iloc[0], disclosure['Prompt'].iloc[0], disclosure['Woord'].iloc[0]]
    
def get_associated_prompt(prompt_id):
    prompt_id = int(prompt_id.replace('P',''));
    prompt = prompt_df.iloc[prompt_id-1]
    return prompt['Prompt_NL']
    
def parse_content(content, say_name, name):
    #Names to be used in the interaction (can be changed but should be the same across children)
    nameFriend = "Danni" #robot's best robot friend
    nameSister = "Alex" #robot's sister
    nameOwner = "Marco" #name of child who previously owned robot
    nameNurse = "Julia" #name of nurse that robot has a crush on. Ideally, one that works at hospital and that the child knows.
    nameR1 = "Elmo" #another male care robot in the hospital
    nameR2 = "Pippa" #new female care robot in the hospital
    nameR3 = "Kris" #bully, also robot in the hospital
    nameDoctor = "na"
    genderDoctor = "Female"
    
    content = content.replace("{name-friend}",nameFriend)
    content = content.replace("{name-sis}",nameSister)
    content = content.replace("{name-owner}",nameOwner)
    content = content.replace("{name-r1}",nameR1)
    content = content.replace("{name-r2}",nameR2)
    content = content.replace("{name-r3}",nameR3)
    content = content.replace("{name-dr}",nameDoctor)
    content = content.replace("{name-nurse}", nameNurse)
    if genderDoctor == "Male":
        content = content.replace("{dr-gender-pn}", "Hij")
    else:
        content = content.replace("{dr-gender-pn}","Zij")
    #name hospital, name university, name city
    content = content.replace("{name-hospital}", "dit ziekenhuis")
    content = content.replace("{name-university}", "Radboud Universiteit Nijmegen")
    content = content.replace("{name-city}", "Nijmegen")
    
    content = content.replace("Dr. ", "Doktor ")
    
    if say_name:
        content = content.replace("{name-child}", name)
    else:
        content = content.replace(", {name-child}", "");
        content = content.replace(",{name-child}", "");
        content = content.replace("{name-child},", "");
    return content
        

def write_used_disclosures(filename, dic):
    book = xlwt.Workbook()
    sh = book.add_sheet("Sheet1")
    i=0
    for key in dic.keys():
        values = dic[key]
        sh.write(0,i,key)
        for j in range(len(values)):
            sh.write(j+1, i, values[j])
        i+=1
    book.save(filename)
    





