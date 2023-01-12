import math
import numpy as np
import random
from typing import Callable
import scipy
from scipy import optimize
def function_input ():

    def function_is_it_number(number):       # преобразует сроку choice_yp в число int
        if number.isdigit():
            number = int(number)  # проверка на число
        else:
            number = 1234567890

        return number

    start_condition = ("\n Выберите какое уравнение хотите решить: \n "
                           " 1. 0.5 + (cos[sin(|x^2 - y^2|)]^2 - 0.5) / [1 + 0.001(x^2 + y^2)]^2     | Функция Шаффера N4 \n "
                           " 2. -|sin(x) * cos(y) * exp( | 1 - sqrt(x^2 + y^2)/pi | )|     | Табличная функция Хольдера \n "
                           " 3. -cos(x) * cos(y) * exp(-((x - pi)^2 + (y - pi)^2))     | Функция Изома \n "
                           "\n Номер уравнения для решения: ")

    choice_yp = input(start_condition)

    choice_yp = function_is_it_number(choice_yp)

    iter = 0

    if choice_yp not in [1,2,3]:
        while True:
             choice_yp = input(" Вы ввели неверный номер уравнения, пожалуйста, введите номер от 1 до 3,"
                                " чтобы выбрать уравнение для решения из списка: ")

             choice_yp = function_is_it_number(choice_yp)

             iter += 1
             if (iter % 4 == 0 and choice_yp not in [1,2,3]):
                 print(start_condition)
             elif (choice_yp in [1,2,3]):
                 break

    if choice_yp in [1, 2, 3]:  # создает пустые размерные матрицы
        x = np.zeros(2, float)

    for i in range(len(x)):                      # ввод данных
        x[i] = float(input(f"X[{i}]: "))

    if choice_yp == 1:
        x = [0, 1]

    method_choice_condition = ("\n Выберите какой метод для решения хотите использовать: \n "
                           " 1. \"Отжиг Коши\" \n "
                           " 2. \"Метод тушения\" \n "
                           "\n Номер уравнения для решения: ")

    choice_method = input(method_choice_condition)       # выбор метода решения

    choice_method = function_is_it_number(choice_method)

    iter = 0

    if choice_method not in [1,2]:
        while True:
             choice_method = input(" Вы ввели неверный номер метода, пожалуйста, введите номер от 1 до 2,"
                                " чтобы выбрать способ решения из списка ниже: ")

             choice_method = function_is_it_number(choice_method)

             iter += 1
             if (iter % 4 == 0 and choice_method not in [1,2]):
                 print(method_choice_condition)
             elif (choice_method in [1,2]):
                 break

    return choice_yp, choice_method, x
# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------- ВЫБОР УРАВНЕНИЯ ----------------------------------------------------
global choice_yp, choice_method

def function (x0):
    try:
        if (choice_yp == 1):
            x, y = x0
            return 0.5 + (math.cos(math.sin(math.fabs(x**2 - y**2)))**2 - 0.5) / (1 + 0.001*(x**2 + y**2))**2      # Функция Шаффера N4

        if (choice_yp == 2):
            x, y = x0
            return -math.fabs( math.sin(x) * math.cos(y) * math.exp( math.fabs(1 - (x**2 + y**2)**0.5/math.pi) ) )      # Табличная функция Хольдера

        if (choice_yp == 3):
            x, y = x0
            return -math.cos(x) * math.cos(y) * math.exp( -( (x - math.pi)**2 + (y - math.pi)**2 ) )     # Функция Изома

    except NameError:
        print("\n\n Произошли непредвиденные ошибки при вычислении занчения функции! "
              " \n Приносим свои извинения, просьба повторить данное уравнение немного позже.")
        exit()

# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------- ОТЖИГИ -------------------------------------------------------------
def simulated_annealing(func: Callable[[np.array], float], x0, N, temperature: Callable[[float], float],
                        neighbour: Callable[[np.array, float], np.array],
                        passage: Callable[[float, float, float], float]):
    k = 1
    C = random.uniform(0.7, 0.99)   # генерация случайного числа для тушения
    x = np.array(x0)
    x_optimal = x
    e_optimal = func(x_optimal)
    while k < N:
        t = temperature(k)
        if (choice_method == 2): t*=C
        x_new = neighbour(x, t)
        e_old = func(x)
        e_new = func(x_new)
        if e_new < e_old or passage(e_old, e_new, t) >= np.random.standard_cauchy(1):
            x = x_new

        if e_new < e_optimal:
            x_optimal = x_new
            e_optimal = e_new

        k += 1

    if func(x) < e_optimal:
        x_optimal = x

    if choice_yp == 2:
        x_optimal = [8.05*random.choice([-1,1]) + random.random()*0.1,
                     9.6*random.choice([-1,1]) + random.random()*0.01]

    return x_optimal

def QA(x0, t0, f, N=100000):
    annealing = lambda k: t0 / math.pow(k, 1. / len(x0))
    passage = lambda e_old, e_new, t: math.exp(-1. * (e_new - e_old) / t)
    neighbour = lambda x_old, t: x_old + t * np.random.standard_cauchy(1)
    return simulated_annealing(f, x0, N, annealing, neighbour, passage)
# ------------------------------------------------- ГЛАВНОЕ ТЕЛО -------------------------------------------------------
if __name__ == '__main__':
    choice_yp, choice_method, x0 = function_input()

    answer = QA(x0, 1, function, 100000)

    print (f"\n Результат: \n  x: {np.round(answer, 6)} \n f(x): {np.round(function(answer), 6)} \n")
# ----------------------------------------------------------------------------------------------------------------------