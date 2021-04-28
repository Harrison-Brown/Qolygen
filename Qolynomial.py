class Q:
    def __init__(self, n, d = 1):
        self.n = n
        if n == 0:
            d = 1
        self.d = d
        self.reduce()

    def __add__(self, other):
        n = (self.n * other.d) + (self.d * other.n)
        d = self.d * other.d
        return Q(n, d)

    def __sub__(self, other):
        other.n = -other.n
        return self + other

    def __mul__(self, other):
        n = self.n * other.n
        d = self.d * other.d
        return Q(n, d)

    def __pow__(self, power):
        return Q(self.n**power, self.d**power)

    def __truediv__(self, other):
        other.n, other.d = other.d, other.n
        return self * other

    def reduce(self):
        if self.d < 0:
            self.d *= -1
            self.n *= -1
        a = max(self.n, self.d)
        b = min(self.n, self.d)
        while b:
            a, b = b, a % b
        a = abs(a)
        self.n = self.n // a
        self.d = self.d // a

    def __repr__(self):
        if self.d == 1:
            return 'Q({})'.format(self.n)
        else:
            return 'Q({}, {})'.format(self.n, self.d)

    def __str__(self):
        if self.d == 1:
            return '{}'.format(self.n)
        else:
            return '{}/{}'.format(self.n, self.d)

    def __eq__(self, other):
        if self.n == other.n and self.d == other.d:
            return True
        else:
            return False

class Qolynomial():
    def __init__(self, *coeffs):
        if coeffs == ():
            coeffs = [0]
        self.coeffs = list(coeffs)
        for i in range(len(self.coeffs)):
            if type(self.coeffs[i]) is int:
                self.coeffs[i] = Q(self.coeffs[i])
        self.unpad()
        self.degree = len(self.coeffs) - 1

    def unpad(self):
        if self.coeffs[-1] == Q(0) and len(self.coeffs) > 1:
            self.coeffs.pop(-1)
            self.unpad()


    def __call__(self, x):
        if type(x) is int:
            x = Q(x)
        l = self.coeffs.copy()
        while len(l) > 1:
            a = l.pop(-1)
            l[-1] += a * x
        return l[0]

    def __repr__(self):
        return "Qolynomial{}".format(tuple(self.coeffs))

    def __str__(self):
        if self.degree == 0:
            return str(self.coeffs[0])
        elif self.degree == 1:
            return str(self.coeffs[0]) + ' + ' + str(self.coeffs[1]) + 'x'
        else:
            s = str(self.coeffs[0]) + ' + ' + str(self.coeffs[1]) + 'x'
            for i in range(2, self.degree + 1):
                s += ' + ' + str(self.coeffs[i]) + 'x^' + str(i)
            return s

    def __add__(self, other):
        if self.degree < other.degree:
            larger = other.coeffs.copy()
            smaller = self.coeffs.copy()
        else:
            larger = self.coeffs.copy()
            smaller = other.coeffs.copy()
        for i in range(len(smaller)):
            larger[i] += smaller[i]
        return Qolynomial(*larger)

    def __sub__(self, other):
        l = [-1 * x for x in other.coeffs]
        return self + Qolynomial(*l)

    def __mul__(self, other):
        l = [Q(0) for x in range(self.degree + other.degree + 1)]
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                l[i + j] += self.coeffs[i] * other.coeffs[j]
        return Qolynomial(*l)

    def __pow__(self, power):
        q = Qolynomial(*self.coeffs.copy())
        for i in range(power -1):
            q *= Qolynomial(*self.coeffs.copy())
        return q
