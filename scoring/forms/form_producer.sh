#!/bin/bash


folder_name="GMIT"
file_name=$folder_name"93"

title="پرسشنامه هوش‌های چندگانه گاردنر"

description="## دستور اجرای آزمون\n\nخواهشمند است که هر یک از جمله های زیر را با دقت بخوانید و براساس میزان توافق خود با هر یک از عبارات، یکی از گزینه های مقابل را انتخاب کنید."

option_positions_is_typical_form=$true
option_list_array="cat dog mouse frog"


if [ $option_positions_is_typical_form = $true ];then

python3 json_producer.py --folder_name $folder_name --file_name $file_name --title $title \
--description $description --option_positions_is_typical_form $option_positions_is_typical_form \
--option_list_array $option_list_array

else

python3 json_producer.py --folder_name $folder_name --file_name $file_name --title $title \
--description $description --option_positions_is_typical_form $option_positions_is_typical_form
fi


