import unilities
import warnings
import json
import sys
import re

class risloo():
    def __init__(self, **args):
        input_type = args['input_type']
        data = args['input_data']
        args['output_type']
        scale_name = "_" + args['scale']if re.search("^\d", args['scale']) else args['scale']
        try:
            self.scale = getattr(__import__('scales.' + scale_name, fromlist=[scale_name]), scale_name)(data, input_type)
        except:
            raise Exception('scale `%s` not defined', scale_name)
        self.scale.scoring()

    def export(self):
        print(json.dumps(self.scale.score.toDict()), flush=True)
        
if (__name__ == '__main__'):
    rsl = risloo(**unilities.get_args())
    sys.stdout.flush()
    rsl.export()