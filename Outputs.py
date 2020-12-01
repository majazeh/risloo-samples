
import urllib.request, json 
import unittest

class Outputs():
    def __init__(self , json_data , Inputs) :
        self.json_data = json_data 
        # self.test_scores =  test_Scores
        self.Inputs = Inputs
        #self.save_output (self.Inputs.output_address)
        

        if  self.Inputs.unittest:
            self.run_unittest()

    
    def save_output (self  , test_Scores ,report) :
        temp_dic = test_Scores.scores.copy()
        temp_dic['report'] = report
        
        self.json_data['score'] = temp_dic
        return self.json_data

        
    def run_unittest(self):
        unittest = Testdata(self)
        unittest.test_equality()

                
    
    


class Testdata(unittest.TestCase):

    def __init__(self , test_Outputs):
        self.test_Outputs = test_Outputs
    
    def test_equality(self):
        if self.test_Outputs.json_data :
            self.assertEqual(self.test_Outputs.json_data['score'], self.test_Outputs.json_data['correct_scores']) # second must be the correct data

        else :
            print("You must first save your output_json_data !")
        


