from argparse import ArgumentParser

parser = ArgumentParser(prog='ShellTests',
                        usage='ShellTests [arg]',
                        description='''\n
                        Para usar isso, faça isso''',
                        epilog='Entendeu???',
                        fromfile_prefix_chars='@')

#parser.add_argument('x')
#parser.add_argument('y')
parser.add_argument('-foo', '-f', '--foo', type=float,
                    action='append', dest='xpto')
parser.add_argument('-i', const=int,
                    action='append_const', dest='xpto')
parser.add_argument('-v', action='count', default=0)
parser.add_argument('-xpto2', '-x', default=0, type=int,
                    choices=[1, 2, 3], required=True,
                    help='Ligado, Desligado, não sei', metavar='XPTO')

parser.print_help()
args = parser.parse_args()

print(args)

