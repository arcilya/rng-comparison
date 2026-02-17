class BaseRNG:
    """
    Базовый класс генератора псевдослучайных чисел
    """

    def next_int(self):
        """
        Должен возвращать следующее псевдослучайное целое число
        Реализуется в подклассах
        """
        raise NotImplementedError("Метод next_int() должен быть реализован в подклассе")

    def next_float(self):
        """
        Следующее псевдослучайное число в [0,1)
        """
        return self.next_int() / self.m

    def randint(self, low, high):
        """
        Случайное целое число в [low, high]
        """
        if low > high:
            raise ValueError("low должен быть <= high")
        return low + int(self.next_float() * (high - low + 1))

    def random_array(self, n):
        """
        Сгенерировать список из n чисел в [0,1)
        """
        return [self.next_float() for _ in range(n)]



class LCG(BaseRNG):
    """
    Линейный конгруэнтный генератор (LCG)
    X_(n+1) = (a * X_n + c) mod m
    """

    def __init__(self, seed=1, a=1664525, c=1013904223, m=2 ** 32):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next_int(self):
        """
        Следующее псевдослучайное целое число (0 ... m-1)
        """
        self.state = (self.a * self.state + self.c) % self.m
        return self.state




class CustomGenerator(BaseRNG):
    """
    Заглушка для другого Xorshift
    TODO: реализовать алгоритм генерации
    """

    def __init__(self, seed=1):
        # TODO: инициализировать внутреннее состояние
        self.state = seed

        # Задается модуль m (диапазон) для LCG
        self.m = 2 ** 32

    def next_int(self):
        """
        TODO: реализовать генерацию следующего числа
        """
        raise NotImplementedError("CustomGenerator.next_int() ещё не реализован")


# тестирование


if __name__ == "__main__":
    print("Тест LCG)")

    lcg = LCG(seed=123)

    print("LCG float:", [lcg.next_float() for _ in range(5)])
    print("LCG randint:", [lcg.randint(0, 10) for _ in range(5)])
    print("LCG array:", lcg.random_array(10))


