#!/bin/bash


folder_name="LMIQ"
file_name=$folder_name"93"

title="پرسشنامه هوش اخلاقی لینک و همکاران"

description="## دستور اجرای آزمون\n\nلطفا هر یک از عبارات زیر را خوانده و میزان موافقت خود را با آن مشخص کنید:"

option_positions_is_typical_form=$true
option_list_array="cat dog mouse frog"


###########################################

if [ $option_positions_is_typical_form = $true ];then

python3 json_producer.py --folder_name $folder_name --file_name $file_name --title $title \
--description $description --option_positions_is_typical_form $option_positions_is_typical_form \
--option_list_array $option_list_array

else

python3 json_producer.py --folder_name $folder_name --file_name $file_name --title $title \
--description $description --option_positions_is_typical_form $option_positions_is_typical_form
fi


