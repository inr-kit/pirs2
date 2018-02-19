from . import convertors

from ...solids import Box, Cylinder
from ...core.trageom.vector import Vector3, pi

import time

def get_rod_grid(gm, rks, fks, xs, ys, zs, mats, warnings=False, log=True):
    """
    get a rectangular grid in which all rods (accessed by rks in gm) and fuel
    elements (accessed by fks) fit and list of cladding/fuel material
    combinations.

    xs and ys are the lists of x and y coordinates for the grid.

    zs is the list of z coordinates for the axial decomposition of fuel elements.

    >>> xs = ys = [0]
    >>> b = Box()
    >>> c = b.insert('clad', Cylinder())
    >>> g = c.insert('gap',  Cylinder())
    >>> f = g.insert('fuel', Cylinder())
    >>> c.material = 'zirc'
    >>> f.material = 'uo2'
    >>> get_rod_grid(b, [('clad')], [('clad', 'gap', 'fuel')], xs, ys, [1], {'zirc': 'zircaloy', 'uo2': 'uo2'})
    ({(0, 0): {'perimeter': 0.06283185307179587, 'diameter': 0.02, 'axial': [[1, 0.0]], 'material': 1, 'key': 'clad', 'area': 0.0003141592653589793, 'heated': True, 'fake': False}}, [('zircaloy', 'uo2', 0.02, 0.0, 0.0)])

    """
    DEFAULT_CLAD_THICKNESS = 0.01 # m
    DEFAULT_GAS_VOLUME = 0.1 # m^3

    if log:
        TFORMAT='get_rod_grid:{} {}'
        t1 = time.time()

    rLST = []
    fLST = []
    for k in rks:
        r = gm.get_child(k)
        x = r.abspos().x/100.
        y = r.abspos().y/100.
        rLST.append((r, x, y, k))
    for k in fks:
        f = gm.get_child(k)
        x = f.abspos().x/100.
        y = f.abspos().y/100.
        fLST.append((f, x, y, k))


    def find_rod(gm, x, y):
        for (r, rx, ry, rk) in rLST:
            if x == rx and y == ry:
                return (r, rk)
        else:
            return (None, None)
            

    def find_fuel(gm, x, y):
        for (f, fx, fy, fk) in fLST:
            if x == fx and y == fy:
                return f
        else:
            return None

    empty = map(lambda z: [z, 0], zs)

    g = {}
    m = []
    for y in ys:
        for x in xs:
            r, key = find_rod(gm, x, y)
            f = find_fuel(gm, x, y)
            if r is not None:

                rr = r.R / 100.0
                if f is not None:
                    fm = mats[f.material]
                    fd = (f.R/100.0) * 2
                else:
                    if warnings:
                        print 'warning: no fuel material found for rod at {0}/{1}, {2}'.format(x,y, r.children_keys)
                    fm = 'uo2'
                    fd = rr * 0.9

                if 'gap' in r.children_keys:
                    gr = r.get_child('gap').R / 100.0
                    # thick = gr - fd/2.
                    thick = rr -gr # clad thickness
                    vol = (rr**2 - gr**2) * pi * (r.Z/100)
                elif r.clad_thickness is not None:
                    thick = r.clad_thickness 
                    gr = rr - thick
                    vol = (gr**2 - fd**2/4.) * pi * (r.Z/100)
                else:
                    if warnings:
                        print 'warning: no gap found for rod at {0}/{1}'.format(x,y)
                    thick = rr * 0.1
                    vol = DEFAULT_GAS_VOLUME

                try:
                    puf = r.pu_fraction
                except AttributeError:
                    puf = 0.

                mat = (mats[r.material], fm, fd, thick, vol, puf)
                if mat not in m: # inefficient
                    m.append(mat)

                if f is not None:
                    ah = axial_heat(f, x, y, zs)
                else:
                    ah = empty

                v = { 'diameter':  rr * 2,
                      'area':      pi * rr**2,
                      'perimeter': pi * 2 * rr,
                      'heated':    f is not None,
                      'material':  m.index(mat) + 1,
                      'axial':     ah,
                      'key':       key,
                      'fake':      False }
            else:
                mini = 1e-12
                mir  = mini
                mid  = 2 * mir
                mia  = pi * mir**2
                mip  = pi * 2 * mir
                if warnings:
                    print 'warning: fake rod at {0}/{1}'.format(x, y)
                mat = ('zircaloy', 'uo2', mini, mini, mini)
                if mat not in m: # inefficient
                    m.append(mat)

                v = { 'diameter': mid, 'area': mia, 'perimeter': mip, 'heated': False,
                        'material': m.index(mat) + 1, 'axial': empty, 'key': key,
                        'fake': True}

            g[(x,y)]=v

    return (g, m)

