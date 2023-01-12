import sys
import numpy as np
import boltzmann_method

import matplotlib.pyplot as plt



import scipy
from scipy.optimize import minimize

import ultrafast_annealing


def f1(x):
    x1, x2 = x
    return 0.5 + ( (np.sin(x1**2-x2**2)**2 - 0.5 )/( 1+0.001*(x1**2+x2**2))**2 ) #Функция Шаффера N2  -100 100 f(0, 0)=0

def f2(x):
    x1, x2 = x
    # Подставка для яиц -512 512 f(512, 404,2319)=-959.6407
    return -(x2+47) * np.sin(np.sqrt(np.abs(x1*0.5 + (x2+47)))) - x1 * np.sin(np.sqrt(np.abs(x1 - (x2+47))))

def f3(x):
    x1, x2 = x
    return -20*np.exp(-0.2*np.sqrt((x1*x1+x2*x2)/2))-np.exp((np.cos(2*np.pi*x1)+np.cos(2*np.pi*x2))/2)+20+np.exp(1) #Экли -5 5 f(0, 0)=0



def outputLine(res, fnc_res):
    r = "".join(f"{j:.{5}f} " for j in res)
    print(r)
    print(f"Значение функции в точке: ")
    print(fnc_res)


try:
    print('\nfunction_1: Функция Шаффера N2')
    print('function_2: Функция "подставка для яиц“'),
    print('function_3: Функция Экли')


    chosenFunc = int(input('Выберите функцию: '))
except:
    print("Неправильный ввод функции")
    sys.exit(1)


def main():
    try:
        if chosenFunc == 1:
            X, Y = np.meshgrid([i for i in range(-50, 50)], [i for i in range(-50, 50)])
            Z = 0.5 + ( (np.sin(X**2-Y**2)**2 - 0.5 )/( 1+0.001*(X**2+Y**2))**2 )
            # Задаем пространство
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            # Название нашего объекта --необязательно
            ax.set_title('Функция Шаффера N2')
            # Кладем фигуру в пространство с наложенным скином
            ax.plot_surface(X, Y, Z, cmap='inferno')
            # Смотрим, что вышло
            plt.show()

            print("\nБольцмановский отжиг")
            res = boltzmann_method.boltzmann_method([5., 5.], 1., f1, 100000)
            outputLine(res, f1(res))

            print("\nСверхбыстрый отжиг")
            res = ultrafast_annealing.ultrafast_annealing(f1, [5., 5.], 100, 400, 1, 0.00001, 0.1)
            outputLine(res, f1(res))
        elif chosenFunc == 2:
            # Задаем значения x, y, z
            # Я визуализирую функцию eggholder
            X, Y = np.meshgrid([i for i in range(-512, 512)], [i for i in range(-512, 512)])
            Z = -(X + 47) * np.sin(np.sqrt(abs(X / 2 + (Y + 47)))) - X * np.sin(np.sqrt(abs(X - (Y + 47))))

            # Задаем пространство
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            # Название нашего объекта --необязательно
            ax.set_title('Функция "подставка для яиц"')
            # Кладем фигуру в пространство с наложенным скином
            ax.plot_surface(X, Y, Z, cmap='inferno')
            # Смотрим, что вышло
            plt.show()

            print("\nБольцмановский отжиг")
            res = boltzmann_method.boltzmann_method([300., 300.], 1., f2, 100000)
            outputLine(res, f2(res))

            print("\nСверхбыстрый отжиг")
            res = ultrafast_annealing.ultrafast_annealing(f2, [300., 300.], 100, 500, 1, 0.00001, 0.01)
            outputLine(res, f2(res))
        elif chosenFunc == 3:
            X, Y = np.meshgrid([i for i in range(-10, 10)], [i for i in range(-15, 15)])
            Z = -20*np.exp(-0.2*np.sqrt(0.5*(X**2 + Y**2))) - np.exp(0.5*(np.cos(2*np.pi*X) + np.cos(2*np.pi*Y))) + np.exp(1) + 20

            # Задаем пространство
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            # Название нашего объекта --необязательно
            ax.set_title('Функция Экли')
            # Кладем фигуру в пространство с наложенным скином
            ax.plot_surface(X, Y, Z, cmap='inferno')
            # Смотрим, что вышло
            plt.show()

            print("\nБольцмановский отжиг")
            res = boltzmann_method.boltzmann_method([3., 3.], 1., f3, 100000)
            outputLine(res, f3(res))

            print("\nСверхбыстрый отжиг")
            res = ultrafast_annealing.ultrafast_annealing(f3, [0., 0.], 100, 400, 1, 0.00001, 0.01)
            outputLine(res, f3(res))
        else:
            print("Неправильный ввод 1")
            return 0
    except:
        print("Неправильный ввод 2")
        sys.exit(1)


main()

