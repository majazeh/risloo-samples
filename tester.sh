#!/bin/sh

folder_name="JCSI"
file_name="JCSI93"

option_numbers=5
question_numbers=34




jsonStr=$(jq '.' ./scoring/forms/$folder_name/$file_name.json)


a=$(shuf -i 1-$option_numbers -n $question_numbers -r)


new_jsonStr=$(jq --arg eidx 1 '.items[($eidx|tonumber)].answer + {"user_answered":"4"}' <<< $jsonStr)

# echo $new_jsonStr
$(jq '.items[($eidx|tonumber)].answer = new_jsonStr' <<< $jsonStr)



# + {"user_answered":"2"}
# echo $b


# python3 ./risloo.py -s $file_name -it file -id ./scoring/tests/$folder_name/$file_name$test_key$VARIABLE.json 


