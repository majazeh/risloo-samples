import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("scale", help="scale id [MBTI93, MBTI9A, Raven93, ...]")
    parser.add_argument("-it", "--input_type", help="tell what's input_type [raw,local,remote]", default='raw')
    parser.add_argument("-id", "--input_data", help="absolute addrress of where you want to read", required=True)
    parser.add_argument("-ot", "--output_type", help="absolute addrress of where you want to read", default='raw')
    parser.add_argument("-u", "--unittest", help="performing unittest of this test", action="store_true")
    return dict(parser.parse_args().__dict__.items())