def channel_row(c, grid, coords, wrapped=False):
    """
    Calculate the row for channel c in the channel position table.

    c: the channel index,
    grid: the x/y map of rod representations,
    coords: [(lx, ly), (rx, ry)]
    lx: x coordinate of the lower left adjacent rod
    ly: y coordinate of the lower left adjacent rod
    rx: x coordinate of the top right adjacent rod
    ry: y coordinate of the top right adjacent rod
    rods: a string to describe how mary adjacent rods exist (1-4)

    In case of the bottom row, ry is the coordinate of the boundary cell
    (because there are no adjacent rods below). The other coordinates refer to
    the boundary cell analogously for the different boundary cases.

    Return a tuple containing the x and y coordinates of the channel,
    the radius of the adjacent rod (at x/y) and the actual row table entry.

    >>> g = {(-2, -1): {'area': 1, 'perimeter': 1, 'heated': True}, (-2, 1): {'area': 1, 'perimeter': 1, 'diameter': 2, 'heated': False}, (2, 1): {'area': 1, 'perimeter': 1, 'diameter': 2, 'heated': False}}
    >>> channel_row(42, g, [(-2,-1), (2,1)])
    (0.0, 0.0, 1.0, 2.0, [42, 7.25, 0.75, 0.25, 0.0, 0.0])

    """

    [(lx, ly), (rx, ry)] = coords
    cx = lx + (rx - lx) / 2.0
    cy = ly + (ry - ly) / 2.0

    def g(x, y):
        try:
            r = grid[(x, y)]
        except KeyError:
            r = {'area': 0, 'perimeter': 0, 'heated': False, 'diameter': 0}
        return r

    def ar(x, y):
        return g(x, y)['area'] / 4.0
    def per(x, y):
        return g(x, y)['perimeter'] / 4.0
    def he(x, y):
        if g(x, y)['heated']:
            return per(x, y)
        return 0
    def rad(x, y):
        return g(x, y)['diameter'] / 2.0
        
    crr = rad(rx, ly) + rad(rx, ry)
    crt = rad(lx, ry) + rad(rx, ry)

    pins = [(lx, ly), (rx, ly), (lx, ry), (rx, ry)]

    area = (rx - lx) * (ry - ly)
    area -= sum(map(lambda (x, y): ar(x, y), pins))

    heat = sum(map(lambda (x, y): he(x, y), pins))
    wett = sum(map(lambda (x, y): per(x, y), pins))

    return (cx, cy, crr, crt, [c, area, wett, heat, cx, cy])

