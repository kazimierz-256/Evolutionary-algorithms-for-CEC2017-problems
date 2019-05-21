DIFF = 'diff'
RAND = 'rand'
LIPOLD = 'lipold'
COMPACTOR = 'compactor'

algo = DIFF
limit = 100

filename_prefix = 'out/' + algo + '_' + str(limit) + '_'


def get_filename_prefix(algo_name=''):
    if algo_name == '':
        algo_name = algo
    return 'out/' + algo_name + '_' + str(limit) + '_'
