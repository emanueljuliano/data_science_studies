from argparse import ArgumentParser

parser = ArgumentParser(
    prog='O Nome do programa (default: sys.argv[0]',
    usage='String descrevendo como usar o programa',
    description='Mensagem que será exibida no help (default: none',
    epilog='Texto que será exibido após os parametros (default: none)',
    fromfile_prefix_chars='@') # 'Arquivos com os parâmetros pré-fixados'
