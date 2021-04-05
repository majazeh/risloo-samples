import json
from random import randint
from openpyxl import Workbook ,load_workbook
from pathlib import Path

my_path = str(Path(__file__).resolve().parent)



# raw form loading
with open( my_path +'/raw.json', 'r') as file:
    data = json.load(file)


########################### Parameter setting ################################
test_name = 'PSDI'
file_name = 'PSDI'

options_list = [
                    "گزینه ۱",
                    "گزینه ۲",
                    "گزینه ۳",
                    "گزینه ۴"
                    ]
num_options = len(options_list)

data["title"] = "پرسش‌نامه سطوح تحول روانی معنوی جان‌بزرگی"
data["description"] ="## دستور اجرای آزمون\n\nابتدا هر مجموعه را بخوانید و سپس نزدیک‌ترین فکر متناسب با حال کنونی خود را مشخص کنید. تاکید می‌کنیم که هر چند ممکن است شما با چند گزینه موافق باشید اما صرفا یک گزینه را انتخاب کنید که بازگو کننده زبان حال کنونی شماست"  
# data["description"] = "## دستور اجرای آزمون\n\nلطفا پس از مطالعه هر عبارت، اگر محتوای آن درباره شما درست است، گزینه بلی را انتخاب کنید و اگر درباره شما نادرست است، گزینه نه را انتخاب کنید. در این پرسشنامه پاسخ‌های صحیح یا غلط و پرسش‌های گمراه‌کننده وجود ندارد. به تمام عبارات با سرعت پاسخ دهید و درباره معنای دقیق آن‌ها وقت خود را زیاد تلف نکنید. "
# data["description"] ="## دستور اجرای آزمون\n\nافراد از این جمله‌ها ممکن است برای توصیف خودشان استفاده کنند. لطفا هر جمله را به دقت بخوانید و ببینید که چقدر به آن جمله اعتقاد دارید یا بر اساس مقیاس فراوانی به آن پاسخ دهید. " 
# data["version"] = ""
# data["edition"] = ""

# data["edition_version"]=
# data["filler"]=
 





###############################################################################


items = []
item ={}
item = data["items"][0].copy()
item["answer"]["options"] = options_list

########################## load questions excell ###########################

book = load_workbook(my_path + '/' + test_name +'/' + file_name  + '.xlsx')
sheet = book.active


question_numbers =  sheet.max_row - 1
print(question_numbers)


for i in range(question_numbers):
    item["text"] = sheet.cell(row = i+2, column=1).value
    items.append(item.copy())

data["items"] = items


with open( my_path + '/' + test_name + '/' + file_name +'.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False ,indent= 4)



# Test producing
##################### user_answered #######################################
data["prerequisites"][0] ["user_answered"] = "2" # 1 for woman and 2 for man
data["prerequisites"][1] ["user_answered"] = "37" # age
data["prerequisites"][2] ["user_answered"] = "8"#str(randint(1,10)) # education options from 1 to 10

for j in range (2):
    book = Workbook()
    sheet = book.active
    
    sheet.title = "question_answers"
   
    sheet.cell(row = 1, column=1).value = 'شماره سوالات'
    sheet.cell(row = 1, column=2).value = 'پاسخ  گزینه فرد'
    
    
    for i,item in enumerate(data["items"]):
        
        item ["user_answered"] = str(randint(1,num_options))
        sheet.cell(row = i+2, column=1).value = i+1
        sheet.cell(row = i+2, column=2).value = item ["user_answered"]
    
        



    book.save( my_path + '/' + test_name +'/' + file_name + '_test_' + str(j+1) + '.xlsx') 

    with open( my_path + '/' + test_name + '/' + file_name +'_test_'+ str(j+1) + '.json', 'w') as file:
        json.dump(data, file , ensure_ascii=False ,indent= 4)