def channel_neighbour_row(xs, ys, xi, yi, c, crr, crt):
    """
    Return the row for channel c in the channel neighbours table and the Box
    object representing the channel.

    xs and ys are the x and y coordinates of pins,
    xi and yi the indices into the coordinate lists for the upper right corner
                  of the channel,
    cx and cy the x and y coordinates of the channel center,


    Examples:

    A channel in the center has two 'normal' neighbours:

    >>> (b, r) = channel_neighbour_row([0,2,4,6], [0,2,5,6], 2, 2, 42, 2, 1)
    >>> r
    [42, 43, 1, 2.0, 45, 1, 2.0]
    >>> b.X
    2
    >>> b.Y
    3

    The channel at the top right corner has no neighbours. It does not use the
    corner radius values:

    >>> (b, r) = channel_neighbour_row([0,2,4,6], [0,2,5,6], 3, 3, 42, 'not', 'used')
    >>> r
    [42, 0, 0, 0, 0, 0, 0]
    >>> b.X
    2
    >>> b.Y
    1


    The channel at the lower left corner has two neighbours:

    >>> (b, r) = channel_neighbour_row([0,2,4,6], [0,2,5,6], 1, 1, 42, 1, 0)
    >>> r
    [42, 43, 1, 2.0, 45, 2, 2.5]
    >>> b.X
    2
    >>> b.Y
    2


    A channel at the right border only has a top neighbour. It uses only the
    top corner radius:

    >>> (b, r) = channel_neighbour_row([0,2,4,6], [0,2,5,6], 3, 1, 42, 'unused', 1)
    >>> r
    [42, 0, 0, 0, 45, 1, 2.5]
    >>> b.X
    2
    >>> b.Y
    2

    A channel at the top border only has a right neighbour. It uses only the
    right corner radius:
    >>> (b, r) = channel_neighbour_row([0,2,4,6], [0,2,5,6], 1, 3, 42, 0.5, 'unused')
    >>> r
    [42, 43, 0.5, 2.0, 0, 0, 0]

    """

    line = len(xs) - 1

    y_len = ys[yi] - ys[yi-1]
    cy = ys[yi-1] + y_len / 2.0

    x_len = xs[xi] - xs[xi-1]
    cx = xs[xi-1] + x_len / 2.0

    if xi + 1 < len(xs):
        r = c + 1
        r_d = (xs[xi+1] - xs[xi-1]) / 2.0
        r_g = y_len - crr
    else:
        r = r_d = r_g = 0

    if yi + 1 < len(ys):
        t = c + line
        t_d = (ys[yi+1] - ys[yi-1]) / 2.0
        t_g = x_len - crt
    else:
        t = t_d = t_g = 0
    
    b = Box()
    b.X = x_len
    b.Y = y_len

    return (b, [c,r,r_g,r_d,t,t_g,t_d])

def make_channel(c, xi, yi, constraints):
    """
    Create channel c identified by (urx, ury) at the upper right corner with
    given constraints and return the triple of its row, neighbour row and Box
    object.

    """

    (grid, xs, ys, wrapped, borders) = constraints
    (left, right, bottom, top) = borders

    cxs = [left]
    cxs.extend(xs)
    cxs.append(right)
    cys = [bottom]
    cys.extend(ys)
    cys.append(top)

    (cx, cy, crr, crt, row) = channel_row(c, grid, [(cxs[xi], cys[yi]), (cxs[xi+1], cys[yi+1])], wrapped)
    (box, nrow) = channel_neighbour_row(cxs, cys, xi+1, yi+1, c, crr, crt)

    return (row, nrow, box)

def rod_tables(grid, xs, ys, power_fraction):
    """
    Create the tables with rod positions and rod neighbouring relationships.

    grid: the map of rod representations,
    xs:   the x coordinate of grid map entries,
    ys:   the y coordinate of grid map entries,
    power_fraction: the initial power fraction of each rod

    Return a triple containing the rod table, the rod neighbours table and the
    axial discretization table.

    >>> xs = ys = [0,1]
    >>> g = {(0,0): None, (1,0): {'heated': False, 'material': 'mat1', 'diameter': 'diam1', 'axial': [[1, 'unused']], 'key': 'key1'}, (0,1): {'heated': True, 'material': 'mat2', 'diameter': 'diam2', 'axial': [[2, 2]], 'key': 'key2'}, (1,1): None}
    >>> rod_tables(g, xs, ys, 42)
    ([[1, 'mat1', 'diam1', 0, 1, 0], [2, 'mat2', 'diam2', 42, 0, 1]], [[1, 2, 0.25, 3, 0.25, 5, 0.25, 6, 0.25], [2, 4, 0.25, 5, 0.25, 7, 0.25, 8, 0.25]], [[1, 1, 0], [1, 2, 2.0]], ['key1', 'key2'])

    """
    rods = []
    r_ns = []
    r_ax = []
    index_key_mapping = []
    r = 1
    for yi,y in enumerate(ys):
        for xi,x in enumerate(xs):
            rd = grid[(x,y)]
            if rd == None:
                continue
            elif rd['heated']:
                pf = power_fraction
            else:
                pf = 0
            rods.append([r, rd['material'], rd['diameter'], pf, x, y])
            ll = 1 + yi * (len(xs) + 1) + xi
            ul = ll + len(xs) + 1
            r_ns.append([r, ll, 0.25, ll + 1, 0.25, ul, 0.25, ul + 1, 0.25])
            axheat = rd['axial']
            zc = 1
            for [z, v] in axheat:
                if rd['heated']:
                    r_ax.append([zc, r, convertors.to_float(v)])
                else:
                    r_ax.append([zc, r, 0])
                zc += 1
            index_key_mapping.append(rd['key'])
            r += 1

    return (rods, r_ns, r_ax, index_key_mapping)

