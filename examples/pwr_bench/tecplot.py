def read_tecplot(fname):
    data = {}
    with open(fname, 'r') as f:
        for l in f:
            entries = l.split()
            i, j, k = map(int, entries[:3])
            v = float(entries[3])

            data[(i,j,k)] = v
    return data


if __name__ == '__main__':
    d = read_tecplot('TFUEL_AI.dat')
    for ijk in ((1, 1, 10), (51, 1, 10), (1, 51, 10), (51, 51, 10), (4, 4, 10)):
        print ijk, d[ijk]

    


