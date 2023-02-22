from cowsay import cowsay, list_cows
import argparse

def set_args_parser():
    # set command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=str, help='String with the eyes pattern (2 chars)')
    parser.add_argument('-f', type=str, help='File with the cow picture')
    parser.add_argument('-l', help='If set, lists available cows')
    parser.add_argument('-n', help='If set, the given message will not be word-wrapped')
    parser.add_argument('-T', type=str, help='String with the tongue pattern (2 chars)')
    parser.add_argument('-W', type=int, help='The width of the text bubble')
    preset = 'bdgpstwy'
    for option in preset:
        parser.add_argument('-' + option, help='The cow behavior mode')

    return parser.parse_args()