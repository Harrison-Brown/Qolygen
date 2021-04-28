from Qolynomial import *

def Qolygen(points):
    result = Qolynomial(0)
    for i in range(len(points)):
        point = points.pop(i)
        q = Qolynomial(1)
        d = 1
        for p in points:
            q *= Qolynomial(-p[0], 1)
            d *= (point[0] - p[0])
        q *= Qolynomial(Q(point[1], d))
        result += q
        points.insert(i, point)
    return result

def main():
    points = [(2, 3), (10, 3), (-2, 1), (7, 6)]
    print('Points given:')
    print(points)
    q = Qolygen(points)
    print('Function found:')
    print('f(x) = ' + str(q))
    for p in points:
        print('f({}) = {}'.format(p[0], q(p[0])))

if __name__ == '__main__':
    main()
