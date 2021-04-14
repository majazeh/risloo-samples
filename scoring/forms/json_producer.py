import json
from openpyxl import Workbook ,load_workbook
from pathlib import Path

my_path = str(Path(__file__).resolve().parent)
my_par_dir = my_path.split('/forms')[0]


# raw form loading
with open( my_path +'/raw.json', 'r') as file:
    data = json.load(file)


########################### Parameter setting ################################
test_name = 'Alaki'
file_name = 'Alaki'

options_list = [
                    "گزینه الف",
                    "گزینه ب",
                    "گزینه پ",
                    "گزینه ت",
                    "گزینه ث"
                    ]
num_options = len(options_list)

data["title"] = "افسردگی کودکان و نوجوانان - جان‌بزرگی"
# data["description"] ="## دستور اجرای آزمون\n\nابتدا هر مجموعه را بخوانید و سپس نزدیک‌ترین فکر متناسب با حال کنونی خود را مشخص کنید. تاکید می‌کنیم که هر چند ممکن است شما با چند گزینه موافق باشید اما صرفا یک گزینه را انتخاب کنید که بازگو کننده زبان حال کنونی شماست"  
# data["description"] = "## دستور اجرای آزمون\n\nلطفا پس از مطالعه هر عبارت، اگر محتوای آن درباره شما درست است، گزینه بلی را انتخاب کنید و اگر درباره شما نادرست است، گزینه نه را انتخاب کنید. در این پرسشنامه پاسخ‌های صحیح یا غلط و پرسش‌های گمراه‌کننده وجود ندارد. به تمام عبارات با سرعت پاسخ دهید و درباره معنای دقیق آن‌ها وقت خود را زیاد تلف نکنید. "
data["description"] ="## دستور اجرای آزمون\n\nافراد از این جمله‌ها ممکن است برای توصیف خودشان استفاده کنند. لطفا هر جمله را به دقت بخوانید و ببینید که چقدر به آن جمله اعتقاد دارید یا بر اساس مقیاس فراوانی به آن پاسخ دهید. " 
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

book = load_workbook(my_par_dir + '/tests/'  + test_name +'/' + file_name  + '.xlsx')
sheet = book.active


question_numbers =  sheet.max_row - 1
print("question_numbers: ",question_numbers)


for i in range(question_numbers):
    item["text"] = str(sheet.cell(row = i+2, column=1).value)
    items.append(item.copy())

data["items"] = items


with open( my_path + '/' + test_name + '/' + file_name +'.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False ,indent= 4)





