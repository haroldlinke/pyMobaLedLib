# -*- coding: utf-8 -*-
import csv
import os
import json
from tkinter import ttk,messagebox,filedialog

def replace_chars(key):
    
    value = csvdict[key]
    value = value.replace("“","'")
    value = value.replace("”","'")
    value = value.replace("|","\n")
    value = value.replace("„","'")
    value = value.replace("“","'")
    csvdict[key] = value

def create_macro_str(macro):
    
    if macro != "":
        macro = macro.replace (" ","")
    
        macropartlist = macro.split("(")
               
        macroname = macropartlist[0]
        
        if len(macropartlist)==2:
        
            params = macropartlist[1]
            params = params [:-1] # remove ")"
            paramlist = params.split(",")
        else:
            paramlist = []
        
        macro_str = macroname
        
        for param in paramlist:
            macro_str = macro_str + "{"+param+"},"
        
        # delete last ","
        macro_str = macro_str[:-1] + ")"
        
    else:
        macro_str = ""
        paramlist = []
    
    return macro_str, paramlist
    
def saveDicttoFile(filepath, dict):

    try:
        with open(filepath, 'w', encoding='utf8') as outfile:
            json.dump(dict, outfile, ensure_ascii=False, indent=4)
    except:
        pass


filepath = filedialog.askopenfilename(filetypes=[("csv files","*.csv")],defaultextension=".csv")
if filepath:
    jsondict = {}
    reader = csv.DictReader(open(filepath,"r"),delimiter=";")
    for line in reader:
        
        csvdict=dict(line)
        for key in csvdict:
            replace_chars(key)
            
        macro_str, paramlist = create_macro_str(csvdict["Macro"])
        
        csvdict["MacroStr"] = macro_str
        csvdict["Params"] = paramlist
        
        macro=csvdict.get("Name","")
        if macro:
            jsondict[macro]=csvdict
 
print(jsondict)   
filename, file_extension = os.path.splitext(filepath)

json_filename = filename+ ".json"

saveDicttoFile(json_filename,jsondict)



    
                       
