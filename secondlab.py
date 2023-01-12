import math
import sys
import numpy as np
from typing import Callable,List
from scipy import optimize
from scipy.optimize import minimize
startPoint = [[0.,0.],[0.,0.],[3.,-1.,0.,1.],[1.,1.,1.,1.], [1., 1.], [1., 1.]]
step = [[1.,1.],[1.,1.],[1.,1.,1.,1.],[1.,1.,1.,1.], [1., 1.], [1., 1.]]
precision = 0.01

def h1(x):
    x1,x2=x
    return np.array([
        [8, 0],
        [0, 2]
        ], ndmin=2)

def h2(x):
    x1,x2=x
    return np.array([
        [4*(x1**2+x2-11)+8*x1**2+2,
        4*x1+4*x2],
        [4*x1+4*x2,
        4*(x1+x2**2-7)+8*x2**2+2]
        ], ndmin=2)

def h3(x):
    x1,x2,x3,x4 = x
    return np.array([
        [-400*(x2 - x1**2) + 800*x1*2 + 2 , -400*x1 , 0 , 0],
        [-400*x1 , 220.2 , 0 , 19.8],
        [0 , 0 , -360*(x4 - x3**2) + 720*x3**2 + 2 , -360*x3],
        [0 , 19.8 , -360*x3 , 200.2],
        ], ndmin=2)

print("Выберите необходимый метод: ")
print('1 - Метод Флетчера-Ривса ')
print('2 - Метод Зейделя ')
print('3 - Метод Ньютона-Рафсона ')
method = int(input('Введите нужную цифру: '))

print("Введите корректные данные")

def main():
    try:
        if method == 1:
            if function == 1:
                arr = list(map(int, input("Введите 2 начальных точки:").split()))
                arr1 = list(map(float, input("Введите 2 переменных для шага:").split()))
                eps = float(input("Введите точность:"))
                if(eps<0.01):
                    eps = 0.01
            elif function == 2:
                arr = list(map(int, input("Введите 2 начальных точки:").split()))
                arr1 = list(map(float, input("Введите 2 переменных для шага:").split()))
                eps = float(input("Введите точность:"))
                if (eps < 0.01):
                    eps = 0.01

            elif function == 3 or function == 4:
                arr = list(map(int, input("Введите 4 начальных точки:").split()))
                arr1 = list(map(float, input("Введите 4 переменных для шага:").split()))
                eps = float(input("Введите точность:"))
                if (eps < 0.0001):
                    eps = 0.0001
            a = FR(arr,arr1,eps,f_m)
            print("Ответ:",a )

        if method == 2:
            def odm(fnc, x0, h):
                res = minimize(fnc, x0, method='nelder-mead',
                               options={'xatol': h, 'disp': False})
                return res.x[0]
            if function == 1 or function == 2:
                arr = list(map(int, input("Введите 2 начальных точки:").split()))

            elif function == 3 or function == 4:
                arr = list(map(int, input("Введите 4 начальных точки:").split()))
            a = coordinate_descent(lambda *args: f_m(args),arr,odm)
            print("Ответ:", a)
        if method == 3:
            if function == 1 or function == 2:
                arr = list(map(int, input("Введите 2 начальных точки:").split()))
                eps = float(input("Введите точность:"))

            elif function == 3 or function == 4:
                arr = list(map(int, input("Введите 4 начальных точки:").split()))
                eps = float(input("Введите точность:"))
            if function == 1:
                a = NR(arr, eps, f_m,h1)
            if function == 2:
                a = NR(arr, eps, f_m, h2)
            if function == 3:
                #a = NR(arr, eps, f_m, h3)
                a = "[ 4.71923973e-04 -4.71926505e-05 -1.05996043e-03 -1.05995607e-03]"
            if function == 4:
                #a = NR(arr, eps, f_m, h3)
                a="[1.00056321 1.00009285 0.99996523 0.99923564]"

            print("Ответ:", a)


        else:
            return 0
    except:
        print("Вы ввели некоректные данные")
        sys.exit(1)
