# !/usr/bin/env python
import os

ways = {
    1: [('or_not_f1', 'primary'), ('or_f6', 'primary'), ('or_f5', 'func'), ('not_f2', 'func'), ('and_not_f4', 'func'),
        ('and_f3', 'func')],
    2: [('or_not_f1', 'primary'), ('or_f6', 'primary'), ('or_f5', 'func'), ('not_f2', 'func'), ('and_not_f4', 'func'),
        ('and_f3', 'func')],
    3: [('not_f2', 'primary'), ('or_f5', 'primary'), ('or_f6', 'primary'), ('or_not_f1', 'func'),
        ('and_not_f4', 'func'), ('and_f3', 'func')],
    4: [('and_not_f4', 'primary'), ('or_f5', 'primary'), ('or_f6', 'primary'), ('or_not_f1', 'func'),
        ('not_f2', 'func'), ('and_f3', 'func')],
    5: [('and_f3', 'primary'), ('and_not_f4', 'primary'), ('or_f5', 'primary'), ('or_f6', 'primary'),
        ('or_not_f1', 'func'), ('not_f2', 'func')],
    6: [('and_f3', 'primary'), ('and_not_f4', 'primary'), ('or_f5', 'primary'), ('or_f6', 'primary'),
        ('or_not_f1', 'func'), ('not_f2', 'func')],
    7: [('and_not_f4', 'primary'), ('or_f5', 'primary'), ('or_f6', 'primary'), ('or_not_f1', 'func'),
        ('not_f2', 'func'), ('and_f3', 'func')]
}

mul_rules = {(0, 0): 0, (1, 1): 1, (1, 0): 'err', (0, 1): 'err',
             (0, 'x'): 0, (1, 'x'): 1, ('x', 0): 0, ('x', 1): 1,
             ('d', 'x'): 'd', ('d_', 'x'): 'd_', ('x', 'd'): 'd', ('x', 'd_'): 'd_',
             ('d', 'd'): 'd', ('d_', 'd_'): 'd_', ('x', 'x'): 'x'}

cubes = {
    'or_not_f1': {'primary': [['d', 0, 'd_'], [0, 'd', 'd_'], ['d_', 0, 'd'], [0, 'd_', 'd']],
                       'func': [[1, 'x' , 0], ['x', 1, 0], [0, 0, 1]],
                       'positions': (0, 1, 7)},

         'not_f2': {'primary': [['d', 'd_'], ['d_', 'd']],
                    'func': [[1, 0], [0, 1]],
                    'positions': (2, 8)},

         'and_f3': {'primary': [[ 'd', 1, 'd'], [1, 'd', 'd'], [1, 'd_', 'd_'], ['d_', 1, 'd_']],
             'func': [[0, 'x', 0], ['x', 0,  0], [1, 1, 1], ['x', 'x', 'x']],
             'positions': (4, 5, 9)},

         'and_not_f4': {
             'primary': [[1, 1, 'd', 'd_'], [1, 'd', 1, 'd_'], ['d', 1, 1, 'd_'], [1, 1, 'd_', 'd'], [1, 'd_', 1, 'd'],
                         ['d_', 1, 1, 'd']],
             'func': [[0, 'x', 'x', 1], ['x', 0, 'x',  1], ['x', 'x', 0,  1], [1, 1, 1, 0], ['x', 'x', 'x', 'x']],
             'positions': (3, 9, 6, 10)},

         'or_f5': {
             'primary': [['d', 0, 'd'], [0, 'd', 'd'], ['d_', 0, 'd_'], [0, 'd_', 'd_']],
             'func': [[0, 0, 0], [1, 0, 1], [1, 1, 1], [0, 1, 1]],
             'positions': (8, 10, 11)},

         'or_f6': {'primary': [['d', 0, 'd'], [0, 'd', 'd'], ['d_', 0, 'd_'], [0, 'd_', 'd_']],
                  'func': [[0, 0, 0], [1, 0, 1], [1, 1, 1], [0, 1, 1]],
                  'positions': (7, 11, 12)}}


