import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--scale" ,help="scale id [MBTI93, MBTI9A, Raven93, ...]")
    parser.add_argument("-it", "--input_type", help="tell what's input_type [raw,file,remote]", default='raw')
    parser.add_argument("-id", "--input_data", help="absolute addrress of where you want to read", required=True)
    parser.add_argument("-ot", "--output_types", help="which type of output do you want to get? [raw,json,excell]", nargs='*', default=['raw'])
    parser.add_argument("-ip", "--Interpretation", help="Do you want to run interpretation?", action="store_true")
    parser.add_argument("-u", "--unittest", help="performing unittest of this test", action="store_true")
    return dict(parser.parse_args().__dict__.items())
