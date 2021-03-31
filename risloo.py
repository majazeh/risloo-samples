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
            self.scoring_scale = getattr(__import__('scoring.' + dash + args['scale'] , fromlist=[args['scale']]), dash + args['scale'])(data, input_type)
            
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
    
    def export_excell(self):
        my_path = '/home/mostafa/Majazeh/tests/scoring/forms/'
        addr = self.args['input_data'].split('.json')[0]
        num = addr[-1]
        names = addr.split('/')
        
        test_name = names [-2]
        file_name = names [-1].split('_')[0]
        
        
        excell_path = my_path + '/' + test_name + '/' + file_name +'_test_' + num + '.xlsx'
        book = openpyxl.load_workbook(excell_path )
        
        
        book.create_sheet("outputs")
        sheet = book["outputs"]
        sheet.cell(row = 1, column=2).value = 'پاسخ سیستم'
        sheet.cell(row = 1, column=3).value = 'پاسخ دستی کارشناس'
        
        out_dic = self.scoring_scale.score.toDict()
        for i,key in enumerate(out_dic.keys()):
            out_dic[key]
            sheet.cell(row= i+2, column=1).value = key
            sheet.cell(row= i+2, column=2).value = out_dic[key]
        
        book.save(excell_path)

        
if (__name__ == '__main__'):
    rsl = risloo(**unilities.get_args())
    # rsl.export_excell()
    rsl.export()
