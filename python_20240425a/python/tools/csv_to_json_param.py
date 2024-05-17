import csv
import os
import json
from tkinter import ttk,messagebox,filedialog

def saveDicttoFile(filepath, dict):

    try:
        with open(filepath, 'w', encoding='utf8') as outfile:
            json.dump(dict, outfile, ensure_ascii=False, indent=4)
    except:
        pass


filepath = filedialog.askopenfilename(filetypes=[("csv files","*.csv")],defaultextension=".csv")
if filepath:
    jsondict = {}
    reader = csv.DictReader(open(filepath,"r"),delimiter=",")
    for line in reader:
        csvdict=dict(line)
        key=csvdict.get("ParName","")
        if key:
            jsondict[key]=csvdict
    
filename, file_extension = os.path.splitext(filepath)

json_filename = filename+ ".json"

saveDicttoFile(json_filename,jsondict)



    
                       
