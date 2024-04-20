

def test1():
    d = {
        'brand': 'Ford',
        'model': 'Mustang',
        'year': 1964,
    }

    print(d.keys())
    print(list(d.keys()))
    print(sorted(d.keys()))
    print(list(reversed(sorted(d.keys()))))

def test2():
    d = {
        'year': 1964,
        'brand': 'Ford',
        'model': 'Mustang',
    }

    print(d.keys())
    print(list(d.keys()))
    print(sorted(d.keys()))
    print(list(reversed(sorted(d.keys()))))

def test3():
    d = {
        10: 9,
        8: 7,
        6: 5,
        4: 3,
        2: 1,
    }

    print(d.keys())
    print(list(d.keys()))
    print(sorted(d.keys()))
    print(list(reversed(sorted(d.keys()))))

def main():
    test1()
    test2()
    test3()

if __name__ == '__main__':
    main()
