from cowsay import cowsay, list_cows
import argparse

PRESET = 'bdgpstwy'

def set_args_parser():
    # set command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=str, default='oo', help='String with the eyes pattern')
    parser.add_argument('-f', type=str, default='default', help='File with the cow picture')
    parser.add_argument('-l', action='store_true', help='If set, lists available cows')
    parser.add_argument('-n', action='store_false', help='If set, the given message will not be wrapped in a bubble')
    parser.add_argument('-T', type=str, default='  ', help='String with the tongue pattern')
    parser.add_argument('-W', type=int, default=40, help='The width of the text bubble')
    parser.add_argument('msg', nargs='*', type=str, default='', help='A message for the cow to say')
    for option in PRESET:
        parser.add_argument('-' + option, action='store_true', help='The cow behavior mode')

    return parser.parse_args()

args = set_args_parser()
if args.l:
    print(*list_cows())
else:
    if '/' in args.f:
        cow = 'default'
        cowfile = args.f
    else:
        cow = args.f
        cowfile = None
    preset = ''
    for option in PRESET:
        if args.__dict__[option]:
            preset = option
            break
    print(cowsay(' '.join(args.msg),
                 cow=cow,
                 preset=preset,
                 eyes=args.e,
                 tongue=args.T,
                 width=args.W,
                 wrap_text=args.n,
                 cowfile=cowfile))