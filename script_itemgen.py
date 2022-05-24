from main import db, Type, SubType, Item

def inputN_none():
    n = int(input())
    if n == 0:
        n=None
    return n

def inputN():
    n = int(input())
    return n

def inputT():
    n = input()
    return n

def inputB():
    n = int(input())
    if n == 1:
        return True
    else:
        return False

t = True
item_list = []
while t == True:
    
    item = []

    print('-------------------------------------')
    print("Введите название вещи :")
    c = inputT()
    item.append(c)

    print('-------------------------------------')
    print("Введите описание вещи :")
    c = inputT()
    item.append(c)

    print('-------------------------------------')
    print("Выберите тип вещи :")
    t = Type.query.all()
    for tt in t:
        print(tt.id, tt.name)

    c = inputN()
    ti = c
    item.append(c)

    print('-------------------------------------')
    print("Выберите под-тип вещи :")
    t = SubType.query.all()
    for tt in t:
        print(tt.id, tt.name)

    c = inputN_none()
    item.append(c)

    print('-------------------------------------')
    print("Введите tir вещи :")
    c = inputN_none()
    item.append(c)

    if ti == 1:
        print('-------------------------------------')
        print("Выберите урон оружия :")
        c = inputN_none()
        item.append(c)

        print('-------------------------------------')
        print("Выберите Точность оружия :")
        c = inputN_none()
        item.append(c)

        print('-------------------------------------')
        print("Выберите Размер крита оружия :")
        c = inputN_none()
        item.append(c)

        print('-------------------------------------')
        print("Выберите Шанс крита оружия :")
        c = inputN_none()
        item.append(c)
    else:
        item.append(None)
        item.append(None)
        item.append(None)
        item.append(None)

    if ti in [2,3,4,5,6]:
        print('-------------------------------------')
        print("Выберите защиту брони :")
        c = inputN_none()
        item.append(c)
    else:
        item.append(None)

    if ti == 7:
        print('-------------------------------------')
        print("Выберите востонавление сытности еды :")
        c = inputN_none()
        item.append(c)

        print('-------------------------------------')
        print("Выберите востановление настроения еды :")
        c = inputN_none()
        item.append(c)
    else:
        item.append(None)
        item.append(None)


    print('-------------------------------------')
    print("Выберите можно одеть ? :")
    c = inputB()
    item.append(c)

    print('-------------------------------------')
    print("Выберите можно Использовать ? :")
    c = inputB()
    item.append(c)

    print('-------------------------------------')
    print("Выберите можно купиить/продать ? :")
    c = inputB()
    item.append(c)

    if c:
        print('-------------------------------------')
        print("Выберите цену ? :")
        c = inputN()
        item.append(c)
    else:
        item.append(None)

    item_list.append(item)

    print('-------------------------------------')
    print()
    print(item)
    print('-------------------------------------')
    print()
    print(item_list)

    print('====================================================')
    print("Создать еще объект ? 1-Да 2-Нет")
    t = inputB()

    
