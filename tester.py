import json
from random import randint
from pathlib import Path
import os
import subprocess



folder_name="SSS"
file_name="SSS93"
test_numbers = 100

my_path = str(Path(__file__).resolve().parent)

# test form loading
with open( my_path+ '/scoring/forms/' + folder_name + '/' + file_name +'.json', 'r') as file:
    data = json.load(file)



for j in range (test_numbers):
    # Test producing
    ##################### user_answered #######################################
    data["prerequisites"][0] ["user_answered"] = "2" # 1 for woman and 2 for man
    data["prerequisites"][1] ["user_answered"] = "37" # age
    data["prerequisites"][2] ["user_answered"] = "8"#str(randint(1,10)) # education options from 1 to 10

    
    for i,item in enumerate(data["items"]):
        num_options = len(item["answer"]["options"])
        item ["user_answered"] = str(randint(1,num_options))

    y = json.dumps(data,separators=(',', ':'))
    
    command = ["python3", "/home/mostafa/Majazeh/risloo-samples/risloo.py" ,"-s",file_name ,
                "-it","raw","-id" ,y]
    
    rc = subprocess.run(command,capture_output=True)
    print("test %d :" % (j+1) , rc.stdout.decode() + '\n\n')
  
    



