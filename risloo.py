import unilities
import warnings
import json
import sys

class risloo():
    def __init__(self, **args):
        self.args = args 
        input_type = args['input_type']
        data = args['input_data']

        dash = ''
        if args['scale'][0].isdigit():
            dash = '_'


        # Scoring
        try:
            self.scoring_scale = getattr(__import__('scoring.' + args['scale'] , fromlist=[args['scale']]), dash + args['scale'])(data, input_type)
            
        except:
            raise Exception('score scale `%s` not defined', args['scale'])
        self.scoring_scale.scoring()
        
        
        #Interpretation if it is needed
        if args['Interpretation']:

            try:
                self.interpreting_scale = getattr(__import__('interpreting.'  + args['scale'], fromlist=[args['scale']]), dash + args['scale'])(data, input_type)
                
            except:
                raise Exception('interp scale `%s` not defined', args['scale'])


            self.interpreting_scale.interpreting()


    def export(self):
        sys.stdout.write(json.dumps(self.scoring_scale.score.toDict()) + "\n")
        
        if self.args['Interpretation']:
            sys.stdout.write(self.interpreting_scale.interpret.get_text() + "\n")
        
if (__name__ == '__main__'):
    rsl = risloo(**unilities.get_args())
    rsl.export()