def channel_tables(grid, xs, ys, down, up, left, right, wrapped):
    """
    Create the tables with channel positions and channel neighbouring
    relationships.

    grid:  the map of rod representations
    xs:    the x coordinates of rods in the grid map
    ys:    the y coordinates of rods in the grid map
    down:  the lower y boundary of the containing cell
    up:    the upper y boundary of the containing cell
    left:  the lower x boundary of the containing cell
    right: the upper x boundary of the containing cell
    wrapped: True if coolant box is surrounded by a wrapper -> increased wetted area

    Return a triple containing the channel and channel neighbours tables plus
    the channel box objects.
    
    """

    borders = (left, right, down, up)
    constraints = (grid, xs, ys, wrapped, borders)

    chans = []
    nbors = []
    boxes = []
    c = 1
    for yi in range(len(ys)+1):
        for xi in range(len(xs)+1):
            (row, nrow, box) = make_channel(c, xi, yi, constraints)
            chans.append(row)
            nbors.append(nrow)
            boxes.append(box)
            c += 1

    return (chans, nbors, boxes)

def material_tables(materials):
    """
    Produce the cladding and fuel material tables for given materials
    information. Return the tuple of tables.

    >>> ms = [('cladding material', 'fuel material', 'fuel diameter', 'cladding thickness', 'gas volume'), ('V', 'W', 'X', 'Y', 'Z')]
    >>> material_tables(ms)
    ([[1, 'fuel material', 0.0, 0.0, 0.0, 1.0, 0.0], [2, 'W', 0.0, 0.0, 0.0, 1.0, 0.0]], [[1, 'fuel diameter', 0.0, 1.0, 0.0, 3e-06], [2, 'X', 0.0, 1.0, 0.0, 3e-06]], [[1, 'cladding material', 0.0, 0.0, 0.0, 1.0, 0.0], [2, 'V', 0.0, 0.0, 0.0, 1.0, 0.0]], [[1, 'cladding thickness', 10000.0, 'off', 'off', 1e-06, 500000.0, 'gas volume'], [2, 'Y', 10000.0, 'off', 'off', 1e-06, 500000.0, 'Z']])

    """
    fuel_a = []
    fuel_b = []
    clad_a = []
    clad_b = []
    m = 1
    for (cladm, fuelm, diam, thick, vol, puf) in materials:
        fuel_a.append([m, fuelm, 0.0, 0.0, 0.0, 1.0, 0.0])
        fuel_b.append([m, diam, 0.0, 1.0, puf, 3.0e-6])
        clad_a.append([m, cladm, 0.0, 0.0, 0.0, 1.0, 0.0])
        clad_b.append([m, thick, 1e4, 'off', 'off', 1e-6, 5e5, vol])
        m += 1

    return (fuel_a, fuel_b, clad_a, clad_b)

