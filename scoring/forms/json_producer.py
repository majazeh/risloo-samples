import json
from openpyxl import Workbook ,load_workbook
from pathlib import Path
from os.path import join as opj
import os

my_path = str(Path(__file__).resolve().parent)
my_par_dir = my_path.split(os.path.sep +'forms')[0]


# raw form loading
with open( opj(my_path , 'raw.json'), 'r' ) as file:
    data = json.load(file)


########################### Parameter setting ################################
folder_name = 'BAOMEIS'
file_name = 'BAOMEIS93'

options_list = [
                "بسیار زیاد موافق",
                "بسیار موافق",
                "موافق",
                "مخالف",
                "بسیار مخالف",
                "بسیار زیاد مخالف"
                    ]
num_options = len(options_list)

data["title"] = "پرسشنامه حالات هویت بنیون و آدامز"
#data["description"] ="## دستور اجرای آزمون\n\nبرای هر یک از موارد زیر گزینه‌ای را که بیشترین مطابقت را با شرح حال مراجع دارد انتخاب کنید. اطمینان حاصل کنید که از بین گزینه ها، مناسب ترین آنها را انتخاب نموده اید."  
data["description"] = "## دستور اجرای آزمون\n\nخواهشمند است که هر یک از جمله های زیر را با دقت بخوانید و براساس میزان توافق خود با هر یک از عبارات، یکی از گزینه های مقابل را انتخاب کنید. برخی از جمله ها از چند بخش تشکیل شده اند، لطفاً واکنش شما به هر جمله نسبت به کل آن باشد و نه یک بخش خاص از آن."
# data["description"] ="## دستور اجرای آزمون\n\nدانش‌آموز گرامی\nدر اینجا جملاتی وجود دارد که بیان می‌دارد چگونه افراد در مورد خودشان «فکر» و «احساس» می‌کنند. چنانچه فکر می‌کنید جمله در مورد شما درست است جواب «بلی» را نتخاب کنید. ولی اگر فکر می‌کنید که جمله در مورد شما درست نیست، جواب «خیر» را انتخاب کنید.\nسعی کنید به تمام سوالات جواب دهید، اگرچه در بعضی موارد تصممی‌گیری برای شما مشکل باشد. همینطور برای یک جمله هر دو جواب «بلی» و «خیر» را انتخاب نکنید.\nدر این پرسش‌نامه پاسخ درست و غلط وجود ندارد. فقط شما می‌توانید به ما بگویید که در مورد خودتان چگونه «فکر» و «احساس» می‌کنید. به یاد داشته باشید که پس از خواندن هر جمله از خودتان بپرسید که آیا در مورد من درست است؟ اگر درست است، جواب «بلی» و اگر غلط است جواب «خیر» را انتخاب نمایید. قلبا از همکاری شما کمال تشکر را داریم." 
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
print(opj(my_par_dir, 'tests', folder_name, file_name + '.xlsx'))
book = load_workbook(opj(my_par_dir, 'tests', folder_name, file_name + '.xlsx'))
sheet = book.active

question_numbers =  sheet.max_row - 1
print("question_numbers: ",question_numbers)

for i in range(question_numbers):
    item["text"] = str(sheet.cell(row = i+2, column=1).value)
    items.append(item.copy())

data["items"] = items

Path(my_path + os.path.sep + folder_name ).mkdir(exist_ok=True)

with open(opj(my_path, folder_name, file_name + '.json'), 'w') as file:
    json.dump(data, file, ensure_ascii=False ,indent= 4)




