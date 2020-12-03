import unilities
import warnings
import json
import sys

class risloo():
    def __init__(self, **args):
        input_type = args['input_type']
        data = args['input_data']
        args['output_type']
        try:
            self.scale = getattr(__import__('scales.' + args['scale'], fromlist=[args['scale']]), args['scale'])(data, input_type)
        except:
            raise Exception('scale `%s` not defined', args['scale'])
        self.scale.scoring()

    def export(self):
        print(json.dumps(self.scale.score.toDict()), flush=True)
        
if (__name__ == '__main__'):
    rsl = risloo(**unilities.get_args())
    sys.stdout.flush()
    rsl.export()