def axial_heat(f, x, y, zs):
    """
    Calculate the axial heat flux table for fuel element f.

    f: the fuel cylinder
    x: x coordinate of f
    y: y coordinate of f
    zs: list of z coordinates for axial discretization of the heat flux table

    Return the axial heat flux table for rod.

    >>> f = Cylinder()
    >>> f.heat.set_grid([1]*4)
    >>> f.heat.set_values(range(4,8))
    >>> axial_heat(f, 0, 0, [-0.4, -0.2, 0.2, 0.4])
    [[-0.4, 4], [-0.2, 5], [0.2, 6], [0.4, 7]]

    """

    heat = [] 
    for z in zs:
        heat.append([z, f.heat.get_value_by_coord((x, y, z), '1')])

    return heat

def rod_diameter_average(grid):
    """
    Calculate the average diameter of all non-fake rods in grid.

    >>> g = {1: {'fake': False, 'diameter': 1}, 2: {'fake': False, 'diameter': 3}, 3: {'fake': True, 'diameter': 100}}
    >>> rod_diameter_average(g)
    2.0

    """

    diamt_sum = 0
    rod_count = 0
    for r in grid.values():
        if not r['fake']:
            diamt_sum += r['diameter']
            rod_count += 1

    return float(diamt_sum) / rod_count

def calculate_tables(gm, coolant_key, rod_keys, fuel_keys, mdict, wrapped, log=True):
    """
    For the general model gm compute the subchannel grid and return contents
    for the channel layout and channel neighbours tables. mdict is a dictionary
    for translating material names from general model to SCF materials.

    """

    if log:
        TFORMAT = ' calculate_tables(): {} {}'
        t1 = time.time()

    rs = map(lambda rk: gm.get_child(rk).abspos(), rod_keys)
    coolant = gm.get_child(coolant_key)
    first_fuel = gm.get_child(fuel_keys[0])

    xs = sorted(set(map(lambda v: v.x / 100.0, rs)))
    ys = sorted(set(map(lambda v: v.y / 100.0, rs)))
    zs = map(lambda xyz: xyz[-1], first_fuel.temp.element_coords('1'))

    if log:
        t2 = time.time()
        print TFORMAT.format('rs, xs, ys, zs created', t2 -t1)
        t1 = t2
    (g, ms) = get_rod_grid(gm, rod_keys, fuel_keys, xs, ys, zs, mdict)
    if log:
        t2 = time.time()
        print TFORMAT.format('get_rod_grid() called', t2 -t1)
        t1 = t2

    # calculate wall coordinates of the enclosing water box
    down  = (coolant.abspos().y - coolant.Y / 2) / 100.0
    up    = (coolant.abspos().y + coolant.Y / 2) / 100.0
    left  = (coolant.abspos().x - coolant.X / 2) / 100.0
    right = (coolant.abspos().x + coolant.X / 2) / 100.0

    (rod_pos, rod_nbors, rod_ax, rod_mapping) = rod_tables(g, xs, ys, 1.0)
    if log:
        t2 = time.time()
        print TFORMAT.format('rod_tables() called', t2 -t1)
        t1 = t2
    (chan_pos, chan_nbors, chan_boxes) = channel_tables(g, xs, ys, down, up, left, right, wrapped)
    if log:
        t2 = time.time()
        print TFORMAT.format('channel_tables() called', t2 -t1)
        t1 = t2
    (fa, fb, ca, cb) = material_tables(ms)
    if log:
        t2 = time.time()
        print TFORMAT.format('material_tables() called', t2 -t1)
        t1 = t2

    return {'grid': g,
            'rod-positions': rod_pos,
            'rod-neighbours': rod_nbors,
            'channel-positions': chan_pos,
            'channel-neighbours': chan_nbors,
            'channel-boxes': chan_boxes,
            'fuel-materials-1': fa,
            'fuel-materials-2': fb,
            'cladding-materials-1': ca,
            'cladding-materials-2': cb,
            'power-map': rod_ax,
            'rod-diameter': rod_diameter_average(g),
            'rod-mapping' : rod_mapping,
            'm': ms}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
