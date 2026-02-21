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




class Xorshift32(BaseRNG):
    """
    Заглушка для другого Xorshift
    """
    MASK = 0xFFFFFFFF

    def __init__(self, seed=1, a=13, b=17, c=5, m = 2 ** 32):
        if seed == 0:
            raise ValueError("Seed не может быть 0: XOR-сдвиги нуля всегда дают 0")

        self.state = seed & self.MASK
        self.a = a
        self.b = b
        self.c = c
        self.m = m

    def next_int(self):
        """
        Генерация следующего псевдослучайного 32-битного числа.

        Три раунда XOR + сдвиг обеспечивают хорошее перемешивание битов.
        После каждой операции обрезаем до 32 бит маской.
        """
        x = self.state
        x ^= (x << self.a) & self.MASK
        x ^= (x >> self.b)
        x ^= (x << self.c) & self.MASK

        self.state = x
        return self.state


class Xorshift64(BaseRNG):
    """
    Xorshift64 — 64-битная версия

    Состояние: 1 × 64 бита
    Период:    2^64 − 1
    """

    MASK = 0xFFFFFFFFFFFFFFFF  # 64-битная маска

    def __init__(self, seed=1, m=2 ** 64):
        if (seed & self.MASK) == 0:
            raise ValueError("Seed не может быть 0")
        self.a = seed & self.MASK
        self.m = m

    def next_int(self):
        x = self.a
        x ^= (x << 13) & self.MASK
        x ^= (x >> 7)
        x ^= (x << 17) & self.MASK
        self.a = x
        return self.a


class Xorshift128(BaseRNG):
    """
    Xorshift128
    Состояние: 4 × 32 бита = 128 бит
    Период:    2^128 − 1
    """

    MASK = 0xFFFFFFFF  # 32-битная маска

    def __init__(self, seed=None, x0=123456789, x1=362436069, x2=521288629, x3=88675123, m=2 ** 32):
        self.m = m
        if seed is not None:
            if seed == 0:
                raise ValueError("Seed не может быть 0")
            self.x = [0] * 4
            self.x[0] = seed & self.MASK
            for i in range(1, 4):
                self.x[i] = (1812433253 * (self.x[i - 1] ^ (self.x[i - 1] >> 30)) + i) & self.MASK
        else:
            self.x = [x0, x1, x2, x3]
            if all(v == 0 for v in self.x):
                raise ValueError("Хотя бы одно значение состояния должно быть ненулевым")

    def next_int(self):
        t = self.x[3]

        s = self.x[0]
        self.x[3] = self.x[2]
        self.x[2] = self.x[1]
        self.x[1] = s

        t ^= (t << 11) & self.MASK
        t ^= t >> 8
        self.x[0] = t ^ s ^ (s >> 19)
        return self.x[0]

# тестирование
def demo(generator_object):
    print("Тест " + type(generator_object).__name__)
    print(type(generator_object).__name__ + " float: ", [generator_object.next_float() for _ in range(5)])
    print(type(generator_object).__name__ + " randint: ", [generator_object.randint(0, 10) for _ in range(5)])
    print(type(generator_object).__name__ + " array: ", generator_object.random_array(10))
    print()

if __name__ == "__main__":
    generators = [LCG(seed=123), Xorshift32(seed=123), Xorshift64(seed=123), Xorshift128(seed=123)]

    for g in generators:
        demo(g)