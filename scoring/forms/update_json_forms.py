import json
from openpyxl import Workbook ,load_workbook
from pathlib import Path
import os 
from os.path import join as opj

my_path = str(Path(__file__).resolve().parent)
my_par_dir = my_path.split('/forms')[0]


#form loading
folder_names = os.listdir(my_path)
for folder_name in folder_names :
    if os.path.isdir(opj(my_path,folder_name)): 
        for file_name in os.listdir(opj(my_path,folder_name)):
            print(file_name)
            with open( opj(my_path ,folder_name ,file_name) , 'r') as file:
                data = json.load(file)
    
            new_field = {
                        "type": "text",
                        "label": "marital_status",
                        "text": "وضعیت تأهل",
                        "answer": {
                            "type": "select",
                            "options": [
                                "مجرد",
                                "متأهل"
                            ]
                        },
                        "alias": "marital_status",
                        "force": True
                    }
            if new_field not in  data["prerequisites"]:
                data["prerequisites"].append(new_field)
            
            with open( opj(my_path , folder_name , file_name) , 'w') as file:
                json.dump(data, file, ensure_ascii=False ,indent= 4)