def clear_output(sets):
    res_set = set()
    for xs in sets:
        clean = [1 if i == 'd' else i for i in xs]
        clean = [0 if i == 'd_' else i for i in clean]
        if not clean.count('x'):
            res_set.add(tuple(clean))
            continue

        n_x = [i for i, e in enumerate(clean) if e == 'x']
        expand = [clean]

        for i in n_x:
            new_expand = []
            for exp in expand:
                e = exp.copy()
                e[i] = 0
                new_expand.append(e)
                e = exp.copy()
                e[i] = 1
                new_expand.append(e)
            expand = new_expand
        for c in expand:
            res_set.add(tuple(c))
    return res_set


def find_test_sets(x, const_):
    d = 'd'
    if const_:
        d = 'd_'

    way = ways[x]

    original_cube = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
    original_cube[x - 1] = d

    list_cubes = [original_cube]

    for element, type_func in way:
        positions = cubes[element]['positions']

        new_cubes = []

        for cube in list_cubes:
            f_c = find_cubes(cube, positions, element, type_func)  
            for fc in f_c:
                res = multiply(cube, positions, fc)
                if res:
                    new_cubes.append(res)
        list_cubes = new_cubes

    all_sets = []
    for lc in list_cubes:
        all_sets.append(lc[:7])
        #print(lc[:7])
    return all_sets


def find_cubes(cube, pos, elem, type_func):
    current_cube = [cube[i] for i in pos]

    res = []

    if type_func == 'primary':
        for c in cubes[elem][type_func]:
            ok = False

            for i, j in zip(current_cube[:-1], c[:-1]):
                if i == j == 'd' or i == j == 'd_':
                    ok = True

            if ok:
                res.append(c)

    if type_func == 'func':
        for c in cubes[elem][type_func]:

            if current_cube[-1] == c[-1]:

                res.append(c)

    return res


def multiply(xs, pos, cube):
    res = xs.copy()
    for i, x in zip(pos, cube):
        res[i] = mul_rules[(xs[i], x)]
    if 'err' in res:
        return []
    else:
        return res

def all_func(lists):
    print('\n Набор, покрывающие все входы')
    s = set
    for i in lists:
        s.add(lists[i])
    print("ssss", s)

#----------CHECK-----------------------------------

def F_res(xs, x_err=-1, const_=-1):
    x1_7 = xs.copy()
    if const_ != -1 and x_err > 0 and x_err < 8:
        x1_7[x_err - 1] = const_

    f1 = not (x1_7[0] or x1_7[1])
    f2 = not x1_7[2]
    f3 = x1_7[4] and x1_7[5]
    f4 = x1_7[3] and x1_7[6] and f3
    f5 = f2 or f4
    f6 = f1 or f5
    return f6

def answers(x_err, const_):
    sets = set()
    for x1_7 in range(2 ** 7):
        xs = [int(x) for x in bin(x1_7)[2:].zfill(7)]

        res_ok = F_res(xs)
        res_wrong = F_res(xs, x_err, const_)

        if bool(res_ok) != bool(res_wrong):
            sets.add(tuple(xs))
    return sets


def check():

    print("Должно быть")

    res = answers(7, 0)

    for i in res:
        print(i)

    print("Есть")

    t = clear_output(find_test_sets(4, 0))

    for y in t:
        print(y)

    t_l = list(t)

    if t == res:
        print("Наборы равны")
    else:
        print("Наборы не равны")

#----------CHECK------------------------------

if __name__ == '__main__':

    ex = False

    while ex == False:
        print('Произвести подсчет автоматически? (y/n)')

        ans = input()

        if ans == 'n':
            #os.startfile(r'schema.jpg')

            input_x = int(input('выберите вход\n'))
            constant = int(input('Введите константу (0 или 1 )\n'))

            res = clear_output(find_test_sets(input_x, constant))

            print('****** RESULT ******')
            print(res)

        elif ans == 'y':
            res = ()
            r = []
            for x in range(1, 8):
                for c in [0, 1]:
                    res = clear_output(find_test_sets(x, c))

                    print('****** RESULT ******   вход, константа  -- ', x, c)
                    r.append(res)
                    print(res)

                    #all_func(res)
            #all_func(r)
            print("rrrrr", r)
            ex = True

        else:
            print('Некорректный ввод')

    check()

