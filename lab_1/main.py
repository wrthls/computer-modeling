# x = 2
from time import perf_counter
from math import sqrt
from prettytable import PrettyTable


def square(polynom):
    square = {}
    for first_key in polynom:
        for second_key in polynom:
            power = first_key + second_key
            koef = polynom[first_key] * polynom[second_key]
            if power in square:
                square[power] += koef
            else:
                square[power] = koef
    return square


def integrate(polynom):
    new_polynom = {}
    for key in polynom:
        power = key + 1
        koef = polynom[key] / power
        new_polynom[power] = koef

    return new_polynom


def get_approximation_polynom(n):
    polynom_array = []
    for i in range(n):
        curr = {2: 1}
        if i > 0:
            prev = square(prev)
            curr.update(prev)

        curr = integrate(curr)
        polynom_array.append(curr)
        prev = curr

    return polynom_array


def count_approximation(x, polynom):
    res = 0
    for key in polynom:
        if polynom[key] != 0:
            val = polynom[key]
            for _ in range(key):
                val *= x
            res += val

    return res


def pikar(n, x0, xn, h):
    polynom = get_approximation_polynom(n)
    res_array = []
    for i in range(0, len(polynom)):
        x = x0
        while x <= xn:
            res = count_approximation(x, polynom[i])
            #print("Результат приближения", i + 1, " методом Пикара:", x, res)
            if i + 1 == 3 or i + 1 == 4 or i + 1 == n:
                res_array.append([i + 1, x, res])

            x += h

    return res_array


# Явный метод
def explicit_method(x0, xn, h):
    x = x0
    y = 0
    res_array = [[x, y]]

    while x < xn:
        next_y = y + h * (x * x + y * y)

        y = next_y
        x += h

        res_array.append([x, y])

    return res_array


# Неявный метод
def implicit_method(x0, xn, h):
    x = x0
    y = 0
    res_array = [[x, y]]

    while x < xn:
        discr = 1 - 4 * h * (h * x * x + y)
        if discr > 0:
            next_y = (1 - sqrt(discr))/(2 * h)
            # берем меньший корень, поэтому второй не нужно вычислять
            # next_y2 = (1 + sqrt(discr))/(2 * h)
        else:
            next_y = 0

        x += h
        y = next_y
        res_array.append([x, y])

    return res_array


def print_table(res_pikar, res_explicit, res_implicit, n, time):
    table = PrettyTable(["X", "3 приближение Пикара",
                         "4 приближение Пикара",
                         "{0} приближение Пикара".format(n),
                         "Явный метод", "Неявный метод"])
    n = len(res_implicit)
    for i in range(n):
        row = list()
        row.append(res_implicit[i][0])
        row.append("{:^10.3e}".format(res_pikar[i][2]))
        row.append("{:^10.3e}".format(res_pikar[i + n][2]))
        row.append("{:^10.3e}".format(res_pikar[i + n + n][2]))
        row.append("{:^10.3e}".format(res_explicit[i][1]))
        row.append("{:^10.3e}".format(res_implicit[i][1]))
        table.add_row(row)

    table.border = False

    print()
    print(table)
    print('\nВремя вычисления(сек):', time)


def main(n, x0, xn, h):
    beg = perf_counter()

    res_pikar = pikar(n, x0, xn, h)
    res_explicit = explicit_method(x0, xn, h)
    res_implicit = implicit_method(x0, xn, h)

    end = perf_counter()

    time = end - beg

    print_table(res_pikar, res_explicit, res_implicit, n, time)


if __name__ == "__main__":
    print("Номер приближения: ", end='')
    n = int(input())
    print("X0: ", end='')
    x0 = int(input())
    print("Xn: ", end='')
    xn = int(input())
    print("Введите шаг: ", end='')
    h = int(input())
    main(n, x0, xn, h)
