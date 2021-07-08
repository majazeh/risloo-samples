
## if NOT saving => enumerous tests

# python3 /home/mostafa/Majazeh/risloo-samples/tester.py --folder_name SAM --file_name SAM93 --test_numbers 100 


## just saving for scientific tests

# test producing:
python3 /home/mostafa/Majazeh/risloo-samples/tester.py --folder_name SAM --file_name SAM93 --test_numbers 2 -s
# test scoring
python3 /home/mostafa/Majazeh/risloo-samples/risloo.py -s SAM93 -it file -id /home/mostafa/Majazeh/risloo-samples/scoring/tests/SAM/SAM93_test_1.json -ot raw json excell
python3 /home/mostafa/Majazeh/risloo-samples/risloo.py -s SAM93 -it file -id /home/mostafa/Majazeh/risloo-samples/scoring/tests/SAM/SAM93_test_2.json -ot raw json excell