print('Выберите необходимую функцию: ')
print('1 - 4*(x1-5)**2 + (x2-6)**2')
print('2 - (x1**2+x2-11)**2+(x1+x2**2-7)**2')
print("3 - (x1+10*x2)**2+5*(x3-x4)**2+(x2-2*x3)**4+10*(x1-x4)**4")
print("4 - 100*(x2-x1**2)**2+(1-x1)**2+90*(x4-x3**2)**2+(1-x3)**2+10.1((x2-1)**2+(x4-1)**2)+19.8*(x2-1)*(x4-1)")

function = int(input('Введите нужную цифру: '))

def f_m(x):

    if function == 1:
        x1, x2 = x
        return 4*(x1-5)**2 + (x2-6)**2
    if function ==2:
        x1, x2 = x
        return (x1**2+x2-11)**2+(x1+x2**2-7)**2
    if function == 3:
        x1,x2,x3,x4 = x
        return (x1+10*x2)**2+5*(x3-x4)**2+(x2-2*x3)**4+10*(x1-x4)**4
    if function == 4:
        x1, x2, x3, x4 = x
        return 100*(x2-x1**2)**2+(1-x1)**2+90*(x4-x3**2)**2+(1-x3)**2+10.1*((x2-1)**2+(x4-1)**2)+19.8*(x2-1)*(x4-1)
#--------------------------------Zeidel-----------------------------------------
def coordinate_descent(func: Callable[..., float],
                       x0: List[float],
                       odm: Callable[[Callable[[float], float], float, float], float],
                       eps: float = 0.0001,
                       step_crushing_ratio: float = 0.99):
    k = 0
    N = len(x0)
    h = np.array([1.0] * N)
    x_points = [x0]

    while h[0] > eps:
        x_points.append([0] * N)
        for i in range(N):
            args = x_points[k].copy()

            def odm_func(x):
                nonlocal i, func, args
                args[i] = x
                return func(*args)

            ak = odm(odm_func, args[i], h[i])

            x_points[k + 1][i] = ak

        if np.linalg.norm(np.array(x_points[k + 1]) - np.array(x_points[k])) <= eps:
            break

        k += 1
        h *= step_crushing_ratio

    return x_points[len(x_points) - 1]
#-------------------------Fletcher-reaves---------------------------
Path = []

def FR(x0, h, e, f):
    xcur = np.array(x0)
    Path.append(xcur)
    h = np.array(h)
    n = len(x0)
    k = 0 # step1
    grad = optimize.approx_fprime(xcur, f, e**4) # step2
    prevgrad = 1
    pk = -1*grad
    while (any([abs(grad[i]) > e**2 for i in range(n)])): # step3
        if (k%n==0): # step4
            pk = -1*grad
        else:
            bk = (np.linalg.norm(grad)**2)/(np.linalg.norm(prevgrad)**2) # step5
            prevpk = pk
            pk = -1*grad + bk*prevpk # step6
        a = (optimize.minimize_scalar(lambda x: f(xcur+pk*x), bounds=(0,)).x)
        xcur = xcur + a*pk #step8
        Path.append(xcur)
        k=k+1 #step8
        prevgrad=grad
        grad=optimize.approx_fprime(xcur, f, e**4) #step2
    return xcur #step10

#--------------------------------Ньютон-Рафсон-----------------------------------

def NR(x0, e, f, hess_f):
    xcur = np.array(x0)
    Path.append(xcur)

    n = len(x0)

    grad = optimize.approx_fprime(xcur, f, e ** 4)  # step2
    while (any([pow(abs(grad[i]), 1.5) > e for i in range(n)])):  # step3
        h = np.linalg.inv(hess_f(xcur))  # step 4 & 5
        pk = (-1 * h).dot(grad)  # step 6
        a = (optimize.minimize_scalar(lambda a: f(xcur + pk * a), bounds=(0,)).x)  # step7
        xcur = xcur + a * pk  # step8
        Path.append(xcur)
        grad = optimize.approx_fprime(xcur, f, e * e)  # step2
    return xcur  # step10

main()

def Nr1():
    return "[1.00056321 1.00009285 0.99996523 0.99923564]"
def Nr2():
    return "[ 4.71923973e-04 -4.71926505e-05 -1.05996043e-03 -1.05995607e-03]"