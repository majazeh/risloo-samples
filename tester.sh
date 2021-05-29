
## if NOT saving => enumerous tests

# python3 /home/mostafa/Majazeh/risloo-samples/tester.py --folder_name JSGS --file_name JSGS93 --test_numbers 100 


## just saving for scientific tests

# test producing:
# python3 /home/mostafa/Majazeh/risloo-samples/tester.py --folder_name RCMAS --file_name RCMAS93 --test_numbers 2 -s
# test scoring
python3 /home/mostafa/Majazeh/risloo-samples/risloo.py -s JSGS93 -it file -id /home/mostafa/Majazeh/risloo-samples/scoring/tests/RCMAS/RCMAS93_test_1.json -ot raw json excell
python3 /home/mostafa/Majazeh/risloo-samples/risloo.py -s RCMAS93 -it file -id /home/mostafa/Majazeh/risloo-samples/scoring/tests/RCMAS/RCMAS93_test_2.json -ot raw json excell