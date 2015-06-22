d1 = {'x': 1, 'y':2, 'z': 3}

def myfunc(x, y, **labels):
    print(x, y, labels['z'])

myfunc(**d1)
