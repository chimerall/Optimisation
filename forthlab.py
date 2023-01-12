import numpy as np
import sympy.calculus.util
from sympy import *
from sympy.calculus.util import minimum
from typing import Callable, List
from scipy import optimize
from scipy.optimize import minimize
import numdifftools as nd

# Функции
def function_ch(urav):
    # 2.2
    if urav == 1:
        return lambda x: x[1] + x[2]
    # 2.6
    if urav == 2:
        return lambda x: 4 / x[1] + 9 / x[2] + x[1] + x[2]
    # 2.10
    if urav == 3:
        return lambda x: ln * x[1] - x[2]
    # 2.14
    if urav == 4:
        return lambda x: x[1] ** 2 + x[2] ** 2 + x[3] ** 2


# !!!!!!!!!!
urav = int((input("\n Выберите функцию: \n 1. x[1]+x[2] \n 2. 4/x[1]+9/x[2]+x[1]+x[2] \n \
3. ln*x[1]-x[2] \n \
4. x[1]**2+x[2]**2+x[3]**2 \n\n Номер уравнения: ")))

list_urav = list(range(1, 5))
iter = 0
if urav not in [1, 2, 3, 4]:
    while True:
        urav = int((input(" Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 4: ")))
        iter += 1
        if (iter % 4 == 0):
            # !!!!!!!!!!!!!!!
            print("\n Пожалуйста, выберите номер уравнения из следующего списка: \n 1. x[1]+x[2] \n 2. 4/x[1]+9/x[2]+x[1]+x[2] \n \
3. ln*x[1]-x[2] \n \
4. x[1]**2+x[2]**2+x[3]**2 \n\n Уравнение: ")
        elif (urav in [1, 2]):
            break

method = int(input("\n Выберите метод: \n 1. Метод барьера.\n 2. Метод штрафа.\n\n Метод: "))

j = 0
if method not in [1, 2, 3]:
    while True:
        method = int(input(" Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 3: "))
        j += 1
        if (j % 4 == 0):
            print("\n 1. Метод барьера.\n 2. Метод штрафа.\n\n Метод: ")
        elif (method in [1, 2]):
            break

if urav in [1, 2]:
    x = np.zeros(2, float)

elif urav in [3, 4]:
    x = np.zeros(4, float)

print("\n Введите начальную точку x: ")
for i in range(len(x)):
    x[i] = float(input(f" x[{i}]: "))

eps = float((input(" Введите точность eps: ")))
while eps <= 0:
    eps = float((input(" Вы ввели eps, которой не соответствует условию: eps > 0 \n \
Пожалуйста введите подходящее значение eps: ")))
r = 1
rest_eq = 10
rest_not_eq = 0.1


# Наискорейший спуск

# def euclidean_norm(h: np.array):
#   return np.sqrt((h**2).sum())

def optimal_gradient_method(function_ch: Callable[[List[float]], float], x: List[float], eps: float):
    x = np.array(x)

    def grad(function_ch, xcur, eps) -> np.array:
        return optimize.approx_fprime(xcur, function_ch, eps ** 2)

    gr = grad(function_ch, x, eps)
    a = 0.

    while any([abs(gr[i]) > eps for i in range(len(gr))]):
        # while euclidean_norm(gr) > eps:
        gr = grad(function_ch, x, eps)
        a = optimize.minimize_scalar(lambda koef: function_ch(*[x + koef * gr])).x
        x += a * gr
        if a == 0:
            break

    return x

# Метод барьера
def getAuxilitaryFunctionResult1(f: Callable[..., float], b: List[float], r, rest_not_eq):
    x = np.array(x)
    H = sum(1 / (0.000000001 + pow(max(0, -i(x)), 2)) for i in rest_not_eq)
    return f(x) + r * H


if method == 1:
    xcur = np.array(x)
    xnew = None
    atLeastOnePointFound = False
    while not (atLeastOnePointFound and (((xcur - xnew) ** 2).sum() < eps ** 2)):
        xtemp = optimal_gradient_method(lambda x: getAuxilitaryFunctionResult1(function_ch, r, rest_not_eq, x), xcur,
                                        eps)
        isInside = not any(neq(xtemp[0], xtemp[1]) > eps for neq in rest_not_eq)
        if (isInside):
            if not atLeastOnePointFound:
                atLeastOnePointFound = True
            else:
                xcur = xnew
            xnew = xtemp
        r *= z
    print(xnew)


# Метод штрафа

def getAuxilitaryFunctionResult(function_ch, r, rest_eq, rest_not_eq, x):
    x1 = x[0]
    x2 = x[1]
    H = 0
    for i in rest_eq:
        H += pow(abs(i(x1, x2)), 2)
    for i in rest_not_eq:
        H += pow(max(0, i(x1, x2)), 2)
    return function_ch(x) + r * H


if method == 2:
    xcur = np.array(x0)
    xnew = optimal_gradient_method(lambda x: getAuxilitaryFunctionResult2(function_ch, r, rest_eq, rest_not_eq, x),
                                   xcur, eps)
    while ((xcur - xnew) ** 2).sum() > eps:
        r *= z
        xcur = xnew
        xnew = optimal_gradient_method(lambda x: getAuxilitaryFunctionResult2(function_ch, r, rest_eq, rest_not_eq, x),
                                       xcur, eps)
    print(xnew)