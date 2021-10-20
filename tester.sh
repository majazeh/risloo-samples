
## if NOT saving => enumerous tests

# python3 tester.py --folder_name MMFAD --file_name MMFAD93 --test_numbers 200 

## just saving for scientific tests

# test producing:
python3 tester.py --folder_name MMFAD --file_name MMFAD93 --test_numbers 2 -s
# test scoring
python3 risloo.py -s MMFAD93 -it file -id ./scoring/tests/MMFAD/MMFAD93_test_1.json -ot raw json excell
python3 risloo.py -s MMFAD93 -it file -id ./scoring/tests/MMFAD/MMFAD93_test_2.json -ot raw json excell