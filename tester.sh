
## if NOT saving => enumerous tests
folder_name="GMIT"
file_name=$folder_name"93"

# python3 tester.py --folder_name $folder_name --file_name $file_name --test_numbers 200 

## just saving for scientific tests

# test producing:
python3 tester.py --folder_name $folder_name --file_name $file_name --test_numbers 2 -s
# test scoring
python3 risloo.py -s $file_name -it file -id ./scoring/tests/$folder_name/$file_name"_test_1.json" -ot raw json excell
python3 risloo.py -s $file_name -it file -id ./scoring/tests/$folder_name/$file_name"_test_2.json" -ot raw json excell