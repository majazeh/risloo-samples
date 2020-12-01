
import urllib.request, json 
import argparse

class Inputs():
    
    def __init__(self):
        # Initiate the parser for passing to input class
        parser = argparse.ArgumentParser()

        parser.add_argument("-it", "--input_type", help="tell what's input_type [raw,local,remote]")
        parser.add_argument("-id", "--input_data", help="absolute addrress of where you want to read")
        #parser.add_argument("-oa", "--output_address", help="absolute addrress of where you want to save output")
        parser.add_argument("-u", "--unittest", help="performing unittest of this test", action="store_true")

        # Read arguments from the command line
        args = parser.parse_args()
        self.how_to_read = ['remote','local','raw']
        
        if args.input_data:
            self.input_address = args.input_data        
        else :
            raise NameError("You didn't give any input address!")

        # if args.output_address:
        #     self.output_address = args.output_address        
        # else :
        #     raise NameError("You didn't give any output address!")

        if  args.input_type:
            self.input_type = args.input_type
        else :
            raise NameError("You didn't give any input-type!")

        
        self.unittest = args.unittest
       

    def get_all_types_of_inputs(self):
        return self.how_to_read
    
    def get_json_data(self):
        
        
        if self.input_type in self.how_to_read:
            
            
            if self.input_type == 'raw' :
                json_data = self.input_address
            
            elif self.input_type == 'local' :
                
                with open(self.input_address, 'r') as json_file:
                    json_data = json.loads(json_file.read())

                
            elif self.input_type == 'remote' :
                with urllib.request.urlopen(self.input_address) as url:
                    json_data = json.loads(url.read().decode())
                       
            
        else :
            raise NameError("This kind of input is not defined!")
        
        return json_data
        


class Scores():
    
    def __init__(self):
        self.scores = {}
    
    def increase_score(self, factor = "E" , weight=0):
        self.scores[factor] = self.scores[factor] +  weight
    
    def add_factor(self, factor):
        if factor not in self.scores:
            self.scores[factor] = 0
    
    

