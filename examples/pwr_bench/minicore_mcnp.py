from assembly_mcnp import MI
from minicore_model import minicore

MI.gm = minicore

if __name__ == '__main__':
    MI.run('P')

