import math

# Ввод номера функции
print('Функции: ')
print('1. (x-1)^2')
print('2. (4x^3) - 8x^2 - 11x + 5')
print('3. x + 3/x^2')
print('4. (x + 2,5) / (4 -x^2)')
print('5. -sin(x) - sin(3x)/3')
print('6. -2sin(x) - sin(2x) - 2sin(3x)/3')
numbFunc = int(input("Введите номер функции: "))

# Ввод номера метода
print('Методы: ')
print("1. Метод пассивного поиска")
print("2. Метод Фибоначчи")
numbMethod = int(input("Введите номер метода: "))

# Перечень функций
def func(x, numbFunc):
    if numbFunc == 1:
        return pow((x - 1), 2)
    elif numbFunc == 2:
        return 4 * pow(x, 3) - 8 * pow(x, 2) - 11 * x + 5
    elif numbFunc == 3:
        if x0 == 0:
            print('Пожалуйста, измените входное значение х0')
            quit()
        else:
            return x + (3 / (x ** 2))
    elif numbFunc == 4:
        if x0 == 2 or x0 == -2:
            print('Пожалуйста, измените входное значение х0')
            quit()
        else:
            return (x + 2.5) / (4 - pow(x, 2))
    elif numbFunc == 5:
        return -math.sin(x) - (math.sin(3 * x) / 3)
    elif numbFunc == 6:
        return -2 * math.sin(x) - math.sin(2 * x) - 2 * math.sin(3 * x) / 3

x0 = float(input("Введите X0: "))  # Начальная точка
h = float(input("Введите h: "))  # Шаг

# Метод Дэвиса-Свенна-Кэмпи
def DSK(x0, h, numbFunc):
    a = 0
    b = 0
    k = 0
    incorrect_flag = 0

    if func(x0 + k * h, numbFunc) >= func(x0 + (k + 1) * h, numbFunc):
        a = x0
        k += 1
        while True:
            if k > 100:
                incorrect_flag = 1
                break
            if func(x0 + k * h, numbFunc) < func(x0 + (k + 1) * h, numbFunc):
                b = x0 + (k + 1) * h
                break
            else:
                a = x0 + k * h
                k += 1
            if numbFunc == 4:
                if a == 2 or a == -2:
                    print("Пожалуйста, измените значение х")
                    quit()
                elif b == 2 or b == -2:
                    print("Пожалуйста, измените значение х")
                    quit()
    elif func(x0 - k * h, numbFunc) >= func(x0 - (k + 1) * h, numbFunc):
        b = x0
        k += 1
        while True:
            if k > 100:
                incorrect_flag = 1
                break
            if func(x0 - k * h, numbFunc) < func(x0 - (k + 1) * h, numbFunc):
                a = x0 - (k + 1) * h
                break
            else:
                b = x0 - k * h
                k += 1
    else:
        a = x0 - h
        b = x0 + h

    if incorrect_flag == 0:
        print('[a,b] = [', a, ', ', b, ']')
        return [a, b]
    else:
        return 'Incorrect'

# Метод пассивного поиска
if numbMethod == 1:
    segment = DSK(x0, h, numbFunc)
    a = segment[0]
    b = segment[1]
    N = int(input('Введите количество отрезков: '))
    step = (b - a) / N  # Шаг 1
    min_f_x = func(a, numbFunc)
    min_x = a
    for i in range(N): # Шаг 2
        f_x = func(a+i*step, numbFunc)
        if f_x < min_f_x: # Шаг 3
            min_f_x = f_x
            min_x = a + i * step
    print('f(x*) = min f(x) = ', round(min_f_x*1000)/1000)
    print('x* = ', round(min_x*1000)/1000)

# Метод Фибоначчи
if numbMethod == 2:
    segment = DSK(x0, h, numbFunc)
    a = segment[0]
    b = segment[1]
    eps = float(input('Задайте параметр точности: '))
    sigma = eps / 10    # малая константа "различимости"
    #Шаг 1
    N = int((b - a) / (2 * eps))
    print('Количество вычислений функции как наименьшее целое', N)
    k = 0   # Итерация (шаг 2)
    class FibonacciImpl:    # Вычисление чисел Фибоначчи
        arr = [0, 1, 1]
        def calculate(self, num: int):
            if num < len(self.arr):
                return self.arr[num]
            else:
                for i in range(len(self.arr) - 1, num):
                    new_fib = self.arr[i - 1] + self.arr[i]
                    self.arr.append(new_fib)
                return self.arr[num]
    fib_impl = FibonacciImpl()
    def fib(num):
        global fib_impl
        return fib_impl.calculate(num)
    # Шаг 3
    x1 = a + fib(N - 2) / fib(N) * (b - a)
    x2 = a + fib(N - 1) / fib(N) * (b - a)
    for k in range(2, N - 2):   # Критерий останова k = N-3
        if func(x1, numbFunc) <= func(x2, numbFunc):    # Шаг 4,5
            b = x2
            x2 = x1
            x1 = a + fib(N - k - 3) / fib(N - k - 1) * (b - a)
        else:
            a = x1
            x1 = x2
            x2 = a + fib(N - k - 2) / fib(N - k - 1) * (b - a)
    # Шаг 6
    x2 = x1 + sigma
    if func(x1, numbFunc) <= func(x2, numbFunc):
        b = x2
    else:
        a = x1
    res1 = (a + b) / 2  # Шаг 7
    print(res1)