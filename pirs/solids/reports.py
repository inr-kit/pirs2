def report_solid(solid, name):

    if solid.parent != None:
        print 'report_solid warning: solid is not a root. Root will be analyzed'
        solid = solid.root
        name = 'Root of ' + name

    elst = solid.values(True)
    # number of tree elements.
    NE = len(elst)

    # number of mesh layers:
    Th = 0  # total in all elements
    Tt = 0
    Td = 0
    Mh = 0  # maximal
    Mt = 0
    Md = 0
    for e in elst:
        nh = len(e.heat.values())
        nt = len(e.temp.values())
        nd = len(e.dens.values())

        Th += nh
        Tt += nt
        Td += nd

        if nh > Mh:
            Mh = nh
            Mh_key = e.get_key()
        if nt > Mt:
            Mt = nt
            Mt_key = e.get_key()
        if nd > Md:
            Md = nd
            Md_key = e.get_key()
    
    tab = ' '*6
    print 'Statistics for {0}'.format(name)
    print tab + 'number of tree elements: {0}'.format(NE)

    print tab + 'Total number of axial layers for heat: {0}'.format(Th)
    print tab + 'Total number of axial layers for temp: {0}'.format(Tt)
    print tab + 'Total number of axial layers for dens: {0}'.format(Td)

    print tab + 'Maximal number of axial layers for heat is {0} found in {1}'.format(Mh, Mh_key)
    print tab + 'Maximal number of axial layers for temp is {0} found in {1}'.format(Mt, Mt_key)
    print tab + 'Maximal number of axial layers for dens is {0} found in {1}'.format(Md, Md_key)
    print tab + '*'*80

        

